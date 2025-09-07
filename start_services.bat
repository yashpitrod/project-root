@echo off
echo ========================================
echo    Starting MoneyGoals + Hackaodisha
echo ========================================
echo.

echo Starting Hackaodisha Flask server (Port 5000)...
cd Hackodisha
start "Hackaodisha Flask Server" cmd /k "call venv\Scripts\activate.bat && python app.py"

echo Waiting for Flask server to start...
timeout /t 3 /nobreak > nul

echo Starting MoneyGoals server (Port 4000)...
cd ..
cd moneygoals
start "MoneyGoals Server" cmd /k "npm run dev"

echo.
echo ✅ Both services are starting up!
echo.
echo - MoneyGoals Dashboard: http://localhost:4000
echo - Hackaodisha AI Model: http://localhost:5000
echo.
echo Click the "AI Investment Advisor" button in the dashboard to access the ML model!
echo.
pause


