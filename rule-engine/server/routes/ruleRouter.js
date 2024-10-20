import express from "express";
import {
  createRule,
  evaluateRule,
  updateRule,
  getAllRules,
} from "../controllers/ruleController.js";

const router = express.Router();

router.post("/create_rule", createRule);

router.post("/evaluate_rule", evaluateRule);

router.put("/update_rule", updateRule);

router.get("/rules", getAllRules);

export default router;
