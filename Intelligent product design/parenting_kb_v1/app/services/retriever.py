import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from app.services.classifier import normalize_question


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "cards"
EVIDENCE_PATH = DATA_DIR / "knowledge_cards.sample.json"
METADATA_PATHS = [
    DATA_DIR / "knowledge_cards.sample2.json",
    DATA_DIR / "knowledge_cards.expansion.v0.2.json",
]


def _build_card_map(cards: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {card["card_id"]: card for card in cards if "card_id" in card}


def load_cards() -> List[Dict[str, Any]]:
    metadata_cards: List[Dict[str, Any]] = []
    for path in METADATA_PATHS:
        if path.exists():
            metadata_cards.extend(json.loads(path.read_text(encoding="utf-8")))

    evidence_cards = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    evidence_by_id = _build_card_map(evidence_cards)
    merged_cards: List[Dict[str, Any]] = []
    seen_card_ids = set()

    for metadata in metadata_cards:
        card_id = metadata.get("card_id")
        if not card_id or card_id in seen_card_ids:
            continue

        evidence = evidence_by_id.get(card_id, {})
        merged = {**metadata, **evidence}
        if not merged.get("evidence_note"):
            source_titles = [
                source.get("title", "")
                for source in merged.get("source_refs", [])
                if source.get("title")
            ]
            merged["evidence_note"] = [
                "该卡片来自完整知识卡元数据，来源待进一步人工复核。",
                "来源：" + "；".join(source_titles) if source_titles else "来源待补充。",
            ]
        merged_cards.append(merged)
        seen_card_ids.add(card_id)

    return merged_cards


def _iter_search_texts(card: Dict[str, Any]) -> List[str]:
    texts: List[str] = []

    for key in ("title", "subcategory", "answer_summary", "escalation_advice"):
        value = card.get(key)
        if isinstance(value, str) and value:
            texts.append(value)

    for key in ("question_patterns", "answer_points", "do_list", "dont_list", "red_flags", "evidence_note", "age_scope"):
        value = card.get(key, [])
        if isinstance(value, list):
            texts.extend(item for item in value if isinstance(item, str) and item)

    return texts


def score_card(question: str, card: Dict[str, Any]) -> int:
    q = normalize_question(question)
    if not q:
        return 0

    score = 0
    seen_tokens = set()
    raw_q = _compact(question)

    title = normalize_question(card.get("title", ""))
    if title and title in q:
        score += 15

    raw_title = _compact(card.get("title", ""))
    if raw_title and raw_title in raw_q:
        score += 30

    subcategory = normalize_question(card.get("subcategory", ""))
    if subcategory and subcategory in q:
        score += 8

    for pattern in card.get("question_patterns", []):
        raw_pattern = _compact(pattern)
        if raw_pattern and (raw_pattern in raw_q or raw_q in raw_pattern):
            score += 80

        pattern_norm = normalize_question(pattern)
        if not pattern_norm:
            continue
        if pattern_norm in q or q in pattern_norm:
            score += 20
        else:
            overlap = _count_overlap(q, pattern_norm, seen_tokens)
            score += overlap * 4

    for text in _iter_search_texts(card):
        text_norm = normalize_question(text)
        if not text_norm:
            continue
        overlap = _count_overlap(q, text_norm, seen_tokens)
        score += overlap

    return score


def _compact(text: str) -> str:
    text = (text or "").lower().strip()
    text = text.replace("？", "?").replace("，", ",").replace("。", ".")
    return "".join(text.split())


def _count_overlap(question: str, candidate: str, seen_tokens: set[str]) -> int:
    hits = 0
    max_len = min(len(question), 6)

    for size in range(max_len, 1, -1):
        for i in range(len(question) - size + 1):
            token = question[i:i + size]
            if token in seen_tokens:
                continue
            if token and token in candidate:
                seen_tokens.add(token)
                hits += 1

    return hits


def retrieve_cards(question: str, category: str, top_k: int = 3) -> List[Dict[str, Any]]:
    cards = load_cards()
    if category == "unknown":
        return []

    filtered = [card for card in cards if card.get("category") == category]
    scored: List[Tuple[int, Dict[str, Any]]] = []

    for card in filtered:
        score = score_card(question, card)
        if score > 0:
            scored.append((score, card))

    scored.sort(key=lambda item: (item[0], item[1].get("card_id", "")), reverse=True)
    if not scored:
        return []

    best_score = scored[0][0]
    threshold = max(10, best_score // 2)
    narrowed = [card for score, card in scored if score >= threshold]
    return narrowed[:top_k]
