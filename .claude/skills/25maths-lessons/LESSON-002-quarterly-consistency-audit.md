---
id: LESSON-002
title: 跨多 session ADR layered 加叠隐含 silent inconsistency · 季度 audit 必走
date: 2026-04-26
category: meta
severity: 🟡 important
related_ADR: 0064
keywords: [ADR, consistency, audit, layered, inconsistency]
auto_load: true
---

## Trigger context
Stage 5.10-5.25: 每个 step 加 1-2 ADR · 共 14 步 · 累积 60+ ADR · 没主动审一致性。

## Symptom / error observed
Stage 5.26 直面审查发现 10 处 silent inconsistency:
- 视图数 7 vs 2 漂移
- repo.L4 子类 4→5→6→5→6
- ADR-0032 v1/v2/v3 三版数字
- 红线 7 vs 6 vs 8 命名混淆
- cheatsheet 多版本散落

## Root cause
- 每次加 ADR 时只考虑本地 consistency · 没追溯连带影响
- 不同 session 之间没 inter-ADR cross-reference 检查
- 用户 / NZH 不读 ADR · 不会主动发现冲突

## Fix applied
- Stage 5.26 写 CONSISTENCY_AUDIT.md · 修订 10 处 · 写 V3_FINAL_CHEATSHEET 合并版

## Lesson
- 每加 5+ ADR 必走 quick consistency 自检(15 min)
- 季度做大 consistency audit(1 hr)
- charter sync version 号每次加 ADR 后即升 + 同步,避免漂移
- 用户视角的 cheatsheet 只保留 1 个 FINAL · 旧版 ARCHIVED

## Auto-detection
- `scripts/explain-decision.sh ADR-NNNN`(ADR-0064 § 5 / TASK-126)— 链式追溯
- 周度 lint:同主题 ADR > 3 个 v# 修订 → 提示合并 / promote 一个新 canonical
