---
id: LESSON-003
title: solo dev + Claude Max 20× = 25/75 工时拆分 · 不是 1+1
date: 2026-04-26
category: meta
severity: 🟢 nice-to-know
related_ADR: 0055
keywords: [solo-dev, Claude, workflow, time-budget]
auto_load: true
---

## Trigger context
Stage 5.18 review 判断 "94 TASK 严重低估,9-12 月才能完成"

## Symptom
判断过于悲观 · 没考虑 Claude Code Max 20× 的 5 并行 session 能力

## Root cause
默认假设 "1 NZH = 1 dev" · 而实际 Claude Max 20× 让 NZH 等于 "1 决策者 + 6 虚拟实习生"

## Fix applied
Stage 5.19 重新校准:
- L1 NZH 必决策(10%):仅这部分 NZH 投入
- L2 NZH 灵魂校验(15%):review only
- L3 Claude 全自动(75%):仅 PR merge

NZH 总投入 ~14.5 NZH-day vs Claude ~60 工作日(5 并行 = 12 真实日历)
M1-M6 实际 1.5-2 月密集 + 4 月持续 = 6 月对(不是 9-12 月)

## Lesson
- 工时估算时 · 区分 NZH vs Claude 时间
- NZH 瓶颈是决策 + 灵魂校验 + 学生反馈 + 教学(主业)· 不是编码
- Claude 瓶颈是 5 并行 session · 但每条线本身可极快推进
- 优化方向:NZH 触点简化(简短 PR description / V3_FINAL_CHEATSHEET)· 不是削减 Claude 工作

## Auto-detection
- 任何工时估算 · 显式标注 "(NZH X hr / Claude Y day)" 区分
- 总 plan workload "总 X day" 不直接报 · 拆为 "NZH X hr + Claude Y day"
