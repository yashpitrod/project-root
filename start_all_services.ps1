Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting All MoneyGoals Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting FastAPI prediction service (Port 8080)..." -ForegroundColor Yellow
Set-Location ml_service
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python serve.py"

Write-Host "Waiting for FastAPI service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Hackodisha Flask server (Port 5000)..." -ForegroundColor Yellow
Set-Location ..
Set-Location Hackodisha
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & 'venv\Scripts\Activate.ps1'; python app.py"

Write-Host "Waiting for Flask server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting MoneyGoals server (Port 4000)..." -ForegroundColor Yellow
Set-Location ..
Set-Location moneygoals
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start"

Write-Host ""
Write-Host "✅ All three services are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "- MoneyGoals Dashboard: http://localhost:4000" -ForegroundColor White
Write-Host "- Hackodisha AI Model: http://localhost:5000" -ForegroundColor White
Write-Host "- FastAPI Prediction Service: http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "🚀 All services are now running!" -ForegroundColor Green
Write-Host "Click the 'AI Investment Advisor' button in the dashboard to access the ML model!" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"
