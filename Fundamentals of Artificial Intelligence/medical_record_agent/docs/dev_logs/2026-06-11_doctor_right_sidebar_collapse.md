# 医生端右栏折叠与滚动小修

## 修改日期 / 时间

2026-06-11，时区：Asia/Shanghai

## 修改目标

对 `doctor.html` 医生端右侧“AI辅助与安全校验”区域做小范围交互优化：右栏内部滚动，并按风险等级控制折叠状态。

## 修改前问题

- 右侧栏信息较多时阅读压力较大。
- 正常项、候选项、缺失项和 Agent Trace 的展开状态没有按风险区分。

## 输入

- 用户要求只做医生端右侧栏小修。
- 现有 `doctor.js` 右栏 Tab 渲染逻辑和 `doctor.css` 卡片样式。

## 输出

- 右侧栏内容区明确内部滚动。
- 正常绿色项默认折叠。
- 红色缺失项、黄色候选诊断、错误风险默认展开。
- Agent Trace 默认折叠，有红黄风险时自动展开。

## 修改文件

- `static/doctor.js`
- `static/doctor.css`
- `static/doctor.html`
- `docs/dev_logs/2026-06-11_doctor_right_sidebar_collapse.md`

## 关键设计决策

- 继续保留已有右栏 Tab，不重构页面。
- 使用原生 `<details>` / `<summary>` 控制折叠，避免引入新依赖。
- 风险判断只在前端基于已有 `appState` 数据完成，不改变后端接口。

## 验证步骤

1. 运行 `node --check static\doctor.js`。
2. 运行 `git diff --check -- static\doctor.js static\doctor.css static\doctor.html docs\dev_logs\2026-06-11_doctor_right_sidebar_collapse.md`。

## 验证结果

- `node --check static\doctor.js`：通过。
- `git diff --check -- static\doctor.js static\doctor.css static\doctor.html docs\dev_logs\2026-06-11_doctor_right_sidebar_collapse.md`：通过。

## 未解决问题

- 未做新的真实音频上传演示。

## 下一步计划

- 使用 `fever_01.wav + FunASR` 演示时观察右栏展开状态是否符合现场讲解节奏。
