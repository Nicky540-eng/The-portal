import streamlit as st

st.set_page_config(page_title="Customer Service | Playbet", layout="wide")

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.write("---")

st.markdown("""
    <style>
    .tag-blue { color: #5B8EEB; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .card-desc { color: #A0AEC0; font-size: 0.9rem; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>🎧 Customer Service Hub</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("<span class='tag-blue'>SUPPORT NODE</span>", unsafe_allow_html=True)
        st.subheader("Ticketing & Support")
        st.markdown("<span class='card-desc'>Manage support tickets, VIP queues, and resolutions.</span>", unsafe_allow_html=True)
        st.link_button("Freshdesk Admin", "https://playbet.freshworks.com/", use_container_width=True)
        st.link_button("Live Chat Platform", "https://your-live-chat-link.com/", use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("<span class='tag-blue'>SERVICE METRICS</span>", unsafe_allow_html=True)
        st.subheader("Agent Analytics")
        st.markdown("<span class='card-desc'>Performance KPIs and response time tracking.</span>", unsafe_allow_html=True)
        st.link_button("Support Dashboard", "https://your-analytics-link.com/", use_container_width=True)