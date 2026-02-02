@echo off
REM Chemical Visualizer - Complete Installation & Setup Script
REM This script will guide you through the entire setup process

cls
title Chemical Visualizer - Setup Assistant

echo.
echo ================================
echo   CHEMICAL VISUALIZER SETUP
echo   Dashboard with Charts
echo ================================
echo.

REM Check Node.js
echo [1/5] Checking Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please download from: https://nodejs.org/
    echo Then restart this script.
    pause
    exit /b 1
) else (
    echo [✓] Node.js installed
)

REM Check npm
echo [2/5] Checking npm installation...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm is not installed!
    pause
    exit /b 1
) else (
    echo [✓] npm installed
)

REM Display versions
echo.
echo --- Versions ---
node --version
npm --version
echo.

REM Install frontend dependencies
echo [3/5] Installing frontend dependencies...
cd /d "c:\Users\Surjeet Kumar\chemical_visualizer\chemical-frontend"
if exist "node_modules" (
    echo [!] node_modules already exists, skipping npm install
    echo [?] Run this command to force reinstall:
    echo    npm install --force
) else (
    echo Installing npm packages...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: npm install failed!
        echo Try: npm cache clean --force && npm install
        pause
        exit /b 1
    )
)
echo [✓] Frontend dependencies installed

REM Check database
echo [4/5] Checking database...
cd /d "c:\Users\Surjeet Kumar\chemical_visualizer"
if exist "db.sqlite3" (
    echo [✓] Database exists
) else (
    echo [!] Database not found, creating...
    call python manage.py migrate
)

REM Display startup instructions
echo.
echo [5/5] Setup complete!
echo.
echo ================================
echo   READY TO START
echo ================================
echo.
echo Next steps:
echo.
echo TERMINAL 1 - Backend:
echo   1. Run: cd c:\Users\Surjeet Kumar\chemical_visualizer
echo   2. Run: venv\Scripts\activate
echo   3. Run: python manage.py runserver
echo.
echo TERMINAL 2 - Frontend:
echo   1. Run: cd c:\Users\Surjeet Kumar\chemical_visualizer\chemical-frontend
echo   2. Run: npm start
echo.
echo BROWSER:
echo   Open: http://localhost:3000
echo.
echo ================================
echo   QUICK TEST
echo ================================
echo.
echo After starting both servers:
echo   1. Login or Register
echo   2. Upload sample_data.csv
echo   3. Click "Analyze" to see charts
echo   4. Click "Table" to see data
echo   5. Click "History" to see recent uploads
echo   6. Click "Export PDF" to download report
echo.
echo ================================
echo   FEATURES
echo ================================
echo.
echo ✓ Interactive Charts (Doughnut & Bar)
echo ✓ Data Tables with equipment breakdown
echo ✓ History Management (last 5 uploads)
echo ✓ PDF Export with charts included
echo ✓ Responsive Mobile Design
echo ✓ Professional styling with animations
echo.
echo ================================
echo   DOCUMENTATION
echo ================================
echo.
echo Available guides:
echo   - QUICK_START.md              Quick setup checklist
echo   - CHARTS_FEATURES.md          Detailed feature docs
echo   - DASHBOARD_VISUAL_GUIDE.md   Visual layouts
echo   - RUN_NOW.md                  Complete guide
echo.
echo ================================
echo.
pause
