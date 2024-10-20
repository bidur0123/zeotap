import Rule from "../models.js";
import { Engine } from "json-rules-engine";

const parseCondition = (conditionString) => {
  const match = conditionString.match(/(\w+)\s*(>|<|=)\s*([^\s]+)/);
  if (match) {
    let operator;
    switch (match[2]) {
      case ">":
        operator = "greaterThan";
        break;
      case "<":
        operator = "lessThan";
        break;
      case "=":
        operator = "equal";
        break;
      default:
        throw new Error(`Unknown operator: ${match[2]}`);
    }

    const cleanValue = match[3].replace(/[()]/g, "");
    return {
      fact: match[1],
      operator: operator,
      value: isNaN(cleanValue)
        ? cleanValue.replace(/['"]/g, "")
        : Number(cleanValue),
    };
  }
  throw new Error("Invalid condition: " + conditionString);
};

const create_rule = (ruleString) => {
  const buildConditions = (rule) => {
    const orParts = rule.split(/\sOR\s/i);
    if (orParts.length > 1) {
      return {
        any: orParts.map((orPart) => buildConditions(orPart)),
      };
    }

    const andParts = rule.split(/\sAND\s/i);
    if (andParts.length > 1) {
      return {
        all: andParts.map((andPart) => parseCondition(andPart)),
      };
    }

    return parseCondition(rule.trim());
  };

  return {
    conditions: buildConditions(ruleString),
    event: {
      type: "eligibility",
      params: {
        message: "The user is eligible.",
      },
    },
  };
};

export const createRule = async (req, res) => {
  const { ruleString } = req.body;

  try {
    const ast = create_rule(ruleString);

    const rule = new Rule({ ruleString, ast });
    await rule.save();

    res.json({ rule });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

export const evaluateRule = async (req, res) => {
  const { ruleId, data } = req.body;

  const ruleDoc = await Rule.findById(ruleId);
  if (!ruleDoc) {
    return res.status(404).json({ error: "Rule not found" });
  }

  if (!ruleDoc.ast || !ruleDoc.ast.event || !ruleDoc.ast.conditions) {
    return res.status(400).json({
      error: "Rule is missing the required 'conditions' or 'event' properties",
    });
  }

  const engine = new Engine();

  try {
    engine.addRule(ruleDoc.ast);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }

  engine
    .run(data)
    .then(({ events }) => {
      if (events.length > 0) {
        res.json({ eligible: true });
      } else {
        res.json({ eligible: false });
      }
    })
    .catch((err) => {
      res.status(500).json({ error: err.message });
    });
};

export const updateRule = async (req, res) => {
  const { ruleId, ruleString } = req.body;

  try {
    const ast = create_rule(ruleString);

    const updatedRule = await Rule.findByIdAndUpdate(
      ruleId,
      { ruleString, ast },
      { new: true }
    );

    if (!updatedRule) {
      return res.status(404).json({ error: "Rule not found" });
    }

    res.json({ rule: updatedRule });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

export const getAllRules = async (req, res) => {
  try {
    const rules = await Rule.find({});
    res.json(rules);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
