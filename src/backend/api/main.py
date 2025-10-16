"""
Telco Customer Churn Prediction API

A FastAPI service that serves the trained recall-optimized logistic regression model
for predicting customer churn with 91.7% recall performance.

Author: AI Assistant
Date: October 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from typing import List, Optional
import os
from datetime import datetime
import logging

# Import schemas from the package
from .schemas import CustomerData, ChurnPrediction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="Predict customer churn using a recall-optimized logistic regression model (91.7% recall)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow local dev frontends to access the API (and static EDA) during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model components
model = None
scaler = None
label_encoders = None
model_features = None
model_metadata = None

def load_model_components():
    """Load all model components from the models directory"""
    global model, scaler, label_encoders, model_features, model_metadata
    
    # Get the absolute path to the models directory
    # In Docker container, models are at /app/models/
    if os.path.exists("/app/models"):
        models_dir = "/app/models"
    else:
        # Fallback for local development (3 levels up from current file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(current_dir, "..", "..", "..", "models")
        models_dir = os.path.abspath(models_dir)
    
    try:
        # Load the trained model
        with open(os.path.join(models_dir, "churn_prediction_model.pkl"), 'rb') as f:
            model = pickle.load(f)
            
        # Load the scaler
        with open(os.path.join(models_dir, "feature_scaler.pkl"), 'rb') as f:
            scaler = pickle.load(f)
            
        # Load label encoders
        with open(os.path.join(models_dir, "label_encoders.pkl"), 'rb') as f:
            label_encoders = pickle.load(f)
            
        # Load model features
        with open(os.path.join(models_dir, "model_features.pkl"), 'rb') as f:
            model_features = pickle.load(f)
            
        # Load model metadata
        with open(os.path.join(models_dir, "model_metadata.pkl"), 'rb') as f:
            model_metadata = pickle.load(f)
            
        logger.info("All model components loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model components: {str(e)}")
        return False

# Mount static outputs directory for serving EDA report (and other artifacts)
def mount_outputs_if_available():
    try:
        outputs_dir = None
        if os.path.isdir("/app/outputs"):
            outputs_dir = "/app/outputs"
        else:
            # Compute repo root relative to this file: src/backend/api/main.py -> repo_root/outputs
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            local_outputs = os.path.abspath(os.path.join(repo_root, "outputs"))
            if os.path.isdir(local_outputs):
                outputs_dir = local_outputs

        if outputs_dir:
            app.mount("/outputs", StaticFiles(directory=outputs_dir), name="outputs")
            logger.info(f"Mounted static outputs directory at /outputs from: {outputs_dir}")
        else:
            logger.warning("No outputs directory found to mount. EDA report may not be available.")
    except Exception as e:
        logger.error(f"Failed to mount outputs directory: {e}")

def preprocess_customer_data(customer_data: CustomerData) -> pd.DataFrame:
    """Preprocess customer data to match model expectations"""
    
    # Convert to dictionary
    data_dict = customer_data.dict()
    
    # Create DataFrame
    df = pd.DataFrame([data_dict])
    
    # Apply the same feature engineering as during training
    
    # 1. Senior Citizen Label
    df['SeniorCitizen_Label'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    
    # 2. Life Stage feature
    def determine_life_stage(row):
        if row['SeniorCitizen'] == 1:
            return 'Senior Individual' if row['Partner'] == 'No' else 'Senior Couple'
        else:
            if row['Partner'] == 'No':
                return 'Young Individual'
            elif row['Dependents'] == 'Yes':
                return 'Young Family'
            else:
                return 'Young Couple'
    
    df['LifeStage'] = df.apply(determine_life_stage, axis=1)
    
    # 3. Service Bundle Features
    bundle_definitions = {
        'SecurityBundle': ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection'],
        'StreamingBundle': ['StreamingTV', 'StreamingMovies'], 
        'OnlinePerksBundle': ['OnlineSecurity', 'OnlineBackup', 'TechSupport'],
        'BasicSupportBundle': ['TechSupport', 'DeviceProtection']
    }
    
    for bundle_name, services in bundle_definitions.items():
        df[bundle_name] = (df[services] == 'Yes').sum(axis=1).apply(lambda x: 1 if x >= len(services) else 0)
    
    # 4. Service Adoption Score
    def calculate_service_score(row):
        score = 0
        high_value_services = ['InternetService', 'OnlineSecurity', 'OnlineBackup', 
                              'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        
        for service in high_value_services:
            if service == 'InternetService':
                if row[service] == 'Fiber optic':
                    score += 2
                elif row[service] == 'DSL':
                    score += 1
            else:
                if row[service] == 'Yes':
                    score += 1
        return score
    
    df['ServiceAdoptionScore'] = df.apply(calculate_service_score, axis=1)
    
    # 5. Financial Features
    df['MonthlyChargesPerService'] = df['MonthlyCharges'] / (df['ServiceAdoptionScore'] + 1)
    
    # 6. Tenure categories
    def categorize_tenure(tenure):
        if tenure <= 12:
            return 'New_Customer'
        elif tenure <= 36:
            return 'Established_Customer'
        else:
            return 'Long_Term_Customer'
    
    df['TenureCategory'] = df['tenure'].apply(categorize_tenure)
    
    # 7. Internet Service Quality
    df['HasFiberOptic'] = (df['InternetService'] == 'Fiber optic').astype(int)
    df['HasInternet'] = (df['InternetService'] != 'No').astype(int)
    
    # Encode categorical features
    categorical_features = [
        'gender', 'SeniorCitizen_Label', 'Partner', 'Dependents', 
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod',
        'LifeStage', 'TenureCategory'
    ]
    
    for feature in categorical_features:
        if feature in df.columns and feature in label_encoders:
            # Handle unseen categories
            le = label_encoders[feature]
            df[feature + '_encoded'] = df[feature].apply(
                lambda x: le.transform([x])[0] if x in le.classes_ else 0
            )
    
    # Select final features matching model expectations
    final_df = df[model_features].copy()
    
    # Scale numerical features
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'ServiceAdoptionScore', 'MonthlyChargesPerService']
    numerical_cols_to_scale = [col for col in model_features if col in numerical_features]
    
    if numerical_cols_to_scale:
        final_df[numerical_cols_to_scale] = scaler.transform(final_df[numerical_cols_to_scale])
    
    return final_df

@app.on_event("startup")
async def startup_event():
    """Load model components on startup"""
    logger.info("Starting Telco Churn Prediction API...")
    mount_outputs_if_available()
    
    if not load_model_components():
        logger.error("Failed to load model components. API may not function correctly.")
    else:
        logger.info("API ready to serve predictions!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Telco Customer Churn Prediction API",
        "version": "1.0.0",
        "description": "Predict customer churn with 91.7% recall accuracy",
        "endpoints": {
            "prediction": "/predict",
            "health": "/health",
            "model_info": "/model-info",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None and scaler is not None and label_encoders is not None
    
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().isoformat(),
        "model_info": {
            "name": model_metadata.get("model_name") if model_metadata else "Unknown",
            "recall": f"{model_metadata.get('performance_metrics', {}).get('recall', 0):.3f}" if model_metadata else "Unknown"
        }
    }

@app.get("/model-info")
async def get_model_info():
    """Get detailed model information"""
    if model_metadata is None:
        raise HTTPException(status_code=500, detail="Model metadata not loaded")
    
    return {
        "model_details": model_metadata,
        "feature_count": len(model_features) if model_features else 0,
        "model_type": "Logistic Regression (Recall-Optimized)",
        "deployment_info": {
            "api_version": "1.0.0",
            "last_loaded": datetime.now().isoformat()
        }
    }

@app.post("/predict", response_model=ChurnPrediction)
async def predict_churn(customer_data: CustomerData, customer_id: Optional[str] = None):
    """
    Predict customer churn probability
    
    Returns:
    - Churn probability (0-1)
    - Churn prediction (Will Churn/Will Stay)
    - Risk category and recommended actions
    """
    
    # Check if model is loaded
    if model is None or scaler is None or label_encoders is None:
        raise HTTPException(status_code=500, detail="Model components not properly loaded")
    
    try:
        # Preprocess the data
        processed_data = preprocess_customer_data(customer_data)
        
        # Make prediction
        churn_probability = model.predict_proba(processed_data)[0, 1]
        
        # Use recommended threshold (0.535 for 90% recall)
        recommended_threshold = model_metadata.get("recommended_threshold", 0.5)
        churn_prediction = "Will Churn" if churn_probability >= recommended_threshold else "Will Stay"
        
        # Determine confidence level
        if churn_probability >= 0.8 or churn_probability <= 0.2:
            confidence_level = "High"
        elif churn_probability >= 0.6 or churn_probability <= 0.4:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
        
        # Determine risk category and recommendations
        if churn_probability >= 0.8:
            risk_category = "High Risk"
            recommended_action = "Immediate intervention: Contact customer with retention offers, personalized discounts, or service upgrades"
        elif churn_probability >= 0.535:  # Above recommended threshold
            risk_category = "Medium Risk"
            recommended_action = "Proactive outreach: Schedule customer satisfaction call, offer service bundle upgrades, review account"
        else:
            risk_category = "Low Risk"
            recommended_action = "Monitor: Include in regular customer satisfaction surveys, consider upselling opportunities"
        
        # Prepare model info
        model_info = {
            "model_name": model_metadata.get("model_name", "Unknown"),
            "recall": model_metadata.get("performance_metrics", {}).get("recall", 0),
            "threshold_used": recommended_threshold,
            "prediction_timestamp": datetime.now().isoformat()
        }
        
        return ChurnPrediction(
            customer_id=customer_id,
            churn_probability=round(churn_probability, 4),
            churn_prediction=churn_prediction,
            confidence_level=confidence_level,
            risk_category=risk_category,
            recommended_action=recommended_action,
            model_info=model_info
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch")
async def predict_churn_batch(customers: List[CustomerData]):
    """
    Predict churn for multiple customers
    
    Returns list of predictions for batch processing
    """
    
    if len(customers) > 100:
        raise HTTPException(status_code=400, detail="Batch size limited to 100 customers")
    
    predictions = []
    
    for i, customer in enumerate(customers):
        try:
            prediction = await predict_churn(customer, customer_id=f"batch_{i}")
            predictions.append(prediction)
        except Exception as e:
            logger.error(f"Error predicting customer {i}: {str(e)}")
            # Add error entry
            predictions.append({
                "customer_id": f"batch_{i}",
                "error": str(e),
                "churn_probability": None,
                "churn_prediction": "Error"
            })
    
    return {
        "batch_size": len(customers),
        "predictions": predictions,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)