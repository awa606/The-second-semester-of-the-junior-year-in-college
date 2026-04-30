# week5 / project_one / 任务 1

这是一个基于 CLIP 的电商商品质检助手，保持 **零样本图片分类** 方案，不额外训练分类器。系统会对上传图片进行三分类：

- 完好
- 外包装破损
- 空盒

后端使用 FastAPI 运行在模型所在电脑上，前端使用一个最小静态页面，可以在另一台电脑浏览器中上传图片并查看结果。

## 项目结构

```text
Project_One/
├─ backend/
│  ├─ app.py
│  ├─ model_service.py
│  └─ requirements.txt
├─ frontend/
│  └─ index.html
├─ scripts/
│  └─ eval.py
├─ Dataset/
│  ├─ good/
│  ├─ damaged/
│  └─ empty/
├─ clip_model/
└─ requirements.txt
```

## 功能说明

- 使用 `transformers.pipeline("zero-shot-image-classification")`
- 优先加载仓库内的 `clip_model/`，缺失时回退到 `openai/clip-vit-base-patch32`
- 提供 `GET /health` 和 `POST /predict`
- 返回 Top-3 分类结果、Top-1 标签、Top-1 分数和业务建议
- 前端允许手动填写后端地址，方便局域网两台电脑联调

## 安装依赖

建议先创建虚拟环境，然后在 `Project_One` 根目录执行：

```bash
pip install -r requirements.txt
```

## 启动后端

在 `Project_One` 根目录执行：

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

启动后可访问：

- 健康检查：`http://127.0.0.1:8000/health`
- 预测接口：`http://127.0.0.1:8000/predict`

## 打开前端

最简单的方法是直接用浏览器打开 `frontend/index.html`。

如果浏览器对本地 `file://` 页面有跨域限制，可以在 `Project_One` 根目录执行一个静态文件服务：

```bash
python -m http.server 5500
```

然后在浏览器访问：

```text
http://你的前端电脑IP:5500/frontend/index.html
```

## 接口格式

### GET /health

```json
{"status": "ok"}
```

### POST /predict

表单字段：

- `file`: 图片文件

返回示例：

```json
{
  "top1_label": "完好",
  "top1_score": 0.812345,
  "top3": [
    {"label": "完好", "score": 0.812345},
    {"label": "外包装破损", "score": 0.123456},
    {"label": "空盒", "score": 0.064199}
  ],
  "advice": "商品整体完好，建议重新上架。",
  "model_name": "C:/.../clip_model",
  "device": "cpu",
  "filename": "sample.png"
}
```

## 评测脚本

默认会读取：

- `Dataset/good` -> 完好
- `Dataset/damaged` -> 外包装破损
- `Dataset/empty` -> 空盒

运行命令：

```bash
python scripts/eval.py
```

可选参数：

```bash
python scripts/eval.py --dataset-dir Dataset --output eval_report.json
```

脚本会输出：

- Top-1 准确率
- Top-3 准确率
- 失败样本列表
- 完整 JSON 评测报告

## 两台电脑局域网联调

### 电脑 A：运行后端模型

1. 确保电脑 A 和电脑 B 在同一个局域网。
2. 在电脑 A 的 `Project_One` 根目录执行：

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

3. 查看电脑 A 的局域网 IP。
   Windows 可以运行：

```bash
ipconfig
```

找到类似 `192.168.x.x` 的 IPv4 地址。

4. 放行 Windows 防火墙中的 `8000` 端口，至少允许局域网访问。

### 电脑 B：打开前端页面

1. 把 `frontend/index.html` 拷到电脑 B，或者通过共享目录/静态服务访问它。
2. 在浏览器打开页面。
3. 将页面中的“后端地址”填写为：

```text
http://电脑A的局域网IP:8000
```

例如：

```text
http://192.168.1.10:8000
```

4. 上传图片，点击“开始识别”，即可得到结果。

## 课堂演示时可以这样说明

这是一个基于 CLIP 的零样本商品质检助手，没有重新训练分类器，而是通过更贴合业务的提示词完成“完好 / 外包装破损 / 空盒”三分类。模型部署在后端电脑，前端页面可以在局域网另一台电脑中上传图片并实时获取质检结果。
