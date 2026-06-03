from __future__ import annotations

import json
import os
import base64
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from app.schemas.asr import ASRResult, ASRSegment


class OnlineASREngine:
    name = "online"

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.api_url = api_url or os.environ.get("ONLINE_ASR_API_URL")
        self.api_key = api_key or os.environ.get("ONLINE_ASR_API_KEY")
        self.timeout_seconds = timeout_seconds
        missing = [
            name
            for name, value in [
                ("ONLINE_ASR_API_URL", self.api_url),
                ("ONLINE_ASR_API_KEY", self.api_key),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Online ASR is not configured. Missing environment variables: "
                f"{', '.join(missing)}. Do not hard-code API keys; set them in the runtime environment."
            )

    def transcribe(self, audio_id: str, audio_path: Path) -> ASRResult:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        payload = {
            "audio_id": audio_id,
            "filename": audio_path.name,
            "audio_base64": base64.b64encode(audio_path.read_bytes()).decode("ascii"),
        }
        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Online ASR request failed: {exc}") from exc

        try:
            data = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Online ASR response is not valid JSON") from exc

        return self._result_from_response(audio_id, data)

    def _result_from_response(self, audio_id: str, data: dict[str, Any]) -> ASRResult:
        text = str(data.get("text") or data.get("transcript") or "")
        conversation_text = str(data.get("conversation_text") or text)
        raw_segments = data.get("segments") if isinstance(data.get("segments"), list) else []
        segments = [
            ASRSegment.model_validate(segment)
            for segment in raw_segments
            if isinstance(segment, dict)
        ]
        if not segments and text:
            segments = [ASRSegment(speaker="online", role=None, text=text)]

        keywords = data.get("medical_keywords")
        if not isinstance(keywords, dict):
            keywords = {"expected": [], "recognized": [], "missing": []}

        return ASRResult(
            audio_id=str(data.get("audio_id") or audio_id),
            engine=str(data.get("engine") or self.name),
            text=text,
            conversation_text=conversation_text,
            segments=segments,
            duration=data.get("duration"),
            medical_keywords={
                "expected": list(keywords.get("expected") or []),
                "recognized": list(keywords.get("recognized") or []),
                "missing": list(keywords.get("missing") or []),
            },
            warnings=list(data.get("warnings") or []),
        )
