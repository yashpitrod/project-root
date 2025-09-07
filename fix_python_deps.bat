@echo off
echo ========================================
echo    Fixing Python Dependencies
echo ========================================
echo.

cd Hackodisha

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip and setuptools...
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

echo Installing core dependencies one by one...
pip install Flask
pip install numpy
pip install pandas
pip install scikit-learn
pip install joblib

echo Installing additional dependencies...
pip install Werkzeug
pip install Jinja2
pip install MarkupSafe
pip install itsdangerous
pip install click
pip install blinker

echo.
echo Testing installation...
python -c "import flask, numpy, pandas, sklearn, joblib; print('✅ All core dependencies installed successfully!')"

if %errorlevel% neq 0 (
    echo ❌ Some dependencies failed to install
    echo Trying alternative installation method...
    pip install --no-deps Flask
    pip install --no-deps numpy
    pip install --no-deps pandas
    pip install --no-deps scikit-learn
    pip install --no-deps joblib
)

echo.
echo ✅ Python dependencies fix complete!
echo You can now run setup.bat again or start the services manually.
echo.
pause



