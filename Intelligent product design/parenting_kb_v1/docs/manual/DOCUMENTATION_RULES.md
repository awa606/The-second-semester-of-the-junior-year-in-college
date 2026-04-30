# 文档更新规则

## 基本规则

每次有实质修改，都要在同一轮迭代中更新文档。

实质修改包括：

- API 行为变化。
- 分类器或检索器变化。
- 新增或修改知识卡。
- 红旗风险规则变化。
- 前端行为变化。
- 运行或部署方式变化。
- 依赖变化。
- 文件夹结构变化。

## 必须更新的位置

始终更新：

- `docs/CHANGELOG.md`

按影响范围更新：

- `docs/manual/PROJECT_STATUS.md`
- `docs/manual/ROADMAP.md`
- `docs/manual/MINIPROGRAM_INTEGRATION.md`
- `docs/RUN_AND_SHARE.md`
- `scripts/powershell/TEST_COMMANDS.ps1`
- `scripts/validate_kb.py`
- 受影响目录下的 `README.md`

## 变更记录格式

使用：

```md
## vX.Y.Z - YYYY-MM-DD

- 改了什么。
- 为什么这样改，如果原因重要。
- 如何验证。
- 还剩什么限制。
```

## 版本号规则

使用小步版本号：

- Patch 版本：文档、测试、小修复。
- Minor 版本：新增知识卡批次、新功能、新接口行为。
- Major 版本：数据库迁移、新架构、公开部署边界变化。

例子：

- `v0.2.3`：目录整理和文档更新。
- `v0.3.0`：较大规模知识库扩展。
- `v1.0.0`：来源已审核、部署说明稳定的展示版本。

## 知识卡更新检查清单

每张新卡都要检查：

- `card_id` 唯一。
- `category` 是 `feeding`、`care`、`development`、`symptom_triage` 之一。
- `question_patterns` 包含自然中文问法。
- `answer_summary` 简洁且不写成诊断结论。
- `answer_points` 实用且有边界。
- `red_flags` 保守。
- `escalation_advice` 说明什么时候需要线下求助。
- `source_refs` 已填写。
- `evidence_note` 说明卡片依据。
- `review_status` 已设置。
- `scripts/validate_kb.py` 可以通过。

## 验证命令

修改知识卡或检索逻辑后：

```powershell
.\.venv\Scripts\python.exe scripts\validate_kb.py
```

修改 API 行为后：

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
powershell -ExecutionPolicy Bypass -File .\scripts\powershell\TEST_COMMANDS.ps1
```

## 安全边界

不要记录或实现会把本项目变成以下形态的改动：

- 诊断工具。
- 药物剂量建议工具。
- 线下医疗服务替代品。

如果未来改动触碰这些边界，需要在 `docs/CHANGELOG.md` 中明确说明风险和处理方式。
