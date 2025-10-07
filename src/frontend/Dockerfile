# Frontend Dockerfile for Streamlit Churn Prediction Interface
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV (fast Python package installer)
RUN pip install uv

# Copy project files from root
COPY ../../pyproject.toml ./
COPY ../../uv.lock ./

# Install Python dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY . ./src/frontend/
COPY ../../outputs/ ./outputs/

# Create directories and set permissions
RUN mkdir -p /app/src/frontend/config \
    && chmod 755 /app/src/frontend/config

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Create Streamlit config directory
RUN mkdir -p /home/appuser/.streamlit

# Create Streamlit configuration
RUN echo '[server]' > /home/appuser/.streamlit/config.toml \
    && echo 'headless = true' >> /home/appuser/.streamlit/config.toml \
    && echo 'port = 8501' >> /home/appuser/.streamlit/config.toml \
    && echo 'address = "0.0.0.0"' >> /home/appuser/.streamlit/config.toml \
    && echo 'enableCORS = false' >> /home/appuser/.streamlit/config.toml \
    && echo 'enableXsrfProtection = false' >> /home/appuser/.streamlit/config.toml

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "src/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]