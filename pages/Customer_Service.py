import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Customer Service Hub", page_icon="📞", layout="wide")

st.markdown("<h1 style='text-align: center;'>📞 Customer Service Shift Hub</h1>", unsafe_allow_html=True)
st.write("---")

# --- 1. DATA HANDLING (Safe Loading) ---
SCHEDULE_FILE = "schedule.csv"
CLOCKIN_FILE = "clockins.csv"

# Create a blank schedule if it doesn't exist yet
if not os.path.exists(SCHEDULE_FILE):
    pd.DataFrame({
        "Name": ["John Doe", "Jane Smith", "Alex Johnson"],
        "Shift": ["07:00 - 16:00", "OFF", "11:00 - 20:00"]
    }).to_csv(SCHEDULE_FILE, index=False)

# Create a blank HR clock-in file if it doesn't exist yet
if not os.path.exists(CLOCKIN_FILE):
    pd.DataFrame({
        "Name": ["John Doe"],
        "ClockInTime": ["06:55"]
    }).to_csv(CLOCKIN_FILE, index=False)

# Load the data
schedule_df = pd.read_csv(SCHEDULE_FILE)
clockin_df = pd.read_csv(CLOCKIN_FILE)

# --- 2. ACCESS CONTROL ---
# Retrieve the role set by app.py. Default to 'staff' if accessed directly without logging in.
user_role = st.session_state.get('role', 'staff')

# --- 3. MANAGER / SUPERVISOR VIEW (Editable) ---
if user_role in ['manager', 'supervisor']:
    st.markdown("### 📝 Edit Weekly Schedule")
    st.info(f"You have **{user_role.capitalize()}** access. Edits made here will update live for the staff.")
    
    # Use column config to force correct data entry
    edited_schedule = st.data_editor(
        schedule_df,
        use_container_width=True,
        num_rows="dynamic", # Allows managers to add or delete rows
        column_config={
            "Name": st.column_config.TextColumn(
                "Employee Name",
                required=True
            ),
            "Shift": st.column_config.SelectboxColumn(
                "Shift Time",
                help="Select the shift or OFF",
                options=["07:00 - 16:00", "08:00 - 17:00", "11:00 - 20:00", "Night Shift", "OFF"],
                required=True
            )
        }
    )
    
    # Save mechanism
    if st.button("💾 Save Schedule", type="primary"):
        edited_schedule.to_csv(SCHEDULE_FILE, index=False)
        st.success("Schedule successfully updated!")

# --- 4. STAFF VIEW (Read-Only with Live Status) ---
else:
    st.markdown("### 📅 Today's Live Status")
    
    # Logic to determine if someone is Clocked In or Missed
    def determine_status(row):
        if row['Shift'] == "OFF":
            return "⚪ OFF"
        # Check if their name appears in today's HR clock-in file
        elif row['Name'] in clockin_df['Name'].values:
            return "🟢 Clocked In"
        else:
            return "🔴 Missed / Pending"

    # Apply the logic to a new 'Status' column
    display_df = schedule_df.copy()
    display_df['Status'] = display_df.apply(determine_status, axis=1)

    # Display as a clean, read-only table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption("Status is updated automatically when HR syncs the clocking machine data.")