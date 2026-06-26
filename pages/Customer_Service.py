import streamlit as st
import pandas as pd
import os
import calendar
from datetime import datetime
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Customer Service Hub", page_icon="📞", layout="wide")

st.sidebar.markdown("### 👤 User Role")
selected_role = st.sidebar.selectbox("Select Role", options=['staff', 'manager', 'supervisor'], index=0)
st.session_state['role'] = selected_role
user_role = st.session_state.get('role', 'staff')

st.markdown("<h1 style='text-align: center;'>📞 Customer Service Hub</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_live_eco_time_data(target_date):
    return None 

# ==========================================
# SECTION 1: CORE SUPPORT TOOLS
# ==========================================
col_cs1, col_cs2 = st.columns(2)

with col_cs1:
    with st.container(border=True):
        st.markdown("#### 🎧 Freshworks Tickets")
        st.link_button("Open Freshworks", "https://playbet.freshworks.com/login", use_container_width=True)

with col_cs2:
    with st.container(border=True):
        st.markdown("#### 📚 Knowledge Base")
        with st.expander("📖 Open Operational Links", expanded=False):
            st.markdown("* [Dispute & Escalation Procedures](#)\n* [Freshworks Ticketing Handbook](#)\n* [Shift Handover Logs](#)\n* [HR Attendance API Documentation](#)")

st.write("---")

# ==========================================
# SECTION 2: DYNAMIC MONTH SELECTION
# ==========================================
if not os.path.exists("rosters"): os.makedirs("rosters")

all_months = [datetime(y, m, 1) for y in range(2026, 2029) for m in range(1, 13) if not (y == 2026 and m < 6)]
selected_dt = st.sidebar.selectbox("Choose Month", all_months, format_func=lambda x: x.strftime("%B %Y"))
filename = selected_dt.strftime("%B_%Y") + ".xlsx"
EXCEL_FILE = os.path.join("rosters", filename)

def generate_roster_logic(filepath, year, month):
    _, last_day = calendar.monthrange(year, month)
    dates = [datetime(year, month, d) for d in range(1, last_day + 1)]
    
    day_team = ["Keabetswe Kuwane", "Inam Mbolekwa", "Ayanda Mngadi", "Viance Ngwenya", "Njabulo Dlamini", "Nonhlanhla Kana", "Mellesa Mphephanduku", "Siphosethu Mbatha", "Gracious Sibanda"]
    night_team = ["Charlotte Njoli", "Sithembile Ndaba", "Nomvelo Gina", "Nkosingiphile Ndinisa", "Noxolo Dakie"]
    
    day_data = {"Name": day_team}
    night_data = {"Name": night_team}
    
    for date_obj in dates:
        # Generate headers as "Mon 01 June 2026"
        col_name = date_obj.strftime("%a %d %B %Y") 
        
        day_shifts = []
        for i, name in enumerate(day_team):
            if (date_obj.day + i) % 7 == 0: shift = "OFF"
            elif name == "Gracious Sibanda": shift = "8-5" if (date_obj.day) % 2 == 0 else "9-6"
            else: shift = "7-4" if (date_obj.day + i) % 2 == 0 else "11-8"
            day_shifts.append(shift)
        day_data[col_name] = day_shifts
        
        night_shifts = []
        for i, name in enumerate(night_team):
            if (date_obj.day + i) % 7 == 0: shift = "OFF"
            else: shift = "8pm-5am" if (date_obj.day + i) % 2 == 0 else "10pm-7am"
            night_shifts.append(shift)
        night_data[col_name] = night_shifts
        
    with pd.ExcelWriter(filepath) as writer:
        pd.DataFrame(day_data).to_excel(writer, sheet_name="Day", index=False)
        pd.DataFrame(night_data).to_excel(writer, sheet_name="Night", index=False)
    st.rerun()

if not os.path.exists(EXCEL_FILE):
    st.warning(f"No roster for {selected_dt.strftime('%B %Y')}. Initialize to build the table.")
    if st.button("Initialize New Roster with Rotation Logic"): generate_roster_logic(EXCEL_FILE, selected_dt.year, selected_dt.month)
    st.stop()

try:
    xls = pd.ExcelFile(EXCEL_FILE)
    day_df = pd.read_excel(xls, sheet_name="Day").fillna("")
    night_df = pd.read_excel(xls, sheet_name="Night").fillna("")
except ValueError:
    st.error("Roster file format is outdated. Updating to Day & Night format...")
    generate_roster_logic(EXCEL_FILE, selected_dt.year, selected_dt.month)
    st.stop()

# ==========================================
# SECTION 3: HR DATA SCANNER
# ==========================================
HR_FILE = "hr_clockins_master.csv"
clocked_in_ids = []
current_hr_logs = pd.DataFrame()

today_str = datetime.now().strftime("%Y-%m-%d")
api_df = fetch_live_eco_time_data(today_str)

if api_df is None or api_df.empty:
    if os.path.exists(HR_FILE):
        try:
            hr_df = pd.read_csv(HR_FILE)
            if 'Date' in hr_df.columns:
                hr_df['Date'] = pd.to_datetime(hr_df['Date'])
                current_hr_logs = hr_df[(hr_df['Date'].dt.month == selected_dt.month) & (hr_df['Date'].dt.year == selected_dt.year)].copy()
                
                # Ensure HR match IDs use the new format
                current_hr_logs['Date_Str'] = current_hr_logs['Date'].dt.strftime("%a %d %B %Y")
                if 'Name' in current_hr_logs.columns:
                    clocked_in_ids = (current_hr_logs['Date_Str'] + "_" + current_hr_logs['Name']).tolist()
        except Exception as e:
            pass

# ==========================================
# SECTION 4: MANAGER EDIT
# ==========================================
if user_role in ['manager', 'supervisor']:
    with st.expander("📝 Edit Master Roster", expanded=False):
        if not st.session_state.get('manager_auth', False):
            if st.text_input("Enter Manager Password", type="password") == "Manager123":
                st.session_state['manager_auth'] = True
                st.rerun()
        else:
            if st.button("Logout"): st.session_state['manager_auth'] = False; st.rerun()
            st.info("💡 **Shift Codes:** Day: `7-4`, `11-8`, `8-5`, `9-6` | Night: `8pm-5am`, `10pm-7am` | `OFF` for off days.")
            tab_edit_day, tab_edit_night = st.tabs(["☀️ Day Shift Team", "🌙 Night Shift Team"])
            with tab_edit_day: edited_day = st.data_editor(day_df, use_container_width=True, num_rows="dynamic")
            with tab_edit_night: edited_night = st.data_editor(night_df, use_container_width=True, num_rows="dynamic")
            
            if st.button("💾 Save All Excel Updates", type="primary"):
                with pd.ExcelWriter(EXCEL_FILE) as writer:
                    edited_day.to_excel(writer, sheet_name="Day", index=False)
                    edited_night.to_excel(writer, sheet_name="Night", index=False)
                st.success("Master Roster updated successfully!"); st.rerun()

# ==========================================
# SECTION 5: STYLED ROSTER VIEWERS
# ==========================================
st.markdown(f"### 📅 Live Roster: {selected_dt.strftime('%B %Y')}")

def highlight_cells(df):
    df_style = pd.DataFrame('', index=df.index, columns=df.columns)
    today = datetime.now().date()
    
    for col in df.columns:
        if col != 'Name':
            # Look for the specific "Mon 01 June 2026" format
            try: 
                col_date = datetime.strptime(str(col), "%a %d %B %Y").date()
            except ValueError: 
                # Fallback parser if it finds an old column format
                try: col_date = datetime.strptime(str(col), "%d-%b-%y").date()
                except ValueError: continue
                
            for idx, name in df['Name'].items():
                val = str(df.at[idx, col]).strip().upper()
                match_id = f"{col}_{name}"
                
                if val == "OFF": df_style.at[idx, col] = 'background-color: #262730; color: #555;'
                elif val != "": 
                    if match_id in clocked_in_ids: df_style.at[idx, col] = 'background-color: #2e7d32; color: white;'
                    elif col_date >= today: df_style.at[idx, col] = 'background-color: #fbc02d; color: black;'
                    else: df_style.at[idx, col] = 'background-color: #d32f2f; color: white;'
    return df_style

tab_view_day, tab_view_night = st.tabs(["☀️ Day Shift", "🌙 Night Shift"])
with tab_view_day: st.dataframe(day_df.style.apply(highlight_cells, axis=None), use_container_width=True, hide_index=True)
with tab_view_night: st.dataframe(night_df.style.apply(highlight_cells, axis=None), use_container_width=True, hide_index=True)

st.markdown("🌐 **Legend:** &nbsp; 🟢 Green = Clocked In &nbsp; | &nbsp; 🔴 Red = Missed &nbsp; | &nbsp; 🟡 Yellow = Pending &nbsp; | &nbsp; ⬛ Grey = OFF")

# ==========================================
# SECTION 6: HR LOGS
# ==========================================
st.write("---")
st.markdown(f"### 🕒 HR System Clock-In Logs ({selected_dt.strftime('%B %Y')})")
if not current_hr_logs.empty:
    st.dataframe(current_hr_logs[['Date_Str', 'Name', 'ClockInTime']].rename(columns={'Date_Str': 'Verified Date'}), use_container_width=True, hide_index=True)
else:
    st.info("🔄 Integrating verified HR data stream for monthly log evaluation...")