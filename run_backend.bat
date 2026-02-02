@echo off
REM Start Django Backend Server
REM This script starts the chemical_visualizer Django backend

echo Starting Chemical Visualizer Backend...
echo.

cd /d "C:\Users\Surjeet Kumar\chemical_visualizer"

if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please create virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run migrations if needed
echo Applying migrations...
python manage.py migrate

REM Start server
echo.
echo Backend starting on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

python manage.py runserver

pause
