import streamlit as st
import pandas as pd

st.set_page_config(page_title="Branch Ops | Playbet", layout="wide")

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.write("---")

st.markdown("<h2>🏬 Branch Operations Analytics</h2>", unsafe_allow_html=True)

# 1. Branch Selector (The "Controller")
branch = st.selectbox("Select Branch for Analysis", ["Malvern", "Pretoria", "Randburg", "White River"])

# 2. Metric Visualization Section
st.write(f"### Current Analysis: {branch}")

# Create tabs to keep the UI clean
tab1, tab2, tab3 = st.tabs(["📊 GGR Performance", "👥 Foot Traffic", "🎰 Game Performance"])

with tab1:
    st.subheader(f"GGR Trends (2024 - Present) for {branch}")
    # Placeholder for your GGR dataframe: st.line_chart(df_ggr)
    st.info("Integrating live Azure Data Factory pipeline for monthly GGR aggregation...")

with tab2:
    st.subheader(f"Foot Traffic Analysis for {branch}")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Monthly Trends")
        # st.bar_chart(df_foot_traffic_monthly)
    with col2:
        st.write("Daily Peak Times")
        # st.area_chart(df_foot_traffic_daily)

with tab3:
    st.subheader(f"Top Performing Games in {branch}")
    # Example table display
    data = {"Game": ["Aviator", "Lucky 7", "Roulette"], "Performance Score": [98, 85, 72]}
    st.table(pd.DataFrame(data))

# 3. Footer Link for Deep Dives
st.write("---")
st.link_button(f"Generate Full {branch} Performance Report", "https://your-internal-dashboard-link.com", use_container_width=True)