"""
Pydantic schemas for the Telco Customer Churn Prediction API

This module contains all data models used for request/response validation.
"""

from typing import Optional, Dict
from pydantic import BaseModel, Field, validator


class CustomerData(BaseModel):
    """Customer data input schema for churn prediction"""
    
    # Demographics
    gender: str = Field(..., description="Customer gender: Male, Female")
    SeniorCitizen: int = Field(..., ge=0, le=1, description="Senior citizen flag: 0 or 1")
    Partner: str = Field(..., description="Has partner: Yes, No")
    Dependents: str = Field(..., description="Has dependents: Yes, No")
    
    # Account Information
    tenure: int = Field(..., ge=0, le=100, description="Number of months with company")
    Contract: str = Field(..., description="Contract type: Month-to-month, One year, Two year")
    PaperlessBilling: str = Field(..., description="Paperless billing: Yes, No")
    PaymentMethod: str = Field(..., description="Payment method: Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges amount")
    TotalCharges: float = Field(..., ge=0, description="Total charges amount")
    
    # Services
    PhoneService: str = Field(..., description="Phone service: Yes, No")
    MultipleLines: str = Field(..., description="Multiple lines: Yes, No, No phone service")
    InternetService: str = Field(..., description="Internet service: DSL, Fiber optic, No")
    OnlineSecurity: str = Field(..., description="Online security: Yes, No, No internet service")
    OnlineBackup: str = Field(..., description="Online backup: Yes, No, No internet service")
    DeviceProtection: str = Field(..., description="Device protection: Yes, No, No internet service")
    TechSupport: str = Field(..., description="Tech support: Yes, No, No internet service")
    StreamingTV: str = Field(..., description="Streaming TV: Yes, No, No internet service")
    StreamingMovies: str = Field(..., description="Streaming movies: Yes, No, No internet service")

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v

    @validator('Partner', 'Dependents', 'PaperlessBilling', 'PhoneService')
    def validate_yes_no(cls, v):
        if v not in ['Yes', 'No']:
            raise ValueError('Value must be Yes or No')
        return v

    @validator('Contract')
    def validate_contract(cls, v):
        valid_contracts = ['Month-to-month', 'One year', 'Two year']
        if v not in valid_contracts:
            raise ValueError(f'Contract must be one of: {valid_contracts}')
        return v

    @validator('PaymentMethod')
    def validate_payment_method(cls, v):
        valid_methods = ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
        if v not in valid_methods:
            raise ValueError(f'PaymentMethod must be one of: {valid_methods}')
        return v

    @validator('InternetService')
    def validate_internet_service(cls, v):
        if v not in ['DSL', 'Fiber optic', 'No']:
            raise ValueError('InternetService must be DSL, Fiber optic, or No')
        return v

    class Config:
        schema_extra = {
            "example": {
                "gender": "Female",
                "SeniorCitizen": 1,
                "Partner": "No",
                "Dependents": "No",
                "tenure": 2,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "No",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "Yes",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 85.25,
                "TotalCharges": 170.50
            }
        }


class ChurnPrediction(BaseModel):
    """Response schema for churn prediction"""
    
    customer_id: Optional[str] = Field(None, description="Customer identifier if provided")
    churn_probability: float = Field(..., description="Probability of churn (0-1)")
    churn_prediction: str = Field(..., description="Churn prediction: Will Churn or Will Stay")
    confidence_level: str = Field(..., description="Confidence level: High, Medium, Low")
    risk_category: str = Field(..., description="Risk category: High Risk, Medium Risk, Low Risk")
    recommended_action: str = Field(..., description="Recommended business action")
    model_info: Dict = Field(..., description="Model performance information")