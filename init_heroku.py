#!/usr/bin/env python3
"""
Heroku Application Initialization Script

This script ensures all necessary components are properly set up
for the Heroku deployment environment.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_model_files():
    """Check if all required model files are present"""
    models_dir = Path("models")
    required_files = [
        "churn_prediction_model.pkl",
        "feature_scaler.pkl", 
        "label_encoders.pkl",
        "model_features.pkl",
        "model_metadata.pkl"
    ]
    
    missing_files = []
    for file in required_files:
        if not (models_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"Missing model files: {missing_files}")
        return False
    
    logger.info("✅ All model files found")
    return True

def check_config_files():
    """Check if configuration files are present"""
    config_dir = Path("src/frontend/config")
    
    if not (config_dir / "users.json").exists():
        logger.error("Missing users.json configuration file")
        return False
    
    logger.info("✅ Configuration files found")
    return True

def check_environment():
    """Check environment variables"""
    required_env_vars = {
        "PORT": "Heroku port assignment",
        "PYTHONPATH": "Python module path"
    }
    
    missing_vars = []
    for var, description in required_env_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({description})")
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        # Set defaults for local development
        if not os.getenv("PORT"):
            os.environ["PORT"] = "8501"
        if not os.getenv("PYTHONPATH"):
            os.environ["PYTHONPATH"] = "/app"
    
    logger.info("✅ Environment variables configured")
    return True

def initialize_app():
    """Initialize the application for Heroku deployment"""
    logger.info("🚀 Initializing Telco Churn Prediction App for Heroku...")
    
    success = True
    
    # Check all requirements
    if not check_model_files():
        success = False
    
    if not check_config_files():
        success = False
        
    if not check_environment():
        success = False
    
    if success:
        logger.info("✅ Application initialization completed successfully!")
        logger.info("📊 ML Model: Logistic Regression with 91.7% recall")
        logger.info("🔐 Authentication: Configured with demo credentials")
        logger.info("🎯 Features: Batch prediction, EDA, Model details, Admin panel")
        return True
    else:
        logger.error("❌ Application initialization failed!")
        return False

if __name__ == "__main__":
    if not initialize_app():
        sys.exit(1)