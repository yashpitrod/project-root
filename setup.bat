@echo off
echo ========================================
echo    MoneyGoals + Hackaodisha Setup
echo ========================================
echo.

echo [1/5] Setting up MoneyGoals (Node.js)...
cd moneygoals
call npm install
if %errorlevel% neq 0 (
    echo ❌ Error installing MoneyGoals dependencies
    pause
    exit /b 1
)
echo ✅ MoneyGoals dependencies installed
cd ..

echo.
echo [2/5] Setting up Hackaodisha (Python)...
cd Hackodisha

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Error creating virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
echo Upgrading pip first...
python -m pip install --upgrade pip
echo Installing setuptools and wheel...
pip install --upgrade setuptools wheel
echo Installing core dependencies...
pip install Flask numpy pandas scikit-learn joblib
if %errorlevel% neq 0 (
    echo ❌ Error installing core dependencies
    pause
    exit /b 1
)
echo Installing additional dependencies...
pip install Werkzeug Jinja2 MarkupSafe itsdangerous click blinker
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Some optional dependencies failed, but continuing...
)
echo ✅ Hackaodisha dependencies installed

echo.
echo [3/5] Generating ML models...
python generate_all_pickles.py
if %errorlevel% neq 0 (
    echo ⚠️ Warning: ML model generation failed, but continuing...
)

echo.
echo [4/5] Starting services...
echo Starting Hackaodisha Flask server (Port 5000)...
start "Hackaodisha Flask Server" cmd /k "call venv\Scripts\activate.bat && python app.py"

echo Waiting for Flask server to start...
timeout /t 5 /nobreak > nul

echo Starting MoneyGoals server (Port 4000)...
cd ..
cd moneygoals
start "MoneyGoals Server" cmd /k "npm run dev"

echo.
echo [5/5] Setup Complete! 🎉
echo.
echo Services are starting up:
echo - MoneyGoals Dashboard: http://localhost:4000
echo - Hackaodisha AI Model: http://localhost:5000
echo.
echo Click the "AI Investment Advisor" button in the dashboard to access the ML model!
echo.
pause

