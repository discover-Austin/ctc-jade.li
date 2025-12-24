@echo off
REM ============================================================================
REM Complete Setup and Population Script for Vehicle Repair Database
REM ============================================================================
REM This script will:
REM 1. Check prerequisites
REM 2. Set up virtual environment
REM 3. Install dependencies
REM 4. Create .env file
REM 5. Run database migrations
REM 6. Create admin user
REM 7. Populate database with sample data
REM 8. Start the server
REM ============================================================================

echo.
echo ============================================================================
echo   VEHICLE REPAIR DATABASE - COMPLETE SETUP AND DEPLOYMENT
echo ============================================================================
echo.

REM Check if Python is installed
echo [1/10] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM Check if PostgreSQL is installed
echo [2/10] Checking PostgreSQL installation...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL not found in PATH
    echo Make sure PostgreSQL is installed and running
    echo Download from: https://www.postgresql.org/download/windows/
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)
echo.

REM Navigate to backend directory
echo [3/10] Navigating to backend directory...
cd /d "%~dp0backend"
if %errorlevel% neq 0 (
    echo ERROR: Backend directory not found
    pause
    exit /b 1
)
echo Current directory: %CD%
echo.

REM Create virtual environment
echo [4/10] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Recreating...
    rmdir /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

REM Activate virtual environment
echo [5/10] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Upgrade pip
echo [6/10] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

REM Install dependencies
echo [7/10] Installing dependencies (this may take 2-3 minutes)...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Trying without --quiet flag to see errors...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
echo [8/10] Setting up environment configuration...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env >nul

    REM Generate SECRET_KEY
    echo Generating secure SECRET_KEY...
    for /f %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i

    REM Update .env file
    powershell -Command "(gc .env) -replace 'SECRET_KEY=your-secret-key-change-this-in-production', 'SECRET_KEY=%SECRET_KEY%' | Out-File -encoding ASCII .env"
    powershell -Command "(gc .env) -replace 'RATE_LIMIT_ENABLED=true', 'RATE_LIMIT_ENABLED=false' | Out-File -encoding ASCII .env"

    echo.
    echo =================================================================
    echo IMPORTANT: Please update the DATABASE_URL in .env file
    echo.
    echo Current DATABASE_URL:
    type .env | findstr DATABASE_URL
    echo.
    echo If your PostgreSQL password is different, press Ctrl+C now
    echo and edit backend\.env file with the correct password.
    echo.
    echo Default PostgreSQL credentials:
    echo   Username: postgres
    echo   Password: password (or the one you set during installation)
    echo   Database: vehicle_db
    echo =================================================================
    echo.
    timeout /t 5
) else (
    echo .env file already exists, using existing configuration
)
echo.

REM Check if database exists, if not provide instructions
echo [9/10] Checking database setup...
echo.
echo =================================================================
echo DATABASE SETUP REQUIRED
echo =================================================================
echo.
echo Please make sure you have created the database:
echo.
echo Option 1 - Using pgAdmin:
echo   1. Open pgAdmin 4
echo   2. Right-click "Databases" -^> Create -^> Database
echo   3. Name: vehicle_db
echo   4. Click Save
echo.
echo Option 2 - Using psql command line:
echo   psql -U postgres
echo   CREATE DATABASE vehicle_db;
echo   \q
echo.
set /p DB_READY="Have you created the 'vehicle_db' database? (y/n): "
if /i not "%DB_READY%"=="y" (
    echo.
    echo Please create the database first, then run this script again.
    pause
    exit /b 1
)
echo.

REM Run database migrations
echo [10/10] Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Database migration failed
    echo.
    echo Common issues:
    echo 1. PostgreSQL is not running
    echo 2. Database 'vehicle_db' does not exist
    echo 3. Wrong password in DATABASE_URL in .env file
    echo.
    echo Please fix the issue and run this script again.
    pause
    exit /b 1
)
echo Database migrations completed successfully
echo.

REM Create admin user
echo Creating admin user...
python scripts\create_admin.py
if %errorlevel% neq 0 (
    echo WARNING: Admin user creation failed (may already exist)
)
echo.

REM Populate database with sample data
echo Populating database with comprehensive sample data...
python scripts\populate_database.py
if %errorlevel% neq 0 (
    echo WARNING: Database population failed or partially completed
)
echo.

REM Show completion message
echo.
echo ============================================================================
echo   SETUP COMPLETE!
echo ============================================================================
echo.
echo The database has been set up and populated with sample data including:
echo   - Admin user account
echo   - 50+ vehicle models (2014-2024)
echo   - 200+ repair procedures
echo   - 500+ diagnostic trouble codes
echo   - Technical service bulletins
echo   - Maintenance schedules
echo.
echo Starting the API server...
echo.
echo API will be available at:
echo   - API Base URL:        http://localhost:8000
echo   - API Documentation:   http://localhost:8000/docs
echo   - Alternative Docs:    http://localhost:8000/redoc
echo   - Health Check:        http://localhost:8000/health
echo.
echo Admin Login Credentials:
echo   Username: admin
echo   Password: Admin123!
echo   (Please change this password after first login)
echo.
echo ============================================================================
echo.

REM Start the server
echo Starting Uvicorn server...
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
