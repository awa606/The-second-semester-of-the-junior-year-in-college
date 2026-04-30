# 微信小程序接入说明

## 基本架构

继续使用当前 FastAPI 应用作为后端。

```text
微信小程序
  -> wx.request()
  -> HTTPS 后端域名
  -> FastAPI /api/ask
  -> JSON 知识卡 / 后续数据库
```

小程序不需要内置完整知识库。它只需要把用户问题发给后端，再展示后端返回的结构化结果。

## 可复用后端接口

使用：

```text
POST /api/ask
```

请求体示例：

```json
{
  "question": "宝宝多久喝一次奶粉",
  "age_months": 3,
  "context": {}
}
```

当前响应字段已经适合小程序展示：

- `category`
- `risk_level`
- `answer.summary`
- `answer.advice`
- `answer.warning`
- `sources`
- `disclaimer`

## 小程序页面建议

最低页面：

- `pages/ask/index`：输入问题和宝宝月龄。
- `pages/result/index`：展示回答、提醒、来源和免责声明。
- `pages/feedback/index`：收集有用/无用反馈。

更适合第一版的做法：

- 输入和回答放在同一个页面。
- 始终展示免责声明。
- 当 `risk_level` 是 `medium` 或 `high` 时，把提醒放在建议之前。
- 不做药物剂量输入表单。

## `wx.request` 示例

```js
wx.request({
  url: "https://your-domain.example.com/api/ask",
  method: "POST",
  header: {
    "content-type": "application/json"
  },
  data: {
    question: questionText,
    age_months: ageMonths || null,
    context: {}
  },
  success(res) {
    console.log(res.data)
  },
  fail(err) {
    console.error(err)
  }
})
```

## 开发环境和真实环境区别

本地开发：

- 在电脑上启动后端。
- 使用微信开发者工具。
- 调试时可以在开发者工具里跳过 request 域名校验。

真实用户测试：

- 把后端部署到公网服务器。
- 启用 HTTPS。
- 在小程序管理后台配置 request 合法域名。
- 在 `wx.request` 中使用 HTTPS API 地址。

## 部署要求

真实小程序不能依赖：

```text
http://127.0.0.1:8000
```

这个地址只表示“当前设备自己”。在另一台电脑或手机上，它会指向另一台设备本身，而不是开发电脑。

可选访问方式：

- 局域网演示：`http://<你的电脑局域网IP>:8000/`
- 临时隧道：`https://<临时隧道域名>/`
- 云服务器：`https://your-domain.example.com/`

## 小程序公开前的安全要求

公开测试前至少需要：

- 增加来源审核状态检查。
- 移除生产卡片中的占位来源 URL。
- 添加隐私说明。
- 添加反馈记录。
- 添加基础限流。
- 服务端日志避免暴露不必要的个人信息。
- 保持药物剂量和诊断类拒答规则启用。
