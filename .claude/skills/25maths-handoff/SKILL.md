---
name: 25maths-handoff
description: 多 Claude 账号交接专用 · session start / end / 限额触发 / master.lock 协议 · 5KB cache · invoke `/25maths-handoff`
auto_load: false
---

# 25maths-handoff · 多账号无缝交接

> NZH 立法 2026-05-01 · 限额是常态 · 任一账号必能 5 KB 内上手 · 永不丢 in-flight 工作

## 触发场景

| 场景 | 用 |
|---|---|
| 新账号启动 | `/25maths-handoff` 自动跑 onboard 6 步 |
| 当前账号限额预警 | 跑 wrapup 6 步 |
| 主心骨改前 | 跑 lock check |
| 主心骨改完 | 跑 lock release |

## A · Onboard 6 步(新账号 · ~60s · 统一序)

序与 `BOOT.md § 4` · `SESSION-STATE.md cache-warm checklist` · `CACHE-HANDOFF-ARCHITECTURE § 3` 完全一致。

```bash
PLAN=/Users/zhuxingzhe/Project/ExamBoard/25maths-planning
PRAC=/Users/zhuxingzhe/Project/ExamBoard/25maths-practice

# 0. git pull
cd $PLAN && git pull --rebase --quiet
cd $PRAC && git pull --rebase --quiet

# 1. BOOT.md(60s 上手单文件)
cat $PLAN/BOOT.md

# 2. V3_FINAL_CHEATSHEET(项目全貌)
cat $PLAN/V3_FINAL_CHEATSHEET.md

# 3. SESSION-STATE.md(上次位置 + 下步)
cat $PLAN/SESSION-STATE.md

# 4. SUBPLAN(下一步任务列表)
cat $PLAN/SUBPLAN-2026-05-01-NEXT.md

# 5. master.lock 检
[ -f $PLAN/master.lock ] && cat $PLAN/master.lock

# 6. MEMORY.md 索引(用户偏好)
head -50 /Users/zhuxingzhe/.claude/projects/-Users-zhuxingzhe/memory/MEMORY.md
```

读完即上手 · 不必重读 lessons / ADR(按需 grep)。

## B · Wrapup 6 步(限额触发)

```bash
# 1. 紧急 commit · 防丢
cd <repo> && git add -A && git commit -m "wip: <description>" && git push

# 2. 更新 SESSION-STATE.md
# 写入:Active branch · Last sealed timestamp · In-flight work(若有)· Next step

# 3. 释放 master.lock(若持有)
[ -f master.lock ] && rm master.lock && git add master.lock && git commit -m "release lock" && git push

# 4. 跑 audit guard rail
npm run audit:dimensions:strict 2>&1 | tail -3

# 5. 写 handoff fields(SESSION-STATE 末段)
# Session / Account / Theme / Commits / Sealed / Next

# 6. 通知用户:
# 'Account 即将限额 · 已 commit + push · SESSION-STATE 已写 handoff · 下账号读 BOOT.md 即上手'
```

## C · Master.lock 协议

**何时需要 lock**(改 planning 主心骨前):
- ✓ PROJECT_FUSION_PLAN_V3.md
- ✓ SUBPLAN-2026-05-01-NEXT.md
- ✓ lessons/INDEX.md
- ✓ CLAUDE.md / V3_FINAL_CHEATSHEET / BOOT.md
- ✗ q*.json / per-skill / per-lesson(已 isolated · 不需)

**协议**:
```bash
# 1. 检
[ -f master.lock ] && {
  cat master.lock
  # < 30 min 旧 · 等或 SendMessage 联系
  # > 30 min 旧 · 视为 stale · rm 接手
}

# 2. 立 lock(自家 account-id)
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) account-A scope=PROJECT_FUSION_PLAN_V3" > master.lock

# 3. 工作 · commit + push 改动

# 4. 释
rm master.lock
git add -A && git commit -m "feat: ... · release lock" && git push
```

**注**:`master.lock` 已入 `.gitignore` · 不入 git index · 仅本地存在 · push 时不传。
跨账号 lock 需通过 commit 一个 sentinel:
```bash
git commit --allow-empty -m "lock: account-A claims main · scope=X" && git push
# 完毕
git commit --allow-empty -m "unlock: account-A release · scope=X" && git push
```
新账号 git log 看最近 lock/unlock 即知。

## D · 限额预警 trigger

| 用户说 | 当前 token% | AI 行为 |
|---|---|---|
| "额度到 70%" | 70% | 不启大任务 · 每 section 立 commit · 不批量 |
| "快没额度了" / "85%" / "收尾" | 85% | 立即停 · 跑 Wrapup 6 步 · 0 新工作 |
| "wrapup" / "95%" | 95% | `bash scripts/emergency-wrapup.sh "本次做了什么"` 一行 |

## E · 防丢工作 SOP

- ✗ 不留半成品文件在工作区(Vite glob 扫描会破 build)
- ✓ commit 增量 · 每 1 section 完立即 commit + push
- ✓ stash 临时 · `git stash -u` 含 untracked
- ✓ 不批多 section 才 commit · 每 section 独立

## F · 跨产品同步触发

任一立 lesson / 改 SKILL.md / 改 BOOT.md 后:
```bash
cd /Users/zhuxingzhe/Project/ExamBoard/25maths-planning
python3 scripts/sync-skills-and-lessons.py
```
8 repos 自动同步 · 任一账号 clone 任一仓即得最新。

## G · 心法

> "限额是常态 · 不是异常。每个 commit 都假设 30s 后我会断。"
>
> "新账号读 5 KB 上手 · 比读 50 KB 走神快。BOOT.md = 60s · 永不重读历史。"
>
> "lock 不是 race condition 守门 · 是协作礼貌:别人在改我等等。"

## 配套立法

- **LESSON-021** · 真题数据卫生 + 多 Claude 协作 11 类坑
- **LESSON-022** · lesson 分发 5 步 pipeline
- **LESSON-023** · 多轮审计纪律 R1/R2/R3
- **CHANGE_GOVERNANCE.md** · 任一立法 sealed 须 ≥ 3 轮深审

## 单源 cache(不重复)

- DoD doctrine · 单源:`AUDIT_FRAMEWORK § 9`(其他文件交叉引)
- Cache 5 铁律 · 单源:`25maths-cache-optimizer/SKILL.md`(整改协议交叉引)
- 灵魂 5 问 · cache-anchor · 故意多处复(高频引用 · 不算冗余)
