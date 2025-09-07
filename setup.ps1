Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MoneyGoals + Hackaodisha Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] Setting up MoneyGoals (Node.js)..." -ForegroundColor Yellow
Set-Location moneygoals
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error installing MoneyGoals dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ MoneyGoals dependencies installed" -ForegroundColor Green
Set-Location ..

Write-Host ""
Write-Host "[2/5] Setting up Hackaodisha (Python)..." -ForegroundColor Yellow
Set-Location Hackodisha

Write-Host "Creating virtual environment..."
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error creating virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Activating virtual environment..."
& "venv\Scripts\Activate.ps1"

Write-Host "Installing Python dependencies..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error installing Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Hackaodisha dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Generating ML models..." -ForegroundColor Yellow
python generate_all_pickles.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Warning: ML model generation failed, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/5] Starting services..." -ForegroundColor Yellow
Write-Host "Starting Hackaodisha Flask server (Port 5000)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & 'venv\Scripts\Activate.ps1'; python app.py"

Write-Host "Waiting for Flask server to start..."
Start-Sleep -Seconds 5

Write-Host "Starting MoneyGoals server (Port 4000)..."
Set-Location ..
Set-Location moneygoals
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run dev"

Write-Host ""
Write-Host "[5/5] Setup Complete! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Services are starting up:" -ForegroundColor Cyan
Write-Host "- MoneyGoals Dashboard: http://localhost:4000" -ForegroundColor White
Write-Host "- Hackaodisha AI Model: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Click the 'AI Investment Advisor' button in the dashboard to access the ML model!" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"


