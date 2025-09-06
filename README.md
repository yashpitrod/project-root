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

---

## Technology Stack

- Node.js & Express.js
- MongoDB & Mongoose
- EJS templating engine
- Axios for API requests
- Python ML API

---

## Getting Started

### Prerequisites

- Node.js (v16+ recommended)
- MongoDB running locally or accessible remotely
- Python 3+ and necessary ML dependencies installed

### Installation

1. Clone the repository:

git clone https://github.com/yourusername/moneygoals.git
cd moneygoals

text

2. Install dependencies:

npm install

text

3. Create a `.env` file in the project root with:

PORT=3000
MONGO_URI=mongodb://localhost:27017/moneygoals
SESSION_SECRET=your_secret_key

text

4. Start your local MongoDB server if not running.

5. Start the Python ML prediction API separately.

6. Run your development server:

npm run dev

text

7. Open your browser at [http://localhost:4000](http://localhost:4000)

---

## Usage

- Use the dashboard to submit income and expenses.
- View machine learning based predictions and analysis.
- Manage financial data easily with persistent storage.

---

## Contributing

Contributions are welcome!  
Please open issues or submit pull requests to help improve MoneyGoals.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, open an issue or contact the maintainer at pitrodayash1412007@gmail.com
