import unittest

from app.schemas.asr import ASRResult, ASRSegment
from app.services.asr.role_strategy import apply_manifest_role_strategy


class ASRRoleStrategyTests(unittest.TestCase):
    def test_single_speaker_script_split_restores_doctor_patient_turns(self):
        result = ASRResult(
            audio_id="snakebite_01",
            engine="mock",
            text="你好，哪里不舒服？我是左手手掌被咬了。现在什么感受？感觉这里有点肿痛。",
            conversation_text="",
            segments=[],
        )

        restored = apply_manifest_role_strategy(result, "snakebite_01")

        self.assertEqual(restored.role_strategy, "single_speaker_script_split")
        self.assertFalse(restored.evaluate_diarization)
        self.assertIn("[医生]", restored.conversation_text)
        self.assertIn("[患者]", restored.conversation_text)
        self.assertIn("肿痛", restored.medical_keywords["recognized"])

    def test_manual_speaker_role_map_assigns_roles(self):
        result = ASRResult(
            audio_id="chest_pain_01",
            engine="mock",
            text="哪里不舒服？胸痛。",
            conversation_text="",
            segments=[
                ASRSegment(speaker="spk0", text="哪里不舒服？"),
                ASRSegment(speaker="spk1", text="胸痛。"),
            ],
        )

        mapped = apply_manifest_role_strategy(result, "chest_pain_01")

        self.assertEqual(mapped.role_strategy, "manual_speaker_role_map")
        self.assertTrue(mapped.evaluate_diarization)
        self.assertEqual(mapped.segments[0].role, "医生")
        self.assertEqual(mapped.segments[1].role, "患者")
        self.assertIn("[医生]", mapped.conversation_text)
        self.assertIn("[患者]", mapped.conversation_text)


if __name__ == "__main__":
    unittest.main()
