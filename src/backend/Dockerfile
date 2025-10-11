# Backend Dockerfile for FastAPI Churn Prediction API
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8081

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
COPY pyproject.toml ./

# Install Python dependencies
RUN uv pip install --system --no-cache -e .

# Copy application code
COPY src/backend/ ./src/backend/
COPY models/ ./models/

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD ["sh", "-c", "python -m uvicorn src.backend.api.main:app --host 0.0.0.0 --port ${PORT:-8081}"]