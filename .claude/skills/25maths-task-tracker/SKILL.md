---
name: 25maths-task-tracker
description: ADR-0068 task execution workflow. Locks tasks across sessions (.task-locks.json), auto-syncs status to v3 plan, triggers lesson check, suggests next steps. Invoke `/25maths-task-tracker` for status report or auto-runs on task claim/done.
---

# 25Maths Task Tracker

## 用途
多 session(多个 Claude 账号 / 多个窗口)安全跟踪 v3 plan task 执行。**避免重做 / 漏做 / 冲突**。

## 4 阶段 workflow(ADR-0068)

### Phase 1 · Claim task(开始前)

```bash
# 1. Sync latest
git pull

# 2. Check lock
python3 scripts/task-tracker.py status TASK-NNN
# 输出:
#   ⏳ available · ok to claim
#   🔄 in-progress · sessionA · started 2h ago · SKIP
#   ✅ done · 2026-04-26 · SKIP
#   💀 stale · 35h old · takeover allowed

# 3. Claim
python3 scripts/task-tracker.py claim TASK-NNN
# Writes .task-locks.json + commit + push
```

### Phase 2 · Work on task

正常做 task · 不需特殊步骤(commit 频率自由)

### Phase 3 · Done(完成后)

```bash
python3 scripts/task-tracker.py done TASK-NNN --commit <sha>
# 1. Updates .task-locks.json status: done + completed_at + commit
# 2. Calls scripts/update-task-status.py (sync v3 plan TASK 表)
# 3. Triggers session-summarizer · check if LESSON candidate
# 4. Suggests next-step (read EXECUTION_DECOMPOSITION_PLAN.md dependents)
# 5. Commits + push all updates
```

### Phase 4 · Stale recovery(任意 session)

如果发现 in-progress 但 > 24h 老:
```bash
python3 scripts/task-tracker.py release TASK-NNN
# Marks as stale · allows takeover
```

## Cache hit 验证(每 task claim 前自动)

invoke 时:
1. `grep -i <task-keywords> lessons/INDEX.md` → 找相关 lesson
2. `grep TASK-NNN EXECUTION_DECOMPOSITION_PLAN.md` → 找已 decomposed micro-step
3. 输出"已有先验:[lesson + micro-step] · 可直接套用"

## Status 报告(`/25maths-task-tracker` 调用)

```
当前 .task-locks.json 状态:
  in-progress: 2 (TASK-024 sessionA · TASK-117 sessionB)
  done this week: 5 (TASK-018, 031, 090, 127, 128)
  stale: 0
  待 NZH 决策(A 区): 5
  Claude 可立即跑(B 区 unblocked): 3

最近 lesson candidates:
  LESSON-007 draft (auto_load: false · 等 NZH review)

下一步建议:
  TASK-024 sessionA 70% 完成 · 预计 2h 后 done
  TASK-117 sessionB 等 ADR-0062 NZH confirm 才能进
```

## 与其他 skills 协同

- 调 `25maths-cache-optimizer` 保 cache 健康
- 触发 `25maths-session-summarizer` 写 LESSON
- 读 `25maths-context-loader` 提供的 charter / 红线

## Cross-account 可移植

- `.task-locks.json` git committed · 任何账号 git pull 即得最新
- skill 本身 repo-committed · 跨账号一致行为
- session_id 用账号标识 · 不冲突

## NZH 视角(简化)

NZH 平时不需调:
- 看 `python3 scripts/task-tracker.py status` 即知本周进度
- 看 `git log --grep "TASK-.* done"` 即知做完什么
- 看 lessons/INDEX.md 即知新 lesson(月度 review)
