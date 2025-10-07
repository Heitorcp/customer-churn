"""
Schemas package for the Telco Customer Churn Prediction API

This package contains all Pydantic models used for request/response validation.
"""

from .models import CustomerData, ChurnPrediction

__all__ = ['CustomerData', 'ChurnPrediction']