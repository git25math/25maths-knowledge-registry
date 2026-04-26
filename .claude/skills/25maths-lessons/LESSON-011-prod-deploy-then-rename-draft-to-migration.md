---
name: prod deploy 后 _DRAFT 必须改名入仓 migration · "跑过了" ≠ "入历史了"
description: 2026-04-26 M2 Phase 1 5 个 schema deploy 后未改名 _DRAFT_ 时间戳 · 下次 session grep migrations/ 0 命中误判 · LESSON-009 在 deploy 落地阶段的强化
type: feedback
auto_load: true
---

# LESSON-011 · prod deploy 后 _DRAFT 必须改名入仓 migration

## 触发场景

2026-04-26 M2 Phase 1 部署完 5 个 SQL drafts:

1. NZH 在 Supabase SQL Editor 跑 deploy SQL ✅ prod 已生效
2. ❌ Claude 没把 `_DRAFT_*.sql` 改名为 `20260YYY_*.sql` 时间戳格式
3. ❌ Claude 没在 commit message 标 "已 deployed"
4. 半小时后 NZH 在新 session 跑 LESSON-009 grep `practice_node_progress` 在 `supabase/migrations/` · **0 命中**
5. 新 session Claude 误判 "表不存在 · 部署阻塞" · 险些重新建表(若 IF NOT EXISTS 幂等才救)
6. 暴露:**git migrations 历史与 prod 实际 schema 严重偏离**

## 问题

**Claude 把 "deploy 完成" 等同于 "工作完成"** · 实际:

| 阶段 | 完成 ≠ 完成 |
|---|---|
| SQL 在 prod 跑成功 | "prod 完成" ≠ "git 完成" |
| `_DRAFT_*.sql` 还叫 DRAFT | future grep 看不到这是 deployed |
| 没标时间戳 | future deploy 顺序无依据 |
| 没 commit message 标 deployed | git log 不可读 |

LESSON-009 主旨:**git 不是 single source of truth**(prod 可能偏离)。LESSON-010:起 SQL 前 grep prod schema。**LESSON-011 是闭环**:**deploy 后必须把 prod 真相回流到 git**。

## 规则

**Why**:每次 prod 跑 SQL 而不入仓 = 给未来自己挖坑。下次任何 Claude(或 NZH 自己)grep migrations/ 都被误导。LESSON-009 说"deploy 前先 grep" · 但若 deploy 后不入仓 · grep 永远落后 prod。

**How to apply**:

每次 SQL deploy 后必做 4 步:

1. **改名** `_DRAFT_*.sql` → `20260YYYMMDDHHMMSS_<topic>.sql`(标准时间戳)
   ```bash
   git mv _DRAFT_belief_field_and_diagnosis_rpc.sql 20260426100000_belief_field.sql
   ```

2. **加 header 注释**(每个改名文件首行):
   ```sql
   -- DEPLOYED to prod 2026-MM-DD by NZH (Supabase SQL Editor manual run)
   -- 重跑 idempotent · 全部 CREATE IF NOT EXISTS / ADD COLUMN IF NOT EXISTS / CREATE OR REPLACE
   ```

3. **Commit message 标 deployed**:
   ```
   TASK-XXX · <topic> prod deployed 2026-MM-DD
   - prod schema 改动:<列表>
   - 入仓 migration:20260YYY_*.sql(LESSON-011 治理)
   - backup:backup_2026_MM_DD.<table>(留底)
   ```

4. **未 deploy 的 drafts 保留 `_DRAFT_` 前缀**(区分清晰)
   ```
   ✅ 20260426100000_belief_field.sql       (已 deploy)
   ⏳ _DRAFT_section_health_rpc.sql         (待 deploy · M3)
   ```

## 反例(2026-04-26)

```
NZH 跑 deploy SQL → prod 已生效 ✅
↓
Claude 改 PROJECT_FUSION_PLAN_V3.md 标 ✅ → commit
↓
但 _DRAFT_belief_field_and_diagnosis_rpc.sql 还是这个名字
↓
新 session grep practice_node_progress in migrations/ → 0 命中
↓
新 session Claude 判 "表不存在" → 险些重建表
```

## 正例(本 LESSON 立法后 · 2026-04-26 修正)

```
NZH 跑 deploy SQL → prod ✅
↓
Claude:
  1. git mv _DRAFT_belief_field_and_diagnosis_rpc.sql 20260426100000_belief_field.sql
  2. 加 header 'DEPLOYED 2026-04-26 · idempotent'
  3. commit "TASK-029 ✅ deployed · 入仓 migration"
↓
新 session grep migrations/ → 命中 20260426100000_belief_field.sql
↓
新 session Claude 看 header 知道已 deploy · 不重建
```

## 与 LESSON-007/008/009/010 的关系

四个 LESSON 是**防错位治理铁五角**:

| LESSON | 阶段 | 主旨 |
|---|---|---|
| 007 | 写 TASK 前 | grep v3 plan 防重复 TASK |
| 008 | Beta 期决策 | 不解决未来痛点 · 推迟过早架构 |
| 009 | 立 ADR 前 | grep v3 plan + Stages 防重复治理 |
| 010 | 起 SQL 前 | grep prod schema 防错位假设 |
| **011** | **deploy 后** | **改名入仓 · 防 git 与 prod 偏离** |

闭环:Plan(007)→ Defer judiciously(008)→ Govern(009)→ Pre-deploy verify(010)→ Post-deploy retain(011)。

## 检查清单(每次 SQL deploy 后)

- [ ] `_DRAFT_*.sql` 改名为 `20260YYYMMDDHHMMSS_*.sql`
- [ ] 文件首行加 `-- DEPLOYED to prod 2026-MM-DD by NZH` header
- [ ] 标注幂等性(CREATE IF NOT EXISTS / ADD COLUMN IF NOT EXISTS / CREATE OR REPLACE)
- [ ] backup schema 留底位置 commit message 注明
- [ ] v3 plan TASK 状态改 ✅ 含 'prod deployed YYYY-MM-DD'
- [ ] commit message 标 "prod deployed" 而非仅 "draft 完成"
- [ ] 未 deploy 的 drafts 仍保留 `_DRAFT_` 前缀(区分清晰)

任一未做 → 治理债 + 下次 session 误判风险。

## 立法本身的灵魂自检

- 温度 · ✅ 防 NZH 下次 session 看到 0 命中误判 · 节省排查时间
- 声音 · ✅ NZH 没说"我要 git 一致性" · 但治理稳定 = 信任
- 老师 · ✅ "认真备课写教案 · 不靠记忆"
- 三学生 · N/A(治理 LESSON)
- 走人 · ✅ Future Claude 任何账号接手都能凭 git 知道 prod 真相
