import unittest
from unittest.mock import patch

from app.services.asr import MockASREngine, OnlineASREngine, create_asr_engine


class ASRFactoryTests(unittest.TestCase):
    def test_create_mock_engine(self):
        engine = create_asr_engine("mock")

        self.assertIsInstance(engine, MockASREngine)
        self.assertEqual(engine.name, "mock-asr-v0.2")

    def test_create_default_engine_is_mock(self):
        engine = create_asr_engine()

        self.assertIsInstance(engine, MockASREngine)

    def test_unknown_engine_raises_clear_error(self):
        with self.assertRaises(ValueError) as context:
            create_asr_engine("unknown")

        self.assertIn("Unsupported ASR engine", str(context.exception))
        self.assertIn("mock", str(context.exception))
        self.assertIn("funasr", str(context.exception))
        self.assertIn("online", str(context.exception))

    def test_online_engine_requires_environment(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError) as context:
                create_asr_engine("online")

        self.assertIn("ONLINE_ASR_API_URL", str(context.exception))
        self.assertIn("ONLINE_ASR_API_KEY", str(context.exception))

    def test_create_online_engine_from_environment(self):
        with patch.dict(
            "os.environ",
            {
                "ONLINE_ASR_API_URL": "https://asr.example.test/transcribe",
                "ONLINE_ASR_API_KEY": "test-key-from-env",
            },
            clear=True,
        ):
            engine = create_asr_engine("online")

        self.assertIsInstance(engine, OnlineASREngine)
        self.assertEqual(engine.name, "online")

    def test_online_engine_response_maps_to_asr_result(self):
        engine = OnlineASREngine(
            api_url="https://asr.example.test/transcribe",
            api_key="test-key-from-env",
        )

        result = engine._result_from_response(
            "audio-1",
            {
                "text": "发热三天",
                "conversation_text": "[待校正] 发热三天",
                "segments": [{"speaker": "spk0", "text": "发热三天"}],
                "medical_keywords": {
                    "expected": ["发热"],
                    "recognized": ["发热"],
                    "missing": [],
                },
            },
        )

        self.assertEqual(result.audio_id, "audio-1")
        self.assertEqual(result.engine, "online")
        self.assertEqual(result.text, "发热三天")
        self.assertEqual(result.segments[0].speaker, "spk0")
        self.assertEqual(result.medical_keywords["recognized"], ["发热"])


if __name__ == "__main__":
    unittest.main()
