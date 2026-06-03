import unittest

from app.services.asr import MockASREngine, create_asr_engine


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


if __name__ == "__main__":
    unittest.main()
