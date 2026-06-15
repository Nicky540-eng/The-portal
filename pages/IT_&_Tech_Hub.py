import streamlit as st

st.set_page_config(page_title="IT & Tech Hub", layout="wide")

# Persistent Logo in Sidebar
with st.sidebar:
    try:
        st.image("logo.jpg", use_container_width=True)
    except:
        pass
    st.write("---")

# Custom CSS to match the sleek dark-mode UI and colored tags
st.markdown("""
    <style>
    /* Tag styling */
    .tag-blue { color: #5B8EEB; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; display: block;}
    .tag-green { color: #4ADE80; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; display: block;}
    .tag-orange { color: #F97316; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; display: block;}
    
    /* Description text */
    .card-desc { color: #A0AEC0; font-size: 0.9rem; margin-bottom: 15px; display: block;}
    
    /* Button styling */
    .stLinkButton > a { border: 1px solid #444; transition: all 0.3s ease; }
    .stLinkButton > a:hover { border-color: #5B8EEB; color: #5B8EEB; }
    </style>
    """, unsafe_allow_html=True)

# Data Dictionary for Links
sections = {
    "Environments": [
        ("Live Frontend", "https://playbet.net/page/home"),
        ("Test Frontend", "https://playbet.online.advbet.com/"),
        ("Test Backend", "https://admin-test.adv.bet/"),
        ("Live Backend", "https://admin.advbet.com/")
    ],
    "Gaming": [
        ("EGT Backend", "https://clienthub.egt-digital.com/sign-in/"),
        ("Pragmatic Backend", "https://backoffice-1403.pragmaticplay.net/"),
        ("Spribe Backend", "https://clientarea-af.spribegaming.com/login"),
        ("Betradar Backend", "https://auth.sportradar.com/")
    ],
    "Analytics": [
        ("Ibex Backend", "https://ibex.ai/"),
        ("Google Ads", "https://business.google.com/en-all/google-ads/"),
        ("Google Analytics", "https://analytics.google.com/analytics/web/provision/#/provision")
    ]
}

# --- EXACT UI REPLICATION ---

# Top Row: Large Environments Card
with st.container(border=True):
    st.markdown("<span class='tag-blue'>PRIORITY ALPHA</span>", unsafe_allow_html=True)
    st.markdown("<h3>Environments</h3>", unsafe_allow_html=True)
    st.markdown("<span class='card-desc'>Staging, Production & QA sandbox management.</span>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, (label, url) in enumerate(sections["Environments"]):
        with cols[i]:
            st.link_button(label, url, use_container_width=True)

st.write("") # Small spacer

# Bottom Row: Two Columns for Gaming and Analytics
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("<span class='tag-green'>INTERNAL NODE</span>", unsafe_allow_html=True)
        st.markdown("<h3>Gaming Backends</h3>", unsafe_allow_html=True)
        st.markdown("<span class='card-desc'>Secure access to game provider administration.</span>", unsafe_allow_html=True)
        
        sub_cols = st.columns(2)
        for i, (label, url) in enumerate(sections["Gaming"]):
            with sub_cols[i % 2]:
                st.link_button(label, url, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("<span class='tag-orange'>INTERNAL NODE</span>", unsafe_allow_html=True)
        st.markdown("<h3>System Analytics</h3>", unsafe_allow_html=True)
        st.markdown("<span class='card-desc'>Network latency & uptime monitoring.</span>", unsafe_allow_html=True)
        
        sub_cols = st.columns(2)
        for i, (label, url) in enumerate(sections["Analytics"]):
            with sub_cols[i % 2]:
                st.link_button(label, url, use_container_width=True)