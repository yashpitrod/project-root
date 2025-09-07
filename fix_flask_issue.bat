@echo off
echo ========================================
echo    Fixing Flask Import Issue
echo ========================================
echo.

cd Hackodisha

echo Step 1: Checking current Python environment...
python -c "import sys; print('Python path:', sys.executable)"

echo.
echo Step 2: Deactivating and reactivating virtual environment...
call venv\Scripts\deactivate.bat 2>nul
call venv\Scripts\activate.bat

echo.
echo Step 3: Verifying virtual environment is active...
python -c "import sys; print('Python path after activation:', sys.executable)"

echo.
echo Step 4: Uninstalling and reinstalling Flask...
pip uninstall flask -y
pip install flask

echo.
echo Step 5: Testing Flask installation...
python -c "import flask; print('✅ Flask version:', flask.__version__)"

if %errorlevel% neq 0 (
    echo.
    echo Step 6: Flask still not working, recreating virtual environment...
    call venv\Scripts\deactivate.bat
    rmdir /s /q venv
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install flask numpy pandas scikit-learn joblib
    pip install werkzeug jinja2 markupsafe itsdangerous click blinker
    echo.
    echo Testing Flask after recreation...
    python -c "import flask; print('✅ Flask version:', flask.__version__)"
)

echo.
echo Step 7: Testing all dependencies...
python test_installation.py

echo.
echo ✅ Flask fix complete!
echo You can now run: python app.py
echo.
pause



