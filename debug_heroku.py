"""
Debug page for troubleshooting Heroku deployment issues
"""

import streamlit as st
import os
import sys

def show_debug_info():
    """Show debug information for troubleshooting"""
    
    st.title("🔧 Debug Information")
    st.markdown("---")
    
    # Environment information
    st.subheader("🌐 Environment")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Working Directory:**")
        st.code(os.getcwd())
        
        st.write("**Python Path:**")
        for path in sys.path[:5]:  # Show first 5 paths
            st.code(path)
    
    with col2:
        st.write("**Environment Variables:**")
        env_vars = ['PYTHONPATH', 'PORT', 'STREAMLIT_SERVER_HEADLESS']
        for var in env_vars:
            value = os.getenv(var, "Not set")
            st.code(f"{var}: {value}")
    
    # File system information
    st.subheader("📁 File System")
    
    # Check root directory
    st.write("**Root Directory Contents:**")
    try:
        root_files = os.listdir(".")
        for file in sorted(root_files):
            icon = "📁" if os.path.isdir(file) else "📄"
            st.write(f"{icon} {file}")
    except Exception as e:
        st.error(f"Error listing root directory: {e}")
    
    # Check models directory
    st.write("**Models Directory Check:**")
    models_paths = [
        "models",
        "/app/models",
        "./models",
        os.path.join(os.getcwd(), "models")
    ]
    
    for path in models_paths:
        if os.path.exists(path):
            st.success(f"✅ Found: {path}")
            try:
                files = os.listdir(path)
                st.write(f"Files in {path}:")
                for file in sorted(files):
                    st.write(f"  📄 {file}")
            except Exception as e:
                st.error(f"Error listing {path}: {e}")
        else:
            st.error(f"❌ Not found: {path}")
    
    # Check src directory structure
    st.write("**Source Directory Structure:**")
    src_path = "src"
    if os.path.exists(src_path):
        st.success(f"✅ Found: {src_path}")
        try:
            for root, dirs, files in os.walk(src_path):
                level = root.replace(src_path, '').count(os.sep)
                indent = ' ' * 2 * level
                st.write(f"{indent}📁 {os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    if file.endswith(('.py', '.json', '.txt')):
                        st.write(f"{subindent}📄 {file}")
        except Exception as e:
            st.error(f"Error walking src directory: {e}")
    else:
        st.error(f"❌ Not found: {src_path}")
    
    # Try to import and test prediction service
    st.subheader("🤖 Prediction Service Test")
    try:
        # Import prediction service
        sys.path.append(os.path.join(os.getcwd(), 'src', 'frontend'))
        from prediction_service import ChurnPredictor
        
        st.success("✅ Prediction service imported successfully")
        
        # Try to initialize
        try:
            predictor = ChurnPredictor()
            st.success("✅ Prediction service initialized successfully")
            
            # Try health check
            health = predictor.health_check()
            if health.get("status") == "healthy":
                st.success("✅ Prediction service health check passed")
                st.json(health)
            else:
                st.error("❌ Prediction service health check failed")
                st.json(health)
                
        except Exception as e:
            st.error(f"❌ Failed to initialize prediction service: {e}")
            st.exception(e)
            
    except Exception as e:
        st.error(f"❌ Failed to import prediction service: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_debug_info()