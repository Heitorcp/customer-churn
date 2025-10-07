@echo off
REM Heroku Deployment Script for Windows
REM Telco Customer Churn Prediction App

echo 🚀 Starting Heroku deployment for Telco Customer Churn Prediction App...

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ [ERROR] Heroku CLI is not installed. Please install it first:
    echo https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo ✅ [SUCCESS] Heroku CLI is installed

REM Get current user
for /f "tokens=*" %%i in ('heroku auth:whoami 2^>nul') do set HEROKU_USER=%%i
if "%HEROKU_USER%"=="" (
    echo ❌ [ERROR] You are not logged in to Heroku. Please run: heroku login
    pause
    exit /b 1
)

echo ✅ [SUCCESS] Logged in as: %HEROKU_USER%

REM Get app name from user or use default
set /p APP_NAME="Enter your Heroku app name (or press Enter for auto-generated): "

if "%APP_NAME%"=="" (
    echo 📋 [INFO] Using auto-generated app name...
    heroku create
    REM Get the app name from the output - this is tricky in batch, so we'll continue manually
) else (
    echo 📋 [INFO] Using app name: %APP_NAME%
    heroku create %APP_NAME%
    if errorlevel 1 (
        echo ⚠️ [WARNING] App might already exist. Continuing...
    )
)

if "%APP_NAME%"=="" (
    echo 📋 [INFO] Please note the app name from the output above for the next steps
    set /p APP_NAME="Enter the app name that was created: "
)

echo 📋 [INFO] Setting stack to container...
heroku stack:set container -a %APP_NAME%

echo 📋 [INFO] Setting environment variables...
heroku config:set PYTHONPATH="/app" -a %APP_NAME%
heroku config:set STREAMLIT_SERVER_HEADLESS="true" -a %APP_NAME%
heroku config:set STREAMLIT_BROWSER_GATHER_USAGE_STATS="false" -a %APP_NAME%

echo 📋 [INFO] Adding Heroku remote...
heroku git:remote -a %APP_NAME%

echo 📋 [INFO] Deploying to Heroku... This may take several minutes...
git add .
git commit -m "Deploy to Heroku: %date% %time%"
git push heroku main

if errorlevel 1 (
    echo ❌ [ERROR] Deployment failed. Check the logs above for details.
    echo You can view detailed logs with: heroku logs --tail -a %APP_NAME%
    pause
    exit /b 1
)

echo ✅ [SUCCESS] Deployment completed successfully!
echo 📋 [INFO] Opening the deployed app...
heroku open -a %APP_NAME%

echo.
echo 🎉 Deployment completed successfully!
echo Your app is available at: https://%APP_NAME%.herokuapp.com
echo To view logs: heroku logs --tail -a %APP_NAME%
echo To scale the app: heroku ps:scale web=1 -a %APP_NAME%

echo.
echo 📋 Next steps:
echo 1. Test your application in the browser
echo 2. Monitor logs with: heroku logs --tail -a %APP_NAME%
echo 3. Scale dynos if needed: heroku ps:scale web=1 -a %APP_NAME%
echo 4. View app info: heroku apps:info -a %APP_NAME%

pause