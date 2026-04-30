# data/cards 目录说明

这个目录存放育儿知识卡。当前有效知识卡会被 `app/services/retriever.py` 加载。

## 文件说明

- `knowledge_cards.sample.json`：早期样例卡和部分来源补充，检索器会用它覆盖同 `card_id` 的来源/证据信息。
- `knowledge_cards.sample2.json`：基础完整卡片集合。
- `knowledge_cards.expansion.v0.2.json`：后续扩展卡片集合，当前建议优先把新卡加到这里。

## 新增卡片步骤

1. 在 `knowledge_cards.expansion.v0.2.json` 中新增完整卡片。
2. 确认 `card_id` 唯一。
3. 给 `question_patterns` 写自然中文问法。
4. 确认 `category` 是 `feeding`、`care`、`development`、`symptom_triage` 之一。
5. 保持回答非诊断、非药物剂量建议。
6. 补充 `source_refs`、`evidence_note`、`review_status`。
7. 运行 `scripts/validate_kb.py`。

## 如果新增独立文件

如果以后新增 `knowledge_cards.expansion.v0.3.json` 之类的新批次，需要在 `app/services/retriever.py` 的 `METADATA_PATHS` 中加入该文件路径。
