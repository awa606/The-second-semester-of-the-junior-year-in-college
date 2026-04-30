import json
import sys
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.services.classifier import classify_question
from app.services.retriever import load_cards, retrieve_cards


REQUIRED_FIELDS = [
    "card_id",
    "category",
    "subcategory",
    "title",
    "question_patterns",
    "answer_summary",
    "answer_points",
    "red_flags",
    "escalation_advice",
    "source_refs",
    "evidence_note",
    "review_status",
    "updated_at",
]


def main() -> int:
    cards = load_cards()
    failures = []
    category_counter = Counter(card.get("category") for card in cards)

    seen = set()
    for card in cards:
        card_id = card.get("card_id")
        if card_id in seen:
            failures.append(f"duplicate card_id: {card_id}")
        seen.add(card_id)

        missing = [field for field in REQUIRED_FIELDS if not card.get(field)]
        if missing:
            failures.append(f"{card_id}: missing fields {missing}")

        patterns = card.get("question_patterns") or []
        if not isinstance(patterns, list) or not patterns:
            failures.append(f"{card_id}: question_patterns must be a non-empty list")
            continue

        question = patterns[0]
        category = classify_question(question)
        hits = retrieve_cards(question, category=category, top_k=3)
        hit_ids = [hit.get("card_id") for hit in hits]

        print(
            json.dumps(
                {
                    "card_id": card_id,
                    "question": question,
                    "classified": category,
                    "expected": card.get("category"),
                    "hits": hit_ids,
                },
                ensure_ascii=False,
            )
        )

        if category != card.get("category"):
            failures.append(
                f"{card_id}: classified as {category}, expected {card.get('category')}"
            )

        if card_id not in hit_ids:
            failures.append(f"{card_id}: did not retrieve itself, hits={hit_ids}")

    print("summary:", json.dumps(category_counter, ensure_ascii=False))
    print("cards:", len(cards))

    if failures:
        print("failures:")
        for failure in failures:
            print("-", failure)
        return 1

    print("validation: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
