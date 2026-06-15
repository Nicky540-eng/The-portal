import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# --- 1. LOAD CREDENTIALS (Cloud vs Local) ---
def get_config():
    # If a credentials file exists locally, use it
    if os.path.exists('credentials.yaml'):
        with open('credentials.yaml') as file:
            return yaml.load(file, Loader=SafeLoader)
    # Otherwise, fall back to Streamlit Cloud secrets
    else:
        # CRITICAL FIX: Recursively unlock Streamlit's read-only secrets
        # This converts every nested layer into a standard, writable dictionary
        def unlock_secrets(d):
            if hasattr(d, "items"):
                return {k: unlock_secrets(v) for k, v in d.items()}
            return d
        
        return unlock_secrets(st.secrets)

# Initialize configuration
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
    # --- IF LOGGED IN ---
    with st.sidebar:
        try:
            st.image("logo.jpg", use_container_width=True)
        except:
            pass
        authenticator.logout() 
        st.write("---")
        st.markdown("### 🧭 Navigation")
        st.write("Use the sidebar menu above to access departments.")
    
    st.markdown("<h1 style='text-align: center; color: #D32F2F;'>Playbet Central Operations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Welcome to the unified hub for all departmental tools.</p>", unsafe_allow_html=True)
    st.write("---")

    # Global Internal Dashboard Links
    st.write("### 📊 Internal Operational Dashboards")
    st.link_button("Registrations & Deposits", "https://registration-and-deposits-dashboard-mucnhw8hvduhycncwghrsd.streamlit.app/", use_container_width=True)
    st.link_button("Raventruck ETL Pipeline", "https://playbet-automation-8dvmevk5gcqmbwmes9z2sg.streamlit.app/", use_container_width=True)
    st.link_button("Branch Performance Analytics", "https://playbetbranchanalytics-9y45k3tx55imncdhbq8wc4.streamlit.app/", use_container_width=True)

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your credentials to access the portal.')