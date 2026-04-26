---
name: 25maths-executor
description: ADR-0069 executor terminal. Listens for commands from .agent-bus/queue · claims task via task-tracker · executes · writes result. Cross-account portable.
---

# 25Maths Executor(执行终端 skill)

## 用途
后台 Claude session 跑长任务 · 不阻塞主对话。

## 工作流(执行终端开后即跑)

### 启动 listen
```bash
python3 scripts/agent-message-bus.py listen
# 持续 polling · 5 sec 间隔
# 自动 git fetch · auto ff-pull
# 见新 cmd 即提示 Claude 开始
```

或单次检查:
```bash
python3 scripts/agent-message-bus.py listen --once
```

### 见到新 cmd 后(Claude 自动跑)

```
📨 New command: TASK-018
   command: implement
   context: Fix prod F1 死循环...
   issued_by: master-session-A
   → Claude 应该开始:read full cmd · execute · write result
```

Claude 跑:
```python
# Pseudo-code (Claude 自动做):
1. cmd = read .agent-bus/queue/TASK-018.cmd.json
2. python3 scripts/task-tracker.py claim TASK-018
   (失败 = 其他 session 已 claim · skip)
3. 执行 cmd.context 描述的工作
   (read 相关 ADR · cache hit 检 lesson · 5 灵魂问 · 13 红线)
4. python3 scripts/task-tracker.py done TASK-018 --commit <sha>
5. write .agent-bus/queue/TASK-018.result.json
6. git commit + push (atomic)
7. 继续 listen 下个 cmd
```

### Result 写法

```json
{
  "task_id": "TASK-018",
  "status": "success | partial | blocked | error",
  "summary": "1-3 sentences",
  "artifacts": ["file1.md", "file2.tsx"],
  "next_suggested": "TASK-024 or 完成",
  "completed_at": "2026-04-26T15:00:00Z",
  "executed_by": "executor-session-B"
}
```

### 取消信号
若 `.agent-bus/queue/<task-id>.cancel` 出现 · 立即停 + 写 result status: blocked + summary: "cancelled by master"

## Cache + Soul 自动遵守

执行任务时遵守(skills auto-load):
- **cache-optimizer**:5 铁律 + cache hit lesson grep
- **task-tracker**:claim/done atomic
- **context-loader**:灵魂宪章 + 13 红线 + 5 灵魂问 inject
- **session-summarizer**:每 task done 触发 LESSON candidate 检查

## NZH 角色

- 不直接交互执行终端
- 主终端写 cmd · 执行终端跑 · 结果回主
- NZH 仅在主终端决策

## Cross-account

执行终端可任意 Claude 账号 / 任意机器
- git pull 25maths-planning
- 起 listen
- 主终端写 cmd · 即触发

## 异常

| 异常 | 处理 |
|---|---|
| Cmd schema 不合 | 写 result status: error + summary 解释 |
| task-tracker claim 失败 | 写 result status: blocked + summary "already claimed" |
| Work 中崩溃 | task-tracker 状态留 in-progress · 24h 后 stale · 释放 |
| Push 冲突 | 自动 rebase + retry(`agent-message-bus.py` 内置)|
