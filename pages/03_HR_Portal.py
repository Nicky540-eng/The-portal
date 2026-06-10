import streamlit as st

st.title("HR Portal")

# Simple Auth Check
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter Password", type="password")
    if password == "your_secure_password": # Replace with your password
        st.session_state.authenticated = True
        st.rerun()
else:
    st.write("Welcome to the HR Dashboard. Sensitive data displayed here.")