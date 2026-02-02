@echo off
REM Chemical Visualizer - Diagnostic Script
REM Run this script to diagnose common issues

echo.
echo ========================================
echo Chemical Visualizer Diagnostic Tool
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Python is installed
    python --version
) else (
    echo   ✗ Python is NOT installed
    echo   Please install Python 3.8+ from python.org
    goto end
)

REM Check virtual environment
echo.
echo [2/5] Checking virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo   ✓ Virtual environment exists
    call venv\Scripts\activate.bat
    echo   ✓ Virtual environment activated
) else (
    echo   ✗ Virtual environment NOT found
    echo   Create with: python -m venv venv
    goto end
)

REM Check required packages
echo.
echo [3/5] Checking required packages...
python -c "import django; print('  ✓ Django:', django.__version__)" 2>nul || echo "  ✗ Django not installed"
python -c "import rest_framework; print('  ✓ DRF installed')" 2>nul || echo "  ✗ djangorestframework not installed"
python -c "import rest_framework_simplejwt; print('  ✓ Simple JWT installed')" 2>nul || echo "  ✗ djangorestframework-simplejwt not installed"
python -c "import corsheaders; print('  ✓ CORS Headers installed')" 2>nul || echo "  ✗ django-cors-headers not installed"
python -c "import reportlab; print('  ✓ ReportLab installed')" 2>nul || echo "  ✗ reportlab not installed"

REM Check database
echo.
echo [4/5] Checking database...
if exist "db.sqlite3" (
    echo   ✓ Database file exists
    for /f %%A in ('dir /b db.sqlite3') do set size=%%~zA
    echo   File size: %size% bytes
) else (
    echo   ⚠ Database file NOT found
    echo   Run: python manage.py migrate
)

REM Check important settings
echo.
echo [5/5] Checking Django settings...
python manage.py check 2>nul
if %errorlevel% equ 0 (
    echo   ✓ Django configuration is valid
) else (
    echo   ✗ Django configuration has errors
)

echo.
echo ========================================
echo Summary
echo ========================================
echo.
echo If all checks passed:
echo   1. Start Django: python manage.py runserver
echo   2. Open browser: http://localhost:8000
echo   3. Login page should appear
echo.
echo Common fixes:
echo   - Install packages: pip install -r requirements.txt
echo   - Run migrations: python manage.py migrate
echo   - Clear cache: Delete all files in uploads/ folder
echo.
echo For detailed troubleshooting, see SETUP_GUIDE.md
echo.

:end
pause
