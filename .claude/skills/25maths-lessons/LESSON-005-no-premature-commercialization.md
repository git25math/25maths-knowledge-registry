---
id: LESSON-005
title: 过早商业化设计创造反向灵魂压力 · 推迟到 post-Beta
date: 2026-04-26
category: meta
severity: 🔴 critical
related_ADR: 0040, 0058, 0059, 0060
keywords: [commercialization, soul-charter, paywall, beta, anti-pattern]
auto_load: true
---

## Trigger context
Stage 5.10-5.22: 在用户尚未明确商业化阶段时 · 我连续设计了完整商业化体系:
- ADR-0024 商业化 7 表
- TASK-014a-f 6 商业化子任(三级会员 / Stripe / WeChat / OCR / AI 家教 / 白标)
- ADR-0032 v2 业务数字 Y3 ¥1 亿
- ADR-0057 bootstrap-first
- ADR-0026 Phase trigger 含 revenue 维度

工作量约 14d task + 7 schema + 4 ADR

## Symptom
Stage 5.23 用户突然说:"先取消一切关于付费的功能 · 全部都是内测版 · 注册即是会员 · 没有付费功能 · 现在是属于信息收集阶段 · 服务于我的实际教学"

## Root cause
- 我从 v3 plan 起步就默认 "DFM-killer = 商业产品"
- 过早把 Y3 ¥1 亿 / venture-style growth 写进 plan
- 没问清楚用户的真实阶段 / 真实意图(信息收集 + 服务实际教学)
- 假设 = "所有 EdTech 项目都要商业化" · 错误投射

## Fix applied
- ADR-0058 Internal Beta 撤销商业化
- ADR-0059 创立初心(NZH verbatim 原话保留)
- ADR-0060 Teacher Workbench post-Beta(B 端 SaaS · 学生家长永远免费)
- ADR-0032 v3 业务数字现实化(教师 SaaS 100×$30 = $3000/月)
- 14d 商业化 task → defer post-Beta
- 4 个 0 成本副业 quick wins(TPT/TES/知乎/公众号)与平台分离

## Lesson
- 项目阶段不明时:**问用户**,不要 default-to "venture growth"
- "信息收集" / "服务自身教学" / "Beta" 是合法 / 长期可持续阶段
- 商业化设计应该**晚于**用户明确请求 · 不是默认启动
- 每个 plan 演进步骤 · 自检:"是用户要的 · 还是我假设的?"

## Auto-detection
- 任何"加 paywall / 加付费功能 / 加商业化 schema" 提案 · 必显式标注 "用户明确请求 / 我假设" · 后者 = block
- 13 红线灵魂红线 #1 "为 KPI 必加焦虑特性" 在 lint 中检测
- 月度 NZH review:plan 是否在用户明确请求范围内?
