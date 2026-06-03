# Medical Record Agent V0.2

基于医患对话文本和 Mock ASR 的门诊病历生成 Agent POC。

V0.2 在 V0.1 文本生成病历链路基础上，增加三入口 UI、预录音频上传、Mock ASR 转写测试链路，以及“音频 -> Mock ASR -> 病历生成”的端到端测试链路。当前版本仍不接入真实患者隐私数据、真实医院 HIS/EMR、真实 FunASR 或真实 LLM API。

## V0.2 功能范围

- 从文本生成病历：复用 V0.1 `/api/records/generate` 和 SSE 任务进度。
- 上传预录音频测试转写：上传 wav/mp3，调用 Mock ASR，展示转写文本、segments 和关键词命中情况。
- 上传预录音频生成病历：先 Mock ASR，再使用 `conversation_text` 进入现有病历 Agent 主链路。
- 新增 ASR schema：`ASRSegment`、`ASRResult`、`AudioRecord`。
- 新增 ASR 引擎抽象和 `MockASREngine`，为后续替换 FunASR 预留接口。
- 新增流程文档 `docs/flow_v0_2.md`。

## 目录结构

```text
medical_record_agent/
  app/
    api/
      audio.py
      records.py
      tasks.py
    agents/
    db/
    prompts/
    schemas/
      asr.py
      medical_record.py
      task.py
    services/
      asr/
        base.py
        mock_engine.py
      mock_llm.py
    main.py
  static/
    index.html
  data/
    uploads/
      .gitkeep
    outputs/
      .gitkeep
  docs/
    flow_v0_2.md
  tests/
  README.md
  requirements.txt
```

## 安装

```powershell
cd "C:\Users\AWA007\The-second-semester-of-the-junior-year-in-college\Fundamentals of Artificial Intelligence\medical_record_agent"
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
- V0.2 前端：http://127.0.0.1:8000/static/index.html

## V0.2 API

文本病历生成：

- `POST /api/records/generate`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/steps`
- `GET /api/tasks/{task_id}/events`

音频与 Mock ASR：

- `POST /api/audio/upload`
- `POST /api/audio/{audio_id}/transcribe`
- `GET /api/audio/{audio_id}/transcript`
- `POST /api/audio/{audio_id}/generate-record`

## 测试

```powershell
python -m unittest discover -s tests
```

## V0.2 手动验收

1. 启动 FastAPI。
2. 打开 `http://127.0.0.1:8000/static/index.html`。
3. 确认页面有三个入口：
   - 从文本生成病历
   - 上传预录音频测试转写
   - 上传预录音频生成病历
4. 使用默认蛇咬伤问诊文本，点击“从文本生成病历”，确认进度进入 `WAITING_DOCTOR_REVIEW`。
5. 上传任意 `.wav` 或 `.mp3` 文件，点击“测试 Mock ASR”，确认展示 `engine`、`text`、`conversation_text`、`segments`、`medical_keywords`，且 `missing` 为空。
6. 上传任意 `.wav` 或 `.mp3` 文件，点击“音频生成病历”，确认先展示 Mock ASR，再复用现有 Agent 生成病历草稿。
7. 检查 `data/medical_record_agent.sqlite3` 中 `agent_task`、`agent_task_step`、`audit_log` 是否写入病历生成任务记录。

## V0.2 已知边界

- 不接真实 FunASR。
- 不做实时麦克风录音。
- 不做实时流式转写。
- 不接真实 LLM API。
- 不接真实医院 HIS/EMR。
- 不使用真实患者隐私数据。

## V0.1 回顾与追溯

V0.1 是基于医患对话文本的门诊病历生成 Agent POC。

V0.1 只使用模拟问诊文本和 mock LLM，不接入真实患者隐私数据、真实医院 HIS/EMR、真实 ASR 或真实 LLM API。AI 只生成草稿，任务正常结束后停在 `WAITING_DOCTOR_REVIEW`。

### V0.1 功能范围

- 输入医患对话文本。
- 执行 Prompt 链：字段抽取 -> 草稿生成 -> 安全校验。
- 由 `MedicalRecordOrchestrator` 统一编排状态流转。
- 使用 SSE 推送任务进度。
- 使用 SQLite 记录任务、步骤和审计日志。
- mock LLM 失败时最多重试 2 次，连续失败后进入降级结果。

### V0.1 API

- `POST /api/records/generate`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/steps`
- `GET /api/tasks/{task_id}/events`

### V0.1 手动验收

1. 启动 FastAPI。
2. 打开 `http://127.0.0.1:8000/static/index.html`。
3. 使用页面默认蛇咬伤问诊文本，点击文本病历生成入口。
4. 观察进度依次经过 `CREATED`、`EXTRACTING_FIELDS`、`GENERATING_DRAFT`、`SAFETY_CHECKING`、`WAITING_DOCTOR_REVIEW`。
5. 核对页面显示结构化字段 JSON、病历草稿、安全校验结果和步骤日志。
6. 检查 `data/medical_record_agent.sqlite3` 中 `agent_task`、`agent_task_step`、`audit_log` 是否写入记录。

## 外部数据集处理流程

本项目支持将 Toyhom/Chinese-medical-dialogue-data 中文医疗问答 CSV 转换为课程项目可用的“病历字段抽取测试集”和“问诊表达语料库”。该数据仅用于字段抽取评测和语料分析，不用于真实诊疗、自动诊断或自动处方。

原始 CSV 请放在：

```text
data/raw_external/
```

`data/raw_external/` 已加入 `.gitignore`，不要把原始医疗问答数据提交到 GitHub。仓库只保留清洗脚本、标注指南和必要的小型结构模板。

推荐 PowerShell 流程：

```powershell
python scripts/ingest_toyhom_dataset.py
python scripts/filter_toyhom_cold_cases.py
python scripts/build_pseudo_emr_dataset.py
python scripts/sample_annotation_set.py
python scripts/evaluate_on_gold_set.py
```

输出文件：

- `data/processed/toyhom_clean.jsonl`：统一字段后的清洗数据。
- `data/processed/toyhom_cold_candidates.jsonl`：感冒、发热、咳嗽、鼻塞、流涕、咽痛、上呼吸道感染等候选病例。
- `data/processed/pseudo_emr_cases.jsonl`：规则生成的 `pseudo_fields`，仅作预标注和评测样例，不作为人工真值。
- `data/annotation/annotation_sample_100.jsonl`：人工标注抽样文件。
- `data/annotation/annotation_guide.md`：人工标注指南。
- `data/output/toyhom_gold_evaluation_report.md`：基于 `data/annotation/gold_100.jsonl` 的评估报告。

注意事项：

- Toyhom CSV 常见编码为 `gb18030`，导入脚本会自动尝试常见中文编码。
- 标注时只根据 `title` 和 `question` 记录患者事实，不从 `answer` 中补充新事实。
- 未提及字段必须标记为 `missing=true`，不能默认写“无”。
- 诊断相关内容只能作为“候选/待医生确认”。
- 如发现手机号、微信、QQ、广告或明显无关内容，样本会被标记 `needs_manual_review=true`。
