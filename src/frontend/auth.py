"""
Authentication utilities for the Streamlit frontend

Provides secure login functionality with password hashing and session management.
"""

import streamlit as st
import hashlib
import json
from pathlib import Path
from typing import Dict, Optional

# Configuration file path
CONFIG_DIR = Path(__file__).parent / "config"
USERS_FILE = CONFIG_DIR / "users.json"

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> Dict[str, str]:
    """Load users from configuration file"""
    try:
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create default users if file doesn't exist
            return create_default_users()
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        return create_default_users()

def create_default_users() -> Dict[str, str]:
    """Create default users and save to file"""
    default_users = {
        "admin": hash_password("churn123"),
        "demo": hash_password("demo123"),
        "user": hash_password("user123")
    }
    
    # Ensure config directory exists
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # Save to file
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
    except Exception as e:
        st.error(f"Error creating default users: {str(e)}")
    
    return default_users

def verify_credentials(username: str, password: str) -> bool:
    """Verify username and password"""
    users = load_users()
    hashed_password = hash_password(password)
    return username in users and users[username] == hashed_password

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get current authenticated user"""
    return st.session_state.get("username", None)

def login_user(username: str) -> None:
    """Log in a user"""
    st.session_state["authenticated"] = True
    st.session_state["username"] = username

def logout_user() -> None:
    """Log out the current user"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

def require_authentication():
    """Decorator-like function to require authentication for pages"""
    if not is_authenticated():
        st.error("🔒 **Access Denied**")
        st.info("Please log in through the main page to access this feature.")
        st.stop()

def show_login_form() -> bool:
    """Display login form and handle authentication"""
    st.title("🔐 Telco Churn Prediction - Login")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="text-align: center; color: #1f77b4;">🏢 Secure Access Portal</h3>
            <p style="text-align: center; color: #666;">Enter your credentials to access the churn prediction system</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            col_login, col_info = st.columns([1, 1])
            
            with col_login:
                submit_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            with col_info:
                show_demo_creds = st.form_submit_button("ℹ️ Demo Credentials", use_container_width=True)
        
        # Handle demo credentials display
        if show_demo_creds:
            st.info("""
            **Demo Credentials:**
            - Username: `demo` | Password: `demo123`
            - Username: `user` | Password: `user123`
            - Username: `admin` | Password: `churn123`
            """)
        
        # Handle login
        if submit_button:
            if not username or not password:
                st.error("❌ Please enter both username and password")
                return False
            
            if verify_credentials(username, password):
                login_user(username)
                st.success(f"✅ Welcome, {username}! Redirecting...")
                st.rerun()
                return True
            else:
                st.error("❌ Invalid username or password")
                return False
    
    # Add footer with information
    st.markdown("---")
    
    with st.expander("🔒 Security Information"):
        st.markdown("""
        ### Security Features:
        - 🔐 **Password Hashing**: All passwords are securely hashed using SHA-256
        - 🔒 **Session Management**: Secure session-based authentication
        - 👥 **User Management**: Configurable user credentials
        - 🛡️ **Access Control**: Page-level authentication protection 
        
        ### For Administrators:
        - User credentials are stored in `src/frontend/config/users.json`
        - Passwords are hashed - never stored in plain text
        - Add new users by editing the configuration file
        """)
    
    return False

def show_user_info():
    """Display current user information in sidebar"""
    if is_authenticated():
        st.sidebar.markdown("---")
        st.sidebar.success(f"👤 **Logged in as:** {get_current_user()}")
        
        if st.sidebar.button("🚪 Logout"):
            logout_user()
            st.rerun()

def add_user(username: str, password: str) -> bool:
    """Add a new user (admin function)"""
    try:
        users = load_users()
        users[username] = hash_password(password)
        
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error adding user: {str(e)}")
        return False

def remove_user(username: str) -> bool:
    """Remove a user (admin function)"""
    try:
        users = load_users()
        if username in users:
            del users[username]
            
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            
            return True
        return False
    except Exception as e:
        st.error(f"Error removing user: {str(e)}")
        return False

def change_password(username: str, new_password: str) -> bool:
    """Change user password"""
    try:
        users = load_users()
        if username in users:
            users[username] = hash_password(new_password)
            
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            
            return True
        return False
    except Exception as e:
        st.error(f"Error changing password: {str(e)}")
        return False