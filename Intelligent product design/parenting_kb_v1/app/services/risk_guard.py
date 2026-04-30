import json
from pathlib import Path
from typing import Any, Dict, Optional


RULE_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "red_flags.json"


def load_rules() -> Dict[str, Any]:
    with open(RULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_risk(question: str) -> Optional[Dict[str, Any]]:
    """命中高风险规则时，直接返回拦截结果。"""
    rules = load_rules().get("rules", [])
    for rule in rules:
        for kw in rule.get("keywords", []):
            if kw in question:
                return {
                    "matched_rule_id": rule["rule_id"],
                    "category": rule["category"],
                    "action": rule["action"],
                    "risk_level": rule["risk_level"],
                    "message": rule["message"],
                }
    return None


def get_default_disclaimer() -> str:
    rules = load_rules()
    return rules.get(
        "default_disclaimer",
        "本功能仅提供基础育儿信息参考，不替代医生面诊、诊断和个体化治疗建议。",
    )
