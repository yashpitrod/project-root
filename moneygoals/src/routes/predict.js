const express = require("express");
const router = express.Router();
const axios = require("axios");
const MonthData = require("../models/MonthData");

router.get("/", (req, res) => {
    res.render("input.ejs"); // replace with your actual prediction panel view filename
});

// Primary: FastAPI model (ml_service/serve.py)
const FASTAPI_URL = "http://127.0.0.1:8080/predict";
// Secondary: Flask AI recommendations (Hackodisha)
const FLASK_URL = "http://127.0.0.1:5000/api/recommendations";

router.post("/", async (req, res) => {
    try {
        // Extract and map form fields
        const income = parseInt(req.body.income || 0, 10);
        const houseRent = parseInt(req.body.house_rent || 0, 10);
        const foodCosts = parseInt(req.body.food_costs || 0, 10);
        const electricity = parseInt(req.body.electricity || 0, 10);
        const gas = parseInt(req.body.gas || 0, 10);
        const water = parseInt(req.body.water || 0, 10);
        const misc = parseInt(req.body.misc || 0, 10);
        const monthSelected = (req.body.month && String(req.body.month).trim().toLowerCase()) || null;

        const monthlyExpenses = [houseRent, foodCosts, electricity, gas, water, misc]
            .filter(v => Number.isFinite(v))
            .reduce((s, v) => s + v, 0);

        // 1) Try FastAPI first (returns predicted_baseline, actual_expense, income, status)
        let predictedBaseline;
        let accountBalance;
        let savingsBalance;
        let status;
        let mlData = null; // optional Flask insights

        try {
            const fastapiPayload = {
                income,
                house_rent: houseRent,
                food_costs: foodCosts,
                electricity,
                gas,
                water,
                misc
            };
            const { data: fastResp } = await axios.post(FASTAPI_URL, fastapiPayload, { timeout: 8000 });
            if (fastResp && typeof fastResp.predicted_baseline !== 'undefined') {
                predictedBaseline = Math.round(fastResp.predicted_baseline);
                const actualExpense = Math.round(fastResp.actual_expense ?? monthlyExpenses);
                status = fastResp.status || (income - actualExpense > 0 ? "Good" : "Over Budget");
                accountBalance = income - actualExpense;
                savingsBalance = income - predictedBaseline;
            }
        } catch (e) {
            console.warn("⚠️ FastAPI model not available:", e.message);
        }

        // 2) If FastAPI not available, compute locally and optionally fetch Flask insights
        if (typeof predictedBaseline === 'undefined') {
            predictedBaseline = monthlyExpenses;
            accountBalance = income - monthlyExpenses;
            savingsBalance = income - predictedBaseline;
            status = savingsBalance > 0 ? "Good" : (savingsBalance === 0 ? "Balanced" : "Over Budget");

            try {
                const flaskPayload = {
                    monthly_income: income,
                    monthly_expenses: monthlyExpenses,
                    age: 30,
                    dependents: 1,
                    income_stability: 3
                };
                const { data } = await axios.post(FLASK_URL, flaskPayload, { timeout: 8000 });
                if (data && data.status === "success") mlData = data.data;
            } catch (e) {
                console.warn("⚠️ Flask insights unavailable:", e.message);
            }
        }

        // Save to DB including category breakdown
        const newMonth = new MonthData({
            month: monthSelected || new Date().toLocaleString("default", { month: "long", year: "numeric" }),
            income,
            house_rent: houseRent,
            food_costs: foodCosts,
            electricity,
            gas,
            water,
            misc,
            realExpense: monthlyExpenses,
            predictedBaseline,
            accountBalance,
            savingsBalance,
            status
        });

        await newMonth.save();

        // Render result page (attach ML insights if available)
        res.render("prediction_result", {
            income,
            actual_expense: monthlyExpenses,
            predicted_baseline: predictedBaseline,
            accountBalance,
            savingsBalance,
            status,
            ml: mlData,
            breakdown: {
                house_rent: houseRent || 0,
                food_costs: foodCosts || 0,
                electricity: electricity || 0,
                gas: gas || 0,
                water: water || 0,
                misc: misc || 0
            }
        });
    } catch (err) {
        console.error("❌ Error in prediction route:", err);
        res.status(500).send("Prediction service failed");
    }
});

module.exports = router;
