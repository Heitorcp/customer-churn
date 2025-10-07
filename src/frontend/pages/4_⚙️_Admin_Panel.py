"""
Admin Page - User Management

Administrative interface for managing user accounts and system configuration.
Only accessible by admin users.
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import (
    require_authentication, show_user_info, get_current_user,
    load_users, add_user, remove_user, change_password
)

# Page configuration
st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

def is_admin() -> bool:
    """Check if current user is admin"""
    return get_current_user() == "admin"

def show_user_management():
    """Display user management interface"""
    st.subheader("👥 User Management")
    
    # Load current users
    users = load_users()
    
    # Display current users
    st.write("**Current Users:**")
    user_df_data = []
    for username in users.keys():
        role = "Administrator" if username == "admin" else "Standard User"
        user_df_data.append({"Username": username, "Role": role})
    
    if user_df_data:
        st.table(user_df_data)
    else:
        st.info("No users found.")
    
    # Add new user
    st.markdown("---")
    st.subheader("➕ Add New User")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username", placeholder="Enter new username")
        
        with col2:
            new_password = st.text_input("Password", type="password", placeholder="Enter password")
        
        add_button = st.form_submit_button("➕ Add User", type="primary")
        
        if add_button:
            if not new_username or not new_password:
                st.error("❌ Please provide both username and password")
            elif new_username in users:
                st.error(f"❌ User '{new_username}' already exists")
            else:
                if add_user(new_username, new_password):
                    st.success(f"✅ User '{new_username}' added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add user")
    
    # Remove user
    st.markdown("---")
    st.subheader("❌ Remove User")
    
    with st.form("remove_user_form"):
        remove_username = st.selectbox(
            "Select user to remove:", 
            options=[u for u in users.keys() if u != "admin"],
            help="Admin user cannot be removed"
        )
        
        remove_button = st.form_submit_button("❌ Remove User", type="secondary")
        
        if remove_button and remove_username:
            if st.checkbox(f"⚠️ Confirm removal of user '{remove_username}'"):
                if remove_user(remove_username):
                    st.success(f"✅ User '{remove_username}' removed successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to remove user")
    
    # Change password
    st.markdown("---")
    st.subheader("🔑 Change User Password")
    
    with st.form("change_password_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            change_username = st.selectbox("Select user:", options=list(users.keys()))
        
        with col2:
            new_pwd = st.text_input("New Password", type="password")
        
        change_button = st.form_submit_button("🔑 Change Password", type="primary")
        
        if change_button:
            if not new_pwd:
                st.error("❌ Please provide a new password")
            else:
                if change_password(change_username, new_pwd):
                    st.success(f"✅ Password changed for user '{change_username}'!")
                else:
                    st.error("❌ Failed to change password")

def show_system_info():
    """Display system information"""
    st.subheader("📊 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        users = load_users()
        st.metric("Total Users", len(users))
    
    with col2:
        admin_count = sum(1 for u in users.keys() if u == "admin")
        st.metric("Admin Users", admin_count)
    
    with col3:
        regular_count = len(users) - admin_count
        st.metric("Regular Users", regular_count)
    
    # Authentication stats (could be expanded with actual login tracking)
    st.markdown("---")
    st.subheader("🔐 Security Settings")
    
    with st.expander("Password Security"):
        st.info("""
        **Current Security Measures:**
        - ✅ SHA-256 password hashing
        - ✅ Session-based authentication
        - ✅ Page-level access control
        - ✅ Admin role separation
        
        **Recommendations:**
        - Change default passwords regularly
        - Use strong, unique passwords
        - Monitor user access logs
        - Consider multi-factor authentication for production
        """)

def main():
    # Require authentication
    require_authentication()
    
    # Check admin access
    if not is_admin():
        st.error("🚫 **Access Denied**")
        st.warning("This page is only accessible by administrators.")
        st.info(f"Current user: **{get_current_user()}**")
        st.stop()
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("⚙️ Admin Panel")
    
    st.markdown("""
    Welcome to the **Administrative Panel**. Here you can manage user accounts, 
    view system information, and configure security settings.
    """)
    
    # Admin warning
    st.warning("⚠️ **Administrative Access** - Use these tools carefully!")
    
    # Tabs for different admin functions
    tab1, tab2 = st.tabs(["👥 User Management", "📊 System Info"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_system_info()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        🔐 Admin Panel - Telco Churn Prediction System<br>
        Logged in as: <strong>{}</strong>
    </div>
    """.format(get_current_user()), unsafe_allow_html=True)

if __name__ == "__main__":
    main()