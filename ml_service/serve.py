from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize app first
app = FastAPI(
    title="Expense Predictor API",
    description="ML-based expense tracking and prediction service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Training data
data = {
    'income': [31000, 26000, 28000, 27000, 29563, 30236, 31692, 30699],
    'house_rent': [3000, 3000, 3100, 3200, 3150, 3060, 3111, 3015],
    'food_costs': [9000, 8650, 7520, 9263, 8523, 7532, 9512, 9632],
    'electricity': [600, 650, 625, 693, 450, 423, 582, 601],
    'gas': [820, 825, 862, 851, 810, 810, 821, 875],
    'water': [400, 450, 420, 440, 430, 420, 430, 440],
    'misc': [3020, 2220, 2210, 2230, 1215, 3275, 2246, 2278],
}

# Feature columns for efficiency
EXPENSE_COLUMNS = ['house_rent', 'food_costs', 'electricity', 'gas', 'water', 'misc']
FEATURE_COLUMNS = ['income'] + EXPENSE_COLUMNS

# Prepare DataFrame and calculate baseline
df = pd.DataFrame(data)
df['baseline_expense'] = df[EXPENSE_COLUMNS].sum(axis=1)

# Train model once at startup
def train_model():
    """Train the linear regression model with optimized parameters"""
    X = df[FEATURE_COLUMNS]
    y = df['baseline_expense']
    
    # Using 80-20 split with fixed random state for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize and train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Calculate training score for monitoring
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model trained - Train R²: {train_score:.4f}, Test R²: {test_score:.4f}")
    
    return model

# Train model at startup
model = train_model()

# Environment variables
ML_SECRET_KEY = os.getenv("ML_SECRET_KEY", "default_secret")
PORT = int(os.getenv("PORT", 8080))

# Constants for status logic
SAVINGS_THRESHOLD = -500
BALANCE_THRESHOLD = 300
MISC_HIGH_THRESHOLD = 4000
STATUS_RANGE = (-500, 500)

class InputData(BaseModel):
    """Input data model with validation"""
    income: int
    house_rent: int
    food_costs: int
    electricity: int
    gas: int
    water: int
    misc: int
    
    class Config:
        schema_extra = {
            "example": {
                "income": 30000,
                "house_rent": 3000,
                "food_costs": 8500,
                "electricity": 600,
                "gas": 820,
                "water": 430,
                "misc": 2500
            }
        }

def generate_status(income: int, actual: float, baseline: float, misc: int) -> str:
    """Generate status message based on expense analysis"""
    diff = actual - baseline
    savings = income - actual
    
    # Optimized status generation with clearer logic
    if diff < SAVINGS_THRESHOLD:
        if misc <= MISC_HIGH_THRESHOLD:
            return f"Your income is {income}. Your expenses are less. Congrats you saved {savings:.0f}."
        else:
            return f"Your income is {income}. Your expenses are less. However you are spending more on miscellaneous items. You saved {savings:.0f}."
    
    elif diff < BALANCE_THRESHOLD and misc > MISC_HIGH_THRESHOLD:
        return f"Your income is {income}. Your expenses are balanced. However you are spending more on miscellaneous items. You saved {savings:.0f}."
    
    elif STATUS_RANGE[0] < diff < STATUS_RANGE[1] and misc <= MISC_HIGH_THRESHOLD:
        return f"Your income is {income}. Your expenses are balanced. You save {savings:.0f}."
    
    else:
        return f"Your expenses for this month are a bit higher. Your income is {income}. You save {savings:.0f}."

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Expense Predictor API"}

@app.get("/model/info")
async def model_info():
    """Get model information"""
    return {
        "model_type": "LinearRegression",
        "features": FEATURE_COLUMNS,
        "training_samples": len(df),
        "coefficients": dict(zip(FEATURE_COLUMNS, model.coef_)),
        "intercept": model.intercept_
    }

@app.post("/predict")
def predict(data: InputData):
    """
    Predict baseline expense and analyze spending patterns
    
    Returns:
        - predicted_baseline: ML predicted baseline expense
        - actual_expense: Sum of all actual expenses
        - income: User's income
        - breakdown: Detailed expense breakdown
        - status: Analysis message
    """
    # Efficiently create feature DataFrame
    features = pd.DataFrame([data.dict()])
    
    # Get prediction
    baseline_pred = float(model.predict(features[FEATURE_COLUMNS])[0])
    
    # Calculate actual expense efficiently
    expense_data = data.dict()
    actual_expense = sum(
        expense_data[col] for col in EXPENSE_COLUMNS
    )
    
    # Generate status
    status = generate_status(
        data.income, 
        actual_expense, 
        baseline_pred, 
        data.misc
    )
    
    # Create breakdown dictionary
    breakdown = {
        "House Rent": data.house_rent,
        "Food": data.food_costs,
        "Electricity": data.electricity,
        "Gas": data.gas,
        "Water": data.water,
        "Misc": data.misc
    }
    
    return {
        "predicted_baseline": round(baseline_pred, 2),
        "actual_expense": actual_expense,
        "income": data.income,
        "savings": data.income - actual_expense,
        "variance": round(actual_expense - baseline_pred, 2),
        "breakdown": breakdown,
        "status": status
    }

@app.post("/batch_predict")
def batch_predict(data_list: list[InputData]):
    """
    Batch prediction for multiple expense records
    
    Args:
        data_list: List of InputData objects
    
    Returns:
        List of predictions for each input
    """
    results = []
    for data in data_list:
        results.append(predict(data))
    return {"predictions": results, "count": len(results)}

if __name__ == "__main__":
    # Use environment PORT with proper configuration
    uvicorn.run(
        "serve:app", 
        host="0.0.0.0", 
        port=PORT, 
        reload=False,
        log_level="info"
    )
