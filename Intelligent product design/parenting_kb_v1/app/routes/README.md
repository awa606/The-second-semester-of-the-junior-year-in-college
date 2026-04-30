# app/routes 目录说明

这个目录存放 FastAPI 路由，也就是对外暴露的接口。

## 文件说明

- `ask.py`：主问答接口 `POST /api/ask`，串联风险检查、分类、检索和回答生成。
- `health.py`：健康检查接口 `GET /api/health`。
- `sources.py`：来源查询接口 `GET /api/sources/{doc_id}`。
- `feedback.py`：反馈接口，用于接收简单有用/无用反馈。

## 使用方式

开发时通常先看 `ask.py`，因为演示网页和 PowerShell 测试脚本都主要调用 `/api/ask`。

如果修改接口字段，需要同步更新：

- `app/schemas.py`
- `web/index.html`
- `scripts/powershell/TEST_COMMANDS.ps1`
- `docs/CHANGELOG.md`
