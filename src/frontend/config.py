"""
Configuration utilities for detecting environment and setting appropriate API URLs
"""

import os
import requests
from typing import Optional


def detect_environment() -> str:
    """
    Detect the current environment (local, docker, or cloud_run)
    
    Returns:
        str: 'local', 'docker', or 'cloud_run'
    """
    # Check for Cloud Run environment
    if os.getenv('K_SERVICE') or os.getenv('GOOGLE_CLOUD_PROJECT'):
        return 'cloud_run'
    
    # Check for Docker environment
    if os.path.exists('/.dockerenv') or os.getenv('DOCKER_ENV'):
        return 'docker'
    
    # Default to local
    return 'local'


def get_api_base_url() -> str:
    """
    Get the appropriate API base URL based on the current environment
    
    Returns:
        str: The API base URL to use
    """
    # Environment variable override (highest priority)
    env_url = os.getenv("API_BASE_URL")
    if env_url and env_url.strip():
        # Clean up any potential encoding issues
        cleaned_url = env_url.strip()
        # Fix various corruptions
        cleaned_url = cleaned_url.replace("https;", "https://")
        cleaned_url = cleaned_url.replace("http;", "http://")
        cleaned_url = cleaned_url.replace("https:\\", "https://")
        cleaned_url = cleaned_url.replace("http:\\", "http://")
        cleaned_url = cleaned_url.replace("https:/\\", "https://")
        cleaned_url = cleaned_url.replace("http:/\\", "http://")
        return cleaned_url
    
    env = detect_environment()
    
    # Cloud Run environment - use the actual backend service URL
    if env == 'cloud_run':
        # Use the actual Cloud Run backend URL as default - hardcoded to avoid corruption
        return "https://churn-prediction-backend-973304379787.us-central1.run.app"
    
    # Docker Compose environment
    if env == 'docker':
        return "http://backend:8081"
    
    # Local development
    return "http://localhost:8081"


def generate_hash(project_id: str) -> str:
    """Generate a simple hash for Cloud Run URL pattern"""
    import hashlib
    return hashlib.md5(project_id.encode()).hexdigest()[:8]


def test_api_connectivity(api_url: str) -> bool:
    """
    Test if the API is accessible at the given URL
    
    Args:
        api_url: The base URL to test
        
    Returns:
        bool: True if API is accessible, False otherwise
    """
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def get_working_api_url() -> Optional[str]:
    """
    Get a working API URL by testing multiple possibilities
    
    Returns:
        str or None: A working API URL or None if none found
    """
    # Get the primary URL based on environment detection
    primary_url = get_api_base_url()
    
    # Test the primary URL first
    if test_api_connectivity(primary_url):
        return primary_url
    
    # If primary URL doesn't work, try fallbacks based on environment
    env = detect_environment()
    
    fallback_urls = []
    
    if env == 'cloud_run':
        # Try environment variable if set
        if os.getenv('BACKEND_SERVICE_URL'):
            fallback_urls.append(os.getenv('BACKEND_SERVICE_URL'))
        
        # Try common Cloud Run patterns
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        if project_id:
            fallback_urls.extend([
                "https://churn-prediction-backend-973304379787.us-central1.run.app"
            ])
    
    elif env == 'docker':
        fallback_urls = [
            "http://backend:8081",
            "http://churn-prediction-backend:8081",
            "http://localhost:8081"
        ]
    
    else:  # local
        fallback_urls = [
            "http://localhost:8081",
            "http://127.0.0.1:8081",
            "http://backend:8081"
        ]
    
    # Test fallback URLs
    for url in fallback_urls:
        if test_api_connectivity(url):
            return url
    
    return None


def get_config() -> dict:
    """
    Get complete configuration for the current environment
    
    Returns:
        dict: Configuration dictionary with API settings
    """
    env = detect_environment()
    api_url = get_api_base_url()  # Use direct URL instead of testing multiple URLs
    
    return {
        'environment': env,
        'api_base_url': api_url,
        'api_working': None,  # Will be tested when needed
        'debug_info': {
            'detected_env': env,
            'k_service': os.getenv('K_SERVICE'),
            'google_cloud_project': os.getenv('GOOGLE_CLOUD_PROJECT'),
            'docker_env': os.path.exists('/.dockerenv'),
            'env_api_url': os.getenv('API_BASE_URL'),
            'resolved_api_url': api_url,
        }
    }