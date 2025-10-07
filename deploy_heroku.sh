#!/bin/bash

# Heroku Deployment Script for Telco Customer Churn Prediction App
# 
# This script automates the deployment process to Heroku using container deployment
# Prerequisites: Heroku CLI installed and logged in

set -e  # Exit on any error

echo "🚀 Starting Heroku deployment for Telco Customer Churn Prediction App..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    print_error "Heroku CLI is not installed. Please install it first:"
    echo "https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
HEROKU_USER=$(heroku auth:whoami 2>/dev/null || echo "")
if [ -z "$HEROKU_USER" ]; then
    print_error "You are not logged in to Heroku. Please run: heroku login"
    exit 1
fi

print_success "Heroku CLI is installed and you are logged in as: $HEROKU_USER"

# Get app name from user or use default
read -p "Enter your Heroku app name (or press Enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    print_status "Using auto-generated app name..."
    CREATE_CMD="heroku create"
else
    print_status "Using app name: $APP_NAME"
    CREATE_CMD="heroku create $APP_NAME"
fi

# Create Heroku app
print_status "Creating Heroku app..."
if $CREATE_CMD; then
    print_success "Heroku app created successfully"
    
    # Get the actual app name if auto-generated
    if [ -z "$APP_NAME" ]; then
        APP_NAME=$(heroku apps:info --json | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
        print_status "App name: $APP_NAME"
    fi
else
    print_warning "App might already exist or there was an error. Continuing..."
    if [ -z "$APP_NAME" ]; then
        print_error "Could not determine app name. Please provide one manually."
        exit 1
    fi
fi

# Set stack to container
print_status "Setting stack to container..."
heroku stack:set container -a $APP_NAME

# Set environment variables
print_status "Setting environment variables..."
heroku config:set PYTHONPATH="/app" -a $APP_NAME
heroku config:set STREAMLIT_SERVER_HEADLESS="true" -a $APP_NAME
heroku config:set STREAMLIT_BROWSER_GATHER_USAGE_STATS="false" -a $APP_NAME

# Add Heroku remote if it doesn't exist
if ! git remote get-url heroku &> /dev/null; then
    print_status "Adding Heroku remote..."
    heroku git:remote -a $APP_NAME
else
    print_status "Heroku remote already exists"
fi

# Deploy to Heroku
print_status "Deploying to Heroku... This may take several minutes..."
git add .
git commit -m "Deploy to Heroku: $(date)" || print_warning "No changes to commit"

if git push heroku main; then
    print_success "Deployment successful!"
else
    print_error "Deployment failed. Check the logs above for details."
    print_status "You can view detailed logs with: heroku logs --tail -a $APP_NAME"
    exit 1
fi

# Open the app
print_status "Opening the deployed app..."
heroku open -a $APP_NAME

print_success "🎉 Deployment completed successfully!"
print_status "Your app is available at: https://$APP_NAME.herokuapp.com"
print_status "To view logs: heroku logs --tail -a $APP_NAME"
print_status "To scale the app: heroku ps:scale web=1 -a $APP_NAME"

echo ""
echo "📋 Next steps:"
echo "1. Test your application in the browser"
echo "2. Monitor logs with: heroku logs --tail -a $APP_NAME"
echo "3. Scale dynos if needed: heroku ps:scale web=1 -a $APP_NAME"
echo "4. View app info: heroku apps:info -a $APP_NAME"