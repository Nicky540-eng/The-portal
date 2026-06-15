import streamlit_authenticator as stauth

# Replace 'your-new-password' with the password you actually want
password = 'your-new-password'
hashed = stauth.Hasher([password]).generate()
print(f"Password: {password}")
print(f"Hash: {hashed[0]}")