---
name: Audit Protocol vs Intuition · 审查盲区元教训
description: 上轮 session 完成 60% checklist 后自评"完成",第三轮 meta-审查才发现 5 类盲区 — 协议化 checklist 必胜直觉化扫描
type: feedback
auto_load: true
---

# LESSON-024 · Audit Protocol vs Intuition · 审查盲区元教训

> 立法日期:2026-05-01 · 来源:Practice session 2026-05-01 三轮 meta-审查
> Sealed by:本会话第三轮发现 5 类上两轮漏掉的项

---

## 0. 上下文

Practice session 用户三次说"继续审查是否还有遗漏",第一/二轮我自评"全部通过",第三轮才暴露真实盲区。这条 lesson 复盘**为什么 checklist 之外的项总被忽略**。

---

## 一、本会话三轮审查的对照表

| 项 | 一轮 | 二轮 | 三轮(本)| 应在哪轮发现 |
|---|---|---|---|---|
| 5 金标准沉淀 | ✅ | - | - | 一轮 |
| handoff doc | ✅ | - | - | 一轮 |
| sub-plan FEEDBACK | ✅ | - | - | 一轮 |
| planning TASK-FB1/FB2 | ✅ | - | - | 一轮 |
| SESSION-STATE 更新 | ✅ | - | - | 一轮 |
| DEV-PLAN v2.100.0 段 | ✅ | - | - | 一轮 |
| planning SESSION_SUMMARY | ❌ | ✅ | - | **应一轮**(planning 仓已有此模式) |
| LESSON-021 立法 | ❌ | ✅ | - | **应一轮**(lesson 是 planning 主心骨产出) |
| 跨产品影响评估 | ❌ | ✅ 文字 | ✅ 真 grep | **应一轮**(根 CLAUDE.md 第七阶段强制) |
| 灵魂宪章对齐说明 | ❌ | ✅ | - | **应一轮**(ADR-0040 是产品最高优先级) |
| OPEN PR 列入 SESSION-STATE | ❌ | ❌ | ✅ | **应一轮**(handoff-check 第 7 项警告) |
| package.json 版本号同步 | ❌ | ❌ | ✅ 注意到 | **应一轮**(根 CLAUDE.md 第二阶段) |
| Frontmatter 协议(lessons) | ❌ | ❌ | ✅ | **应一轮**(lessons 仓已有 yaml 协议) |
| CONTRIBUTING.md 引用规则不适用本仓 | ❌ | ❌ | ✅ | **应一轮**(规则差异化) |
| LESSON-024 meta-lesson | ❌ | ❌ | ✅ | 三轮才会浮现 |

**洞察**: 在二轮才发现一批,在三轮还能发现一批,且**没有一项是新生的**——全是一轮就该发现但被跳过。

---

## 二、5 类盲区根因分析

### 2.1 盲区 #1 · "完成主任务" 当成 "全部完成"
**症状**: 一轮我做完用户原始要求的核心交付(handoff / 5 金标准 / sub-plan / DEV-PLAN / planning sync),自评"完成"。

**根因**: 没把根 CLAUDE.md 的"7 阶段交接协议 15 步"逐项过一遍。审查模式是**生成式**(我想到什么写什么),而非**协议式**(checklist 逐项打勾)。

**纠正**: 任何 session 收尾**强制**把根 CLAUDE.md "对话结束交接"7 阶段 15 步贴到 TodoList,逐项打勾。

### 2.2 盲区 #2 · "本仓没有就跳过"导致规则差异化忽略
**症状**: 根 CLAUDE.md 第六阶段说"每个文档要 ≥ 1 次 CONTRIBUTING 引用",我去 grep 全为 0,本能反应是"我违规了",但实际本仓**没有 CONTRIBUTING.md**(用 CLAUDE.md 替代)。

**根因**: 没识别"通用规则 vs 本仓规则"差异,直接套用根模板检查。

**纠正**: 跑根协议检查时,**先看本仓有没有对应文件**。若没有,看 CLAUDE.md 是否声明替代品,作为本仓规则。

### 2.3 盲区 #3 · "并行 session 已做"以为不用做
**症状**: 一轮我跑 git push 报"nothing to commit"反复,以为别人已 commit。但实际 SESSION_SUMMARY、LESSON、跨仓更新等**没有**被并行 session 做,只是我在不同分支。

**根因**: "git status clean" 被错误等价于"all done"。

**纠正**: 协议化收尾**先列待交付清单**(N 个文档 / N 个版本号 / N 个跨仓更新),逐项确认每件落到哪个 commit。

### 2.4 盲区 #4 · "前置文档协议未读"导致 frontmatter 缺失
**症状**: 我创建 LESSON-021 没写 frontmatter(name/description/type/auto_load),并行 session 给我加了。

**根因**: 进入 lessons/ 目录写新文件前,没 sample 既有 LESSON-* 看格式。

**纠正**: 进任何**已有命名规律**的目录前,先 `head -10` 一个既有同类文件,识别 frontmatter / 模板 / 命名约定。

### 2.5 盲区 #5 · "OPEN 但非自己的 PR"被忽略
**症状**: SESSION-STATE 只列了我自己 ship 的 PRs(615-623),漏了仓内仍 OPEN 的 #613/#614。handoff-check 第 7 项已警告但被忽略。

**根因**: handoff = "全仓状态",不是"我的工作日志"。我把它当后者写。

**纠正**: SESSION-STATE 必含**当前 OPEN PR 全表**(不论提交人),这是给接手者的"仓的状态"。

---

## 三、协议化审查 SOP(本会话三轮经验固化)

### 3.1 三层 checklist
```
L0 主任务 checklist          ← 用户原始指令的字面项
L1 根 CLAUDE.md 协议           ← 7 阶段 15 步
L2 仓本身规则(本仓 CLAUDE.md)← 仓内独立规则
```

每收尾必三层逐项打勾,**用 TodoList 显式跟踪**。

### 3.2 每轮收尾前的强制 5 问
1. **Frontmatter / 命名 / 目录**:我创建的文件遵守该目录既有协议吗?(`head -10` 一个既有同类)
2. **跨产品**:我改的接口/字段/schema 在其他仓 grep 真有 0 引用吗?(不是文字推断)
3. **版本号同步**:package.json / config.js / DEV-PLAN 三处是否同步?
4. **OPEN PR / 进行中 task**:handoff 是否包含全仓状态而非我的工作日志?
5. **协议差异化**:本仓有该规则的对应文件 / 替代品吗?

### 3.3 自动化辅助
```bash
bash scripts/handoff-check.sh   # 仓既有 7 项 health check
gh pr list --state open --limit 10  # 全仓 OPEN PR
diff <(grep "version" package.json) <(grep "package " docs/DEVELOPMENT-PLAN.md)
```

---

## 四、应用到 25maths 项目群

| 仓 | 协议层 |
|---|---|
| games-legends | docs/CONTRIBUTING.md(主要)+ CLAUDE.md |
| Keywords / examhub | feedback memory + CLAUDE.md |
| practice | CLAUDE.md(无 CONTRIBUTING)+ docs/golden-standards/(本会话立) |
| website | minimal + Jekyll standard |
| dashboard / video-engine | CONTRIBUTING.md + CLAUDE.md |

进入新仓前先:
```bash
ls CLAUDE.md docs/CONTRIBUTING.md docs/golden-standards/ 2>&1
```
识别本仓的协议层。

---

## 五、Lesson 引用矩阵

- LESSON-021 paper data hygiene + multi-claude · 同期前置 lesson(技术教训)
- LESSON-019 / LESSON-020 · 同期 UI 净化 lesson
- 本 lesson(LESSON-024)= **元教训**:复盘 LESSON-019/020/021 三轮才完整的过程
- LESSON-001 charter sync awk failure · 早期同样反映"协议被跳过"

---

## 六、最高一句话

> **审查不是直觉,是协议**。每收尾用 TodoList 把 L0 + L1 + L2 三层显式打勾,才能保证遗漏率趋零。

---

*LESSON-024 v1.0 · sealed 2026-05-01 · 元教训 · 任何 session 收尾必读。*
