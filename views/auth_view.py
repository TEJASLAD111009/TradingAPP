"""
Authentication View - Handles login and logout UI
"""
import streamlit as st
from models.user import UserModel

class AuthView:
    """View for user authentication (login/logout)"""
    
    def __init__(self, user_model: UserModel):
        """
        Initialize auth view
        
        Args:
            user_model: The user model instance
        """
        self.user_model = user_model
    
    def show_login(self) -> tuple[str, bool]:
        """
        Display login form
        
        Returns:
            Tuple of (username, login_success)
        """
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            if self.user_model.authenticate(username, password):
                st.sidebar.success("Login Successful!")
                return username, True
            else:
                st.sidebar.error("Invalid username or password.")
                return None, False
        
        return None, False
    
    def show_logout(self) -> bool:
        """
        Display logout button
        
        Returns:
            True if logout button clicked, False otherwise
        """
        if st.sidebar.button("Logout"):
            st.sidebar.success("Logged out successfully!")
            return True
        return False
    
    def show_register(self) -> bool:
        """
        Display registration form
        
        Returns:
            True if registration successful, False otherwise
        """
        st.sidebar.header("Register")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        
        if st.sidebar.button("Register"):
            if new_username and new_password:
                if self.user_model.register_user(new_username, new_password):
                    st.sidebar.success("Registration successful! You can now login.")
                    return True
                else:
                    st.sidebar.error("Username already exists.")
            else:
                st.sidebar.error("Please enter both username and password.")
        
        return False
