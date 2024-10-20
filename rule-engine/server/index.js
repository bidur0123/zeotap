import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import ruleRouter from "./routes/ruleRouter.js";

const app = express();

app.use(
  cors({
    origin: "http://localhost:5173",
    methods: "GET,POST,PUT,DELETE",
    allowedHeaders: "Origin, X-Requested-With, Content-Type, Accept",
  })
);

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Rule Engine API");
});

app.use("/", ruleRouter);

mongoose
  .connect("mongodb://mongo:27017/rule-engine-db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((err) => {
    console.error(err);
  });

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
