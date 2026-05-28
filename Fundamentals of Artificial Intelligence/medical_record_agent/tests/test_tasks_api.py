import os
import tempfile
import unittest

from pathlib import Path
from zipfile import ZipFile

from fastapi import HTTPException

from app.agents import MedicalRecordOrchestrator
from app.api.tasks import (
    ReviewRequest,
    _event_from_audit_log,
    approve_task,
    export_task,
    read_task,
    read_task_steps,
    review_task,
)
from app.db import get_audit_logs
from app.main import app
from app.services import WORD_NOTICE


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["MEDICAL_RECORD_AGENT_DB"] = os.path.join(
            self.temp_dir.name,
            "api.sqlite3",
        )
        os.environ["MEDICAL_RECORD_AGENT_OUTPUT_DIR"] = os.path.join(
            self.temp_dir.name,
            "outputs",
        )

    def tearDown(self):
        os.environ.pop("MEDICAL_RECORD_AGENT_DB", None)
        os.environ.pop("MEDICAL_RECORD_AGENT_OUTPUT_DIR", None)
        self.temp_dir.cleanup()

    def test_task_routes_are_registered(self):
        route_paths = {route.path for route in app.routes}

        self.assertIn("/api/tasks/{task_id}", route_paths)
        self.assertIn("/api/tasks/{task_id}/steps", route_paths)
        self.assertIn("/api/tasks/{task_id}/events", route_paths)
        self.assertIn("/api/records/generate", route_paths)

    def test_read_task_and_steps(self):
        result = MedicalRecordOrchestrator().run_from_text(
            "左手手掌被咬了，大概两个小时左右，用酒精冲洗，牙龈出血。"
        )

        task = read_task(result["task_id"])
        steps = read_task_steps(result["task_id"])

        self.assertEqual(task["id"], result["task_id"])
        self.assertEqual(task["status"], MedicalRecordOrchestrator.STATUS_WAITING_DOCTOR_REVIEW)
        self.assertIsInstance(task["result_json"], dict)
        self.assertIn("draft", task["result_json"])
        self.assertEqual(
            [step["step_name"] for step in steps],
            ["extract_fields", "generate_draft", "safety_check"],
        )

    def test_audit_logs_can_be_mapped_to_sse_events(self):
        result = MedicalRecordOrchestrator().run_from_text(
            "左手手掌被咬了，大概两个小时左右，用酒精冲洗，牙龈出血。"
        )

        events = [
            event
            for event in (_event_from_audit_log(log) for log in get_audit_logs(result["task_id"]))
            if event is not None
        ]
        event_names = [event_name for event_name, _ in events]

        self.assertEqual(event_names[0], "CREATED")
        self.assertIn("EXTRACTING_FIELDS", event_names)
        self.assertIn("GENERATING_DRAFT", event_names)
        self.assertIn("SAFETY_CHECKING", event_names)
        self.assertIn("WAITING_DOCTOR_REVIEW", event_names)
        self.assertEqual(event_names[-1], "WAITING_DOCTOR_REVIEW")

    def test_read_missing_task_returns_404(self):
        with self.assertRaises(HTTPException) as context:
            read_task(999)

        self.assertEqual(context.exception.status_code, 404)

    def test_review_approve_and_export_flow(self):
        result = MedicalRecordOrchestrator().run_from_text(
            "左手手掌被咬了，大概两个小时左右，用酒精冲洗，牙龈出血。"
        )
        task_id = result["task_id"]

        fields = result["fields"]
        fields.chief_complaint.value = "左手手掌被咬伤后肿痛约2小时（医生修订）"
        reviewed = review_task(task_id, ReviewRequest(fields=fields))
        self.assertIn("医生修订", reviewed["result_json"]["fields"]["chief_complaint"]["value"])

        with self.assertRaises(HTTPException) as blocked:
            export_task(task_id)
        self.assertEqual(blocked.exception.status_code, 400)

        approved = approve_task(task_id)
        approved_fields = approved["result_json"]["fields"]
        self.assertTrue(approved_fields["chief_complaint"]["confirmed_by_doctor"])
        self.assertTrue(approved_fields["candidate_diagnoses"][0]["confirmed_by_doctor"])

        exported = export_task(task_id)
        markdown_path = Path(exported["exports"]["markdown_path"])
        word_path = Path(exported["exports"]["word_path"])

        self.assertTrue(markdown_path.exists())
        self.assertTrue(word_path.exists())
        self.assertIn(WORD_NOTICE, markdown_path.read_text(encoding="utf-8"))
        with ZipFile(word_path) as docx:
            document_xml = docx.read("word/document.xml").decode("utf-8")
        self.assertIn(WORD_NOTICE, document_xml)


if __name__ == "__main__":
    unittest.main()
