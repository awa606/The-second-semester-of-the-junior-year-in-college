"""scripts/eval.py
示例评测脚本：按目录名统计 Top-1 / Top-3 准确率
"""

from pathlib import Path
from io import BytesIO
import json

from PIL import Image
from fastapi.testclient import TestClient

# 假设你的后端入口是 backend.app:app
from backend.app import app

client = TestClient(app)
DATA_ROOT = Path("data/test")
CLASS_MAP = {
    "intact": "完好商品",
    "damaged": "外包装破损商品",
    "empty_box": "空盒商品",
}


def predict_image(image_path: Path):
    with image_path.open("rb") as f:
        response = client.post(
            "/predict",
            files={"file": (image_path.name, f, "image/jpeg")},
        )
    return response.json()


def main():
    total = 0
    top1_hit = 0
    top3_hit = 0
    failures = []

    for folder, expected in CLASS_MAP.items():
        folder_path = DATA_ROOT / folder
        if not folder_path.exists():
            continue
        for image_path in folder_path.glob("*.*"):
            total += 1
            result = predict_image(image_path)
            top3_labels = [item["label"] for item in result["top3"]]
            if result["top1_label"] == expected:
                top1_hit += 1
            else:
                failures.append({
                    "image": str(image_path),
                    "expected": expected,
                    "predicted": result["top1_label"],
                    "top3": result["top3"],
                })
            if expected in top3_labels:
                top3_hit += 1

    if total == 0:
        print("未找到测试图片，请检查 data/test 目录")
        return

    print(f"总样本数: {total}")
    print(f"Top-1 准确率: {top1_hit / total:.2%}")
    print(f"Top-3 准确率: {top3_hit / total:.2%}")

    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/failures.json").write_text(
        json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("失败案例已输出到 outputs/failures.json")


if __name__ == "__main__":
    main()
