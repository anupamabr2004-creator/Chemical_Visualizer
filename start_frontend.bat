@echo off
REM Start Frontend (React) - npm start
REM Run this in a terminal window

cd chemical-frontend

echo.
echo Starting Chemical Visualizer Frontend (React)...
echo This will open on: http://localhost:3000
echo.
echo Make sure:
echo   1. Backend is running: python manage.py runserver
echo   2. Node.js is installed: npm --version
echo.

npm install
npm start

pause
