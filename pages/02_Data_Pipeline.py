import streamlit as st

st.set_page_config(page_title="Data Pipeline | Playbet", layout="wide")

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.write("---")

st.markdown("<h2>📊 Data & Analytics Pipeline</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("Internal Dashboards")
        st.link_button("Registrations & Deposits", "https://registration-and-deposits-dashboard-mucnhw8hvduhycncwghrsd.streamlit.app/", use_container_width=True)
        st.link_button("Raventruck ETL", "https://playbet-automation-8dvmevk5gcqmbwmes9z2sg.streamlit.app/", use_container_width=True)
        st.link_button("Branch Analytics", "https://playbetbranchanalytics-9y45k3tx55imncdhbq8wc4.streamlit.app/", use_container_width=True)

with col2:
    with st.container(border=True):
        st.subheader("Analytics & AI")
        st.link_button("Ibex AI", "https://ibex.ai/", use_container_width=True)
        st.link_button("Google Ads", "https://business.google.com/en-all/google-ads/", use_container_width=True)
        st.link_button("Google Analytics", "https://analytics.google.com/analytics/web/provision/#/provision", use_container_width=True)