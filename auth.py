import streamlit as st
import hashlib
from database import Database
from styles import apply_custom_styles

def login():
    apply_custom_styles()

    with st.container():
        st.title("Login/Register")

        # Create tabs for login and registration
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", key="login_button"):
                db = Database()
                try:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    if db.check_user_credentials(username, password_hash):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                finally:
                    db.close()

        with tab2:
            new_username = st.text_input("Username", key="reg_username")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

            if st.button("Register", key="register_button"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    db = Database()
                    try:
                        # Check if username exists
                        if db.user_exists(new_username):
                            st.error("Username already exists")
                        else:
                            # Insert new user
                            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                            db.add_user(new_username, password_hash)
                            st.success("Registration successful! Please login.")
                    finally:
                        db.close()

        st.markdown('</div>', unsafe_allow_html=True)

def check_authentication():
    return st.session_state.get('authenticated', False)