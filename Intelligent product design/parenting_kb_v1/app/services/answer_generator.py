from typing import Any, Dict, List


def build_answer_from_cards(cards: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not cards:
        return {
            "summary": "当前知识卡中没有命中这个问题，暂时不提供推测性回答。",
            "advice": ["请换一种更具体的问法，或补充宝宝月龄、主要症状和持续时间。"],
            "warning": ["本系统只在命中相关知识卡时返回基础育儿建议。"],
            "sources": [],
            "category": "unknown",
            "risk_level": "unknown",
        }

    first = cards[0]
    summary = first.get("answer_summary") or "已命中相关知识卡。"
    advice = list(first.get("answer_points", []))[:3]
    warning = []

    escalation_advice = first.get("escalation_advice")
    if escalation_advice:
        warning.append(escalation_advice)

    for red_flag in first.get("red_flags", [])[:2]:
        warning.append(f"如出现{red_flag}，应尽快线下评估。")

    sources = []
    seen = set()
    for card in cards:
        for src in card.get("source_refs", []):
            key = (src.get("title", ""), src.get("url", ""))
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                {
                    "title": src.get("title", "未知来源"),
                    "url": src.get("url", ""),
                }
            )

    return {
        "summary": summary,
        "advice": advice,
        "warning": warning,
        "sources": sources,
        "category": first.get("category", "unknown"),
        "risk_level": "medium" if first.get("category") == "symptom_triage" else "low",
    }
