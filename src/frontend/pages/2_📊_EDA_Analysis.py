"""
Exploratory Data Analysis (EDA) Page

Displays the HTML EDA report generated during the analysis phase.
"""

import streamlit as st
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import require_authentication, show_user_info

# Page configuration
st.set_page_config(
    page_title="EDA Analysis",
    page_icon="📊",
    layout="wide"
)

def load_html_file(file_path: str) -> str:
    """Load HTML content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading HTML file: {str(e)}")
        return None

def main():
    # Require authentication
    require_authentication()
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("📊 Exploratory Data Analysis")
    
    st.markdown("""
    This page displays the comprehensive **Exploratory Data Analysis (EDA)** performed on the Telco customer dataset.
    The analysis includes data quality assessment, feature distributions, correlations, and key insights
    that informed the churn prediction model development.
    """)
    
    # Get the path to the EDA HTML file
    project_root = Path(__file__).parent.parent.parent.parent
    eda_html_path = project_root / "outputs" / "01-EDA.html"
    
    if not eda_html_path.exists():
        st.error("📁 EDA HTML file not found!")
        st.markdown(f"""
        Expected location: `{eda_html_path}`
        
        **To generate the EDA report:**
        1. Run the EDA notebook or script
        2. Ensure the HTML output is saved to the `outputs/` folder
        3. Refresh this page
        """)
        
        # Show file system info for debugging
        with st.expander("🔧 Debug Information"):
            st.write(f"**Current working directory:** {os.getcwd()}")
            st.write(f"**Project root:** {project_root}")
            st.write(f"**Looking for:** {eda_html_path}")
            
            outputs_dir = project_root / "outputs"
            if outputs_dir.exists():
                st.write("**Files in outputs directory:**")
                for file in outputs_dir.iterdir():
                    st.write(f"  - {file.name}")
            else:
                st.write("**Outputs directory does not exist**")
        
        return
    
    # Load and display the HTML content
    st.success("✅ EDA report found! Loading...")
    
    html_content = load_html_file(str(eda_html_path))
    
    if html_content:
        # Add some custom styling to make it look better in Streamlit
        st.markdown("""
        <style>
        .eda-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background-color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the HTML content
        st.components.v1.html(html_content, height=800, scrolling=True)
        
        # Add download button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with open(eda_html_path, 'rb') as file:
                st.download_button(
                    label="📥 Download EDA Report (HTML)",
                    data=file.read(),
                    file_name="01-EDA.html",
                    mime="text/html",
                    help="Download the complete EDA report as an HTML file"
                )
    
    else:
        st.error("❌ Failed to load the EDA HTML content")
    
    # Additional information section
    st.markdown("---")
    
    with st.expander("ℹ️ About this EDA Report"):
        st.markdown("""
        This **Exploratory Data Analysis** was performed to understand the Telco customer dataset and includes:
        
        ### 📈 **Data Overview**
        - Dataset dimensions and structure
        - Data types and missing values analysis
        - Basic statistical summaries
        
        ### 🔍 **Feature Analysis**
        - Distribution of categorical variables
        - Numerical feature distributions and outliers
        - Feature correlations and relationships
        
        ### 🎯 **Churn Analysis**
        - Churn rate distribution
        - Feature importance for churn prediction
        - Customer segmentation insights
        
        ### 📊 **Visualizations**
        - Interactive plots and charts
        - Correlation heatmaps
        - Distribution plots and box plots
        
        ### 💡 **Key Insights**
        - Factors most associated with customer churn
        - Customer behavior patterns
        - Recommendations for feature engineering
        
        This analysis directly informed the feature engineering and model selection process used in the churn prediction system.
        """)

if __name__ == "__main__":
    main()