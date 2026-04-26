---
id: LESSON-006
title: 跨账号可移植 = repo-committed skills · 不要依赖 user-level memory
date: 2026-04-26
category: meta
severity: 🟡 important
related_ADR: 0065, 0066, 0067
keywords: [skills, cross-account, memory, portability, .claude]
auto_load: true
---

## Trigger context
Stage 5.32:用户问"任何 Claude 账号登录运行都能受益的方式来配置"。当前 ADR-0065 lessons 已 sync repo-level · 但 ADR-0040 灵魂宪章 / ADR-0059 创立初心等核心信息**并未结构化为 skill**(只在 ADR md 文件中)· session 启动时不会自动 inject 到 Claude 上下文。

同时,我之前默认 user-level memory(`~/.claude/projects/<user>/memory/`)是项目知识传承的载体 · 这是错的:**user-level memory 是单 Claude 账号绑定的** · 跨账号不可移植。

## Symptom
- 新 Claude 账号 clone 仓 → 启动 session → 不知道 13 红线 / 5 灵魂问 / 创立初心
- 关键信息散落多个 ADR 文件 · 不主动 read 不会进 context
- "Claude Code skills 机制"被忽视(`.claude/skills/<name>/SKILL.md` 自动 detect)

## Root cause
- 默认假设"项目知识 = ADR / TASK 文档" · 但这些是 NZH 读的格式,不是 Claude 自动 load 的格式
- 没区分"长期项目知识"(应入 skill auto-load)vs "临时决策"(在 ADR 即可)
- user-level memory 看起来"work" → 误认为已 cross-account

## Fix
ADR-0067 落地 3 个 portable skills:
- `25maths-context-loader`(auto-load 灵魂 + 红线 + cheatsheet)
- `25maths-cache-optimizer`(ADR-0066 5 铁律 invokable)
- `25maths-session-summarizer`(self-curating lessons)

`scripts/sync-skills-and-lessons.py` 统一 sync 9 仓。

## Lesson
1. **跨账号可移植 = repo-committed**,不是 user-memory
2. **Claude Code skills 机制**(`.claude/skills/<name>/SKILL.md`)是项目知识固化的标准格式,优先使用
3. **关键约定 / 红线 / charter** 应做成 auto-load skill,不只是 ADR md
4. 测试:模拟新账号 clone 仓 → 验证关键信息真的被 auto-load(目视 grep 即可)

## Auto-detection
- 项目内若发现 "user 必须读 X" 类提示(如 CLAUDE.md 里 "MUST READ ..." 列表)→ 考虑做成 auto-load skill
- 项目内若发现"灵魂宪章 / 创立初心 / 红线"等核心约定散在多 ADR → 提炼到 context-loader skill
- 项目内若发现 "经验 / 教训 / 反模式" 散落 → 提炼到 lessons + 设 auto_load: true
