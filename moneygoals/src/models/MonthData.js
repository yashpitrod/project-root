const mongoose = require("mongoose");

const monthDataSchema = new mongoose.Schema({
    month: String,
    income: Number,
    house_rent: Number,
    food_costs: Number,
    electricity: Number,
    gas: Number,
    water: Number,
    misc: Number,
    realExpense: Number,
    predictedBaseline: Number,
    accountBalance: Number,
    savingsBalance: Number,
    status: String
}, { timestamps: true });

module.exports = mongoose.model("MonthData", monthDataSchema);
