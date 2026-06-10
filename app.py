import streamlit as st

# Page Configuration
st.set_page_config(page_title="Playbet Portal 1.0", layout="wide")

# Styling to match Playbet Branding
st.markdown("""
    <style>
    .stButton>button { color: white; background-color: #D32F2F; border: none; font-weight: bold; }
    h1 { color: #D32F2F !important; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with Logo and Navigation
with st.sidebar:
    # Error-safe image loading: Ensure logo.jpg is in your folder
    try:
        st.image("logo.jpg", width=300)
    except:
        st.write("Playbet Portal")
        
    st.title("Navigation")
    st.write("---")
    st.write("### 📊 Internal Dashboards")
    # Stable links to your internal operational apps
    st.markdown("• [Registrations & Deposits](https://registration-and-deposits-dashboard-mucnhw8hvduhycncwghrsd.streamlit.app/)")
    st.markdown("• [Raventruck ETL](https://playbet-automation-8dvmevk5gcqmbwmes9z2sg.streamlit.app/)")
    st.markdown("• [Branch Analytics](https://playbetbranchanalytics-9y45k3tx55imncdhbq8wc4.streamlit.app/)")

# Main Hub Header
st.markdown("<h1 style='text-align: center;'>Playbet Portal 1.0</h1>", unsafe_allow_html=True)

def nav_button(label, url):
    if st.button(label, use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)

# Grid organized by sections from your PDF and requirements
sections = {
    "🌐 Environments": [
        ("Live Frontend", "https://playbet.net/page/home"),
        ("Test Frontend", "https://playbet.online.advbet.com/"),
        ("Test Backend", "https://admin-test.adv.bet/"),
        ("Live Backend", "https://admin.advbet.com/")
    ],
    "🎮 Gaming Backends": [
        ("EGT Backend", "https://clienthub.egt-digital.com/sign-in/"),
        ("Pragmatic Backend", "https://backoffice-1403.pragmaticplay.net/"),
        ("Spribe Backend", "https://clientarea-af.spribegaming.com/login"),
        ("Betradar Backend", "https://auth.sportradar.com/"),
        ("Freshdesk Backend", "https://playbet.freshworks.com/")
    ],
    "📈 Operations & Marketing": [
        ("Walletdoc Backend", "https://www.walletdoc.com/"),
        ("OTT Backend", "https://merchant.ott-mobile.com/"),
        ("Rocketmailer Backend", "https://comms.rocketseed.net/"),
        ("BulkSMS Backend", "https://www.bulksms.com/")
    ],
    "🤖 Analytics & AI": [
        ("Ibex Backend", "https://ibex.ai/"),
        ("Google Ads Backend", "https://business.google.com/en-all/google-ads/"),
        ("Google Analytics Backend", "https://analytics.google.com/analytics/web/provision/#/provision")
    ]
}

# Display sections in a neat grid
for title, buttons in sections.items():
    with st.expander(title, expanded=True):
        cols = st.columns(len(buttons))
        for i, (label, url) in enumerate(buttons):
            with cols[i]:
                nav_button(label, url)