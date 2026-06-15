import streamlit_authenticator as stauth

# Replace 'yourpassword' with the password you want to use
hashed_passwords = stauth.Hasher(['yourpassword']).generate()

print(hashed_passwords[0])