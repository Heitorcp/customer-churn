"""
Generate a sample Excel file with demo customer data for testing the Streamlit app.
"""

import pandas as pd
import os

# Create sample customer data with diverse profiles
sample_data = {
    'gender': ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'SeniorCitizen': [1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'Partner': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes'],
    'Dependents': ['No', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No'], 
    'tenure': [2, 34, 8, 45, 12, 67, 24, 15, 36, 28],
    'PhoneService': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
    'MultipleLines': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No'],
    'InternetService': ['Fiber optic', 'DSL', 'Fiber optic', 'DSL', 'No', 'Fiber optic', 'DSL', 'Fiber optic', 'DSL', 'No'],
    'OnlineSecurity': ['No', 'Yes', 'No', 'Yes', 'No internet service', 'No', 'Yes', 'No', 'Yes', 'No internet service'],
    'OnlineBackup': ['No', 'No', 'No', 'Yes', 'No internet service', 'Yes', 'No', 'No', 'Yes', 'No internet service'],
    'DeviceProtection': ['No', 'Yes', 'No', 'Yes', 'No internet service', 'No', 'Yes', 'No', 'Yes', 'No internet service'],
    'TechSupport': ['No', 'Yes', 'No', 'Yes', 'No internet service', 'No', 'Yes', 'No', 'Yes', 'No internet service'],
    'StreamingTV': ['Yes', 'No', 'Yes', 'No', 'No internet service', 'Yes', 'No', 'Yes', 'No', 'No internet service'],
    'StreamingMovies': ['Yes', 'No', 'Yes', 'No', 'No internet service', 'Yes', 'No', 'Yes', 'No', 'No internet service'],
    'Contract': ['Month-to-month', 'Two year', 'Month-to-month', 'One year', 'Month-to-month', 'Two year', 'One year', 'Month-to-month', 'Two year', 'Month-to-month'],
    'PaperlessBilling': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No'],
    'PaymentMethod': ['Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check', 'Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check'],
    'MonthlyCharges': [85.25, 56.95, 75.20, 45.30, 20.05, 89.10, 65.75, 79.85, 52.40, 19.90],
    'TotalCharges': [170.50, 1889.50, 601.60, 2038.50, 240.60, 6007.40, 1578.00, 1197.75, 1888.80, 557.20]
}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create the data directory if it doesn't exist
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Save as Excel file
output_path = os.path.join(data_dir, "sample_customer_data.xlsx")
df.to_excel(output_path, sheet_name='Customer_Data', index=False)

print(f"Sample customer data saved to: {output_path}")
print(f"Number of customers: {len(df)}")
print("\nFirst few rows:")
print(df.head())