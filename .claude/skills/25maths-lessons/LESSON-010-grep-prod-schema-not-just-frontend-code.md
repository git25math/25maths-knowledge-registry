---
name: 起 schema artifact 前必须 grep prod migration · 不能信任 frontend 代码字段
description: 2026-04-26 TASK-029 deploy 时发现 5 个 SQL drafts 全部基于错误 schema 假设 · 因为 grep 了 RouteEngine.ts 而不是 supabase migrations · LESSON-009 的强化版
type: feedback
auto_load: true
---

# LESSON-010 · grep prod schema · 不信任 frontend 代码字段

## 触发场景

2026-04-26 TASK-009 v2 第二轮 grep:

1. Claude grep `RouteEngine.ts` line 116:
   ```typescript
   .from('meta_node_progress').select('kn_id, mastery_score, flm_state, next_review_at')
   ```
2. Claude **基于此**起草 9 SQL drafts · 全部假设 prod `meta_node_progress` 表 4 字段如上
3. NZH 启动 TASK-029 deploy 时再 grep · 发现真相:
   - **真实 prod schema**(根目录 `FIX_20260416-141916_cloud_analytics_schema.sql`):
     - PK `(user_id, kn_id, source)` · **不是** `(user_id, kn_id)`
     - 字段是 `score / attempt_count / correct_count / last_updated`
     - **`mastery_score` 不存在** · 是 `score`
   - 后续 hot-patch(`FIX_20260416-144720`)加 `flm_state + next_review_at`
   - 但 `mastery_score / total_attempts / updated_at` **未在 git 中** · 可能是 dashboard 手改 prod
4. 结果:**5 个 SQL drafts**(belief / section_health / next_step / student_profile / recovery_pack)**全部基于错误前提**
5. NZH 不能直接 deploy · 必须先 SQL editor 跑 `information_schema.columns` 确认 prod 真实列

## 问题

**Claude 信任了 frontend 代码当作 schema 真相源** · 实际:

| 真相源 | 可信度 | 原因 |
|---|---|---|
| `RouteEngine.ts .select(...)` | ❌ 低 | 可能查不存在的列 · supabase 报 400 但 frontend silent fail |
| 仓根目录 `FIX_*.sql` | 🟡 中 | hot-patch 历史 · 但可能未全跑 prod |
| `supabase/migrations/*.sql` | 🟡 中 | 标准 migration · 但本仓 hot-patch 在根 · 不在 migrations |
| `information_schema.columns`(supabase prod 直查)| ✅ 高 | **唯一权威** |

## 加剧因素 · 多 worktree

NZH 习惯多 worktree(`25maths-practice` / `-checklist` / `-exam-fix`)· 都指向同一 GitHub repo · 但本地 working tree 不同 · grep 单一 worktree 可能漏。

## 规则

**Why**:Schema 真相在 supabase prod · 不在 git。Hot-patch / dashboard 改 / 多 worktree 副本都让 git 不再是 single source of truth。Frontend 代码字段是"程序员希望存在的列"· 不是"prod 真实存在的列"。

**How to apply**:

起 SQL 改动 / schema 假设 artifact 前必做 4 步:

1. **grep 多 worktree CREATE/ALTER**:
   ```bash
   cd ~/Project/ExamBoard
   grep -rn "CREATE TABLE.*<table_name>\|ALTER TABLE.*<table_name>" --include="*.sql"
   ```
   不限 `supabase/migrations/` · 看仓根目录 + 跨 worktree。

2. **不信 frontend `.select()`**:
   - `RouteEngine.ts / sync.ts / Dashboard.tsx` 写的字段 ≠ prod 真实字段
   - frontend 可能查不存在的列 · supabase 默认 silent fail / 仅 console error
   - 仅作"代码意图"参考 · 不作 schema 决策依据

3. **要 NZH 跑 `information_schema.columns`**(deploy 前):
   ```sql
   SELECT column_name, data_type, is_nullable, column_default
   FROM information_schema.columns
   WHERE table_name = '<table>' AND table_schema = 'public'
   ORDER BY ordinal_position;
   ```
   这是**唯一权威**真相源。

4. **PK 也必须确认**:
   ```sql
   SELECT a.attname
   FROM pg_index i
   JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
   WHERE i.indrelid = '<table>'::regclass AND i.indisprimary;
   ```
   `ON CONFLICT (...)` 必须匹配真实 PK · 否则 deploy 失败。

## 反例(2026-04-26 第一版)

```
grep RouteEngine.ts:
  .from('meta_node_progress').select('mastery_score, flm_state, next_review_at')
  ↓
Claude 起 9 SQL drafts:
  - 假设 mastery_score 列存在(错 · 真名 score)
  - 假设 PK (user_id, kn_id)(错 · 真 PK 含 source)
  - 假设 updated_at(错 · 真名 last_updated)
  ↓
TASK-029 deploy 时 NZH 卡住
```

## 正例

```
起 SQL 前:
  grep -rn "CREATE TABLE.*meta_node_progress\|ALTER TABLE.*meta_node_progress" --include="*.sql"
  ↓ 找到 FIX_20260416-141916 + 144720
  ↓ schema 真相:(user_id, kn_id, source) PK · score (非 mastery_score)
  ↓ 让 NZH 跑 information_schema.columns 确认 prod 当前真状态
  ↓ 起 SQL · 用真实字段名 + 真实 PK
```

## 与 LESSON-009 的关系

- **LESSON-009**:立新 ADR 前 grep v3 plan + Stages 综合 · 防重复治理
- **LESSON-010**:起 schema artifact 前 grep migrations + 跑 information_schema · 防错位假设

LESSON-010 是 LESSON-009 在 schema 域的强化版。

## 同类 LESSON 关联

- **LESSON-007**:多 stage 综合先做 v3 plan TASK inventory
- **LESSON-008**:Beta 期不解决"未来痛点"
- **LESSON-009**:立新 ADR 前 grep v3 plan + Stages
- **LESSON-010**:起 schema artifact 前 grep prod migration + information_schema(本)

四 LESSON 共同主旨:**任何 artifact 立 / 改 / deploy 前 · 必先 grep 真相源(不限 git · 含 prod schema)**。

## 检查清单(每次 SQL artifact 起草前)

- [ ] grep `CREATE TABLE.*<table>` 跨全部仓 worktree
- [ ] grep `ALTER TABLE.*<table>` 找全部 patch 历史
- [ ] **NZH 在 supabase SQL editor 跑 information_schema.columns**(若 deploy 前)
- [ ] 确认 PK 字段(`pg_index` query)
- [ ] 字段名 / 类型 / 默认值 / NOT NULL 全部对照 prod
- [ ] 不信 frontend `.select()`(可能查不存在的列)

任一未做 → 不许 deploy。

## 立法本身的灵魂自检

- 温度 · ✅ 救 NZH 不被 deploy 失败的挫败感
- 声音 · ✅ 学生没说"我要 schema 一致" · 但 prod break = 学生体验崩
- 老师 · ✅ "认真的老师备课不靠记忆 · 一定翻教案"
- 三学生 · ✅ 19 学生数据安全(防 ALTER 失败 + rollback 灾难)
- 走人 · ✅ deploy 干净 · NZH 心安
