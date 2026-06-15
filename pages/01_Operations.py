import streamlit as st

st.set_page_config(page_title="Operations | Playbet", layout="wide")

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.write("---")

st.markdown("""
    <style>
    .tag-blue { color: #5B8EEB; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .tag-green { color: #4ADE80; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .card-desc { color: #A0AEC0; font-size: 0.9rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>⚙️ Operations Hub</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("<span class='tag-blue'>PRIORITY ALPHA</span>", unsafe_allow_html=True)
        st.subheader("Environments")
        st.markdown("<span class='card-desc'>Live & Test Frontend/Backend management.</span>", unsafe_allow_html=True)
        for label, url in [("Live FE", "https://playbet.net/page/home"), ("Test FE", "https://playbet.online.advbet.com/"), 
                           ("Test BE", "https://admin-test.adv.bet/"), ("Live BE", "https://admin.advbet.com/")]:
            st.link_button(label, url, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("<span class='tag-green'>INTERNAL NODE</span>", unsafe_allow_html=True)
        st.subheader("Gaming Backends")
        for label, url in [("EGT", "https://clienthub.egt-digital.com/sign-in/"), ("Pragmatic", "https://backoffice-1403.pragmaticplay.net/"),
                           ("Spribe", "https://clientarea-af.spribegaming.com/login"), ("Betradar", "https://auth.sportradar.com/")]:
            st.link_button(label, url, use_container_width=True)