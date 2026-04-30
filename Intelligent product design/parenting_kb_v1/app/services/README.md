# app/services 目录说明

这个目录存放问答流程中的核心业务逻辑。

## 文件说明

- `classifier.py`：规则分类器，负责把自然中文问题归到 `feeding`、`care`、`development`、`symptom_triage` 或 `unknown`。
- `retriever.py`：知识卡加载和检索，先按分类过滤，再按相关性打分排序。
- `answer_generator.py`：把命中的知识卡整理成接口返回的结构化回答。
- `risk_guard.py`：读取 `data/rules/red_flags.json`，优先拦截诊断、药物剂量和高风险问题。

## 使用方式

新增知识卡后，如果自然问法无法识别，优先修改 `classifier.py` 的别名或关键词。

修改检索逻辑后运行：

```powershell
.\.venv\Scripts\python.exe scripts\validate_kb.py
```

## 安全边界

这里的逻辑不能为了提高命中率而绕过风险拦截，也不能在无命中时返回其他类别的知识卡。
