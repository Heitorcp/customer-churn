# Docker Deployment Guide

This guide explains how to deploy the Telco Customer Churn Prediction system using Docker containers.

## 🐳 Docker Architecture

The application consists of two services:
- **Backend**: FastAPI service (port 8081)
- **Frontend**: Streamlit interface (port 8501)

## 📋 Prerequisites

- Docker Desktop or Docker Engine installed
- Docker Compose installed
- At least 2GB RAM available
- Ports 8081 and 8501 available

## 🚀 Quick Start

### 1. Build and Start Services
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 2. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8081/docs

### 3. Login Credentials
- **Username**: `demo` **Password**: `demo123`
- **Username**: `admin` **Password**: `churn123`
- **Username**: `user` **Password**: `user123`

## 🛠️ Docker Commands

### Build Services
```bash
# Build backend only
docker-compose build backend

# Build frontend only
docker-compose build frontend

# Build both services
docker-compose build
```

### Service Management
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Container Management
```bash
# List running containers
docker-compose ps

# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend bash

# Remove all containers and networks
docker-compose down --volumes --remove-orphans
```

## 📁 Volume Mounts

The compose file includes strategic volume mounts:

- **Models**: `./models:/app/models:ro` (read-only)
- **Outputs**: `./outputs:/app/outputs:ro` (read-only)  
- **Config**: `./src/frontend/config:/app/src/frontend/config` (read-write for user management)

## 🔧 Configuration

### Environment Variables
```bash
# Backend
PORT=8081
PYTHONPATH=/app

# Frontend
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
API_BASE_URL=http://backend:8081
```

### Network Configuration
- Services communicate via `churn-network` bridge network
- Frontend connects to backend using service name `backend`
- External access via exposed ports

## 🏥 Health Checks

Both services include health checks:
- **Backend**: `GET /health` endpoint
- **Frontend**: Streamlit health endpoint
- Automatic restart on failure

## 🔒 Security Features

- **Non-root users**: Services run as `appuser` (UID 1000)
- **Read-only mounts**: Models and outputs mounted read-only
- **Network isolation**: Services communicate via private network
- **Authentication**: Login required for frontend access

## 📊 Monitoring

### View Service Status
```bash
# Check health status
docker-compose ps

# View resource usage
docker stats

# Follow logs in real-time
docker-compose logs -f --tail=100
```

### Debugging
```bash
# Access backend container
docker-compose exec backend bash

# Access frontend container
docker-compose exec frontend bash

# Check backend API health
curl http://localhost:8081/health

# Check frontend health
curl http://localhost:8501/_stcore/health
```

## 🚀 Production Deployment

### Optimizations for Production
1. **Multi-stage builds**: Reduce image size
2. **Secrets management**: Use Docker secrets
3. **SSL/TLS**: Add reverse proxy (nginx)
4. **Resource limits**: Set memory/CPU limits
5. **Logging**: Configure log aggregation

### Sample Production Compose
```yaml
version: '3.8'
services:
  backend:
    # ... existing config
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
    restart: unless-stopped
    
  frontend:
    # ... existing config
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.3'
    restart: unless-stopped
```

## 🔧 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the port
lsof -i :8081
lsof -i :8501

# Stop conflicting services
docker-compose down
```

**2. Permission Denied**
```bash
# Fix file permissions
chmod -R 755 ./src/frontend/config
```

**3. Service Won't Start**
```bash
# View detailed logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild without cache
docker-compose build --no-cache
```

**4. API Connection Issues**
- Ensure backend service is healthy
- Check network connectivity between services
- Verify API_BASE_URL environment variable

## 📈 Scaling

### Horizontal Scaling
```yaml
# Scale frontend replicas
docker-compose up --scale frontend=3

# Use load balancer for multiple instances
```

### Resource Monitoring
```bash
# Monitor resource usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Backup Configuration
```bash
# Backup user configuration
cp src/frontend/config/users.json backup/
```

## 🎯 Next Steps

1. **Set up monitoring** with Prometheus/Grafana
2. **Add SSL certificates** for HTTPS
3. **Configure log aggregation** with ELK stack
4. **Set up CI/CD pipeline** for automated deployment
5. **Add database** for user management and audit logs