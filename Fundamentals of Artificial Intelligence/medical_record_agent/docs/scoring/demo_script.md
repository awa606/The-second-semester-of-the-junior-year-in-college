# 现场演示讲稿

本文档用于课程现场演示，目标是在 5 到 8 分钟内展示系统能力、Agent 设计、决策系统和伦理合规边界。

## 演示目标

- 证明项目是 `Plan-and-Execute + Human-in-the-loop` 医疗病历生成 Agent。
- 展示文本输入和音频输入两条路径都能进入同一个病历 Agent 主流程。
- 展示 ASR 评测、角色校正提醒、字段证据、安全校验和医生审核。
- 明确说明系统只生成草稿，不替代医生，不接真实患者数据。

## 演示前准备

1. 启动服务：

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2. 准备样例：

- fever clean 问诊文本。
- `fever_01.wav` 本地样例音频。
- FunASR 环境可用时选择 `engine=funasr`；不可用时说明可选依赖未安装并切换 Mock 演示工程链路。

3. 打开页面：

- 入口页：`http://127.0.0.1:8000/static/index.html`
- 医生端：`http://127.0.0.1:8000/static/doctor.html`
- 调试台：`http://127.0.0.1:8000/static/debug.html`

## 演示流程

### 1. 入口与系统定位

打开 `/static/index.html`。

讲解要点：

- 系统名称：AI 生成式电子病历辅助系统。
- 页面分为医生端和调试台。
- 医生端用于模拟真实工作台，调试台用于展示 JSON、任务步骤和安全校验证据。

### 2. 文本生成病历

进入 `/static/doctor.html`，点击“文本导入”，粘贴 fever clean 文本，确认生成。

讲解要点：

- 左栏展示主诉、现病史、既往处理、伴随症状、既往史、过敏史、查体、候选诊断和处理建议。
- 中栏展示对话转写。
- 右栏展示缺失项、候选诊断、字段证据、安全校验和操作区。
- AI 输出停在医生审核阶段，不直接导出最终病历。

### 3. 音频生成病历

点击“上传生成病历”，上传 `fever_01.wav`，选择 FunASR。

讲解要点：

- 音频先进入 ASR 感知层，统一输出 `ASRResult`。
- `ASRResult.conversation_text` 再进入病历 Agent 主流程。
- ASR 引擎是可对比模块，不替换 FunASR baseline。

### 4. ASR 评测

打开“ASR 评测”，输入人工标注文本和关键词，点击评测。

讲解要点：

- CER 用于衡量字符级错误率。
- keyword_recall 用于衡量医学关键词召回。
- recognized 和 missing 可以解释 ASR 对病历生成的影响。

### 5. 角色校正提醒

如果 `ASRResult.role_strategy=single_segment_needs_review`，展示右栏提醒。

讲解要点：

- 医生/患者角色不可靠时，系统不会强行标注。
- 医疗问诊角色影响字段归属，因此需要人工校正。

### 6. 调试台与审计追踪

打开 `/static/debug.html`，展示 Task、Steps、Safety JSON。

讲解要点：

- `agent_task` 记录任务状态。
- `agent_task_step` 记录字段抽取、草稿生成、安全校验的输入输出。
- `audit_log` 记录状态变化，说明系统可追踪、可审计。

## 结束总结

一句话总结：

本项目不是简单 API 调用，而是一个带感知、计划、执行、反馈和医生审核边界的医疗病历生成 Agent；AI 只生成草稿和候选诊断，最终必须由医生审核确认。
