from collections import Counter

from fastapi import APIRouter

from app.services.retriever import load_cards

router = APIRouter(prefix='/api', tags=['coverage'])


@router.get('/coverage')
def get_coverage() -> dict:
    cards = load_cards()
    counts = Counter(card.get('category', 'unknown') for card in cards)
    return {
        'total_cards': len(cards),
        'categories': dict(sorted(counts.items())),
    }
