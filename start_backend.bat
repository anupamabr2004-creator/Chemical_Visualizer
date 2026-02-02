@echo off
REM Start Backend (Django) - python manage.py runserver
REM Run this in a terminal window

echo.
echo Starting Chemical Visualizer Backend (Django)...
echo This will run on: http://localhost:8000
echo.
echo Make sure:
echo   1. Virtual environment is created: python -m venv venv
echo   2. Dependencies installed: pip install -r requirements.txt
echo   3. Database migrated: python manage.py migrate
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database exists
if not exist "db.sqlite3" (
    echo Database not found. Running migrations...
    python manage.py migrate
)

REM Start server
python manage.py runserver

pause
