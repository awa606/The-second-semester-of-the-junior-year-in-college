# scripts/powershell 目录说明

这个目录存放 Windows PowerShell 测试脚本。

## 文件说明

- `TEST_COMMANDS.ps1`：主要 API 冒烟测试脚本，会请求多组中文育儿问题。
- `test_api.ps1`：早期测试脚本，保留用于对比和追溯。

## 使用方式

先启动服务：

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

再运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\powershell\TEST_COMMANDS.ps1
```

如服务运行在其他地址，可传入 `ApiUrl`：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\powershell\TEST_COMMANDS.ps1 -ApiUrl "http://192.168.1.23:8000/api/ask"
```
