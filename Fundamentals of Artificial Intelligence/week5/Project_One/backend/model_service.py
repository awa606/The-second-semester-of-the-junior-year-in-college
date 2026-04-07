from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import torch
from PIL import Image
from transformers import pipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_DIR = PROJECT_ROOT / "clip_model"

LABEL_PROMPTS = [
    {
        "label": "完好",
        "prompt": "a photo of an intact returned product with complete packaging, no visible damage, ready for resale",
    },
    {
        "label": "外包装破损",
        "prompt": "a photo of a returned product with damaged outer packaging, crushed box, torn parcel, or visible shipping damage",
    },
    {
        "label": "空盒",
        "prompt": "a photo of an empty product box with the item or accessories missing, only the package remains",
    },
]

PROMPT_TO_LABEL = {item["prompt"]: item["label"] for item in LABEL_PROMPTS}


def _resolve_model_name() -> str:
    """优先使用仓库内的本地 CLIP 模型，缺失时再回退到官方模型名。"""
    env_path = os.getenv("CLIP_MODEL_PATH")
    if env_path:
        return env_path
    if DEFAULT_MODEL_DIR.exists():
        return str(DEFAULT_MODEL_DIR)
    return "openai/clip-vit-base-patch32"


class ClipQualityService:
    """封装 CLIP 零样本分类逻辑，供 API 和评测脚本复用。"""

    def __init__(self) -> None:
        self.device = 0 if torch.cuda.is_available() else -1
        self.model_name = _resolve_model_name()
        self.classifier = pipeline(
            task="zero-shot-image-classification",
            model=self.model_name,
            device=self.device,
        )

    def predict(self, image: Image.Image) -> dict[str, Any]:
        results = self.classifier(
            image,
            candidate_labels=[item["prompt"] for item in LABEL_PROMPTS],
        )
        top3 = [
            {
                "label": PROMPT_TO_LABEL.get(item["label"], item["label"]),
                "score": round(float(item["score"]), 6),
            }
            for item in results[:3]
        ]

        top1 = top3[0]
        advice = self._build_advice(top1["label"], top1["score"])

        return {
            "top1_label": top1["label"],
            "top1_score": top1["score"],
            "top3": top3,
            "advice": advice,
            "model_name": self.model_name,
            "device": "gpu" if self.device == 0 else "cpu",
        }

    @staticmethod
    def _build_advice(label: str, score: float) -> str:
        if score < 0.40:
            return "结果置信度较低，建议人工复核后再决定是否重新上架或退款。"
        if label == "完好" and score >= 0.55:
            return "商品整体完好，建议重新上架。"
        if label == "外包装破损":
            return "检测到外包装破损，建议人工复核或直接退款。"
        if label == "空盒":
            return "疑似空盒或缺件，建议直接退款并保留异常记录。"
        return "结果存在一定不确定性，建议人工复核。"


_service: ClipQualityService | None = None


def get_service() -> ClipQualityService:
    global _service
    if _service is None:
        _service = ClipQualityService()
    return _service
