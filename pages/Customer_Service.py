import streamlit as st
import pandas as pd
import os
import calendar
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Customer Service Hub", page_icon="📞", layout="wide")

# --- ADD ROLE SELECTOR IN SIDEBAR ---
st.sidebar.markdown("### 👤 User Role")
selected_role = st.sidebar.selectbox(
    "Select Role",
    options=['staff', 'manager', 'supervisor'],
    index=0
)
st.session_state['role'] = selected_role

user_role = st.session_state.get('role', 'staff')
st.markdown("<h1 style='text-align: center;'>📞 Customer Service Hub</h1>", unsafe_allow_html=True)

# ==========================================
# SECTION 1: CORE SUPPORT TOOLS & KNOWLEDGE BASE
# ==========================================
col_cs1, col_cs2, col_cs3 = st.columns(3)
with col_cs1:
    with st.container(border=True):
        st.markdown("#### 🎧 Freshworks Tickets")
        st.link_button("Open Freshworks", "https://playbet.freshworks.com/login?redirect_uri=https%3A%2F%2Fplaybet.freshworks.com%2F", use_container_width=True)
with col_cs2:
    with st.container(border=True):
        st.markdown("#### 📊 Customer Service Dashboard")
        st.button("Coming Soon", disabled=True, use_container_width=True)
with col_cs3:
    with st.container(border=True):
        st.markdown("#### 📚 Knowledge Base")
        with st.expander("📖 Open Operational Links", expanded=False):
            st.markdown("""
            * [Dispute & Escalation Procedures](#)
            * [Freshworks Ticketing Handbook](#)
            * [Shift Handover Logs](#)
            * [HR Attendance API Documentation](#)
            """)

st.write("---")

# ==========================================
# SECTION 2: DYNAMIC MONTH SELECTION
# ==========================================
if not os.path.exists("rosters"): os.makedirs("rosters")

all_months = []
for year in range(2026, 2029):
    for month in range(1, 13):
        if year == 2026 and month < 6: continue
        dt = datetime(year, month, 1)
        all_months.append(dt)

st.sidebar.markdown("### 📅 Select Roster Month")
selected_dt = st.sidebar.selectbox("Choose Month", all_months, format_func=lambda x: x.strftime("%B %Y"))
filename = selected_dt.strftime("%B_%Y") + ".xlsx"
EXCEL_FILE = os.path.join("rosters", filename)

# --- THE BLANK TEMPLATE GENERATOR (DAY & NIGHT) ---
def generate_blank_roster(filepath, year, month):
    _, last_day = calendar.monthrange(year, month)
    dates = [datetime(year, month, d) for d in range(1, last_day + 1)]
    
    day_team = ["Keabetswe Kuwane", "Inam Mbolekwa", "Ayanda Mngadi", "Viance Ngwenya", 
                "Njabulo Dlamini", "Nonhlanhla Kana", "Mellesa Mphephanduku", 
                "Siphosethu Mbatha", "Gracious Sibanda"]
                
    night_team = ["Charlotte Njoli", "Sithembile Ndaba", "Nomvelo Gina", 
                  "Nkosingiphile Ndinisa", "Noxolo Dakie"]
    
    day_data = {"Name": day_team}
    night_data = {"Name": night_team}
    
    for date_obj in dates:
        col_name = date_obj.strftime("%d-%b-%y")
        day_data[col_name] = [""] * len(day_team)
        night_data[col_name] = [""] * len(night_team)
        
    with pd.ExcelWriter(filepath) as writer:
        pd.DataFrame(day_data).to_excel(writer, sheet_name="Day", index=False)
        pd.DataFrame(night_data).to_excel(writer, sheet_name="Night", index=False)
    st.rerun()

# Trigger Initialization
if not os.path.exists(EXCEL_FILE):
    st.warning(f"No roster for {selected_dt.strftime('%B %Y')}. Initialize to build the empty table.")
    if st.button("Initialize New Roster Template"): 
        generate_blank_roster(EXCEL_FILE, selected_dt.year, selected_dt.month)
    st.stop()

# --- LOAD DATA ---
try:
    xls = pd.ExcelFile(EXCEL_FILE)
    day_df = pd.read_excel(xls, sheet_name="Day").fillna("")
    night_df = pd.read_excel(xls, sheet_name="Night").fillna("")
except ValueError:
    st.error("Roster file format is outdated. Updating to Day & Night format...")
    generate_blank_roster(EXCEL_FILE, selected_dt.year, selected_dt.month)
    st.stop()

# ==========================================
# SECTION 3: REAL-TIME HR DATA SCANNER
# ==========================================
HR_FILE = "hr_clockins_master.csv"
clocked_in_ids = []
current_hr_logs = pd.DataFrame()

# Scan for actual file dropped from HR department
if os.path.exists(HR_FILE):
    try:
        hr_df = pd.read_csv(HR_FILE)
        
        # Check if Date column exists
        if 'Date' in hr_df.columns:
            hr_df['Date'] = pd.to_datetime(hr_df['Date'])
            
            # Automatically clear June 2026 data
            june_2026_count = len(hr_df[(hr_df['Date'].dt.month == 6) & (hr_df['Date'].dt.year == 2026)])
            if june_2026_count > 0:
                hr_df = hr_df[~((hr_df['Date'].dt.month == 6) & (hr_df['Date'].dt.year == 2026))]
                hr_df.to_csv(HR_FILE, index=False)
                st.sidebar.success(f"✅ Cleared {june_2026_count} June 2026 clock-in records")
            
            # Filter strictly for the selected month window
            current_hr_logs = hr_df[(hr_df['Date'].dt.month == selected_dt.month) & (hr_df['Date'].dt.year == selected_dt.year)].copy()
            current_hr_logs['Date_Str'] = current_hr_logs['Date'].dt.strftime("%d-%b-%y")
            
            # Check if Name column exists
            if 'Name' in current_hr_logs.columns:
                clocked_in_ids = (current_hr_logs['Date_Str'] + "_" + current_hr_logs['Name']).tolist()
            else:
                clocked_in_ids = []
        else:
            st.sidebar.warning("HR file missing 'Date' column")
    except Exception as e:
        # Silently handle the error without displaying it
        pass

# ==========================================
# SECTION 4: MANAGER EDIT (DAY & NIGHT TABS)
# ==========================================
if user_role in ['manager', 'supervisor']:
    with st.expander("📝 Edit Master Roster", expanded=False):
        if not st.session_state.get('manager_auth', False):
            if st.text_input("Enter Manager Password", type="password") == "Manager123":
                st.session_state['manager_auth'] = True
                st.rerun()
        else:
            if st.button("Logout"): st.session_state['manager_auth'] = False; st.rerun()
            
            st.info("💡 **Shift Codes:** \n\n **☀️ Day Shifts:** `7-4`, `11-8`, `8-5`, `9-6` \n\n **🌙 Night Shifts:** `8pm-5am`, `10pm-7am` \n\n Use `OFF` to designate scheduled off days.")
            
            tab_edit_day, tab_edit_night = st.tabs(["☀️ Day Shift Team", "🌙 Night Shift Team"])
            with tab_edit_day:
                edited_day = st.data_editor(day_df, use_container_width=True, num_rows="dynamic", key="edit_day")
            with tab_edit_night:
                edited_night = st.data_editor(night_df, use_container_width=True, num_rows="dynamic", key="edit_night")
            
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
            try: col_date = datetime.strptime(str(col), "%d-%b-%y").date()
            except ValueError: continue
                
            for idx, name in df['Name'].items():
                val = str(df.at[idx, col]).strip().upper()
                match_id = f"{col}_{name}"
                
                if val == "OFF": 
                    df_style.at[idx, col] = 'background-color: #262730; color: #555;'
                elif val != "": 
                    if match_id in clocked_in_ids:
                        df_style.at[idx, col] = 'background-color: #2e7d32; color: white;'
                    elif col_date >= today:
                        df_style.at[idx, col] = 'background-color: #fbc02d; color: black;'
                    else:
                        df_style.at[idx, col] = 'background-color: #d32f2f; color: white;'
    return df_style

tab_view_day, tab_view_night = st.tabs(["☀️ Day Shift", "🌙 Night Shift"])
with tab_view_day:
    st.dataframe(day_df.style.apply(highlight_cells, axis=None), use_container_width=True, hide_index=True)
with tab_view_night:
    st.dataframe(night_df.style.apply(highlight_cells, axis=None), use_container_width=True, hide_index=True)

st.markdown("🌐 **Legend:** &nbsp; 🟢 Green = Clocked In &nbsp; | &nbsp; 🔴 Red = Missed &nbsp; | &nbsp; 🟡 Yellow = Pending &nbsp; | &nbsp; ⬛ Grey = OFF")

# ==========================================
# SECTION 6: HR VERIFIED ATTENDANCE LOGS
# ==========================================
st.write("---")
st.markdown(f"### 🕒 HR System Clock-In Logs ({selected_dt.strftime('%B %Y')})")
if not current_hr_logs.empty:
    st.dataframe(current_hr_logs[['Date_Str', 'Name', 'ClockInTime']].rename(columns={'Date_Str': 'Verified Date'}), use_container_width=True, hide_index=True)
else:
    st.info("🔄 Integrating verified HR data stream for monthly log evaluation...")