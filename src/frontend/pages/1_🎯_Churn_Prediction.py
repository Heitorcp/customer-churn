"""
Churn Prediction Page

Interactive page for uploading customer data and getting churn predictions
from the FastAPI backend.
"""

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import time
from typing import Dict, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import require_authentication, show_user_info

# Page configuration
st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🎯",
    layout="wide"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8081")

def check_api_health() -> bool:
    """Check if the API is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("status") == "healthy"
    except Exception:
        return False

def predict_single_customer(customer_data: Dict) -> Dict:
    """Make prediction for a single customer"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=customer_data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {str(e)}")
        return None

def validate_customer_data(df: pd.DataFrame) -> tuple[bool, List[str]]:
    """Validate the uploaded customer data"""
    required_columns = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
        'MonthlyCharges', 'TotalCharges'
    ]
    
    errors = []
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check data types and values
    if 'gender' in df.columns:
        invalid_gender = df[~df['gender'].isin(['Male', 'Female'])]['gender'].unique()
        if len(invalid_gender) > 0:
            errors.append(f"Invalid gender values: {', '.join(invalid_gender)}. Must be 'Male' or 'Female'")
    
    if 'SeniorCitizen' in df.columns:
        invalid_senior = df[~df['SeniorCitizen'].isin([0, 1])]['SeniorCitizen'].unique()
        if len(invalid_senior) > 0:
            errors.append(f"Invalid SeniorCitizen values: {', '.join(map(str, invalid_senior))}. Must be 0 or 1")
    
    # Check Yes/No fields
    yes_no_fields = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for field in yes_no_fields:
        if field in df.columns:
            invalid_values = df[~df[field].isin(['Yes', 'No'])][field].unique()
            if len(invalid_values) > 0:
                errors.append(f"Invalid {field} values: {', '.join(invalid_values)}. Must be 'Yes' or 'No'")
    
    return len(errors) == 0, errors

def create_sample_excel() -> BytesIO:
    """Create a sample Excel file for download"""
    sample_data = {
        'gender': ['Female', 'Male', 'Female', 'Male', 'Female'],
        'SeniorCitizen': [1, 0, 1, 0, 0],
        'Partner': ['No', 'Yes', 'No', 'Yes', 'No'],
        'Dependents': ['No', 'Yes', 'No', 'No', 'Yes'],
        'tenure': [2, 34, 8, 45, 12],
        'PhoneService': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'MultipleLines': ['No', 'Yes', 'No', 'Yes', 'No'],
        'InternetService': ['Fiber optic', 'DSL', 'Fiber optic', 'DSL', 'No'],
        'OnlineSecurity': ['No', 'Yes', 'No', 'Yes', 'No internet service'],
        'OnlineBackup': ['No', 'No', 'No', 'Yes', 'No internet service'],
        'DeviceProtection': ['No', 'Yes', 'No', 'Yes', 'No internet service'],
        'TechSupport': ['No', 'Yes', 'No', 'Yes', 'No internet service'],
        'StreamingTV': ['Yes', 'No', 'Yes', 'No', 'No internet service'],
        'StreamingMovies': ['Yes', 'No', 'Yes', 'No', 'No internet service'],
        'Contract': ['Month-to-month', 'Two year', 'Month-to-month', 'One year', 'Month-to-month'],
        'PaperlessBilling': ['Yes', 'No', 'Yes', 'No', 'Yes'],
        'PaymentMethod': ['Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check'],
        'MonthlyCharges': [85.25, 56.95, 75.20, 45.30, 20.05],
        'TotalCharges': [170.50, 1889.50, 601.60, 2038.50, 240.60]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Customer_Data', index=False)
    output.seek(0)
    
    return output

def main():
    # Require authentication
    require_authentication()
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("🎯 Customer Churn Prediction")
    
    # Check API health
    if not check_api_health():
        st.error("🚨 **API Server is not running!**")
        st.markdown("""
        Please start the API server first:
        ```bash
        uv run task server
        ```
        The API should be running on http://127.0.0.1:8081
        """)
        return
    
    st.success("✅ API Server is running and healthy!")
    
    # Download sample template
    st.subheader("📥 Download Sample Template")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("Download the sample Excel template to see the expected data format")
    
    with col2:
        sample_excel = create_sample_excel()
        st.download_button(
            label="📊 Download Sample Excel",
            data=sample_excel,
            file_name="sample_customer_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📤 Upload Customer Data")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file with customer data",
        type=['xlsx', 'xls'],
        help="Upload an Excel file containing customer data following the sample template format"
    )
    
    if uploaded_file is not None:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.info(f"📊 **Total customers:** {len(df)}")
            
            # Validate data
            is_valid, validation_errors = validate_customer_data(df)
            
            if not is_valid:
                st.error("❌ **Data Validation Failed:**")
                for error in validation_errors:
                    st.error(f"• {error}")
                return
            
            st.success("✅ Data validation passed!")
            
            # Prediction section
            if st.button("🔮 **Predict Churn for All Customers**", type="primary"):
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                predictions = []
                
                for idx, row in df.iterrows():
                    status_text.text(f"Processing customer {idx + 1} of {len(df)}...")
                    progress_bar.progress((idx + 1) / len(df))
                    
                    # Convert row to dictionary for API
                    customer_data = row.to_dict()
                    
                    # Make prediction
                    prediction = predict_single_customer(customer_data)
                    
                    if prediction:
                        predictions.append({
                            'Customer_ID': idx + 1,
                            'Churn_Probability': prediction['churn_probability'],
                            'Churn_Prediction': prediction['churn_prediction'],
                            'Risk_Category': prediction['risk_category'],
                            'Confidence_Level': prediction['confidence_level'],
                            'Recommended_Action': prediction['recommended_action']
                        })
                    else:
                        predictions.append({
                            'Customer_ID': idx + 1,
                            'Churn_Probability': 'Error',
                            'Churn_Prediction': 'Error',
                            'Risk_Category': 'Error',
                            'Confidence_Level': 'Error',
                            'Recommended_Action': 'Prediction failed'
                        })
                    
                    # Small delay to prevent overwhelming the API
                    time.sleep(0.1)
                
                status_text.text("✅ Predictions completed!")
                progress_bar.progress(1.0)
                
                # Display results
                st.subheader("📊 Prediction Results")
                
                results_df = pd.DataFrame(predictions)
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    high_risk = len(results_df[results_df['Risk_Category'] == 'High Risk'])
                    st.metric("High Risk Customers", high_risk)
                
                with col2:
                    medium_risk = len(results_df[results_df['Risk_Category'] == 'Medium Risk'])
                    st.metric("Medium Risk Customers", medium_risk)
                
                with col3:
                    low_risk = len(results_df[results_df['Risk_Category'] == 'Low Risk'])
                    st.metric("Low Risk Customers", low_risk)
                
                with col4:
                    will_churn = len(results_df[results_df['Churn_Prediction'] == 'Will Churn'])
                    st.metric("Predicted Churners", will_churn)
                
                # Display full results table
                st.dataframe(results_df, use_container_width=True)
                
                # Download results
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Original data
                    df.to_excel(writer, sheet_name='Original_Data', index=False)
                    # Predictions
                    results_df.to_excel(writer, sheet_name='Predictions', index=False)
                    # Combined data
                    combined_df = pd.concat([df.reset_index(drop=True), results_df.drop('Customer_ID', axis=1)], axis=1)
                    combined_df.to_excel(writer, sheet_name='Combined_Results', index=False)
                
                output.seek(0)
                
                st.download_button(
                    label="📥 Download Prediction Results",
                    data=output,
                    file_name=f"churn_predictions_{time.strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure your Excel file follows the correct format. Download the sample template for reference.")

if __name__ == "__main__":
    main()