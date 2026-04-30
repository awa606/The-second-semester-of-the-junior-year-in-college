"""兼容课程模板的启动入口。

保留零样本 CLIP 方案，不再使用 Gradio 单体页面。
运行本文件会启动 FastAPI 后端，前端请打开 frontend/index.html。
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=False)
