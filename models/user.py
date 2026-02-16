"""
User Model - Handles user authentication and session management
"""

class UserModel:
    """Model for user authentication and management"""
    
    def __init__(self):
        # In production, replace with a real database
        self.users_db = {
            "user1": "password1",
            "user2": "password2"
        }
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials
        
        Args:
            username: The username to authenticate
            password: The password to authenticate
            
        Returns:
            True if credentials are valid, False otherwise
        """
        if username in self.users_db:
            return self.users_db[username] == password
        return False
    
    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists
        
        Args:
            username: The username to check
            
        Returns:
            True if user exists, False otherwise
        """
        return username in self.users_db
    
    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user
        
        Args:
            username: The username to register
            password: The password for the user
            
        Returns:
            True if registration successful, False if user already exists
        """
        if username not in self.users_db:
            self.users_db[username] = password
            return True
        return False
