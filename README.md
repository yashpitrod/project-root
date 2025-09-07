# 💰 FinFlow

**Personal Finance Tracker with Machine Learning Predictions**

---

## Overview

MoneyGoals is a full-stack web application designed to help users track monthly income and expenses while leveraging machine learning predictions for smarter budgeting and saving. It features a responsive dashboard, detailed expense input forms, and integrates seamlessly with a Python-based ML prediction service.

---

## Features

- Input and manage income and categorized expenses (rent, food, utilities, etc.)
- Machine learning-based baseline expense and savings predictions
- Visual dashboard displaying financial summary, savings, and buffer accounts
- RESTful API backend with Node.js, Express, and MongoDB
- Data persistence using MongoDB and Mongoose
- Modern frontend with EJS templating and responsive design
- Python ML microservice for financial predictions
- **🤖 AI Button Integration:** Clicking the "AI Investment Advisor" button in the MoneyGoals dashboard opens the Hackaodisha ML model interface seamlessly!

---

## Technology Stack

- **Frontend:** Node.js, Express.js, EJS templating, Bootstrap 5
- **Backend:** MongoDB, Mongoose
- **ML Service:** Python, Flask, scikit-learn, pandas, numpy
- **AI Model:** Hackaodisha - Advanced ML investment advisor

---

## 🚀 Quick Start (Automated Setup)

### Prerequisites

- **Node.js** (v16+ recommended) - [Download here](https://nodejs.org/)
- **Python 3.8+** - [Download here](https://python.org/)
- **MongoDB** - [Download here](https://mongodb.com/try/download/community)

### One-Click Setup

#### For Windows:

1. **Run the automated setup script:**
   ```cmd
   setup.bat
   ```
   
   Or for PowerShell:
   ```powershell
   .\setup.ps1
   ```

2. **The script will automatically:**
   - Install all Node.js dependencies for MoneyGoals
   - Create Python virtual environment for Hackaodisha
   - Install all Python ML dependencies
   - Generate ML models and pickle files
   - Start both servers (MoneyGoals on port 4000, Hackaodisha on port 5000)

3. **Access your applications:**
   - **MoneyGoals Dashboard:** http://localhost:4000
   - **Hackaodisha AI Model:** http://localhost:5000

---

## 🔧 Manual Setup (If needed)

### 1. MoneyGoals Setup

```bash
cd moneygoals
npm install
npm run dev
```

### 2. Hackaodisha ML Model Setup

```bash
cd Hackodisha
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python generate_all_pickles.py
python app.py
```

### 3. Start MongoDB

Make sure MongoDB is running on your system (default port 27017).

---

## 📱 Usage

1. **Open MoneyGoals Dashboard:** http://localhost:4000
2. **Add your financial data** using the input forms
3. **View your dashboard** with financial summaries and predictions
4. **Click the "🤖 AI Investment Advisor" button** to access the advanced ML model
5. **Get personalized investment recommendations** powered by machine learning

---

## 🎯 Key Features

### MoneyGoals Dashboard
- Beautiful, responsive interface with modern design
- Real-time financial data visualization
- Monthly breakdown with income, expenses, and predictions
- Account balance and savings tracking

### Hackaodisha AI Model
- **Machine Learning-powered investment recommendations**
- Personalized portfolio allocation based on your profile
- Risk assessment and capacity analysis
- Multiple investment options (Equity, Debt, Gold, Emergency Fund)
- Expected return predictions with confidence scores

---

## 📁 Project Structure

```
project-root/
├── moneygoals/                 # Node.js frontend
│   ├── src/                   # Server code
│   ├── views/                 # EJS templates
│   ├── public/                # Static files (images, CSS, JS)
│   │   └── images/
│   │       └── generated-image-4.jpg   # <-- Place your background image here, no spaces in filename!
│   └── package.json
├── Hackodisha/                # Python ML backend
│   ├── app.py                 # Flask application
│   ├── ml_models/             # ML models and data
│   ├── templates/             # HTML templates
│   └── requirements.txt
├── setup.bat                  # Windows setup script
├── setup.ps1                  # PowerShell setup script
└── README.md
```

**Important:**  
- All static images (like `generated-image-4.jpg`) must be placed in `moneygoals/public/images/` and have filenames **without spaces**.
- If your image is not loading, check the filename and path, and restart your Node.js server.

---

## 🛠️ Troubleshooting

### Common Issues:

1. **Port already in use:**
   - MoneyGoals runs on port 4000
   - Hackaodisha runs on port 5000
   - Make sure these ports are available

2. **MongoDB connection error:**
   - Ensure MongoDB is running
   - Check connection string in the code

3. **Python dependencies error:**
   - Make sure you're in the virtual environment
   - Try: `pip install --upgrade pip` then `pip install -r requirements.txt`

4. **ML models not loading:**
   - Run `python generate_all_pickles.py` in the Hackodisha directory
   - Check if all pickle files are generated in `ml_models/saved_models/`

5. **Static images not loading:**
   - Ensure your image is in `moneygoals/public/images/`
   - Use filenames **without spaces** (e.g., `generated-image-4.jpg`)
   - Reference images in your EJS/CSS as `/images/generated-image-4.jpg`
   - Restart your Node.js server after adding new images

---

## 🤖 AI Integration

The AI button in the MoneyGoals dashboard seamlessly integrates with the Hackaodisha ML model:

- **One-click access** to advanced investment recommendations
- **Personalized analysis** based on your financial profile
- **Machine learning predictions** for optimal portfolio allocation
- **Real-time recommendations** with confidence scores

---

## 📊 ML Model Features

- **Advanced Algorithms:** Random Forest, Gradient Boosting
- **Feature Engineering:** 11+ financial parameters analyzed
- **Risk Assessment:** Age, income stability, dependents analysis
- **Portfolio Optimization:** Dynamic allocation based on ML predictions
- **Confidence Scoring:** Model confidence levels for each recommendation

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests to help improve MoneyGoals.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, open an issue or contact the maintainer at **pitrodayash1412007@gmail.com**

---

## 🎉 Enjoy Your AI-Powered Financial Journey!

Start tracking your finances and get intelligent investment recommendations with just one click!
