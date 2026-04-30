"""backend/app.py
后端服务：本机加载 CLIP，提供给另一台电脑前端调用
"""

from io import BytesIO
from typing import List, Dict

import torch
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from transformers import pipeline

app = FastAPI(title="Task1 E-commerce Quality Inspector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = 0 if torch.cuda.is_available() else -1
LABELS = [
    "a photo of an intact returned product with complete packaging",
    "a photo of a returned product with damaged outer packaging",
    "a photo of an empty box missing the product or accessories",
]
LABEL_ALIAS = {
    LABELS[0]: "完好商品",
    LABELS[1]: "外包装破损商品",
    LABELS[2]: "空盒商品",
}

classifier = pipeline(
    task="zero-shot-image-classification",
    model="openai/clip-vit-base-patch32",
    device=DEVICE,
)


def build_advice(top_label: str, top_score: float) -> str:
    if top_score < 0.40:
        return "⚠️ 结果不稳定，建议人工复核"
    if top_label == "完好商品" and top_score >= 0.55:
        return f"✅ 商品完好，建议重新上架（置信度 {top_score:.1%}）"
    if top_label == "外包装破损商品":
        return f"❌ 包装异常，建议人工复核或直接退款（置信度 {top_score:.1%}）"
    if top_label == "空盒商品":
        return f"❌ 疑似空盒或缺件，建议直接退款（置信度 {top_score:.1%}）"
    return f"⚠️ 建议人工复核（置信度 {top_score:.1%}）"


def predict_pil(image: Image.Image) -> Dict:
    results = classifier(image, candidate_labels=LABELS)
    top3: List[Dict] = []
    for item in results[:3]:
        cn_label = LABEL_ALIAS.get(item["label"], item["label"])
        top3.append({"label": cn_label, "score": round(float(item["score"]), 4)})

    top1_label = top3[0]["label"]
    top1_score = top3[0]["score"]
    return {
        "top1_label": top1_label,
        "top1_score": top1_score,
        "top3": top3,
        "advice": build_advice(top1_label, top1_score),
    }


@app.get("/health")
def health():
    return {"status": "ok", "device": "gpu" if DEVICE == 0 else "cpu"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return predict_pil(image)
