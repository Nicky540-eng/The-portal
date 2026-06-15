import streamlit as st

st.set_page_config(page_title="Marketing & Promos | Playbet", layout="wide")
if not st.session_state.get('authentication_status'):
    st.error("🔒 Access Denied. Please log in from the main portal page.")
    st.stop()  

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.write("---")

st.markdown("<h2>📣 Marketing & Promotions</h2>", unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Communication & Affiliate Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Rocketmailer", "https://comms.rocketseed.net/", use_container_width=True)
        st.link_button("BulkSMS", "https://www.bulksms.com/", use_container_width=True)
    with col2:
        st.link_button("Freshdesk", "https://playbet.freshworks.com/", use_container_width=True)
        st.link_button("Walletdoc", "https://www.walletdoc.com/", use_container_width=True)