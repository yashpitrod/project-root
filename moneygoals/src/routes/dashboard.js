const express = require("express");
const router = express.Router();
const MonthData = require("../models/MonthData");

router.get("/", async (req, res) => {
    try {
        const monthFilter = req.query.month || null;
        const query = monthFilter ? { month: monthFilter } : {};
        const months = await MonthData.find(query);
        const latest = await MonthData.findOne().sort({ createdAt: -1 });

        // Calculate totals
        let totalAccountBalance = months.reduce((sum, m) => sum + m.accountBalance, 0);
        let totalSavingsBalance = months.reduce((sum, m) => sum + m.savingsBalance, 0);

        // All distinct months for filter dropdown
        const distinctMonths = await MonthData.distinct('month');

        res.render("dashboard", {
            totalAccountBalance,
            totalSavingsBalance,
            months,
            latest,
            distinctMonths,
            monthFilter
        });

    } catch (err) {
        console.error("❌ Error loading dashboard:", err.message);
        res.status(500).send("Dashboard error");
    }
});

module.exports = router;
