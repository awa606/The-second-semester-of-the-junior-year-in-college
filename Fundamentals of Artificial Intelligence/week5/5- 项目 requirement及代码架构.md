
一、5个项目的 requirements.txt


# CLIP 零样本图像分类课程项目
# 适用：项目1~5 全部通用
# Python 版本：3.10
# 最后更新：2026-03

# 核心 AI 框架
torch==2.2.1
transformers==4.38.1

# Web 交互界面
gradio==4.20.0

# 图片处理
Pillow==10.2.0
```

安装命令（在服务器上执行）：

```bash
pip install -r requirements.txt
```
***

二、5个项目通用代码架构

每个项目的代码都由以下**6个固定模块**组成，本课程只需要修改标注 ✏️ 的部分：

```
app.py
│
├── 【模块1】硬件检测          ← 固定不动，复制粘贴
│   └── 自动检测 GPU/CPU
│
├── 【模块2】模型加载          ← 固定不动，复制粘贴
│   └── 加载 CLIP 模型
│
├── 【模块3】标签词表  ✏️      ← 核心工作！反复修改优化
│   └── LABELS = ["...", "...", "..."]
│
├── 【模块4】推理函数          ← 固定不动，复制粘贴
│   └── 调用 CLIP，输出概率字典
│
├── 【模块5】告警逻辑  ✏️      ← 本课程需要根据业务场景自定义
│   └── if "破损" in top_label → 触发告警
│
└── 【模块6】Gradio 界面 ✏️   ← 本课程可以调整界面文字和布局
    └── demo.launch(port=786x)
```



三、本课程的"代码模板"

这是一份**通用脚手架**，本课程只需要填写 `✏️ 修改这里` 的部分，其余全部复制粘贴即可：

```python
# ============================================================
# CLIP 零样本图像分类 - 通用项目模板
# 本课程只需修改：LABELS、告警逻辑、界面文字、端口号
# ============================================================

import torch
import gradio as gr
from transformers import pipeline

# ---- 模块1：硬件检测（固定不动）----
device = 0 if torch.cuda.is_available() else -1
print(f"✅ 当前设备：{'GPU' if device == 0 else 'CPU'}")

# ---- 模块2：模型加载（固定不动）----
print("⏳ 加载 CLIP 模型中...")
classifier = pipeline(
    task="zero-shot-image-classification",
    model="openai/clip-vit-base-patch32",
    device=device
)
print("✅ 模型加载完成！")

# ---- 模块3：标签词表 ✏️ 修改这里 ----
LABELS = [
    "第一个标签描述",    # 替换成项目的业务标签
    "第二个标签描述",
    "第三个标签描述",
]

# ---- 模块4：推理函数（固定不动）----
def predict(image):
    if image is None:
        return None, "请先上传图片"
    results = classifier(image, candidate_labels=LABELS)
    output_dict = {res["label"]: res["score"] for res in results}
    top_label = results[0]["label"]
    top_score = results[0]["score"]

    # ---- 模块5：告警逻辑 ✏️ 修改这里 ----
    if "你的告警关键词" in top_label and top_score > 0.5:
        alert = f"🚨 告警！检测到{top_label}（确信度{top_score:.1%}）"
    else:
        alert = f"✅ 正常（确信度{top_score:.1%}）"

    return output_dict, alert

# ---- 模块6：Gradio 界面 ✏️ 修改这里 ----

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ✏️ 填写你的项目标题")
    gr.Markdown("✏️ 填写你的项目功能说明")

    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="上传图片")
            btn = gr.Button("开始识别", variant="primary")
        with gr.Column():
            label_output = gr.Label(num_top_classes=3, label="Top-3 预测结果")
            alert_output = gr.Textbox(label="系统建议", lines=3)

    btn.click(fn=predict, inputs=img_input, outputs=[label_output, alert_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=786x)  # ✏️ 改成你自己端口号
```

***

本课程需要大家把100%的精力放在标签工程和业务分析上，而不是在搞清楚代码结构上浪费时间。

