---
name: 立新 ADR 前 grep v3 plan + Stages 综合 · 防重复治理
description: 2026-04-26 ADR-0073 撤回反思 · v3 plan 已明文存在 6 视图正交注册表 + 5 对应 TASK · 立新 ADR 是重复治理
type: feedback
auto_load: true
---

# LESSON-009 · 立新 ADR 前先 grep v3 plan

## 触发场景

2026-04-26 ADR-0073 起草过程:

1. Stage 5.3 发现 ADR-0008 三视图不够 · 需要 diagnostic + product 第 4-5 视图
2. Claude 起草 ADR-0073 Draft 框架(140 行)· 含三决策点供 NZH 填
3. NZH 让综合分析 · Claude 重新 grep v3 plan
4. 发现 v3 plan 第 86 行已明文存在 **6 视图正交注册表**:
   - engine.L1-L8 + repo.L1-L4 + practice.L0-L4(原)
   - **diagnostic.L1-L6 + product.L1-L5 + stakeholder.L1-L6**(新)
5. 5 个对应 TASK 已就位(TASK-029/013/038/037/121)
6. **结论**:ADR-0073 撤回 · ADR-0008 加 1 行修订即覆盖
7. 节省:1 个 ADR 立法成本 + NZH 30 min 决策时间

## 问题

**Stage 综合产出 ≠ ADR 立法**。

Claude 默认倾向:
- 看到 Gap → 起草 ADR
- 起草 ADR → 写决策点框架
- 写决策点 → 让 NZH 拍板

但实际:
- 多数 Gap **早已在 v3 plan / Stages 累积成果中被记录**
- 框架是重复 · NZH 拍板成本是浪费
- 真正需要的:**1 行修订指向已有真相源**

## 规则

**Why**:v3 plan(137 TASK + 视图机制行 + 5 累积 stages 成果)是 25Maths 的 **operational truth source**。立新 ADR 前若不先 grep · 极易重复治理。LESSON-007 防 TASK 重复 · LESSON-008 防架构过早 commit · 本 LESSON 防 ADR 立法重复。

**How to apply**:

立新 ADR 前必做 3 步:

1. **grep v3 plan**:
   ```bash
   cd 25maths-planning
   grep -E "<关键词>" PROJECT_FUSION_PLAN_V3.md
   ```
   关键词例:`视图`, `belief`, `diagnostic`, `product`, `角色`, `KP ID`

2. **grep RESEARCH_STAGE*.md + SYNTHESIS_*.md**:
   ```bash
   grep -E "<同关键词>" RESEARCH_STAGE*.md SYNTHESIS_*.md
   ```
   多数 Gap 在 Stage 综合时已分类 · 已分配 TASK 编号

3. **grep ADR 注册表**(若有):
   ```bash
   ls 25maths-os/decisions/ | grep -i "<主题>"
   ```

**任一命中 → 优先选** "1 行修订指向已有真相源" · 而非立新 ADR。

## 反例(2026-04-26 第一版)

```
Stage 5.3 发现"三视图不够"
  → Claude 起草 ADR-0073 Draft(140 行)
  → 含三决策点 § 2.1-2.3
  → 让 NZH 填 30 min
  → NZH 综合分析后撤回
```

## 正例(2026-04-26 修正)

```
Stage 5.3 发现"三视图不够"
  → grep v3 plan "视图"
  → 命中"6 视图正交注册表"
  → grep TASK · 命中 TASK-029/013/038/037/121
  → ADR-0008 加 1 行修订指向 v3 plan
  → ADR-0073 撤回
  → 0 NZH 决策时间
```

## 同类 LESSON 关联

- **LESSON-007**:多 stage 综合先做 v3 plan TASK inventory(防重复 TASK)
- **LESSON-008**:Beta 期不解决"未来痛点"(防过早架构 commit)
- **LESSON-009**:立新 ADR 前 grep v3 plan + Stages(防重复治理)

三者共同主旨:**v3 plan + Stages 累积成果 = operational truth source · 任何新 artifact 立法前必先 grep**。

## 检查清单(每次 ADR 提议前问自己)

- [ ] 已 grep v3 plan 关键词?
- [ ] 已 grep RESEARCH_STAGE*.md + SYNTHESIS_*.md?
- [ ] 已 grep 现有 ADR 注册表?
- [ ] 真相源已存在? → 1 行修订指向 · 不立新 ADR
- [ ] 真相源不存在 + Beta 期 prod 不 break? → 推迟到 MN(LESSON-008)
- [ ] 真相源不存在 + 真实痛点 + Beta 期就需要? → 才立新 ADR

任一勾选 "已存在" → 优先 1 行修订。
