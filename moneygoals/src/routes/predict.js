const express = require("express");
const router = express.Router();
const axios = require("axios");
const MonthData = require("../models/MonthData");

router.get("/", (req, res) => {
    res.render("input.ejs"); // replace with your actual prediction panel view filename
});

const ML_URL = "http://127.0.0.1:8080/predict"; // Python ML API

router.post("/", async (req, res) => {
    try {
        const response = await axios.post(ML_URL, req.body);
        const prediction = response.data;

        // Calculate balances
        const accountBalance = prediction.income - prediction.actual_expense;
        const savingsBalance = prediction.income - prediction.predicted_baseline;

        // Save to DB
        const newMonth = new MonthData({
            month: new Date().toLocaleString("default", { month: "long", year: "numeric" }),
            income: prediction.income,
            realExpense: prediction.actual_expense,
            predictedBaseline: prediction.predicted_baseline,
            accountBalance,
            savingsBalance,
            status: prediction.status
        });

        await newMonth.save();

        // Render result page
        res.render("prediction_result", prediction);
    } catch (err) {
        console.error("❌ Error calling ML API:", err.message);
        res.status(500).send("Prediction service failed");
    }
});

module.exports = router;
