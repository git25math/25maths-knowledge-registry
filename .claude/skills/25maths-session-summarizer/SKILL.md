---
name: 25maths-session-summarizer
description: Auto-extract lessons + write SESSION_SUMMARY at session end or when user says "总结" / "session 结束". Proposes 1-3 LESSON-NNN drafts to lessons/ dir. Cross-account portable.
---

# 25Maths Session Summarizer

## 用途
长 session(> 30 turns)或 user 显式触发时 · Claude 自动提炼经验 · 减轻 NZH 复述负担。

## 触发条件

### 自动
- session > 30 turns + 包含 ≥ 1 修复 / ADR 修订 / 红线触发
- 用户说"暂停 / 重新审视"(ADR-0064 § 8 escape hatch · 类 5.18-5.23 模式)

### 手动
- `/25maths-session-summarizer` · 用户主动调
- 关键词:"总结一下 · 写 session summary · 经验 / 教训"

## 输出 1 · `SESSION_SUMMARY_YYYY-MM-DD.md`

模板:
```markdown
# Session Summary · YYYY-MM-DD

## 解决的问题
(1-3 句话)

## 关键决策
- [ ] 新加 ADR-NNNN: 标题
- [ ] 修订 ADR-NNNN v2: 原因
- [ ] 加 TASK-NNNN: 内容

## 修订 / 修复
- 类型(schema / charter / 文档 / 红线)
- 触发 + 根因 + 修复
- 是否提炼 lesson? (LESSON-NNN draft)

## NZH 决策点(下次 session)
1. ...
2. ...

## Continue point(下 Claude 接手)
建议读:
- V3_FINAL_CHEATSHEET.md(60 秒)
- 本 SESSION_SUMMARY
- 其他相关 doc
```

## 输出 2 · 1-3 个 LESSON-NNN 草稿

按 ADR-0065 模板生成:
```markdown
---
id: LESSON-NNN  (next available)
title: 一句话总结
date: YYYY-MM-DD
category: schema-migration | red-line | ADR-revision | sync | test | feedback | meta
severity: 🔴 | 🟡 | 🟢
related_ADR: ...
keywords: [...]
auto_load: false  ← 默认 false · NZH review 后改 true 触发 sync
---

## Trigger context
## Symptom
## Root cause
## Fix
## Lesson
## Auto-detection (若有)
```

写到 `25maths-planning/lessons/LESSON-NNN-*.md` · NZH 月度 review 决定是否 sync(改 `auto_load: true` 即触发)

## 输出 3 · 给 NZH 的 review checklist(可选)

如果 session 含战略级决策:
```
NZH 30 sec review:
- [ ] ADR-XXXX 同意?
- [ ] LESSON-NNN draft 是否值得 auto_load?
- [ ] 下次 continue from where?
```

## Cross-account 可移植

skill 文件提交 git · 任何账号 clone 即得。
模板 / 触发条件 不依赖 user-specific memory。

## Cache-warm checklist(账号 B 接手必走 · 2026-05-01 加)

账号 A 限额 / 切换前 · 账号 B 接手时 · 让 B 不用从 0 重建心智模型:

```
1. git pull · git log --oneline -20      → 看最近 commit 主题
2. cat lessons/INDEX.md                  → 14 active lessons (≤ 100 行)
3. cat V3_FINAL_CHEATSHEET.md            → 60 秒战略全景
4. ls SUBPLAN-*.md | tail -1 | xargs cat → 当前活跃 subplan(本次 = SUBPLAN-2026-05-01-NEXT)
5. cat 最新 SESSION_SUMMARY_*.md          → 上 session 决策点
6. python3 scripts/task-tracker.py status → 锁状态 + 在跑 task
7. (跨仓时)读对应 L4 仓 CLAUDE.md + DEV-PLAN.md head 60 行
```

**铁律**:不要默认 read PROJECT_FUSION_PLAN_V3.md(763 行)· 仅 grep 关键词。Cache 友好顺序 = 短文件先 · 大文件按需。

每个 SESSION_SUMMARY 必含的 hand-off 字段:
- **Last good commit**: `<sha>` on branch `<name>`
- **Active subplan**: `SUBPLAN-YYYY-MM-DD-*.md`
- **Active lesson**: `LESSON-NNN-*` (本 session 衍生)
- **Cross-repo state**: practice@v?.??.0 / examhub@v?.?? / play@v?.?
- **Open ports**: 几个 sprint pending · 谁 blocking 谁

## 与 ADR-0064 escape hatch 配合

NZH 任何时候说"暂停 · 重新审视" → 此 skill 自动调用 + 写完整 PLAN_REALITY_CHECK style 文档(类 5.18 模式)。
