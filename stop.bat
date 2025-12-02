@echo off
REM ============================================================================
REM Vehicle Repair Database - Stop All Services (Windows)
REM ============================================================================

echo.
echo Stopping Vehicle Repair Database services...
echo.

REM Kill backend processes
taskkill /F /FI "WINDOWTITLE eq Vehicle DB - Backend*" >nul 2>&1
if %errorLevel% equ 0 (
    echo    √ Backend stopped
) else (
    echo    ! Backend not running
)

REM Kill frontend processes
taskkill /F /FI "WINDOWTITLE eq Vehicle DB - Frontend*" >nul 2>&1
if %errorLevel% equ 0 (
    echo    √ Frontend stopped
) else (
    echo    ! Frontend not running
)

REM Fallback: kill by process name on ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    if %errorLevel% equ 0 echo    √ Killed process on port 8000
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    if %errorLevel% equ 0 echo    √ Killed process on port 3000
)

echo.
echo All services stopped.
echo.
echo To restart, run: launch.bat
echo.
pause
