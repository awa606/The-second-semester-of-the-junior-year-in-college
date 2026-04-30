from fastapi import APIRouter, HTTPException

from app.services.retriever import load_cards

router = APIRouter(prefix="/api", tags=["sources"])


@router.get("/sources/{doc_id}")
def get_source(doc_id: str):
    cards = load_cards()
    for card in cards:
        for src in card.get("source_refs", []):
            if src.get("doc_id") == doc_id:
                return src
    raise HTTPException(status_code=404, detail="source not found")
