#!/bin/bash
# Start both Frontend and Backend simultaneously
# Usage: ./start_all.sh

echo ""
echo "========================================="
echo "Chemical Visualizer - Full Stack Startup"
echo "========================================="
echo ""

# Check if in correct directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found!"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Starting Backend (Django) on port 8000..."
echo "Starting Frontend (React) on port 3000..."
echo ""
echo "Backend will run at: http://localhost:8000"
echo "Frontend will run at: http://localhost:3000"
echo ""

# Start backend in background
source venv/bin/activate
python manage.py migrate 2>/dev/null
python manage.py runserver &
BACKEND_PID=$!

sleep 3

# Start frontend in background
cd chemical-frontend
npm install 2>/dev/null
npm start &
FRONTEND_PID=$!

sleep 5

echo "========================================="
echo "✓ Backend running at http://localhost:8000"
echo "✓ Frontend running at http://localhost:3000"
echo "========================================="
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Keep script running
wait
