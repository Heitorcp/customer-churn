"""
Unified Churn Prediction Service

Consolidated prediction service that can be used directly without FastAPI,
designed for Heroku single dyno deployment.

Author: AI Assistant
Date: October 2025
"""

import pickle
import pandas as pd
from typing import Dict, List
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChurnPredictor:
    """Unified churn prediction service"""
    
    def __init__(self, models_dir: str = "models"):
        """Initialize the predictor with model directory"""
        self.models_dir = models_dir
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.model_features = None
        self.model_metadata = None
        self._load_model_components()
    
    def _load_model_components(self):
        """Load all model components from the models directory"""
        try:
            # Load the trained model
            model_path = os.path.join(self.models_dir, "churn_prediction_model.pkl")
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            logger.info("✅ Model loaded successfully")
            
            # Load the feature scaler
            scaler_path = os.path.join(self.models_dir, "feature_scaler.pkl")
            with open(scaler_path, "rb") as f:
                self.scaler = pickle.load(f)
            logger.info("✅ Feature scaler loaded successfully")
            
            # Load label encoders
            encoders_path = os.path.join(self.models_dir, "label_encoders.pkl")
            with open(encoders_path, "rb") as f:
                self.label_encoders = pickle.load(f)
            logger.info("✅ Label encoders loaded successfully")
            
            # Load model features list
            features_path = os.path.join(self.models_dir, "model_features.pkl")
            with open(features_path, "rb") as f:
                self.model_features = pickle.load(f)
            logger.info("✅ Model features loaded successfully")
            
            # Load model metadata
            metadata_path = os.path.join(self.models_dir, "model_metadata.pkl")
            with open(metadata_path, "rb") as f:
                self.model_metadata = pickle.load(f)
            logger.info("✅ Model metadata loaded successfully")
            
            logger.info(f"🎯 Model ready! Features: {len(self.model_features)}")
            
        except Exception as e:
            logger.error(f"❌ Error loading model components: {str(e)}")
            raise Exception(f"Failed to load model components: {str(e)}")
    
    def _validate_input_data(self, data: Dict) -> Dict:
        """Validate and clean input data"""
        required_fields = [
            'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
            'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
            'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
            'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
            'MonthlyCharges', 'TotalCharges'
        ]
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Clean and validate data
        cleaned_data = data.copy()
        
        # Handle TotalCharges - convert to float if it's a string
        if isinstance(cleaned_data.get('TotalCharges'), str):
            try:
                cleaned_data['TotalCharges'] = float(cleaned_data['TotalCharges'].strip())
            except ValueError:
                cleaned_data['TotalCharges'] = 0.0
        
        # Ensure numeric fields are numeric
        numeric_fields = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
        for field in numeric_fields:
            if field in cleaned_data:
                try:
                    cleaned_data[field] = float(cleaned_data[field])
                except (ValueError, TypeError):
                    cleaned_data[field] = 0.0
        
        return cleaned_data
    
    def _preprocess_data(self, data: Dict) -> pd.DataFrame:
        """Preprocess input data for prediction"""
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Apply label encoders to categorical columns
        categorical_columns = [
            'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
            'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
            'PaperlessBilling', 'PaymentMethod'
        ]
        
        for column in categorical_columns:
            if column in df.columns and column in self.label_encoders:
                encoder = self.label_encoders[column]
                try:
                    df[column] = encoder.transform(df[column])
                except ValueError:
                    # Handle unseen categories by using the most frequent category
                    logger.warning(f"Unseen category in {column}: {df[column].iloc[0]}. Using most frequent category.")
                    most_frequent_category = encoder.classes_[0]  # Use first class as fallback
                    df[column] = encoder.transform([most_frequent_category])
        
        # Ensure all model features are present
        for feature in self.model_features:
            if feature not in df.columns:
                df[feature] = 0  # Default value for missing features
        
        # Select only the features used in training
        df = df[self.model_features]
        
        # Scale the features
        df_scaled = pd.DataFrame(
            self.scaler.transform(df),
            columns=df.columns,
            index=df.index
        )
        
        return df_scaled
    
    def predict_single(self, customer_data: Dict) -> Dict:
        """Make prediction for a single customer"""
        try:
            # Validate input data
            validated_data = self._validate_input_data(customer_data)
            
            # Preprocess the data
            processed_data = self._preprocess_data(validated_data)
            
            # Make prediction
            prediction_proba = self.model.predict_proba(processed_data)[0]
            churn_probability = float(prediction_proba[1])  # Probability of churn (class 1)
            prediction = int(churn_probability > 0.535)  # Optimal threshold
            
            # Determine risk category and recommendation
            if churn_probability > 0.80:
                risk_category = "High Risk"
                confidence = "High"
                recommendation = "Immediate intervention required. Contact customer with retention offers."
            elif churn_probability > 0.535:
                risk_category = "Medium Risk"
                confidence = "Medium"
                recommendation = "Monitor closely. Consider proactive engagement or targeted offers."
            else:
                risk_category = "Low Risk"
                confidence = "High" if churn_probability < 0.3 else "Medium"
                recommendation = "Standard service. Focus on maintaining satisfaction."
            
            return {
                "prediction": prediction,
                "churn_probability": round(churn_probability, 4),
                "risk_category": risk_category,
                "confidence": confidence,
                "recommendation": recommendation,
                "model_version": self.model_metadata.get("version", "1.0.0"),
                "prediction_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise Exception(f"Prediction failed: {str(e)}")
    
    def predict_batch(self, customers_data: List[Dict]) -> List[Dict]:
        """Make predictions for multiple customers"""
        results = []
        for i, customer_data in enumerate(customers_data):
            try:
                result = self.predict_single(customer_data)
                result["customer_id"] = i + 1
                results.append(result)
            except Exception as e:
                logger.error(f"Error predicting customer {i+1}: {str(e)}")
                results.append({
                    "customer_id": i + 1,
                    "error": str(e),
                    "prediction": None
                })
        
        return results
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            "model_type": self.model_metadata.get("model_type", "Logistic Regression"),
            "version": self.model_metadata.get("version", "1.0.0"),
            "recall_score": self.model_metadata.get("recall_score", 0.917),
            "precision_score": self.model_metadata.get("precision_score", 0.791),
            "f1_score": self.model_metadata.get("f1_score", 0.849),
            "features_count": len(self.model_features),
            "features": self.model_features
        }
    
    def health_check(self) -> Dict:
        """Health check for the prediction service"""
        try:
            # Test with dummy data
            dummy_data = {
                'gender': 'Male',
                'SeniorCitizen': 0,
                'Partner': 'No',
                'Dependents': 'No',
                'tenure': 12,
                'PhoneService': 'Yes',
                'MultipleLines': 'No',
                'InternetService': 'Fiber optic',
                'OnlineSecurity': 'No',
                'OnlineBackup': 'No',
                'DeviceProtection': 'No',
                'TechSupport': 'No',
                'StreamingTV': 'Yes',
                'StreamingMovies': 'No',
                'Contract': 'Month-to-month',
                'PaperlessBilling': 'Yes',
                'PaymentMethod': 'Electronic check',
                'MonthlyCharges': 70.0,
                'TotalCharges': 840.0
            }
            
            result = self.predict_single(dummy_data)
            
            return {
                "status": "healthy",
                "model_loaded": True,
                "components_loaded": {
                    "model": self.model is not None,
                    "scaler": self.scaler is not None,
                    "encoders": self.label_encoders is not None,
                    "features": self.model_features is not None,
                    "metadata": self.model_metadata is not None
                },
                "test_prediction": result.get("prediction") is not None,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Global predictor instance
_predictor = None

def get_predictor() -> ChurnPredictor:
    """Get the global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = ChurnPredictor()
    return _predictor