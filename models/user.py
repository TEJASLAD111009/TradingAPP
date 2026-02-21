"""User model for authentication and user management."""
import json
import os
from typing import Optional
from datetime import datetime
import hashlib


class User:
    """User model to handle user data and authentication."""
    
    def __init__(self, username: str, password: str = None): # type: ignore
        """Initialize a user object.
        
        Args:
            username: Username for the user
            password: Password for the user (hashed)
        """
        self.username = username
        self.password = password
        self.created_at = datetime.now().isoformat()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }


class UserManager:
    """Manages user persistence and authentication."""
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    
    @classmethod
    def initialize_default_users(cls):
        if not os.path.exists(cls.USERS_FILE):
            os.makedirs(os.path.dirname(cls.USERS_FILE), exist_ok=True)

            default_users = {
                'demo': User.hash_password('demo123'),
                'trader': User.hash_password('trader123'),
                'user': User.hash_password('password123')
            }
            with open(cls.USERS_FILE, 'w') as f:
                json.dump(default_users, f, indent=4)
    @classmethod
    def authenticate(cls, username: str, password: str) -> bool:
        """Authenticate a user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            True if authentication is successful
        """
        cls.initialize_default_users()
        try:
            with open(cls.USERS_FILE, 'r') as f:
                users = json.load(f)
            
            if username not in users:
                return False
            
            hashed_password = User.hash_password(password)
            return users[username] == hashed_password
        except Exception as e:
            print(f"Error during authentication: {e}")
            return False
    
    @classmethod
    def user_exists(cls, username: str) -> bool:
        """Check if a user exists.
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists
        """
        cls.initialize_default_users()
        try:
            with open(cls.USERS_FILE, 'r') as f:
                users = json.load(f)
            return username in users
        except Exception:
            return False
    
    @classmethod
    def create_user(cls, username: str, password: str) -> bool:
        """Create a new user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            True if user was created successfully
        """
        cls.initialize_default_users()
        try:
            with open(cls.USERS_FILE, 'r') as f:
                users = json.load(f)
            
            if username in users:
                return False  # User already exists
            
            users[username] = User.hash_password(password)
            
            with open(cls.USERS_FILE, 'w') as f:
                json.dump(users, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
