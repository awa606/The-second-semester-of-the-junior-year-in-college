# 本地验证指南（v0.2.5）

请按下面顺序执行，避免“测试脚本先跑但服务未启动”的误报。

1. 激活虚拟环境

```powershell
.\.venv\Scripts\Activate.ps1
```

2. 先验证知识库结构、分类与检索

```powershell
python scripts\validate_kb.py
```

3. 启动 FastAPI 服务

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

4. 浏览器打开首页

```text
http://127.0.0.1:8000/
```

5. 另开终端运行 API 冒烟测试

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\powershell\TEST_COMMANDS.ps1
```

## 预期行为

- 若服务未启动，`TEST_COMMANDS.ps1` 会先检查 `GET /api/health`，并提示：
  `请先运行 uvicorn app.main:app --host 127.0.0.1 --port 8000`。
- 若服务已启动，脚本会逐条输出 `category`、`risk_level`、`summary`、`sources` 数量和 `hit_card_ids`。
