from __future__ import annotations

from app.services.asr.base import ASREngine
from app.services.asr.mock_engine import MockASREngine


def create_asr_engine(engine_name: str = "mock") -> ASREngine:
    normalized_name = (engine_name or "mock").strip().lower()
    if normalized_name == "mock":
        return MockASREngine()
    if normalized_name == "funasr":
        from app.services.asr.funasr_engine import FunASREngine

        return FunASREngine()
    raise ValueError(f"Unsupported ASR engine: {engine_name}. Expected 'mock' or 'funasr'.")
