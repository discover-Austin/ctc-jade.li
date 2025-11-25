@echo off
REM ============================================================================
REM Vehicle Repair Database - Comprehensive Local Setup Script for Windows
REM ============================================================================
REM This script sets up the complete development environment on Windows
REM
REM Prerequisites:
REM   - Python 3.11+ installed and in PATH
REM   - Node.js 18+ installed and in PATH
REM   - PostgreSQL 15+ installed and running
REM   - Git installed
REM ============================================================================

echo.
echo ========================================================================
echo Vehicle Repair Database - Windows Setup
echo ========================================================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo WARNING: Not running as Administrator. Some operations may fail.
    echo Right-click and select "Run as Administrator" for best results.
    echo.
    pause
)

REM Set color for better visibility
color 0A

echo [1/10] Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found:
python --version

REM Check Node.js
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo ✓ Node.js found:
node --version

REM Check PostgreSQL
psql --version >nul 2>&1
if %errorLevel% neq 0 (
    echo WARNING: PostgreSQL command-line tools not found in PATH
    echo Continuing anyway, but you'll need to set up the database manually.
    echo.
) else (
    echo ✓ PostgreSQL found:
    psql --version
)

echo.
echo ========================================================================
echo [2/10] Setting up environment variables
echo ========================================================================
echo.

REM Create .env file from example
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created
    echo.
    echo IMPORTANT: Edit .env file with your database credentials!
    echo Default database: postgresql://postgres:password@localhost:5432/vehicle_db
    echo.
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================================================
echo [3/10] Creating PostgreSQL database
echo ========================================================================
echo.

set /p DB_CREATE="Do you want to create the database now? (y/n): "
if /i "%DB_CREATE%"=="y" (
    echo.
    set /p DB_PASSWORD="Enter PostgreSQL password for user 'postgres': "

    REM Create database
    echo Creating database 'vehicle_db'...
    set PGPASSWORD=%DB_PASSWORD%
    psql -U postgres -h localhost -c "CREATE DATABASE vehicle_db;" 2>nul
    if %errorLevel% equ 0 (
        echo ✓ Database created successfully
    ) else (
        echo Note: Database may already exist or there was an error
    )

    REM Create user (optional)
    echo Creating database user...
    psql -U postgres -h localhost -c "CREATE USER vehicle_user WITH PASSWORD 'vehicle_pass';" 2>nul
    psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE vehicle_db TO vehicle_user;" 2>nul

    set PGPASSWORD=
    echo ✓ Database setup complete
) else (
    echo Skipping database creation. Make sure database exists before running the app.
)

echo.
echo ========================================================================
echo [4/10] Setting up Python virtual environment
echo ========================================================================
echo.

cd backend

REM Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated

echo.
echo ========================================================================
echo [5/10] Installing Python dependencies
echo ========================================================================
echo.

echo Installing backend dependencies (this may take a few minutes)...
pip install --upgrade pip
pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✓ Backend dependencies installed

echo.
echo ========================================================================
echo [6/10] Setting up database schema
echo ========================================================================
echo.

set /p RUN_MIGRATIONS="Do you want to run database migrations? (y/n): "
if /i "%RUN_MIGRATIONS%"=="y" (
    echo.
    echo Running database migrations...

    REM Initialize Alembic if not already done
    if not exist alembic (
        echo Initializing Alembic...
        alembic init alembic
    )

    REM Run migrations
    alembic upgrade head

    if %errorLevel% equ 0 (
        echo ✓ Database migrations completed
    ) else (
        echo WARNING: Migration may have failed. Check the error messages above.
    )
) else (
    echo Skipping migrations
)

echo.
echo ========================================================================
echo [7/10] Populating database with sample data
echo ========================================================================
echo.

set /p POPULATE_DB="Do you want to populate the database with sample data? (y/n): "
if /i "%POPULATE_DB%"=="y" (
    echo.
    echo Fetching data from NHTSA and EPA APIs...
    echo This may take 5-10 minutes depending on your internet connection...
    echo.

    REM Create data population script
    echo import asyncio > populate_db.py
    echo from app.db.base import SessionLocal >> populate_db.py
    echo from app.services.data_scraper import AutomotiveDataScraper >> populate_db.py
    echo. >> populate_db.py
    echo async def main(): >> populate_db.py
    echo     db = SessionLocal() >> populate_db.py
    echo     scraper = AutomotiveDataScraper(db) >> populate_db.py
    echo     await scraper.scrape_nhtsa_database(year_start=2020) >> populate_db.py
    echo     db.close() >> populate_db.py
    echo. >> populate_db.py
    echo if __name__ == "__main__": >> populate_db.py
    echo     asyncio.run(main()) >> populate_db.py

    python populate_db.py

    if %errorLevel% equ 0 (
        echo ✓ Sample data imported successfully
    ) else (
        echo WARNING: Data import may have failed. Check error messages above.
    )

    del populate_db.py
) else (
    echo Skipping data population
)

cd..

echo.
echo ========================================================================
echo [8/10] Setting up frontend
echo ========================================================================
echo.

cd frontend

echo Installing frontend dependencies (this may take a few minutes)...
call npm install

if %errorLevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo ✓ Frontend dependencies installed

REM Create frontend .env file
echo Creating frontend .env file...
echo VITE_API_URL=http://localhost:8000/api/v1 > .env.local
echo ✓ Frontend .env created

cd..

echo.
echo ========================================================================
echo [9/10] Running tests
echo ========================================================================
echo.

set /p RUN_TESTS="Do you want to run the test suite? (y/n): "
if /i "%RUN_TESTS%"=="y" (
    echo.
    echo Running backend tests...
    cd backend
    call venv\Scripts\activate.bat
    pytest tests/ -v
    cd..
    echo.
    echo ✓ Tests completed
) else (
    echo Skipping tests
)

echo.
echo ========================================================================
echo [10/10] Creating startup scripts
echo ========================================================================
echo.

REM Create backend startup script
echo @echo off > start-backend.bat
echo echo Starting Vehicle Repair Database Backend... >> start-backend.bat
echo cd backend >> start-backend.bat
echo call venv\Scripts\activate.bat >> start-backend.bat
echo echo. >> start-backend.bat
echo echo Backend API starting at http://localhost:8000 >> start-backend.bat
echo echo API Documentation: http://localhost:8000/docs >> start-backend.bat
echo echo. >> start-backend.bat
echo uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 >> start-backend.bat
echo ✓ Created start-backend.bat

REM Create frontend startup script
echo @echo off > start-frontend.bat
echo echo Starting Vehicle Repair Database Frontend... >> start-frontend.bat
echo cd frontend >> start-frontend.bat
echo echo. >> start-frontend.bat
echo echo Frontend starting at http://localhost:3000 >> start-frontend.bat
echo echo. >> start-frontend.bat
echo npm run dev >> start-frontend.bat
echo ✓ Created start-frontend.bat

REM Create combined startup script
echo @echo off > start-all.bat
echo echo Starting Vehicle Repair Database - Full Stack >> start-all.bat
echo echo. >> start-all.bat
echo echo Starting Backend and Frontend... >> start-all.bat
echo echo. >> start-all.bat
echo echo Backend API: http://localhost:8000 >> start-all.bat
echo echo API Docs: http://localhost:8000/docs >> start-all.bat
echo echo Frontend: http://localhost:3000 >> start-all.bat
echo echo. >> start-all.bat
echo start "Vehicle DB - Backend" cmd /k start-backend.bat >> start-all.bat
echo timeout /t 3 /nobreak ^>nul >> start-all.bat
echo start "Vehicle DB - Frontend" cmd /k start-frontend.bat >> start-all.bat
echo ✓ Created start-all.bat

REM Create Docker startup script
echo @echo off > start-docker.bat
echo echo Starting Vehicle Repair Database with Docker... >> start-docker.bat
echo echo. >> start-docker.bat
echo echo This will start all services using Docker Compose >> start-docker.bat
echo echo. >> start-docker.bat
echo docker-compose up -d >> start-docker.bat
echo echo. >> start-docker.bat
echo echo ✓ Services started! >> start-docker.bat
echo echo. >> start-docker.bat
echo echo Access points: >> start-docker.bat
echo echo   Frontend:  http://localhost:3000 >> start-docker.bat
echo echo   Backend:   http://localhost:8000 >> start-docker.bat
echo echo   API Docs:  http://localhost:8000/docs >> start-docker.bat
echo echo   Grafana:   http://localhost:3001 (admin/admin) >> start-docker.bat
echo echo. >> start-docker.bat
echo echo View logs: docker-compose logs -f >> start-docker.bat
echo echo Stop all:  docker-compose down >> start-docker.bat
echo pause >> start-docker.bat
echo ✓ Created start-docker.bat

echo.
echo ========================================================================
echo Setup Complete!
echo ========================================================================
echo.
echo The Vehicle Repair Database has been set up successfully!
echo.
echo Quick Start Options:
echo.
echo   Option 1 - Local Development (Recommended for Development):
echo     1. Run: start-backend.bat   (in one terminal)
echo     2. Run: start-frontend.bat  (in another terminal)
echo     OR
echo     Run: start-all.bat (starts both in separate windows)
echo.
echo   Option 2 - Docker (Recommended for Testing):
echo     Run: start-docker.bat
echo     (Requires Docker Desktop to be installed and running)
echo.
echo Access Points:
echo   - Frontend:        http://localhost:3000
echo   - Backend API:     http://localhost:8000
echo   - API Docs:        http://localhost:8000/docs
echo   - ReDoc:           http://localhost:8000/redoc
echo.
echo Next Steps:
echo   1. Edit .env file with your actual database credentials
echo   2. Run start-all.bat to launch the application
echo   3. Visit http://localhost:3000 to start searching vehicles
echo   4. Check the API documentation at http://localhost:8000/docs
echo.
echo For production deployment, see DEPLOYMENT.md
echo.
echo ========================================================================
echo.

pause
