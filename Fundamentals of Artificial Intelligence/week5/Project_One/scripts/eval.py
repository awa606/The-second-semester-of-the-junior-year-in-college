from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.model_service import get_service  # noqa: E402


CLASS_DIR_TO_LABEL = {
    "good": "完好",
    "damaged": "外包装破损",
    "empty": "空盒",
}

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def iter_samples(dataset_dir: Path):
    for class_dir_name, expected_label in CLASS_DIR_TO_LABEL.items():
        class_dir = dataset_dir / class_dir_name
        if not class_dir.exists():
            continue
        for image_path in sorted(class_dir.iterdir()):
            if image_path.is_file() and image_path.suffix.lower() in IMAGE_SUFFIXES:
                yield image_path, expected_label


def evaluate(dataset_dir: Path) -> dict:
    service = get_service()
    samples = list(iter_samples(dataset_dir))
    if not samples:
        raise FileNotFoundError(f"未在 {dataset_dir} 下找到可评测图片。")

    top1_hits = 0
    top3_hits = 0
    details = []
    failures = []

    for image_path, expected_label in samples:
        with Image.open(image_path).convert("RGB") as image:
            prediction = service.predict(image)

        top3_labels = [item["label"] for item in prediction["top3"]]
        top1_label = prediction["top1_label"]

        top1_ok = top1_label == expected_label
        top3_ok = expected_label in top3_labels

        if top1_ok:
            top1_hits += 1
        if top3_ok:
            top3_hits += 1
        if not top1_ok:
            failures.append(
                {
                    "file": str(image_path.relative_to(PROJECT_ROOT)),
                    "expected": expected_label,
                    "predicted": top1_label,
                    "top3": prediction["top3"],
                }
            )

        details.append(
            {
                "file": str(image_path.relative_to(PROJECT_ROOT)),
                "expected": expected_label,
                "top1_label": top1_label,
                "top1_score": prediction["top1_score"],
                "top3": prediction["top3"],
                "top1_correct": top1_ok,
                "top3_correct": top3_ok,
            }
        )

    total = len(samples)
    return {
        "dataset_dir": str(dataset_dir),
        "total_samples": total,
        "top1_accuracy": round(top1_hits / total, 4),
        "top3_accuracy": round(top3_hits / total, 4),
        "details": details,
        "failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="评测 CLIP 零样本商品质检模型。")
    parser.add_argument(
        "--dataset-dir",
        default=str(PROJECT_ROOT / "Dataset"),
        help="数据集根目录，默认使用 Project_One/Dataset",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "eval_report.json"),
        help="评测结果 JSON 输出路径",
    )
    args = parser.parse_args()

    report = evaluate(Path(args.dataset_dir))
    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"总样本数: {report['total_samples']}")
    print(f"Top-1 准确率: {report['top1_accuracy']:.2%}")
    print(f"Top-3 准确率: {report['top3_accuracy']:.2%}")
    print(f"失败样本数: {len(report['failures'])}")
    print(f"评测报告已写入: {output_path}")


if __name__ == "__main__":
    main()
