from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ASRSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    speaker: str | None = None
    role: str | None = None
    text: str
    start_time: float | None = None
    end_time: float | None = None
    confidence: float | None = None


class ASRResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audio_id: str
    engine: str
    text: str
    conversation_text: str
    segments: list[ASRSegment]
    duration: float | None = None
    medical_keywords: dict[str, list[str]] | None = None


class AudioRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audio_id: str
    filename: str
    path: str
    status: str
