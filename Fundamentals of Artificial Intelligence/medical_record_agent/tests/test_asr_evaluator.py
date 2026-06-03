import unittest

from app.services.asr import ASREvaluator


class ASREvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = ASREvaluator()

    def test_same_text_has_zero_cer(self):
        cer, reference_length, distance = self.evaluator.cer("左手肿痛两个小时", "左手肿痛两个小时")

        self.assertEqual(cer, 0)
        self.assertGreater(reference_length, 0)
        self.assertEqual(distance, 0)

    def test_one_wrong_character_has_nonzero_cer(self):
        cer, reference_length, distance = self.evaluator.cer("左手肿痛两个小时", "右手肿痛两个小时")

        self.assertGreater(cer, 0)
        self.assertEqual(distance, 1)
        self.assertGreater(reference_length, 0)

    def test_keyword_recall_is_one_when_all_keywords_hit(self):
        result = self.evaluator.keyword_metrics(
            ["蛇咬伤", "肿痛"],
            "患者左手蛇咬伤后肿痛。",
        )

        self.assertEqual(result["keyword_recall"], 1)
        self.assertEqual(result["missing"], [])

    def test_keyword_recall_reports_missing_keywords(self):
        result = self.evaluator.keyword_metrics(
            ["蛇咬伤", "胸闷"],
            "患者左手蛇咬伤后肿痛。",
        )

        self.assertLess(result["keyword_recall"], 1)
        self.assertEqual(result["missing"], ["胸闷"])


if __name__ == "__main__":
    unittest.main()
