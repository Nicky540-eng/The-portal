import streamlit as st

# Secure the page so only logged-in users can see it
if st.session_state.get('authentication_status'):

    # --- ADD SIDEBAR LOGO ---
    with st.sidebar:
        try:
            st.image("logo.jpg", use_container_width=True)
        except:
            pass
        st.write("---")
        
    # --- MAIN PAGE ---
    st.markdown("<h2 style='text-align: center; color: #D32F2F;'>📚 Central Knowledge Base</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Select a module below to view standard operating procedures.</p>", unsafe_allow_html=True)
    st.write("---")

    # --- KNOWLEDGE BASE DATA ---
    kb_articles = {
        "FICA Compliance Guidelines": """
        ### FICA Verification Process
        All FICA verifications are strictly processed using the **Aardvark system**. 
        Ensure all customer documents (ID and Proof of Residence) are captured and verified directly through the Aardvark portal.
        """,
        
        "Fixtures": """
        ### Daily Fixtures Protocol
        *Standard operating procedures for managing fixtures are currently being documented and will be uploaded here soon.*
        """
    }

    # --- SELECTION & DISPLAY ---
    topic_titles = ["-- Select a Training Module --"] + list(kb_articles.keys())
    selected_topic = st.selectbox("Search Training Modules:", topic_titles)

    if selected_topic != "-- Select a Training Module --":
        st.write("---")
        with st.container(border=True):
            st.markdown(kb_articles[selected_topic])

else:
    st.warning("Please log in from the main app page to view the Knowledge Base.")