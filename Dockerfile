# Unified Dockerfile for Heroku deployment
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Install UV (fast Python package installer)
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY src/ ./src/
COPY models/ ./models/
COPY outputs/ ./outputs/
COPY init_heroku.py ./

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
    && echo 'enableCORS = false' >> /home/appuser/.streamlit/config.toml \
    && echo 'enableXsrfProtection = false' >> /home/appuser/.streamlit/config.toml

# Default command (will be overridden by Procfile)
CMD ["streamlit", "run", "src/frontend/app.py", "--server.headless=true"]