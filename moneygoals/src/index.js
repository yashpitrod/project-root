const express = require("express");
const mongoose = require("mongoose");
const path = require("path");

const predictRoutes = require("./routes/predict.js");
const dashboardRoutes = require("./routes/dashboard.js");

const app = express();
const PORT = process.env.PORT || 4000;
const HOST = process.env.HOST || "0.0.0.0";
const MONGO_URL = process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/moneygoals";

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
app.use(express.static("public"));


// Root
app.get("/", (req, res) => {
    res.render("home");
});

app.get("/predict", (req, res) => {
    res.render("input.ejs");
});

// Connect Mongo + Start server
mongoose.connect(MONGO_URL)
    .then(async () => {
        console.log("✅ MongoDB connected");
        try {
            await mongoose.connection.db.dropDatabase();
            console.log("🧹 MongoDB database cleared on startup");
        } catch (e) {
            console.warn("⚠️ Failed to clear MongoDB database:", e.message);
        }
        app.listen(PORT, HOST, () => {
            console.log(`🚀 Server running at http://${HOST}:${PORT}`);
        });
    })
    .catch(err => console.error("❌ MongoDB connection error:", err));
