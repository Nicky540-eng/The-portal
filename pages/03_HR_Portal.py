import streamlit as st

st.set_page_config(page_title="HR Portal | Playbet", layout="wide")

# Persistent Logo in Sidebar
with st.sidebar:
    try:
        st.image("logo.jpg", use_container_width=True)
    except:
        pass
    st.write("---")

st.markdown("""
    <style>
    h2 { color: #D32F2F !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>👥 HR Portal</h2>", unsafe_allow_html=True)
st.write("Employee directories, leave management, and internal resources.")
st.write("---")

st.info("HR dashboard integration is currently in development. Modules will be available here soon.")