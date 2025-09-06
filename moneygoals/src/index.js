const express = require("express");
const mongoose = require("mongoose");
const path = require("path");

const predictRoutes = require("./routes/predict.js");
const dashboardRoutes = require("./routes/dashboard.js");

const app = express();
const PORT = process.env.PORT || 4000;
const MONGO_URL = "mongodb://127.0.0.1:27017/moneygoals";

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

// Views setup
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "../views"));


// Routes
app.use("/predict", predictRoutes);
app.use("/dashboard", dashboardRoutes);

// Root
app.get("/", (req, res) => {
    res.render("home");
});

// Connect Mongo + Start server
mongoose.connect(MONGO_URL)
    .then(() => {
        console.log("✅ MongoDB connected");
        app.listen(PORT, () => {
            console.log(`🚀 Server running at http://localhost:${PORT}`);
        });
    })
    .catch(err => console.error("❌ MongoDB connection error:", err));
