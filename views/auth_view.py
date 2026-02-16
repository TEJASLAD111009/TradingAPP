"""Streamlit views for authentication."""
import streamlit as st
from controllers import AuthController
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def login_page():
    """Display login page."""
    st.title("🔐 Trading App - Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Sign In to Your Account")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_login, col_demo = st.columns(2)
        
        with col_login:
            if st.button("🔓 Login", use_container_width=True):
                if username and password:
                    success, message = AuthController.login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter both username and password")
        
        with col_demo:
            st.markdown("**Demo Credentials:**")
            st.markdown("""
            - Username: `demo`
            - Password: `demo123`
            
            - Username: `trader`
            - Password: `trader123`
            """)
        
        st.divider()
        
        st.markdown("### Create New Account")
        new_username = st.text_input("New Username", placeholder="Choose a username", key="new_user")
        new_password = st.text_input("New Password", type="password", placeholder="Create a password", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="confirm_pass")
        
        if st.button("📝 Register", use_container_width=True):
            if not new_username or not new_password:
                st.warning("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                success, message = AuthController.register(new_username, new_password)
                if success:
                    st.success(message)
                    st.info("You can now login with your new account!")
                else:
                    st.error(message)


def logout():
    """Handle logout."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully!")
    st.rerun()


def check_login():
    """Check if user is logged in."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
    
    return st.session_state.logged_in, st.session_state.username
