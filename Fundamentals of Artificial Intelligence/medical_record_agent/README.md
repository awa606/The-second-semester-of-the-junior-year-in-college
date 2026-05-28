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

## 已知边界

- 暂不做真实语音采集和 ASR。
- 暂不接真实 LLM API。
- 暂不接真实医院 HIS/EMR。
- 暂不使用真实患者隐私数据。
- Word 导出依赖已预留，医生确认后导出流程放到 V0.2。
