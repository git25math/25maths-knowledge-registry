---
name: backend deploy ≠ user experience ship · 学生看不到 = 灵魂温度问 系统性漏洞
description: 2026-04-26 NZH 严正指出 7 个 prod schema deployed 但前端 0 wire-up · 学生体感 0 提升 · 立法升级 Definition of Done(DoD)
type: feedback
auto_load: true
---

# LESSON-013 · backend deploy ≠ user experience ship

## 🔴 核心铁律(NZH 2026-04-26 升级 · LESSON-013 哲学根基)

> **后端的所有优化 · 都是为了让前端有更好的体验。**
> **所有一切的后端功能 · 都要服务于前端的特定需求。**
> **没有前端明确需求的后端优化 = 无效。**
>
> **反向**:所有前端需求 · 都要通过后端来实现 · 而后端功能的架设必须要在前端将其作用发挥出来。
>
> **这是推动开发的动力。后端开发的最终点 = 前端更好地为用户服务。**

### 推论 1 · Frontend-Driven Development(FDD)

任何后端 TASK 起草前 · 必先回答 3 问:
1. **这个 backend 改动服务于哪个具体前端 feature?**
2. **这个前端 feature 服务于哪个具体用户场景?**(学生/教师/家长 在哪个屏幕做什么)
3. **没有这个 backend · 前端能做到吗?**(若能 · 后端是 over-engineering · 推迟)

任一答不出 · TASK 不许立 · 不许 deploy。

### 推论 2 · 反 anti-pattern · "未来可能用上"

❌ "现在加 belief 字段 · 未来某天加 UI"
❌ "先把 schema 都准备好 · 前端慢慢追"
❌ "RPC 先写 · 等前端组要时再 wire"

✅ "学生在 X 屏幕需要看到 Y · 所以加 backend RPC Z 服务这个 feature"

### 推论 3 · TASK 配对原则

每个 backend TASK 必有配对 frontend TASK · 同时排期 · 同时 ship。
- TASK-029 belief field(backend)+ TASK-029.f belief 学生反馈 UI(frontend)
- 两个同时 done · 才整体 done
- 拆分排期 = 制造孤儿 backend(LESSON-013 灵魂红线)

### 推论 4 · 验收必须从用户屏幕开始

不是从 supabase Editor 跑 RPC 看 jsonb · 而是:
1. 学生 / 教师 / 家长 真账号登录
2. 从某屏幕某按钮触发
3. 看到 UI 上的数据 / 反馈 / 状态
4. 灵魂 6 问全过(温度/声音/老师/三学生/走人/可见性)

backend RPC 跑通 = staging milestone · 不是 done。

---

## 触发场景(2026-04-26 严重事故)

1. NZH 跑 7 个 SQL deploy 全成功(belief / method_marks / pedagogy_etl / student_profile_v5 / phase0_remaining_4 / section_health / get_next_step_v1)
2. Claude 标 "TASK-013 / 021 / 026 / 028 / 038 / 014e / 029 ✅ deployed"
3. v3 plan 完成率 +18.5%
4. tag v3.26-7-sql-deployed
5. **NZH 问**:"这些改动在前端都有显示了吗?"
6. **真相**:11 个新能力中 **仅 3 个**(EDX 隐藏 / F1 / RouteEngine 表错配)前端可见 · **8 个 0 wire-up**
7. NZH 严正命名为"严重漏洞"

## 问题根本

**Claude 把"backend ready"等同于"task done"**。但灵魂宪章 ADR-0040 衡量标准是:**学生感知到 Δ 才算 done**。

| 阶段 | Backend | Frontend | 学生感知 | 是否 done? |
|---|---|---|---|---|
| Schema deployed | ✅ | ❌ | ❌ | **NO** |
| RPC exists | ✅ | ❌ | ❌ | **NO** |
| RLS policy | ✅ | ❌ | ❌ | **NO** |
| 前端调用 RPC | ✅ | ✅ | ❌(无 UI) | **NO** |
| UI 显示数据 | ✅ | ✅ | ✅ | **YES · 真 done** |

**Bug 根源**:Claude 报 ✅ 时只到第 3 阶段 · NZH 以为是第 5 阶段。**这是温度问红线触犯**(ADR-0040 红线 1)— "工程师以为完成 ≠ 学生感受到温度"。

## 规则 · Definition of Done(DoD)升级

**Why**:每个学生面 / 教师面 / 家长面的 backend 能力 · 必须有对应 UI wire-up 才算完成。否则只是"埋了个准备好的 schema 等永远不响"。这是**灵魂红线 1 反向**(反向论证 KPI 焦虑特性的镜像 — "为完成度数字而声称 done")。

**How to apply**:

### DoD · 6 步全过才算 ✅

```
1. backend schema deployed     · supabase 真有列/表/RPC
2. backend acceptance 通过     · spoof user 跑 RPC 返回正确 jsonb
3. backend → 入仓 migration    · LESSON-011 改名 + DEPLOYED header
4. frontend wire 调用方        · src/* 有 .rpc('<name>') 或 client SDK 调用
5. frontend UI 入口            · 学生 / 教师 / 家长 能看到 / 触发 / 点击
6. 灵魂温度自检 · NZH 用真实学生账号 → 5 灵魂问 5/5 通过
```

**任一未做 → TASK 必须保持 🟡 in-progress · 不许标 ✅。**

### TASK 状态升级

```
⏳ 未开始
🟡 backend ready(schema + RPC + acceptance · LESSON-011 入仓)
🔵 wired(frontend 调用 + UI 入口 · 但未灵魂自检)
✅ done(NZH 灵魂自检通过 · 学生真实感知到)
```

错位用 ✅ → LESSON-013 触犯。

## 验收第 7 维度(AUDIT_FRAMEWORK 升级)

之前 6 维度:功能一致性 / UI 一致性 / 产品质量 / 数学正确性 / 产品闭环 / 操作简易性。

**加 § 7 · 前端可见性(Visibility)**:
- 任何 prod backend 改动 · 必有学生 / 教师 / 家长 UI 入口
- "backend 已就位 · 前端待做"不是延期理由 · 是 task incomplete
- TASK 标 ✅ 必须截屏 / 录视频证明 UI 实际触发并展示数据

## 5 灵魂问扩展为 6 灵魂问

加 **第 6 问 · 可见性问**:**这个改动学生 / 教师 / 家长 在哪个屏幕的哪个按钮能看到?能描述具体 UI 位置吗?**

任一答不出具体 UI 位置 = task NOT done。

## 反例(2026-04-26)

```
TASK-029 belief 字段 + RPC deployed
↓
Claude:"✅ deployed 2026-04-26"
↓
v3 plan 标 ✅ · 完成率 +1
↓
NZH 问"前端有显示吗?"
↓
真相:UI 0 入口 · 学生从未触发过 RPC
↓
"完成度"是假的 · 学生感知 0
```

## 正例(本 LESSON 立法后)

```
TASK-029 backend deploy 后
↓
TASK 标 🟡 ready(不是 ✅)
↓
拆 sub-TASK:
  · 029.frontend.1 学生面 belief UI(失败题后弹 "感觉如何"三选)
  · 029.frontend.2 调用 submit_diagnosis_with_belief
  · 029.acceptance NZH 真账号测试看到 UI
↓
全部 done 后才能标 TASK-029 ✅
↓
NZH 灵魂自检 5/5 通过 · 学生看到 UI · 真 done
```

## 与铁六角的关系 · 升级铁七角

| LESSON | 阶段 | 防止 |
|---|---|---|
| 007 | 写 TASK 前 | 重复造 TASK |
| 008 | Beta 决策 | 过早架构 commit |
| 009 | 立 ADR 前 | 重复治理 |
| 010 | 起 SQL 前(schema) | 错位列假设 |
| 011 | deploy 后 | git 与 prod 偏离 |
| 012 | deploy 前(RPC) | 同名 ambiguity |
| **013** | **task 标 ✅ 前** | **backend ready ≠ user 感知 · DoD 漏洞** |

铁六角 → **铁七角**。

## 立即应用 · 修当前 7 个 prod deployed 状态

v3 plan 中:
- TASK-029 ✅ → 🟡 ready(belief schema + RPC · UI 0)
- TASK-026 ✅ → 🟡 ready(method_marks · UI 0)
- TASK-028 ✅ → 🟡 ready(pedagogy_etl · UI 0)
- TASK-038 ✅ → 🟡 ready(student_profile_v5 · UI 0)
- TASK-014e ✅ → 🟡 ready(7 表 schema · UI 0)
- TASK-021 ✅ → 🟡 ready(section_health · UI 0)
- TASK-013 ✅ → 🟡 ready(get_next_step_v1 · UI 0)

仅以下保留 ✅(真实 ship):
- TASK-018 EDX 隐藏 + F1(prod 立竿见影)
- TASK-140 RouteEngine 表错配修复(KnowledgeMap / Dashboard 真实数据)

## 立紧急 TASK-141 · M3 前端 wire-up sprint

**TASK-141 · 7 backend 能力前端 wire-up**(6-8d · M3 必做):

1. DerivationToasts 挂载(0.3d)
2. get_next_step_v1 Dashboard banner(1d)
3. submit_diagnosis_with_belief 失败后弹三选(0.5d)
4. get_section_health KnowledgeMap circle(0.5d)
5. submit_method_marks 教师批改 UI(2d)
6. student_profile_v5 家长月报页(1.5d)
7. export/delete GDPR 按钮(0.5d)

完成后才能 v3.26 → v3.27 · 否则停留 v3.26-backend-only。

## 立法本身的灵魂自检

- 温度 · ✅ 防 NZH 19 学生看不到工程"完成"的虚假温度
- 声音 · ✅ NZH 没说出口的内心 OS:"为什么我还看不到 belief 输入?"
- 老师 · ✅ "认真老师不只备课 · 还要走进教室看学生反应"
- 三学生 · ✅ 差/中/优都需 UI 入口才感知
- 走人 · ✅ 学生离开一周回来 · UI 能感知 backend 改动 · 不是空白
- **可见性(新)** · ✅ 本 LESSON 自身的 UI = INDEX 索引 + skills 注入 · 下次 session 启动必读

## 检查清单(每次 TASK 标 ✅ 前)

- [ ] backend schema / RPC deployed?(LESSON-011 入仓)
- [ ] backend acceptance 通过?(spoof 验收)
- [ ] **frontend 有 .rpc() / client 调用?**
- [ ] **frontend 有 UI 入口?**(学生/教师/家长能看到)
- [ ] **NZH 用真账号登录看到 UI?**(截屏 / 录像)
- [ ] 6 灵魂问全过(温度 / 声音 / 老师 / 三学生 / 走人 / 可见性)?

任一未勾 → 标 🟡 ready · 不标 ✅。
