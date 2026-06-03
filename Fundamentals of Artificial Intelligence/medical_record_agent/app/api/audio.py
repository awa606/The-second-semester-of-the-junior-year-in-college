from __future__ import annotations

import json
import os
import shutil
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.agents import MedicalRecordOrchestrator
from app.api.records import run_record_generation_task
from app.schemas import ASRResult, AudioRecord
from app.services.asr import MockASREngine


router = APIRouter(prefix="/audio", tags=["audio"])

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"
ALLOWED_AUDIO_EXTENSIONS = {".wav", ".mp3"}


def get_upload_dir() -> Path:
    return Path(os.environ.get("MEDICAL_RECORD_AGENT_UPLOAD_DIR", DEFAULT_UPLOAD_DIR))


def _safe_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only wav/mp3 audio files are supported")
    return extension


def _audio_path(audio_id: str) -> Path:
    upload_dir = get_upload_dir()
    matches = list(upload_dir.glob(f"{audio_id}.*"))
    audio_matches = [
        path for path in matches if path.suffix.lower() in ALLOWED_AUDIO_EXTENSIONS
    ]
    if not audio_matches:
        raise HTTPException(status_code=404, detail="Audio not found")
    return audio_matches[0]


def _transcript_path(audio_id: str) -> Path:
    return get_upload_dir() / f"{audio_id}.transcript.json"


def _write_transcript(result: ASRResult) -> None:
    path = _transcript_path(result.audio_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _read_transcript(audio_id: str) -> ASRResult:
    path = _transcript_path(audio_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Transcript not found")
    return ASRResult.model_validate_json(path.read_text(encoding="utf-8"))


@router.post("/upload")
def upload_audio(file: UploadFile = File(...)) -> AudioRecord:
    extension = _safe_extension(file.filename or "")
    upload_dir = get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    audio_id = uuid.uuid4().hex
    filename = f"{audio_id}{extension}"
    destination = upload_dir / filename
    with destination.open("wb") as output:
        shutil.copyfileobj(file.file, output)

    return AudioRecord(
        audio_id=audio_id,
        filename=file.filename or filename,
        path=str(destination),
        status="uploaded",
    )


@router.post("/{audio_id}/transcribe")
def transcribe_audio(audio_id: str) -> dict[str, Any]:
    audio_path = _audio_path(audio_id)
    result = MockASREngine().transcribe(audio_id, audio_path)
    _write_transcript(result)
    return {
        "audio_id": audio_id,
        "status": "completed",
        "asr_result": result.model_dump(),
    }


@router.get("/{audio_id}/transcript")
def read_audio_transcript(audio_id: str) -> ASRResult:
    return _read_transcript(audio_id)


@router.post("/{audio_id}/generate-record")
def generate_record_from_audio(
    audio_id: str,
    background_tasks: BackgroundTasks,
) -> dict[str, object]:
    result = _read_transcript(audio_id)
    orchestrator = MedicalRecordOrchestrator()
    task_id = orchestrator.create_text_task(result.conversation_text)
    background_tasks.add_task(
        run_record_generation_task,
        task_id,
        result.conversation_text,
    )

    return {
        "task_id": task_id,
        "status": MedicalRecordOrchestrator.STATUS_CREATED,
        "events_url": f"/api/tasks/{task_id}/events",
    }
