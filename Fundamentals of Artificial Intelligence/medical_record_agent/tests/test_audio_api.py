import os
import tempfile
import unittest

from fastapi import BackgroundTasks, HTTPException

from app.api.audio import (
    generate_record_from_audio,
    read_audio_transcript,
    transcribe_audio,
    upload_audio,
)
from app.api.tasks import read_task
from app.main import app


class FakeUploadFile:
    filename = "sample.wav"

    def __init__(self, content: bytes):
        self.file = tempfile.SpooledTemporaryFile()
        self.file.write(content)
        self.file.seek(0)

    def close(self):
        self.file.close()


class AudioApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["MEDICAL_RECORD_AGENT_DB"] = os.path.join(
            self.temp_dir.name,
            "audio.sqlite3",
        )
        os.environ["MEDICAL_RECORD_AGENT_UPLOAD_DIR"] = os.path.join(
            self.temp_dir.name,
            "uploads",
        )

    def tearDown(self):
        os.environ.pop("MEDICAL_RECORD_AGENT_DB", None)
        os.environ.pop("MEDICAL_RECORD_AGENT_UPLOAD_DIR", None)
        self.temp_dir.cleanup()

    def test_audio_routes_are_registered(self):
        route_paths = {route.path for route in app.routes}

        self.assertIn("/api/audio/upload", route_paths)
        self.assertIn("/api/audio/{audio_id}/transcribe", route_paths)
        self.assertIn("/api/audio/{audio_id}/transcript", route_paths)
        self.assertIn("/api/audio/{audio_id}/generate-record", route_paths)

    def test_upload_transcribe_and_read_transcript(self):
        fake_file = FakeUploadFile(b"RIFF....WAVEfmt ")
        try:
            uploaded = upload_audio(fake_file)
        finally:
            fake_file.close()

        self.assertEqual(uploaded.status, "uploaded")
        self.assertTrue(os.path.exists(uploaded.path))

        transcribed = transcribe_audio(uploaded.audio_id)
        asr_result = transcribed["asr_result"]

        self.assertEqual(transcribed["status"], "completed")
        self.assertIn("蛇咬伤", asr_result["text"])
        self.assertIn("[医生]", asr_result["conversation_text"])
        self.assertEqual(asr_result["medical_keywords"]["missing"], [])

        transcript = read_audio_transcript(uploaded.audio_id)
        self.assertEqual(transcript.audio_id, uploaded.audio_id)
        self.assertIn("[患者]", transcript.conversation_text)

    def test_generate_record_from_audio_requires_transcript(self):
        fake_file = FakeUploadFile(b"RIFF....WAVEfmt ")
        try:
            uploaded = upload_audio(fake_file)
        finally:
            fake_file.close()

        with self.assertRaises(HTTPException) as context:
            generate_record_from_audio(uploaded.audio_id, BackgroundTasks())

        self.assertEqual(context.exception.status_code, 404)

    def test_generate_record_from_audio_creates_text_task(self):
        fake_file = FakeUploadFile(b"RIFF....WAVEfmt ")
        try:
            uploaded = upload_audio(fake_file)
        finally:
            fake_file.close()
        transcribe_audio(uploaded.audio_id)

        response = generate_record_from_audio(uploaded.audio_id, BackgroundTasks())

        self.assertIsInstance(response["task_id"], int)
        self.assertEqual(response["status"], "CREATED")
        task = read_task(response["task_id"])
        self.assertEqual(task["status"], "CREATED")
        self.assertIn("[医生]", task["input_text"])


if __name__ == "__main__":
    unittest.main()
