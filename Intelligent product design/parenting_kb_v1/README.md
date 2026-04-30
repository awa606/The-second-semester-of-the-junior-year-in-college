# parenting_kb_v1 项目说明

`parenting_kb_v1` 是一个可本地运行、可验证、可展示的基础育儿助手原型。它用 FastAPI 提供接口，用静态网页做演示，用 JSON 知识卡作为当前知识库。

当前版本：`v0.2.3`

## 当前能展示什么

- 打开本地网页，输入育儿问题并查看结构化回答。
- 调用 `POST /api/ask`，返回 `summary`、`advice`、`warning`、`sources`、`disclaimer`。
- 支持常见分类：`feeding`、`care`、`development`、`symptom_triage`。
- 已覆盖第一口辅食、奶粉喂养、红屁屁、鼻塞、湿疹、发育观察、发热、拉肚子、呕吐、摔到头等基础问题。
- 对诊断、个体化药物剂量、高风险症状保留安全边界。
- 无命中时不乱返回其他类别卡片。

这个项目不是诊断工具，不能替代线下医生判断，也不能提供个体化药物剂量建议。

## 快速运行

在项目根目录执行：

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

浏览器打开：

```text
http://127.0.0.1:8000/
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

如果本机没有 `.venv`，先创建环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 如何验证

验证知识卡、分类和检索：

```powershell
.\.venv\Scripts\python.exe scripts\validate_kb.py
```

当前期望结果：

```text
cards: 39
validation: ok
```

启动服务后运行 API 冒烟测试：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\powershell\TEST_COMMANDS.ps1
```

测试脚本会请求“第一口辅食”“奶粉怎么冲”“红屁屁”“鼻塞”“拉肚子”“摔到头”“药物剂量拒答”等问题。

## 文件夹结构

```text
parenting_kb_v1/
  app/                  FastAPI 后端代码
  data/                 JSON 知识卡和风险规则
  docs/                 项目文档、变更记录、交接资料
  scripts/              验证脚本和命令行测试脚本
  web/                  本地演示网页
  requirements.txt      Python 依赖
  README.md             项目入口说明
```

每个主要文件夹下都有自己的 `README.md`，用于说明该文件夹的职责和使用方式。

## 关键入口文件

- `app/main.py`：创建 FastAPI 应用，挂载路由，并把 `web/index.html` 作为首页。
- `app/routes/ask.py`：主问答接口，负责风险检查、分类、检索、回答生成和调试输出。
- `app/services/classifier.py`：规则分类器，维护中文自然表达、别名和分类关键词。
- `app/services/retriever.py`：加载知识卡，按分类过滤后打分检索。
- `data/cards/`：知识卡 JSON 文件。
- `data/rules/red_flags.json`：风险边界和默认免责声明。
- `web/index.html`：最简可展示前端。
- `scripts/validate_kb.py`：知识库验证脚本。
- `scripts/powershell/TEST_COMMANDS.ps1`：中文 API 冒烟测试脚本。

## 如何扩展知识库

当前建议继续使用 JSON，不急着上数据库。原因是卡片字段、审核标准和来源格式仍在迭代，JSON 更适合快速人工审核。

新增卡片建议放在：

```text
data/cards/knowledge_cards.expansion.v0.2.json
```

如果新增一个独立批次文件，需要同步更新：

```text
app/services/retriever.py
```

把新文件加入 `METADATA_PATHS`。

每张卡片至少要检查：

- `card_id` 唯一。
- `category` 只能是 `feeding`、`care`、`development`、`symptom_triage`。
- `question_patterns` 要包含自然中文问法。
- `answer_summary` 和 `answer_points` 不能写成诊断结论。
- `red_flags` 和 `escalation_advice` 要保守。
- `source_refs` 和 `evidence_note` 要能说明依据。
- `review_status` 要明确。

新增或修改卡片后运行：

```powershell
.\.venv\Scripts\python.exe scripts\validate_kb.py
```

如果新问题无法被正确分类，还需要更新：

```text
app/services/classifier.py
```

## 如何让别人访问网页

同一 Wi-Fi 或局域网内演示：

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
ipconfig
```

找到本机 IPv4 地址，例如 `192.168.1.23`，别人电脑打开：

```text
http://192.168.1.23:8000/
```

如果打不开，通常是 Windows 防火墙没有放行 Python/Uvicorn 或 8000 端口。

临时公网演示、云服务器部署、微信小程序接入说明见：

```text
docs/RUN_AND_SHARE.md
docs/manual/MINIPROGRAM_INTEGRATION.md
```

## 当前限制

- 分类器还是规则匹配，不是大模型语义理解。
- 检索是关键词打分，不是向量搜索。
- 知识库只有 39 张有效卡片，覆盖面仍有限。
- 部分早期来源 URL 仍需人工复核和替换。
- 还没有后台管理页面、账号系统、数据库迁移和生产部署配置。
- 前端是展示原型，不是完整用户产品。

## 交接建议

后续每次有实质修改，都要同步更新：

- `docs/CHANGELOG.md`
- 受影响目录下的 `README.md`
- 如涉及产品状态、路线图或小程序接入，也更新 `docs/manual/`

不要删除风险边界，不要加入个体化药物剂量建议，不要为了有结果而返回无关知识卡。
