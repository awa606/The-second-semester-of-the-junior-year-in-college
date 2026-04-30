from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., description="用户问题")
    age_months: Optional[int] = Field(default=None, description="婴幼儿月龄")
    context: Dict[str, Any] = Field(default_factory=dict, description="额外上下文")


class SourceItem(BaseModel):
    title: str
    url: str


class AnswerBody(BaseModel):
    summary: str
    advice: List[str] = Field(default_factory=list)
    warning: List[str] = Field(default_factory=list)


class AskResponse(BaseModel):
    request_id: str
    category: str
    risk_level: str
    answer: AnswerBody
    sources: List[SourceItem] = Field(default_factory=list)
    disclaimer: str


class FeedbackRequest(BaseModel):
    request_id: str
    rating: int = Field(..., ge=0, le=1, description="0=差评, 1=好评")
    feedback_type: str
    comment: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
