from uuid import uuid4

from fastapi import APIRouter

from app.schemas import AnswerBody, AskRequest, AskResponse, SourceItem
from app.services.answer_generator import build_answer_from_cards
from app.services.classifier import classify_question
from app.services.retriever import retrieve_cards
from app.services.risk_guard import check_risk, get_default_disclaimer

router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    request_id = f"req_{uuid4().hex[:10]}"
    disclaimer = get_default_disclaimer()

    risk_result = check_risk(payload.question)
    if risk_result:
        print(
            f"DEBUG ask request_id={request_id} question={payload.question!r} "
            f"risk_category={risk_result['category']} matched_rule={risk_result['matched_rule_id']}",
            flush=True,
        )
        return AskResponse(
            request_id=request_id,
            category=risk_result["category"],
            risk_level=risk_result["risk_level"],
            answer=AnswerBody(
                summary=risk_result["message"],
                advice=["请尽快联系医生、药师或线下医疗机构。"],
                warning=["当前问题超出基础育儿助手的安全回答边界。"],
            ),
            sources=[],
            disclaimer=disclaimer,
        )

    category = classify_question(payload.question)
    cards = retrieve_cards(payload.question, category=category, top_k=3)
    hit_card_ids = [card.get("card_id") for card in cards]

    print(
        f"DEBUG ask request_id={request_id} question={payload.question!r} "
        f"category={category} hit_card_ids={hit_card_ids}",
        flush=True,
    )

    result = build_answer_from_cards(cards)

    return AskResponse(
        request_id=request_id,
        category=result["category"],
        risk_level=result["risk_level"],
        answer=AnswerBody(
            summary=result["summary"],
            advice=result["advice"],
            warning=result["warning"],
        ),
        sources=[SourceItem(**source) for source in result["sources"]],
        disclaimer=disclaimer,
    )
