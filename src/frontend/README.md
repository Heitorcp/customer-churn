# Telco Customer Churn Prediction - Streamlit Frontend

A comprehensive web interface for the Telco Customer Churn Prediction system, built with Streamlit.

## 🎯 Features

### 📈 **Churn Prediction** (Main Page)
- Upload Excel files with customer data
- Batch prediction processing
- Risk categorization (High/Medium/Low)
- Downloadable prediction reports
- Real-time API integration

### 📊 **EDA Analysis**
- Interactive exploratory data analysis
- Data quality insights
- Feature correlation analysis
- Customer behavior patterns

### 🤖 **Model Details**
- Model performance metrics
- Feature importance analysis
- Technical implementation details
- Model comparison results

## 🚀 Quick Start

### Prerequisites
- FastAPI backend server running on port 8081
- Python environment with required dependencies

### 🔐 Authentication
The application requires login credentials. Default accounts:

| Username | Password | Role |
|----------|----------|------|
| `admin` | `churn123` | Administrator |
| `demo` | `demo123` | Demo User |
| `user` | `user123` | Standard User |

⚠️ **Change default passwords before production use!**

### Running the Frontend

1. **Start the backend API server:**
   ```bash
   uv run task server
   ```

2. **Start the Streamlit frontend:**
   ```bash
   uv run task frontend
   ```

3. **Or run both simultaneously:**
   ```bash
   uv run task dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8081/docs

## 📋 Data Format

Your Excel file should contain the following columns:

### Customer Demographics
- `gender`: Male, Female
- `SeniorCitizen`: 0 (No), 1 (Yes)
- `Partner`: Yes, No
- `Dependents`: Yes, No

### Account Information
- `tenure`: Number of months with company (0-100)
- `Contract`: Month-to-month, One year, Two year
- `PaperlessBilling`: Yes, No
- `PaymentMethod`: Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)
- `MonthlyCharges`: Monthly charges amount (numeric)
- `TotalCharges`: Total charges amount (numeric)

### Services
- `PhoneService`: Yes, No
- `MultipleLines`: Yes, No, No phone service
- `InternetService`: DSL, Fiber optic, No
- `OnlineSecurity`: Yes, No, No internet service
- `OnlineBackup`: Yes, No, No internet service
- `DeviceProtection`: Yes, No, No internet service
- `TechSupport`: Yes, No, No internet service
- `StreamingTV`: Yes, No, No internet service
- `StreamingMovies`: Yes, No, No internet service

## 📁 Project Structure

```
src/frontend/
├── app.py                          # Main Streamlit application (with login)
├── auth.py                         # Authentication utilities
├── config/
│   ├── users.json                  # User credentials (hashed)
│   └── README.md                   # Authentication documentation
└── pages/
    ├── 1_🎯_Churn_Prediction.py    # Main prediction interface
    ├── 2_📊_EDA_Analysis.py         # EDA report display
    ├── 3_🤖_Model_Details.py        # Model analysis display
    └── 4_⚙️_Admin_Panel.py          # User management (admin only)
```

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web interface framework
- **Pandas**: Data manipulation
- **Requests**: API communication
- **OpenPyXL**: Excel file handling

### API Integration
The frontend communicates with the FastAPI backend through REST endpoints:
- `GET /health`: Check API status
- `POST /predict`: Single customer prediction
- `GET /model-info`: Model metadata

### Error Handling
- API connectivity checks
- Data validation before prediction
- User-friendly error messages
- Graceful fallbacks

## 📊 Usage Examples

### 1. Single Customer Prediction
1. Navigate to "🎯 Churn Prediction"
2. Download the sample template
3. Fill in customer data
4. Upload and get instant predictions

### 2. Batch Processing
1. Prepare Excel file with multiple customers
2. Upload file (validates data format)
3. Process all customers at once
4. Download comprehensive results report

### 3. Explore Analysis
1. Visit "📊 EDA Analysis" for data insights
2. Check "🤖 Model Details" for technical information
3. Download HTML reports for offline viewing

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop and mobile
- **Progress Indicators**: Real-time processing feedback
- **Data Validation**: Input validation with helpful error messages
- **Download Capabilities**: Export results as Excel files
- **Interactive Components**: Expandable sections and metrics
- **Professional Styling**: Clean, business-appropriate interface

## 🚨 Troubleshooting

### Common Issues

1. **API Server Not Running**
   - Ensure FastAPI server is running on port 8081
   - Check with: `curl http://127.0.0.1:8081/health`

2. **Excel Upload Errors**
   - Verify all required columns are present
   - Check data types match expected format
   - Download and use the sample template

3. **HTML Reports Not Loading**
   - Ensure HTML files exist in `outputs/` folder
   - Re-run analysis notebooks to generate reports

4. **Slow Predictions**
   - Large files may take time to process
   - Consider breaking into smaller batches

## 🔮 Future Enhancements

- Real-time predictions without file upload
- Customer segmentation visualization
- Historical trend analysis
- A/B testing interface for different models
- Integration with business intelligence tools