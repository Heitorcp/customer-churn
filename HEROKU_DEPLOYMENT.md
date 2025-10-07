# Heroku Deployment Guide for Telco Customer Churn Prediction App

This guide explains how to deploy your containerized churn prediction application to Heroku using a single web dyno.

## 📋 Prerequisites

1. **Heroku CLI**: Install from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. **Git**: Ensure your project is in a Git repository
3. **Heroku Account**: Sign up at [https://heroku.com](https://heroku.com)

## 🚀 Quick Deployment

### Option 1: Using the Deployment Script (Recommended)

```bash
# Make the script executable
chmod +x deploy_heroku.sh

# Run the deployment script
./deploy_heroku.sh
```

The script will:
- Check prerequisites
- Create a Heroku app
- Set up container deployment
- Configure environment variables
- Deploy your application
- Open the deployed app

### Option 2: Manual Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   # OR for auto-generated name:
   heroku create
   ```

3. **Set the stack to container**
   ```bash
   heroku stack:set container -a your-app-name
   ```

4. **Set environment variables**
   ```bash
   heroku config:set PYTHONPATH="/app" -a your-app-name
   heroku config:set STREAMLIT_SERVER_HEADLESS="true" -a your-app-name
   heroku config:set STREAMLIT_BROWSER_GATHER_USAGE_STATS="false" -a your-app-name
   ```

5. **Add Heroku remote**
   ```bash
   heroku git:remote -a your-app-name
   ```

6. **Deploy the application**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Open your app**
   ```bash
   heroku open -a your-app-name
   ```

## 📁 Deployment Files

The following files are configured for Heroku deployment:

- **`heroku.yml`**: Defines the build and run processes for container deployment
- **`Procfile`**: Specifies the command to run the web dyno
- **`Dockerfile`**: Unified container with both frontend and ML model
- **`app.json`**: App metadata and configuration for Heroku

## 🔧 Configuration Details

### Container Configuration
- **Base Image**: `python:3.12.4-slim`
- **Package Manager**: UV for fast dependency installation
- **Port**: Dynamic port assignment via `$PORT` environment variable
- **Process Type**: Web dyno running Streamlit

### Environment Variables
- `PYTHONPATH`: Set to `/app` for proper module imports
- `STREAMLIT_SERVER_HEADLESS`: Enabled for server deployment
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: Disabled for privacy

### Single Dyno Architecture
Since we're using the lightest Heroku dyno, the application runs as a single container that includes:
- Streamlit frontend
- ML prediction service (integrated directly)
- Authentication system
- Model artifacts

## 📊 Application Features (Post-Deployment)

Your deployed app will include:
- **🎯 Churn Prediction**: Upload Excel files for batch predictions
- **📊 EDA Analysis**: Interactive data exploration
- **🤖 Model Details**: Performance metrics and technical details
- **⚙️ Admin Panel**: User management (admin access)
- **🔐 Authentication**: Secure login system

### Default Login Credentials
- **Username**: `demo`
- **Password**: `demo123`

## 🔍 Monitoring and Management

### View Logs
```bash
heroku logs --tail -a your-app-name
```

### Scale Dynos
```bash
# Scale to 1 web dyno (recommended for basic plan)
heroku ps:scale web=1 -a your-app-name

# Scale down (stop the app)
heroku ps:scale web=0 -a your-app-name
```

### View App Information
```bash
heroku apps:info -a your-app-name
```

### Access Heroku Dashboard
Visit [https://dashboard.heroku.com](https://dashboard.heroku.com) to manage your app through the web interface.

## 💰 Pricing Information

- **Basic Dyno**: $7/month (recommended)
  - 512 MB RAM
  - Sleeps after 30 minutes of inactivity
  - No sleeping with Basic dyno plan

- **Eco Dyno**: $5/month
  - 512 MB RAM
  - Sleeps after 30 minutes of inactivity
  - 1000 hours included across all Eco dynos

## 🔧 Troubleshooting

### Common Issues

1. **Build Timeout**
   - The initial build may take 10-15 minutes due to ML dependencies
   - This is normal for the first deployment

2. **Memory Issues**
   - Use Basic dyno ($7/month) instead of free tier
   - The ML model requires adequate memory

3. **Port Binding Issues**
   - Heroku automatically assigns the PORT environment variable
   - The app is configured to use `$PORT` automatically

4. **Model Loading Errors**
   - Ensure all files in `models/` directory are committed to Git
   - Check that model files are not in `.gitignore`

### Debug Commands
```bash
# Check dyno status
heroku ps -a your-app-name

# Restart the app
heroku restart -a your-app-name

# Run bash in dyno (for debugging)
heroku run bash -a your-app-name

# Check config variables
heroku config -a your-app-name
```

## 🌐 URL Structure

After deployment, your app will be available at:
- **Main App**: `https://your-app-name.herokuapp.com`
- **Login Page**: Redirected automatically if not authenticated
- **Health Check**: App includes internal health monitoring

## 📋 Post-Deployment Checklist

- [ ] App builds successfully
- [ ] Authentication system works
- [ ] Model predictions work correctly
- [ ] Excel upload/download functions properly
- [ ] All pages are accessible
- [ ] Performance is acceptable on Basic dyno

## 🔄 Updates and Redeployment

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Update: describe your changes"
git push heroku main
```

Heroku will automatically rebuild and redeploy your container.

---

🎉 **Congratulations!** Your ML application is now deployed on Heroku and accessible worldwide!