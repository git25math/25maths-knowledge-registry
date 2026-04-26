---
name: 25maths-orchestrator
description: ADR-0069 master terminal. Issues commands to executor terminals via .agent-bus/queue. Reads results · decides next step. NZH 在主 terminal 用此 skill 控制后台执行。Cross-account portable.
---

# 25Maths Orchestrator(主终端 skill)

## 用途
NZH 想"分派 task 给后台 · 自己继续主对话 · 等结果再决策"时使用。

## 4 个核心动作

### 1 · 分派 task
```bash
python3 scripts/agent-message-bus.py write_cmd TASK-018 implement \
  --context "Fix prod F1 死循环 + F2 EDX 空白 · 详见 ADR-0018" \
  --priority P0
```
- 写 `.agent-bus/queue/TASK-018.cmd.json` + atomic commit + push
- 执行终端 listen 即见

### 2 · 检查 pending
```bash
python3 scripts/agent-message-bus.py list_pending
```
- 显示所有未完成的 cmd 状态

### 3 · 读取结果
```bash
python3 scripts/agent-message-bus.py read_result TASK-018
```
- 显示 result.json · 含 status / artifacts / next_suggested

### 4 · 取消
```bash
python3 scripts/agent-message-bus.py cancel TASK-018
```
- 写 cancel 文件 · 执行终端见即停

## NZH 真实工作流示例

```
NZH 主终端(Claude session A):
NZH: "我要做 TASK-018 prod bug fix · 派给执行终端"

主 Claude:
  好。先 read ADR-0018 + V3_FINAL_CHEATSHEET 的相关上下文。
  然后写 cmd:
  
  $ python3 scripts/agent-message-bus.py write_cmd TASK-018 implement \
    --context "Fix prod F1/F2 bugs · 详见 ECOSYSTEM-ANALYSIS · NZH 已授权 prod fix" \
    --priority P0
  ✅ Wrote command for TASK-018 · pushed to origin

NZH: "好,等结果"

主 Claude: 你可以继续做其他事 · 我每隔几分钟 check 一次。
            (或者 NZH 说"check now"再 read_result)

(执行终端跑 ~30 min)

NZH: "结果如何?"

主 Claude:
  $ python3 scripts/agent-message-bus.py read_result TASK-018
  {
    "task_id": "TASK-018",
    "status": "success",
    "summary": "F1 修复 + F2 EDX 静态页 placeholder · 19 学生测试无回归",
    "artifacts": [
      "25maths-website/membership/index.html",
      "25maths-website/_data/releases.json"
    ],
    "next_suggested": "TASK-024 考局隔离运行时"
  }
  
  评估:执行良好 · 灵魂层无触犯 · 建议下一步 TASK-024。NZH 同意?
```

## 决策权限(ADR-0064 governance)

主 terminal 主控:
- L4 永不改 · L3 战略:仅 NZH 决策 · 主 Claude 不替决
- L2 架构:主 Claude 可起草 · NZH 5-10 min review
- L1 可频繁:主 Claude 自决

## 与其他 skills 协同

- **task-tracker**:执行终端用 · 主 terminal 仅查 status
- **session-summarizer**:主 Claude 整合 result + 写 SESSION_SUMMARY
- **lessons**:整合后写 LESSON candidates(若任务有教训)
- **cache-optimizer**:cmd / result 文件结构 friendly · 自然 cache hit

## NZH 何时用此 skill

✅ 适合:
- 长任务(>2h)分派给后台 · NZH 不阻塞
- 多任务并行(分派给多个执行终端)
- NZH 明确要求"看着进度"

❌ 不适合:
- 短任务(< 30 min)· 直接做更快
- 强交互调试 · 直接 Claude 主对话即可

## Cross-account / 多机器

`.agent-bus/queue/` git-committed · 任意机器克隆即得状态。
执行终端可在另一台机器(只要 git 同步)。
