@echo off
echo ========================================
echo   Starting All MoneyGoals Services
echo ========================================
echo.

echo Starting FastAPI prediction service (Port 8080)...
cd ml_service
start "FastAPI Prediction Service" cmd /k "python serve.py"

echo Waiting for FastAPI service to start...
timeout /t 3 /nobreak > nul

echo Starting Hackodisha Flask server (Port 5000)...
cd ..
cd Hackodisha
start "Hackodisha Flask Server" cmd /k "call venv\Scripts\activate.bat && python app.py"

echo Waiting for Flask server to start...
timeout /t 3 /nobreak > nul

echo Starting MoneyGoals server (Port 4000)...
cd ..
cd moneygoals
start "MoneyGoals Server" cmd /k "npm start"

echo.
echo ✅ All three services are starting up!
echo.
echo - MoneyGoals Dashboard: http://localhost:4000
echo - Hackodisha AI Model: http://localhost:5000
echo - FastAPI Prediction Service: http://localhost:8080
echo.
echo 🚀 All services are now running!
echo Click the "AI Investment Advisor" button in the dashboard to access the ML model!
echo.
pause
