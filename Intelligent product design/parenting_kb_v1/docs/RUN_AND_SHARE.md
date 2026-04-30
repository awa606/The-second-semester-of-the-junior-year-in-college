# 运行与分享说明

## 本机运行

在项目根目录执行：

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

打开：

```text
http://127.0.0.1:8000/
```

## 同一 Wi-Fi / 局域网演示

把 `127.0.0.1` 换成 `0.0.0.0`：

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

查看本机局域网 IP：

```powershell
ipconfig
```

找到 IPv4 地址，例如：

```text
192.168.1.23
```

同一 Wi-Fi 下的其他电脑可以打开：

```text
http://192.168.1.23:8000/
```

如果打不开，通常需要检查 Windows 防火墙，允许 Python/Uvicorn 使用专用网络，或临时放行 TCP 端口 `8000`。

## 临时公网访问

如果只是短时间给不在同一网络的人演示，可以使用隧道工具，例如：

```powershell
ngrok http 8000
```

然后分享工具生成的 HTTPS 地址。

## 更正式的部署

如果要长期给别人访问，建议部署到云服务器：

- 把项目放到服务器。
- 使用 `pip install -r requirements.txt` 安装依赖。
- 用 Uvicorn 启动 FastAPI。
- 用 Nginx 或其他反向代理转发请求。
- 绑定域名并启用 HTTPS。

## 当前安全提醒

当前原型还没有登录系统。如果暴露到公网，任何拿到链接的人都能访问。公开发布前需要补充认证、访问限制、日志脱敏和隐私说明。
