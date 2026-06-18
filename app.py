import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# --- PAGE CONFIGURATION (MUST BE THE FIRST COMMAND) ---
st.set_page_config(
    page_title="Playbet Central Operations", 
    page_icon="📊", 
    layout="wide"
)

# --- 1. LOAD CREDENTIALS ---
def get_config():
    if os.path.exists('credentials.yaml'):
        with open('credentials.yaml') as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        def unlock_secrets(d):
            if hasattr(d, "items"):
                return {k: unlock_secrets(v) for k, v in d.items()}
            return d
        return unlock_secrets(st.secrets)

config = get_config()

# 2. Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 3. Render login
try:
    authenticator.login()
except Exception as e:
    st.error(f"Login Error: {e}")

# 4. Access Control
if st.session_state.get('authentication_status'):
    
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        try:
            st.image("logo.jpg", use_container_width=True)
        except:
            pass
        authenticator.logout() 
        st.write("---")
        st.markdown("### 🧭 Navigation")
        st.write("Use the menu above to access departments.")

    # --- MAIN PAGE HEADER ---
    st.markdown("<h1 style='text-align: center; color: #D32F2F;'>Playbet Central Operations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>The unified intelligence hub for Playbet data, compliance, and forecasting.</p>", unsafe_allow_html=True)
    st.write("---")

    # --- SECTION 1: INTERNAL OPERATIONAL DASHBOARDS ---
    st.markdown("### 📊 Internal Operational Dashboards")
    col_op1, col_op2 = st.columns(2)

    with col_op1:
        with st.container(border=True):
            st.markdown("#### 💳 Registrations & Deposits")
            st.caption("Real-time monitoring of customer sign-ups and transaction flows.")
            st.link_button("Launch Dashboard", "https://registration-and-deposits-dashboard-mucnhw8hvduhycncwghrsd.streamlit.app/", use_container_width=True)

    with col_op2:
        with st.container(border=True):
            st.markdown("#### 🏢 Branch Performance")
            st.caption("Granular analytics regarding individual branch metrics and KPIs.")
            st.link_button("Launch Analytics", "https://playbetbranchanalytics-9y45k3tx55imncdhbq8wc4.streamlit.app/", use_container_width=True)

    st.write("") # Spacing

    # --- SECTION 2: DATA EXTRACTION & UTILITIES ---
    st.markdown("### 🛠️ Data Extraction & Utilities")
    col_ut1, col_ut2, col_ut3 = st.columns(3)

    with col_ut1:
        with st.container(border=True):
            st.markdown("#### 🦅 Raventruck ETL")
            st.caption("Automated ingestion and transformation of branch data.")
            st.link_button("Open Pipeline", "https://playbet-automation-8dvmevk5gcqmbwmes9z2sg.streamlit.app/", use_container_width=True)

    with col_ut2:
        with st.container(border=True):
            st.markdown("#### 🛡️ Self-Exclusion Extractor")
            st.caption("Compliance tool for parsing and verifying exclusion records.")
            st.link_button("Open Extractor", "https://huggingface.co/spaces/nicollafundira/self-exclusion-extractor", use_container_width=True)

    with col_ut3:
        with st.container(border=True):
            st.markdown("#### 🗃️ Bulk Data Filtering")
            st.caption("Process and filter large-scale datasets for ad-hoc analysis.")
            st.link_button("Open Tool", "https://playbet-data-pipeline-khdjba2deejx2pegeamfsi.streamlit.app/", use_container_width=True)

    st.write("") # Spacing

    # --- SECTION 3: PREDICTIVE MODELING ---
    st.markdown("### 📈 Predictive Modeling")
    col_pr1, col_pr2 = st.columns(2) # Using 2 cols so the card isn't too wide

    with col_pr1:
        with st.container(border=True):
            st.markdown("#### 🔮 GGR & Deposit Forecasting")
            st.caption("Predictive model analyzing historical trends to project future revenue.")
            st.link_button("Run Forecast", "https://huggingface.co/spaces/nicollafundira/ggr-deposit-forecast", use_container_width=True)

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your credentials to access the portal.')