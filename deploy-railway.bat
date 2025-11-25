@echo off
REM ============================================================================
REM Vehicle Repair Database - Railway Deployment Script for Windows
REM ============================================================================
REM This script automates deployment to Railway.app
REM
REM Prerequisites:
REM   - Railway CLI installed (npm install -g @railway/cli)
REM   - Railway account created
REM   - Git repository initialized
REM ============================================================================

echo.
echo ========================================================================
echo Vehicle Repair Database - Railway Deployment
echo ========================================================================
echo.

color 0B

echo [Step 1/8] Checking prerequisites...
echo.

REM Check Railway CLI
railway --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Railway CLI is not installed
    echo.
    echo Install it with: npm install -g @railway/cli
    echo.
    pause
    exit /b 1
)
echo ✓ Railway CLI found

REM Check Git
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Git is not installed
    pause
    exit /b 1
)
echo ✓ Git found

echo.
echo ========================================================================
echo [Step 2/8] Railway Login
echo ========================================================================
echo.

echo Opening browser for Railway authentication...
railway login

if %errorLevel% neq 0 (
    echo ERROR: Railway login failed
    pause
    exit /b 1
)

echo ✓ Successfully logged in to Railway

echo.
echo ========================================================================
echo [Step 3/8] Creating Railway Project
echo ========================================================================
echo.

set /p PROJECT_NAME="Enter project name (default: vehicle-repair-db): "
if "%PROJECT_NAME%"=="" set PROJECT_NAME=vehicle-repair-db

echo Creating Railway project '%PROJECT_NAME%'...
railway init --name %PROJECT_NAME%

if %errorLevel% neq 0 (
    echo WARNING: Project may already exist. Continuing...
)

echo ✓ Railway project initialized

echo.
echo ========================================================================
echo [Step 4/8] Adding Database Services
echo ========================================================================
echo.

echo Adding PostgreSQL database...
railway add --plugin postgresql

echo.
echo Adding Redis cache...
railway add --plugin redis

echo.
echo ✓ Database services added

echo.
echo ========================================================================
echo [Step 5/8] Configuring Environment Variables
echo ========================================================================
echo.

echo Setting environment variables...

REM Generate secret key
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i

echo Setting SECRET_KEY...
railway variables --set SECRET_KEY=%SECRET_KEY%

echo Setting PYTHON_VERSION...
railway variables --set PYTHON_VERSION=3.11.0

echo Setting API_V1_STR...
railway variables --set API_V1_STR=/api/v1

echo Setting LOG_LEVEL...
railway variables --set LOG_LEVEL=INFO

echo.
echo ✓ Environment variables configured

echo.
echo ========================================================================
echo [Step 6/8] Creating railway.json Configuration
echo ========================================================================
echo.

REM Create railway.json for backend
echo { > railway.json
echo   "$schema": "https://railway.app/railway.schema.json", >> railway.json
echo   "build": { >> railway.json
echo     "builder": "DOCKERFILE", >> railway.json
echo     "dockerfilePath": "backend/Dockerfile" >> railway.json
echo   }, >> railway.json
echo   "deploy": { >> railway.json
echo     "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT", >> railway.json
echo     "healthcheckPath": "/health", >> railway.json
echo     "healthcheckTimeout": 100, >> railway.json
echo     "restartPolicyType": "ON_FAILURE", >> railway.json
echo     "restartPolicyMaxRetries": 10 >> railway.json
echo   } >> railway.json
echo } >> railway.json

echo ✓ railway.json created

echo.
echo ========================================================================
echo [Step 7/8] Deploying Backend to Railway
echo ========================================================================
echo.

echo Committing latest changes...
git add -A
git commit -m "Prepare for Railway deployment" 2>nul

echo.
echo Deploying to Railway (this may take 3-5 minutes)...
echo.
railway up

if %errorLevel% neq 0 (
    echo ERROR: Deployment failed
    echo.
    echo Check Railway dashboard for error details:
    echo https://railway.app/dashboard
    pause
    exit /b 1
)

echo.
echo ✓ Backend deployed successfully!

echo.
echo ========================================================================
echo [Step 8/8] Getting Deployment Information
echo ========================================================================
echo.

echo Generating public domain...
railway domain

echo.
echo Getting deployment URL...
for /f "delims=" %%i in ('railway status --json ^| findstr "url"') do (
    echo Backend URL: %%i
)

echo.
echo ========================================================================
echo Deployment Complete!
echo ========================================================================
echo.
echo Your Vehicle Repair Database backend is now live on Railway!
echo.
echo Next Steps:
echo.
echo 1. Check deployment status:
echo    railway status
echo.
echo 2. View logs:
echo    railway logs
echo.
echo 3. Access Railway dashboard:
echo    https://railway.app/dashboard
echo.
echo 4. Run database migrations:
echo    railway run alembic upgrade head
echo.
echo 5. Deploy frontend separately:
echo    - Create new Railway service
echo    - Link to frontend directory
echo    - Set VITE_API_URL to backend URL
echo.
echo 6. Populate database:
echo    railway run python scripts/populate_db.py
echo.
echo Environment Variables Set:
echo   - SECRET_KEY: [Generated]
echo   - DATABASE_URL: [Auto-configured from Postgres plugin]
echo   - REDIS_URL: [Auto-configured from Redis plugin]
echo   - PYTHON_VERSION: 3.11.0
echo.
echo Useful Commands:
echo   railway logs              - View application logs
echo   railway status            - Check deployment status
echo   railway variables         - List environment variables
echo   railway run [command]     - Run command in Railway environment
echo   railway link              - Link to different project
echo.
echo Estimated Monthly Cost:
echo   Free Tier: $5 credit/month (good for testing)
echo   Hobby: $5/month per service
echo   Recommended: ~$15-20/month for production
echo.
echo ========================================================================
echo.

echo Opening Railway dashboard...
start https://railway.app/dashboard

pause
