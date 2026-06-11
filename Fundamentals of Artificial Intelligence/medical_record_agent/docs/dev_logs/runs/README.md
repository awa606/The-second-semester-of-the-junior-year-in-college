# 运行日志目录

本目录用于保存课程演示或关键验收时生成的运行日志。

运行日志由脚本生成：

```powershell
python scripts/save_run_log.py --task-id 19 --audio-id xxx --title fever_01_demo
```

默认输出格式：

```text
docs/dev_logs/runs/YYYY-MM-DD_fever_01_demo.md
```

日志会汇总：

- 运行时间
- 输入音频
- ASR engine
- ASRResult 摘要
- CER / keyword_recall
- role_strategy / warnings
- LLM provider / model / latency / fallback
- 任务状态
- 步骤日志摘要
- 病历草稿摘要
- 安全校验摘要

提交规则：

- 课程汇报需要留存的具体运行日志可以按需提交。
- 含真实患者数据、真实 API Key、个人身份信息或大体积音视频的日志不得提交。
- 本地调试临时日志可以保留在本目录但不提交。
