@echo off
echo ========================================
echo    Installation Verification
echo ========================================
echo.

echo Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js first.
    pause
    exit /b 1
)
echo ✅ Node.js is installed

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python is installed

echo.
echo Checking MongoDB...
mongo --version
if %errorlevel% neq 0 (
    echo ⚠️ MongoDB not found. Please install MongoDB or ensure it's running.
) else (
    echo ✅ MongoDB is installed
)

echo.
echo Checking MoneyGoals dependencies...
cd moneygoals
if exist "node_modules" (
    echo ✅ MoneyGoals dependencies are installed
) else (
    echo ❌ MoneyGoals dependencies not found. Run setup.bat first.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Checking Hackaodisha dependencies...
cd Hackodisha
if exist "venv" (
    echo ✅ Hackaodisha virtual environment exists
) else (
    echo ❌ Hackaodisha virtual environment not found. Run setup.bat first.
    cd ..
    pause
    exit /b 1
)

if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment is properly configured
) else (
    echo ❌ Virtual environment activation script not found.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Checking ML models...
cd Hackodisha
if exist "ml_models\saved_models\ml_models.pkl" (
    echo ✅ ML models are generated
) else (
    echo ⚠️ ML models not found. They will be generated on first run.
)
cd ..

echo.
echo ========================================
echo    Installation Check Complete!
echo ========================================
echo.
echo All systems are ready! You can now run:
echo - setup.bat (for first-time setup)
echo - start_services.bat (to start both services)
echo.
pause


