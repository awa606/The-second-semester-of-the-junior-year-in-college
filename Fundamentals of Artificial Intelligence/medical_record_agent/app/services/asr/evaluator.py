from __future__ import annotations

import re

from app.schemas.asr import ASREvaluationResult


PUNCTUATION_PATTERN = re.compile(r"[\s，。！？、；：,.!?;:\-—（）()《》<>\"'“”‘’\[\]【】]+")


class ASREvaluator:
    def normalize_text(self, text: str) -> str:
        return PUNCTUATION_PATTERN.sub("", text or "")

    def edit_distance(self, reference: str, hypothesis: str) -> int:
        ref = self.normalize_text(reference)
        hyp = self.normalize_text(hypothesis)
        if not ref:
            return len(hyp)
        if not hyp:
            return len(ref)

        previous = list(range(len(hyp) + 1))
        for i, ref_char in enumerate(ref, start=1):
            current = [i]
            for j, hyp_char in enumerate(hyp, start=1):
                cost = 0 if ref_char == hyp_char else 1
                current.append(
                    min(
                        previous[j] + 1,
                        current[j - 1] + 1,
                        previous[j - 1] + cost,
                    )
                )
            previous = current
        return previous[-1]

    def cer(self, reference: str, hypothesis: str) -> tuple[float, int, int]:
        normalized_reference = self.normalize_text(reference)
        reference_length = len(normalized_reference)
        distance = self.edit_distance(reference, hypothesis)
        if reference_length == 0:
            return (0.0 if distance == 0 else 1.0, reference_length, distance)
        return distance / reference_length, reference_length, distance

    def keyword_metrics(
        self,
        expected_keywords: list[str],
        recognized_text: str,
    ) -> dict[str, object]:
        expected = list(dict.fromkeys(keyword.strip() for keyword in expected_keywords if keyword.strip()))
        normalized_text = self.normalize_text(recognized_text)
        recognized = [
            keyword
            for keyword in expected
            if self.normalize_text(keyword) in normalized_text
        ]
        missing = [keyword for keyword in expected if keyword not in recognized]
        recall = len(recognized) / len(expected) if expected else 0.0
        return {
            "expected": expected,
            "recognized": recognized,
            "missing": missing,
            "keyword_recall": recall,
        }

    def evaluate(
        self,
        *,
        audio_id: str,
        engine: str,
        ground_truth_text: str,
        recognized_text: str,
        expected_keywords: list[str],
    ) -> ASREvaluationResult:
        cer_value, reference_length, distance = self.cer(ground_truth_text, recognized_text)
        keyword_result = self.keyword_metrics(expected_keywords, recognized_text)
        return ASREvaluationResult(
            audio_id=audio_id,
            engine=engine,
            cer=cer_value,
            reference_length=reference_length,
            edit_distance=distance,
            keyword_recall=float(keyword_result["keyword_recall"]),
            medical_keywords={
                "expected": keyword_result["expected"],
                "recognized": keyword_result["recognized"],
                "missing": keyword_result["missing"],
            },
        )
