# scripts 目录说明

这个目录存放项目验证和维护脚本。

## 文件说明

- `validate_kb.py`：验证知识卡字段、分类结果和检索命中。
- `powershell/`：Windows PowerShell 测试脚本。

## 使用方式

修改知识卡、分类器或检索器后运行：

```powershell
.\.venv\Scripts\python.exe scripts\validate_kb.py
```

如果验证失败，先根据输出中的 `card_id`、分类结果和命中卡片修复知识卡或分类词。
