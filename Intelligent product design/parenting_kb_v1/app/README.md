# app 目录说明

这个目录存放 FastAPI 后端代码，是本项目的服务入口。

## 主要文件

- `main.py`：创建 FastAPI 应用，挂载 API 路由，并把 `web/index.html` 作为首页。
- `schemas.py`：定义请求和响应的数据结构。
- `version.py`：记录当前应用版本和迭代名称。
- `routes/`：按接口拆分的路由层。
- `services/`：分类、检索、风险拦截和回答生成等业务逻辑。

## 使用方式

在项目根目录启动服务：

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

打开本地页面：

```text
http://127.0.0.1:8000/
```

查看接口文档：

```text
http://127.0.0.1:8000/docs
```

## 修改提醒

如果修改了 API 行为、分类逻辑、检索逻辑或版本号，请同步更新 `docs/CHANGELOG.md` 和相关目录的 `README.md`。
