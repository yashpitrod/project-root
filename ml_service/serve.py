from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Data WITH 'misc' considered in model training
data = {
    'income':[31000,26000,28000,27000,29563,30236,31692,30699],
    'house_rent':[3000, 3000, 3100, 3200, 3150,3060,3111,3015],
    'food_costs':[9000, 8650, 7520, 9263, 8523, 7532, 9512, 9632],
    'electricity':[600,650,625,693,450,423,582,601],
    'gas':[820,825,862,851,810,810,821,875],
    'water':[400, 450, 420, 440, 430,420,430,440],
    'misc':[3020,2220,2210,2230,1215,3275,2246,2278], # present for reference, NOT used for baseline prediction
}

df = pd.DataFrame(data)
df['baseline_expense'] = df[['house_rent','food_costs','electricity','gas','water','misc']].sum(axis=1)

# TRAIN MODEL WITH misc
X = df[['income','house_rent','food_costs','electricity','gas','water','misc']]
y = df['baseline_expense']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

app = FastAPI()

class InputData(BaseModel):
    income: int
    house_rent: int
    food_costs: int
    electricity: int
    gas: int
    water: int
    misc: int

@app.post("/predict")
def predict(data: InputData):
    # Prepare features for prediction: include misc
    features = pd.DataFrame([{
        "income": data.income,
        "house_rent": data.house_rent,
        "food_costs": data.food_costs,
        "electricity": data.electricity,
        "gas": data.gas,
        "water": data.water,
        "misc": data.misc
    }])
    baseline_pred = float(model.predict(features)[0])

    # Actual expense = sum of all (including misc)
    sumall = (
        data.house_rent +
        data.food_costs +
        data.electricity +
        data.gas +
        data.water +
        data.misc
    )
    income = data.income
    misc = data.misc

    # Matching your logic and wording
    if sumall - baseline_pred < -500 and misc <= 4000:
        status = f"Your income is {income}. Your expenses are less. Congrats you saved {income - sumall}."
    elif sumall - baseline_pred < -500 and misc > 4000:
        status = f"Your income is {income}. Your expenses are less. However you are spending more on miscellaneous items. You saved {income - sumall}."
    elif sumall - baseline_pred < 300 and misc > 4000:
        status = f"Your income is {income}. Your expenses are balanced. However you are spending more on miscellaneous items. You saved {income - sumall}."
    elif -500 < sumall - baseline_pred < 500 and misc <= 4000:
        status = f"Your income is {income}. Your expenses are balanced. You save {income - sumall}."
    else:
        status = f"Your expenses for this month are a bit higher. Your income is {income}. You save {income - sumall}."

    breakdown = {
        "House Rent": data.house_rent,
        "Food": data.food_costs,
        "Electricity": data.electricity,
        "Gas": data.gas,
        "Water": data.water,
        "Misc": data.misc
    }

    return {
        "predicted_baseline": baseline_pred,
        "actual_expense": sumall,
        "income": data.income,
        "breakdown": breakdown,
        "status": status
    }

if __name__ == "__main__":
    # Start FastAPI server
    uvicorn.run("serve:app", host="0.0.0.0", port=8080, reload=False)
