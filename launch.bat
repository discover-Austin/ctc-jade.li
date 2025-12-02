@echo off
REM ============================================================================
REM Vehicle Repair Database - One-Command Launcher (Windows)
REM ============================================================================
REM Just run: launch.bat
REM Everything else is automatic!
REM ============================================================================

cls
color 0B

echo.
echo ============================================================================
echo.
echo           Vehicle Repair Database - Auto Launcher v1.0
echo.
echo              Just sit back... We'll handle everything!
echo.
echo ============================================================================
echo.

REM ============================================================================
REM [1/5] Check environment
REM ============================================================================

echo [1/5] Checking environment...

REM Check if .env exists
if not exist .env (
    echo    -^> Creating .env file...
    copy .env.example .env >nul
    echo    √ Configuration created
) else (
    echo    √ Configuration exists
)

REM Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo    X Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
echo    √ Python found

REM Check Node
set NODE_AVAILABLE=false
node --version >nul 2>&1
if %errorLevel% equ 0 (
    echo    √ Node.js found
    set NODE_AVAILABLE=true
) else (
    echo    ! Node.js not found - frontend won't be available
)

REM ============================================================================
REM [2/5] Setup backend
REM ============================================================================

echo.
echo [2/5] Setting up backend...

cd backend

REM Create venv if needed
if not exist venv (
    echo    -^> Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM Install dependencies
if not exist venv\.deps_installed (
    echo    -^> Installing dependencies ^(first time only, ~2 min^)...
    pip install -q --upgrade pip >nul 2>&1
    pip install -q -r requirements.txt >nul 2>&1
    type nul > venv\.deps_installed
    echo    √ Dependencies installed
) else (
    echo    √ Dependencies already installed
)

cd ..

REM ============================================================================
REM [3/5] Setup frontend
REM ============================================================================

if "%NODE_AVAILABLE%"=="true" (
    echo.
    echo [3/5] Setting up frontend...

    cd frontend

    if not exist node_modules (
        echo    -^> Installing npm packages ^(first time only, ~2 min^)...
        call npm install --silent >nul 2>&1
        echo    √ Packages installed
    ) else (
        echo    √ Packages already installed
    )

    REM Create frontend .env
    if not exist .env.local (
        echo VITE_API_URL=http://localhost:8000/api/v1 > .env.local
    )

    cd ..
) else (
    echo.
    echo [3/5] Skipping frontend ^(Node.js not available^)
)

REM ============================================================================
REM [4/5] Clean up old processes
REM ============================================================================

echo.
echo [4/5] Cleaning up old processes...

taskkill /F /IM python.exe /FI "WINDOWTITLE eq Vehicle DB*" >nul 2>&1
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Vehicle DB*" >nul 2>&1
echo    √ Cleanup complete

timeout /t 2 /nobreak >nul

REM ============================================================================
REM [5/5] Launch services
REM ============================================================================

echo.
echo [5/5] Launching services...

REM Create logs directory
if not exist logs mkdir logs

REM Start backend
cd backend
call venv\Scripts\activate.bat
start "Vehicle DB - Backend" /MIN cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ..\logs\backend.log 2>&1"
cd ..

echo    √ Backend started

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Start frontend if available
if "%NODE_AVAILABLE%"=="true" (
    cd frontend
    start "Vehicle DB - Frontend" /MIN cmd /k "npm run dev > ..\logs\frontend.log 2>&1"
    cd ..
    echo    √ Frontend started
)

REM ============================================================================
REM Verify services
REM ============================================================================

echo.
echo Verifying services...

timeout /t 2 /nobreak >nul

REM Check backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorLevel% equ 0 (
    echo    √ Backend API: ONLINE
    set BACKEND_STATUS=ONLINE
) else (
    echo    X Backend API: FAILED - Check logs\backend.log
    set BACKEND_STATUS=OFFLINE
)

REM Check frontend
if "%NODE_AVAILABLE%"=="true" (
    timeout /t 2 /nobreak >nul
    curl -s http://localhost:3000 >nul 2>&1
    if %errorLevel% equ 0 (
        echo    √ Frontend: ONLINE
        set FRONTEND_STATUS=ONLINE
    ) else (
        echo    ! Frontend: STARTING ^(wait ~10s^)
        set FRONTEND_STATUS=STARTING
    )
) else (
    set FRONTEND_STATUS=NOT AVAILABLE
)

REM ============================================================================
REM Success screen
REM ============================================================================

cls
color 0A

echo.
echo ============================================================================
echo.
echo                        √ Launch Complete!
echo.
echo ============================================================================
echo.
echo ============================================================================
echo Service Status:
echo ============================================================================
echo   Backend API:          %BACKEND_STATUS%
echo   Frontend App:         %FRONTEND_STATUS%
echo ============================================================================
echo.
echo ============================================================================
echo Access Your App:
echo ============================================================================

if "%FRONTEND_STATUS%"=="ONLINE" (
    echo   Frontend:     http://localhost:3000
)
if "%FRONTEND_STATUS%"=="STARTING" (
    echo   Frontend:     http://localhost:3000 ^(starting...^)
)
echo   API Docs:     http://localhost:8000/docs
echo   API Root:     http://localhost:8000
echo   Health:       http://localhost:8000/health
echo ============================================================================
echo.
echo ============================================================================
echo Useful Commands:
echo ============================================================================
echo   View logs:        type logs\backend.log
echo   Stop services:    stop.bat
echo   Restart:          launch.bat
echo   Full setup:       setup-windows.bat
echo ============================================================================
echo.
echo Services running in background. Logs in .\logs\
echo.

REM Auto-open browser
if "%FRONTEND_STATUS%"=="ONLINE" (
    echo Opening browser in 3 seconds...
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
) else (
    if "%FRONTEND_STATUS%"=="STARTING" (
        echo Opening browser in 3 seconds...
        timeout /t 3 /nobreak >nul
        start http://localhost:3000
    ) else (
        echo Opening API docs in 3 seconds...
        timeout /t 3 /nobreak >nul
        start http://localhost:8000/docs
    )
)

echo.
