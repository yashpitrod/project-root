from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 🟢 Example dataset (dummy, just to train a small model)
data = {
    'income':[31000,26000,28000,27000,29563,30236,31692,30699],
    'house_rent':[3000,3000,3100,3200,3150,3060,3111,3015],
    'food_costs':[9000,8650,7520,9263,8523,7532,9512,9632],
    'electricity':[600,650,625,693,450,423,582,601],
    'gas':[820,825,862,851,810,810,821,875],
    'water':[400,450,420,440,430,420,430,440],
    'misc':[3020,2220,2210,2230,1215,3275,2246,2278],
}

df = pd.DataFrame(data)
df['baseline_expense'] = df[['house_rent','food_costs','electricity','gas','water','misc']].sum(axis=1)

X = df[['income','house_rent','food_costs','electricity','gas','water','misc']]
y = df['baseline_expense']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

app = FastAPI()

# 🟢 Input data format
class InputData(BaseModel):
    income: int
    house_rent: int
    food_costs: int
    electricity: int
    gas: int
    water: int
    misc: int

# 🟢 Prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    features = pd.DataFrame([{
        "income": data.income,
        "house_rent": data.house_rent,
        "food_costs": data.food_costs,
        "electricity": data.electricity,
        "gas": data.gas,
        "water": data.water,
        "misc": data.misc
    }])

    baseline_pred = model.predict(features)[0]
    sumall = (data.house_rent + data.food_costs + data.electricity +
              data.gas + data.water + data.misc)

    if sumall - baseline_pred < -500:
        status = f"Expenses are low. Saved {data.income - sumall}."
    elif -500 <= sumall - baseline_pred <= 500:
        status = f"Expenses are balanced. Saved {data.income - sumall}."
    else:
        status = f"Expenses are higher."

    return {
        "predicted_baseline": baseline_pred,
        "actual_expense": sumall,
        "income": data.income,
        "status": status
    }
