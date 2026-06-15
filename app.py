import streamlit as st

# Sets up the main landing page
st.set_page_config(page_title="Playbet Portal", page_icon="🎲", layout="centered")

# Sidebar Logo and Navigation
with st.sidebar:
    try:
        st.image("logo.jpg", use_container_width=True)
    except:
        pass
    st.write("---")
    st.markdown("### 🧭 Navigation")
    st.write("Use the sidebar menu above to access specific departments.")

# Main Title and Welcome
st.markdown("<h1 style='text-align: center; color: #D32F2F;'>Playbet Central Operations</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome to the unified hub for all departmental tools and analytics.</p>", unsafe_allow_html=True)
st.write("---")

# Global Internal Dashboard Links
st.write("### 📊 Internal Operational Dashboards")
st.link_button("Registrations & Deposits", "https://registration-and-deposits-dashboard-mucnhw8hvduhycncwghrsd.streamlit.app/", use_container_width=True)
st.link_button("Raventruck ETL Pipeline", "https://playbet-automation-8dvmevk5gcqmbwmes9z2sg.streamlit.app/", use_container_width=True)
st.link_button("Branch Performance Analytics", "https://playbetbranchanalytics-9y45k3tx55imncdhbq8wc4.streamlit.app/", use_container_width=True)