"""
Model Analysis Page

Displays the HTML modeling report with performance metrics, feature importance,
and technical details about the churn prediction model.
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
    page_title="Model Details",
    page_icon="🤖",
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
    
    st.title("🤖 Model Development & Analysis")
    
    st.markdown("""
    This page displays the comprehensive **Model Development and Analysis** report, including:
    - Model selection and comparison
    - Performance metrics and evaluation
    - Feature importance analysis
    - Hyperparameter tuning results
    - Model interpretation and insights
    """)
    
    # Get the path to the Modeling HTML file
    # In Docker container, outputs are at /app/outputs/
    if os.path.exists("/app/outputs"):
        modeling_html_path = Path("/app/outputs") / "02-Modelling.html"
    else:
        # Fallback for local development
        project_root = Path(__file__).parent.parent.parent.parent
        modeling_html_path = project_root / "outputs" / "02-Modelling.html"
    
    if not modeling_html_path.exists():
        st.error("📁 Modeling HTML file not found!")
        st.markdown(f"""
        Expected location: `{modeling_html_path}`
        
        **To generate the Modeling report:**
        1. Run the modeling notebook or script
        2. Ensure the HTML output is saved to the `outputs/` folder
        3. Refresh this page
        """)
        
        # Show file system info for debugging
        with st.expander("🔧 Debug Information"):
            st.write(f"**Current working directory:** {os.getcwd()}")
            st.write(f"**Project root:** {project_root}")
            st.write(f"**Looking for:** {modeling_html_path}")
            
            outputs_dir = project_root / "outputs"
            if outputs_dir.exists():
                st.write("**Files in outputs directory:**")
                for file in outputs_dir.iterdir():
                    st.write(f"  - {file.name}")
            else:
                st.write("**Outputs directory does not exist**")
        
        return
    
    # Load and display the HTML content
    st.success("✅ Modeling report found! Loading...")
    
    html_content = load_html_file(str(modeling_html_path))
    
    if html_content:
        # Add some custom styling
        st.markdown("""
        <style>
        .modeling-container {
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
            with open(modeling_html_path, 'rb') as file:
                st.download_button(
                    label="📥 Download Modeling Report (HTML)",
                    data=file.read(),
                    file_name="02-Modelling.html",
                    mime="text/html",
                    help="Download the complete modeling report as an HTML file"
                )
    
    else:
        st.error("❌ Failed to load the Modeling HTML content")
    
    # Model summary section
    st.markdown("---")
    
    st.subheader("📈 Model Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Recall (Primary Metric)",
            value="91.7%",
            delta="Optimized for recall",
            help="Percentage of actual churners correctly identified"
        )
    
    with col2:
        st.metric(
            label="Precision",
            value="79.1%",
            delta="Good balance",
            help="Percentage of predicted churners that actually churned"
        )
    
    with col3:
        st.metric(
            label="F1-Score",
            value="85.0%",
            delta="Harmonic mean",
            help="Balanced measure of precision and recall"
        )
    
    with col4:
        st.metric(
            label="Accuracy",
            value="85.2%",
            delta="Overall performance",
            help="Percentage of all predictions that were correct"
        )
    
    # Additional information section
    with st.expander("ℹ️ About the Churn Prediction Model"):
        st.markdown("""
        ### 🎯 **Model Selection**
        - **Algorithm**: Recall-Optimized Logistic Regression
        - **Optimization**: Focused on maximizing recall (sensitivity) to catch potential churners
        - **Threshold**: Custom threshold (0.535) to achieve 91.7% recall
        
        ### 🔧 **Feature Engineering**
        - **Original Features**: 20 customer attributes
        - **Engineered Features**: Life stage, service bundles, adoption scores
        - **Preprocessing**: Label encoding, standard scaling, class balancing
        
        ### ⚖️ **Model Configuration**
        - **Class Weights**: Balanced with emphasis on churn class (2x penalty)
        - **Regularization**: L2 regularization to prevent overfitting  
        - **Solver**: Limited-memory BFGS for optimization
        
        ### 🎪 **Why Recall Optimization?**
        In churn prediction, **false negatives** (missing actual churners) are more costly than 
        **false positives** (flagging loyal customers). Our model prioritizes identifying 
        potential churners, even if it means some false alarms.
        
        ### 📊 **Business Impact**
        - **91.7% Recall**: Catches 9 out of 10 customers who will actually churn
        - **Risk Stratification**: Categorizes customers into High/Medium/Low risk
        - **Actionable Insights**: Provides specific retention recommendations
        """)
    
    with st.expander("🔍 Model Comparison Details"):
        st.markdown("""
        ### 📈 **Models Evaluated**
        
        | Model | Recall | Precision | F1-Score | Notes |
        |-------|--------|-----------|----------|-------|
        | **Logistic Regression (Recall-Opt)** | **91.7%** | **79.1%** | **85.0%** | **Selected** |
        | Random Forest (Recall-Opt) | 88.3% | 73.2% | 80.1% | Good performance |
        | LightGBM (Recall-Opt) | 83.4% | 82.1% | 82.7% | Balanced approach |
        | Standard Logistic Regression | 79.1% | 85.6% | 82.2% | Baseline |
        
        ### 🏆 **Selection Criteria**
        1. **Primary**: Maximize recall (catch churners)
        2. **Secondary**: Maintain reasonable precision
        3. **Tertiary**: Model interpretability and speed
        """)

if __name__ == "__main__":
    main()