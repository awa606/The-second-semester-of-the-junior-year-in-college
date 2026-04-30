# HANDOFF_TO_CODEX.md

## 项目名称
parenting_kb_v1

## 项目目标
这是一个“基础育儿信息助手”原型，不是诊断工具，不提供个体化用药或治疗建议。
项目目标是做出一个“可本地运行、可验证、可演示”的初期版本，后续可接网页前端或微信小程序。

## 当前已有内容
- FastAPI 后端骨架已存在
- /api/ask, /api/health, /api/sources, /api/feedback 路由已建立
- data/cards/knowledge_cards.sample.json 中已有基础知识卡
- data/rules/red_flags.json 中已有高风险拦截规则
- 部分知识卡 source_refs 已替换为真实官方来源
- 项目已能启动，但分类器和检索器较弱，演示效果不稳定

## 当前主要问题
1. classifier.py 对自然语言表达识别不稳定
   - 如“红屁屁”“拉肚子”“第一口辅食”可能识别失败

2. retriever.py 召回不稳定
   - 命不中时可能返回错误类别的卡片
   - 需要改成“找不到就返回空，不乱答”

3. Windows PowerShell 下中文测试命令不稳定
   - 需要提供稳定的 TEST_COMMANDS.ps1

4. 目前还没有一个简单可展示的前端页面
   - 需要做一个最简 HTML 页面来调用 /api/ask

## 项目开发约束
- 不要把系统改造成“诊断工具”
- 不要加入个体化用药剂量建议
- 不要删除已有的 red_flags 风险边界
- 保持接口返回结构尽量稳定
- 尽量只做当前阶段最必要的改动，不要大重构

## 当前阶段目标
做出一个“可本地运行、可展示”的最小版本，满足：
- 能启动 FastAPI
- 能通过前端页面或 /docs 测试 4 个问题
- 能正确区分 feeding / care / symptom_triage
- 高风险问题会触发拦截或分流
- 回答中显示来源和免责声明

## 需要优先处理的文件
- app/services/classifier.py
- app/services/retriever.py
- app/routes/ask.py
- 新增一个简单前端，例如 web/index.html
- 新增或修复 TEST_COMMANDS.ps1

## 不要优先做的事情
- 不要先写爬虫
- 不要先接微信小程序
- 不要先接复杂数据库
- 不要先做复杂大模型编排