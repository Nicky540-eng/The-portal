import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Load your credentials
with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# 2. Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 3. Render login (New v0.4+ Syntax: No variable unpacking)
try:
    authenticator.login()
except Exception as e:
    st.error(f"Login Error: {e}")

# 4. Access Control (New v0.4+ Syntax: Check session state)
if st.session_state.get('authentication_status'):
    
    # --- IF LOGGED IN ---
    with st.sidebar:
        try:
            st.image("logo.jpg", use_container_width=True)
        except:
            pass
        # Renders the logout button automatically in the sidebar
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