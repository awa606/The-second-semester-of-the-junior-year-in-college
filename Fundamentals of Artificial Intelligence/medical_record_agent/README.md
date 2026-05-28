# Medical Record Agent V0.1

基于医患对话文本的门诊病历生成 Agent POC。

V0.1 只使用模拟问诊文本和 mock LLM，不接入真实患者隐私数据、真实医院 HIS/EMR、真实 ASR 或真实 LLM API。AI 只生成草稿，任务正常结束后停在 `WAITING_DOCTOR_REVIEW`，后续医生确认和 Word 导出留给 V0.2。

## 功能范围

- 输入医患对话文本。
- 执行 Prompt 链：字段抽取 -> 草稿生成 -> 安全校验。
- 由 `MedicalRecordOrchestrator` 统一编排状态流转。
- 使用 SSE 推送任务进度。
- 使用 SQLite 记录任务、步骤和审计日志。
- mock LLM 失败时最多重试 2 次，连续失败后进入降级结果。

## 目录结构

```text
medical_record_agent/
  app/
    api/
    agents/
    db/
    prompts/
    schemas/
    services/
    utils/
    main.py
  static/
    index.html
  data/
    medical_record_agent.sqlite3
    outputs/
  tests/
  README.md
  requirements.txt
```

## 安装

```powershell
cd "C:\Users\AWA007\Desktop\Data\school\The second semester of the junior year in college\Fundamentals of Artificial Intelligence\medical_record_agent"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

如果 PowerShell 禁止激活脚本，可以改用：

```bat
.venv\Scripts\activate
```

## 启动

```powershell
uvicorn app.main:app --reload
```

启动后访问：

- API 健康检查：http://127.0.0.1:8000/health
- V0.1 前端：http://127.0.0.1:8000/static/index.html

## 测试

```powershell
python -m unittest discover -s tests
```

## 手动验收

1. 启动 FastAPI。
2. 打开 `http://127.0.0.1:8000/static/index.html`。
3. 使用页面默认蛇咬伤问诊文本，点击“生成病历草稿”。
4. 观察进度依次经过 `CREATED`、`EXTRACTING_FIELDS`、`GENERATING_DRAFT`、`SAFETY_CHECKING`、`WAITING_DOCTOR_REVIEW`。
5. 核对页面显示结构化字段 JSON、病历草稿、安全校验结果和步骤日志。
6. 检查 `data/medical_record_agent.sqlite3` 中 `agent_task`、`agent_task_step`、`audit_log` 是否写入记录。

## V0.1 API

- `POST /api/records/generate`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/steps`
- `GET /api/tasks/{task_id}/events`

## 已知边界

- 暂不做真实语音采集和 ASR。
- 暂不接真实 LLM API。
- 暂不接真实医院 HIS/EMR。
- 暂不使用真实患者隐私数据。
- Word 导出依赖已预留，医生确认后导出流程放到 V0.2。
