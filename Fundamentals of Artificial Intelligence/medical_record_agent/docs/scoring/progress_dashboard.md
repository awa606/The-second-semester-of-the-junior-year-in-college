# 项目进度与评分对照看板

本文档用于汇报前快速确认项目主链路、功能完成度、评分证据和现场备用方案。它是 `docs/scoring/course_scoring_plan.md` 的进度版补充，重点回答“现在做到哪里、能展示什么、哪里有风险”。

## 当前主链路

```text
fever_01.wav
  -> FunASR
  -> ASRResult / conversation_text
  -> Online LLM 或 MockLLM fallback
  -> 字段抽取
  -> 病历草稿
  -> 安全校验
  -> 医生审核
  -> Agent Trace
  -> 运行日志
```

说明：

- FunASR 是当前最稳音频 baseline。
- Online LLM 可用于真实字段抽取能力展示，但必须通过环境变量配置；失败、超时或 JSON 不完整时自动 fallback 到 MockLLM。
- MockLLM / deterministic extractor 是稳定演示兜底，保证 fever clean 和 fever_01 主线可跑通。
- Agent Trace 将 task、steps、ASRResult、SafetyCheckResult 和 LLM 状态组装成可解释轨迹。
- 运行日志由 `scripts/save_run_log.py` 根据 `task_id` 和 `audio_id` 生成，输出到 `docs/dev_logs/runs/`。

## 当前完成度表

| 模块 | 当前状态 | 完成内容 | 可展示入口 / 文件 | 风险 |
| --- | --- | --- | --- | --- |
| 文本导入 | 已完成 | 粘贴 fever clean 文本，生成字段、草稿、安全校验和 Agent Trace | `/static/doctor.html` 文本导入；`POST /api/records/generate` | 低 |
| 音频上传 | 已完成 | 上传 wav 等预录音频，获得 `audio_id` 并进入转写或生成病历链路 | `/static/doctor.html` 上传转写 / 上传生成病历 | 低 |
| FunASR | 已完成 | `fever_01.wav` 可作为 baseline 转写并进入病历生成 | `engine=funasr`；`app/services/asr/funasr_engine.py` | 中：首次加载模型可能慢 |
| Online LLM | 已接入 | OpenAI-compatible provider，支持 DeepSeek 等兼容接口做字段抽取 | `LLM_PROVIDER=online`；`app/services/llm/online_provider.py` | 中：依赖网络、环境变量和模型 JSON 稳定性 |
| MockLLM fallback | 已完成 | 默认兜底；Online/Ollama 失败、超时或 JSON 不完整时回退 | `app/services/llm/mock_provider.py`；Agent Trace LLM 区 | 低 |
| Agent Trace | 已完成 | 显示 `agent_mode`、`input_type`、`perception`、`plan`、`executed_steps`、`decision` | doctor 右栏 Agent Trace；debug Agent Trace JSON | 低 |
| doctor.html | 已完成 | 医生端工作台；三栏布局；运行上下文；右栏 Tab；保存草稿说明 | `/static/doctor.html` | 低 |
| debug.html | 已完成 | 保留 ASRResult、Task、Steps、Safety、Agent Trace、LLM Trace JSON | `/static/debug.html` | 低 |
| 保存草稿 | 已明确 | “保存草稿到SQLite”保存当前字段到 Task `result_json`，不生成导出文件 | doctor 底部按钮；debug 草稿保存说明 | 低 |
| 运行日志 | 已完成 | 根据 `task_id` / `audio_id` 生成 Markdown 运行日志 | `scripts/save_run_log.py`；doctor/debug 复制命令按钮 | 低：具体运行日志需演示后按需生成 |

## 评分细则对照表

| 评分项 | 分值 | 当前完成内容 | 可展示证据 | 仍需补充 | 预计得分风险 |
| --- | ---: | --- | --- | --- | --- |
| 智能体设计模式 | 10 | 已实现 Plan-and-Execute + Human-in-the-loop；文本/音频感知；字段抽取、草稿生成、安全校验、医生审核；Agent Trace 可视化 | `docs/scoring/agent_design.md`；`docs/scoring/agent_architecture_diagram.md`；`app/agents/medical_record_orchestrator.py`；doctor 右栏 Agent Trace | 汇报时需要主动讲清楚 Agent 不是单个 LLM 调用，而是任务编排和状态闭环 | 低 |
| 决策系统设计 | 10 | 输入类型分流；ASR 引擎选择；Online LLM / Mock fallback；字段 missing/confidence；角色校正提醒；安全校验和导出门禁 | `docs/scoring/decision_system.md`；`app/services/llm/factory.py`；`app/services/agent_trace.py`；debug Task/Steps JSON | 现场要展示 `export_allowed=false` 和 `doctor_review_required`，否则决策闭环不够显眼 | 中低 |
| 伦理合规设计 | 5 | 模拟数据；API Key 环境变量；不接真实患者数据；AI 只生成草稿；医生审核；审计日志；安全校验 | `docs/scoring/ethics_compliance.md`；README；`docs/dev_logs/DEVELOPMENT_RULES.md`；doctor 保存说明 | 汇报时需要明确 Online ASR / Online LLM 不提交真实 Key，不上传真实患者数据 | 低 |
| 演示流畅度 | 10 | doctor 工作台、debug 调试台、文本导入、FunASR 音频链路、ASR 评测、运行日志命令均可展示 | `/static/index.html`；`/static/doctor.html`；`/static/debug.html`；`docs/scoring/demo_checklist.md` | 演示前要预热 FunASR；准备 fever clean 文本和已生成运行日志作为兜底 | 中 |
| 表达与逻辑 | 10 | 已有 12-15 分钟正式讲稿、评分计划、演示清单、代码讲解路线和本进度看板 | `docs/scoring/demo_script.md`；`docs/scoring/course_scoring_plan.md`；`docs/scoring/progress_dashboard.md` | 需要按“背景 -> Agent -> 决策 -> 伦理 -> 演示 -> 代码”控制时间 | 中低 |
| 代码展示 | 5 | Orchestrator、Schema、Prompt、LLM Adapter、ASR Factory、Agent Trace、SQLite 任务步骤均有可讲代码点 | `docs/scoring/code_walkthrough.md`；`app/agents/`；`app/schemas/`；`app/prompts/`；`app/services/`；`app/db/sqlite.py` | 代码展示时间短，建议只选 4-5 个关键文件，不展开所有实现 | 低 |

## 当前最稳演示路线

### 1. 文本导入 fever clean

1. 打开 `/static/doctor.html`。
2. 点击“文本导入”。
3. 粘贴 fever clean 问诊文本。
4. 展示左栏字段卡片、右栏缺失项、候选诊断、安全校验和 Agent Trace。

展示重点：

- 文本输入直接进入 Agent 主流程。
- MockLLM fallback 保证稳定演示。
- AI 输出只是草稿，医生审核前不允许自动导出。

### 2. 上传 fever_01.wav + FunASR

1. 点击“上传生成病历”。
2. 选择 `fever_01.wav`。
3. ASR 选择 FunASR。
4. 等待 ASRResult 和病历生成。

展示重点：

- `fever_01.wav -> FunASR -> ASRResult -> 病历 Agent`。
- 中栏展示转写文本，右栏展示 ASR warnings 或角色校正提醒。
- 如果 `role_strategy=single_segment_needs_review`，强调系统不强行猜医生/患者角色。

### 3. 查看 Agent Trace

1. 在 doctor 右栏切换到 `Agent Trace`。
2. 展示输入类型、感知结果、计划步骤、当前状态、导出决策和医生审核边界。
3. 打开 `/static/debug.html`，展示完整 Agent Trace JSON。

展示重点：

- `decision.export_allowed=false`。
- `decision.reason=doctor_review_required`。
- Human-in-the-loop 是系统设计的一部分，不是临时人工兜底。

### 4. 保存运行日志

1. 在 doctor 或 debug 页面查看当前 `task_id` 和 `audio_id`。
2. 点击“复制运行日志命令”。
3. 执行类似命令：

```powershell
python scripts/save_run_log.py --task-id 19 --audio-id xxx --title fever_01_demo
```

4. 打开 `docs/dev_logs/runs/YYYY-MM-DD_fever_01_demo.md`。

展示重点：

- 运行日志汇总 ASRResult、CER、keyword_recall、LLM fallback、Agent Trace、任务步骤、草稿和安全校验。
- 具体运行日志按需提交，不提交真实患者数据、真实 API Key、音频或数据库。

## 现场备用方案

| 现场问题 | 处理方式 | 讲解话术 |
| --- | --- | --- |
| Online LLM 失败、超时或 JSON 不完整 | 保持 `LLM_PROVIDER=mock`，或说明系统自动 fallback 到 MockLLM | “真实 LLM 是可替换 provider，失败时不会破坏 Orchestrator，系统自动使用 MockLLM 保证医疗演示稳定。” |
| FunASR 卡顿或模型首次加载过慢 | 改用文本导入 fever clean；必要时用 Mock ASR 展示音频接口链路 | “FunASR 是本地可选 ASR baseline，现场卡顿不影响 Agent 主流程；ASR 输出统一为 ASRResult，后续流程不变。” |
| doctor.html 异常 | 打开 `/static/debug.html` 展示 Task、Steps、Safety、Agent Trace JSON；打开运行日志 | “医生端是演示工作台，调试台保留完整 API 和 JSON 证据，运行日志证明链路此前完整跑通。” |
| ASR 角色无法自动区分 | 展示 `single_segment_needs_review` 提醒 | “系统不会在医疗场景中强行猜测医生/患者角色，而是要求人工校正。” |
| 生成结果字段缺失 | 展示缺失项提醒和医生审核边界 | “缺失不是失败，而是系统提示医生继续补充问诊或查体，最终由医生确认。” |

## 汇报前检查顺序

1. 打开 `docs/scoring/demo_script.md`，按 12-15 分钟讲稿排练。
2. 打开 `docs/scoring/demo_checklist.md`，逐项检查页面、链路和安全边界。
3. 预热 FunASR，提前跑一次 `fever_01.wav`。
4. 保存一份脱敏运行日志到 `docs/dev_logs/runs/`。
5. 确认没有提交真实 API Key、真实患者数据、音频、SQLite 数据库、模型缓存或大体积视频。
