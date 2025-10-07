"""
Telco Customer Churn Prediction - Streamlit Frontend

A comprehensive frontend application for churn prediction with EDA insights,
modeling details, and interactive prediction capabilities.

Author: AI Assistant
Date: October 2025
"""

import streamlit as st
from auth import is_authenticated, show_login_form, show_user_info

# Page configuration
st.set_page_config(
    page_title="Telco Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
def main():
    # Check authentication
    if not is_authenticated():
        show_login_form()
        return
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("📊 Telco Customer Churn Prediction System")
    
    st.markdown("""
    Welcome to the **Telco Customer Churn Prediction System**! This comprehensive platform provides:
    
    ## 🎯 Features
    
    ### 📈 **Customer Churn Prediction** (Main Feature)
    - Upload Excel files with customer data
    - Get instant churn predictions with confidence levels
    - Batch processing for multiple customers
    - Download results as Excel reports
    
    ### 📊 **Exploratory Data Analysis (EDA)**
    - Interactive visualizations and insights
    - Customer behavior patterns
    - Feature correlations and distributions
    
    ### 🤖 **Model Details**
    - Model performance metrics
    - Feature importance analysis
    - Technical implementation details
    
    ## 🚀 Getting Started
    
    1. **Navigate** to the **"🎯 Churn Prediction"** page in the sidebar
    2. **Upload** your Excel file with customer data
    3. **Get** instant predictions with actionable recommendations
    
    ## 📋 Data Format
    
    Your Excel file should contain the following columns:
    - `gender`, `SeniorCitizen`, `Partner`, `Dependents`
    - `tenure`, `PhoneService`, `MultipleLines`, `InternetService`
    - `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`
    - `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`
    - `PaymentMethod`, `MonthlyCharges`, `TotalCharges`
    
    ## 🔧 Technical Stack
    
    - **Backend**: FastAPI with Scikit-learn
    - **Frontend**: Streamlit
    - **Model**: Recall-Optimized Logistic Regression (91.7% recall)
    - **Data Processing**: Pandas, NumPy
    """)
    
    # Add some metrics/stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model Recall", "91.7%", "🎯")
    
    with col2:
        st.metric("Model Precision", "79.1%", "📈")
    
    with col3:
        st.metric("Features Used", "20+", "📊")
    
    with col4:
        st.metric("API Response Time", "< 100ms", "⚡")
    
    st.markdown("---")
    
    # Quick start guide
    st.subheader("🎯 Quick Start Guide")
    
    with st.expander("📝 How to prepare your data"):
        st.markdown("""
        1. **Download** the sample Excel template from the Prediction page
        2. **Fill in** your customer data following the same format
        3. **Upload** the file and get instant predictions
        4. **Review** the results and recommended actions
        """)
    
    with st.expander("🔍 Understanding the predictions"):
        st.markdown("""
        - **Churn Probability**: 0-1 score indicating likelihood of churn
        - **Risk Category**: High Risk (>80%), Medium Risk (53.5-80%), Low Risk (<53.5%)
        - **Confidence Level**: Based on how certain the model is about the prediction
        - **Recommended Action**: Business actions to take based on the prediction
        """)

if __name__ == "__main__":
    main()