from fastapi import APIRouter

from app.schemas import FeedbackRequest

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback")
def submit_feedback(payload: FeedbackRequest):
    # V1: 先直接返回，后续可接 SQLite / 日志文件
    return {
        "status": "received",
        "request_id": payload.request_id,
        "feedback_type": payload.feedback_type,
    }
