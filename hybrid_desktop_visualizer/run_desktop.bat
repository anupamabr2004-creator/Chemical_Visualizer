@echo off
REM Chemical Visualizer Desktop Application Startup Script
REM This script starts the desktop application

echo.
echo ========================================
echo Chemical Visualizer - Desktop App
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Chemical Visualizer Desktop Application...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo Please check the backend is running: python manage.py runserver
    pause
)

exit /b 0
