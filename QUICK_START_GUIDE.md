# 🚀 Quick Start Guide

## Step-by-Step Setup

### 1. Prerequisites Check
First, make sure you have these installed:
- **Node.js** (v16+) - Download from [nodejs.org](https://nodejs.org/)
- **Python 3.8+** - Download from [python.org](https://python.org/)
- **MongoDB** - Download from [mongodb.com](https://mongodb.com/try/download/community)

### 2. Verify Installation
Run this command to check if everything is installed:
```cmd
check_installation.bat
```

### 3. One-Click Setup
Run the automated setup script:
```cmd
setup.bat
```

This will:
- ✅ Install all Node.js dependencies
- ✅ Create Python virtual environment
- ✅ Install all Python ML dependencies
- ✅ Generate ML models
- ✅ Start both servers automatically

### 4. Access Your Applications
After setup completes, you'll have:
- **MoneyGoals Dashboard:** http://localhost:4000
- **Hackaodisha AI Model:** http://localhost:5000

### 5. Using the AI Integration
1. Open http://localhost:4000 in your browser
2. Add your financial data
3. Click the **"🤖 AI Investment Advisor"** button
4. Get personalized ML-powered investment recommendations!

## Troubleshooting

### If setup fails:
1. Make sure all prerequisites are installed
2. Run `check_installation.bat` to verify
3. Try running `setup.bat` again

### If services don't start:
1. Make sure ports 4000 and 5000 are available
2. Check if MongoDB is running
3. Run `start_services.bat` to restart both services

### If AI button doesn't work:
1. Make sure Hackaodisha is running on port 5000
2. Check the browser console for errors
3. Verify the Flask server is accessible at http://localhost:5000

## Manual Commands (If needed)

### Start MoneyGoals only:
```cmd
cd moneygoals
npm run dev
```

### Start Hackaodisha only:
```cmd
cd Hackodisha
venv\Scripts\activate
python app.py
```

## Need Help?
- Check the main README.md for detailed information
- Contact: pitrodayash1412007@gmail.com

---

**🎉 Enjoy your AI-powered financial journey!**




