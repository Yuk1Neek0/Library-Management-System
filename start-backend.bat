@echo off
echo Starting Library Management System - Backend
echo ============================================
cd backend
echo.
echo Initializing database...
python database.py
echo.
echo Starting Flask server on http://localhost:5000
echo.
python app.py
