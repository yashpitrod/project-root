const express = require("express");
const router = express.Router();
const MonthData = require("../models/MonthData");

router.get("/", async (req, res) => {
    try {
        const months = await MonthData.find();

        // Calculate totals
        let totalAccountBalance = months.reduce((sum, m) => sum + m.accountBalance, 0);
        let totalSavingsBalance = months.reduce((sum, m) => sum + m.savingsBalance, 0);

        res.render("dashboard", {
            totalAccountBalance,
            totalSavingsBalance,
            months,
        });
    } catch (err) {
        console.error("❌ Error loading dashboard:", err.message);
        res.status(500).send("Dashboard error");
    }
});

module.exports = router;
