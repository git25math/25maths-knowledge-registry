---
name: deploy 前必 grep prod RPC 名 · 同名不同 signature 也是命名污染
description: 2026-04-26 TASK-013 deploy 撞 prod 已存 get_next_step(uuid) EDX board 路由 RPC · 改 v1 避冲突 · LESSON-009/010 RPC 域强化
type: feedback
auto_load: true
---

# LESSON-012 · deploy 前必 grep prod RPC 名

## 触发场景

2026-04-26 TASK-013 部署 `get_next_step(uuid, text)`:

1. NZH 跑 deploy SQL · CREATE OR REPLACE FUNCTION 不报错(因签名不同 · 是 overload)
2. NZH 跑验收 query 调用 `get_next_step()` (0 args · 用 default)
3. PostgreSQL 抛 `ERROR 42725: function name "get_next_step" is not unique`
4. 诊断 query 揭示 prod 早有 **`get_next_step(p_user_id uuid)`** RPC(EDX board 路由)
5. 我的 2-arg overload 与 prod 1-arg 共存 · 0-arg 调用 ambiguous → 报错
6. 改名为 `get_next_step_v1` 避冲突 · 重 deploy 通过

## 问题

**LESSON-009 (grep v3 plan) + LESSON-010 (grep prod schema columns) 都覆盖** · 但 **RPC 名空间没覆盖**:

| LESSON | 域 | 命中 |
|---|---|---|
| 009 | TASK / ADR / Stage 综合 | ✅ |
| 010 | prod schema 列 + 表 | ✅ |
| **012**(本)| **prod RPC 名 + 签名** | **❌ 漏** |

PostgreSQL 允许同名 RPC overload(不同签名)· 但调用时 default 参数会引发 ambiguity。新 deploy 不报错(因 overload 合法)· 但调用层先 break。

## 规则

**Why**:RPC 名空间 = prod 隐式契约。任何 deploy 新 RPC 都可能撞 prod 已有 · 即使签名不同(因 default 参数引发 ambiguity)。LESSON-010 grep prod 表 / 列 · 但 RPC 域要单独 grep。

**How to apply**:

deploy 任何新 RPC 前必做 2 步:

1. **grep prod 同名 RPC**(NZH 在 SQL Editor 跑):
   ```sql
   SELECT proname, pg_get_function_arguments(oid) AS args, prosecdef
   FROM pg_proc
   WHERE proname = '<RPC_NAME>';
   ```

2. **若返回 ≥ 1 行 · 必须二选一**:
   - **A · 重命名为 v1 / v2 / 业务前缀**(推荐)· 例 `get_next_step` → `get_next_step_v1` 或 `practice_get_next_step`
   - **B · 看 body 是否你写的 · 是则 CREATE OR REPLACE 覆盖**(危险 · 可能破坏其他系统 · 必先 grep 调用方)

## 灵魂宪章关联(variant 1=1=1)

ADR-0040 灵魂红线 7:**variant_mastery 不降级到 unit/section 级**。RPC 命名 v1 / v2 同样语义:**版本独立**(类似 variant)· 不混用一个名字承担多语义。

## 反例(2026-04-26)

```
我:CREATE OR REPLACE FUNCTION get_next_step(uuid, text) ...
prod:已有 get_next_step(uuid) EDX board 路由 RPC
↓
2 个 overload 共存 · default 参数 ambiguity
↓
get_next_step() 调用 → ERROR 42725 not unique
↓
NZH 部署后才发现 · 重命名为 v1 重 deploy
```

## 正例(本 LESSON 立法后)

```
deploy get_next_step 前:
1. SELECT proname FROM pg_proc WHERE proname = 'get_next_step';
2. 命中 → 直接命名 get_next_step_v1
3. CREATE OR REPLACE FUNCTION get_next_step_v1(...) ...
4. 0 冲突 · 0 ambiguity
```

## 与 LESSON-007/008/009/010/011 的关系 · 铁六角

| LESSON | 阶段 | 防止 | 真相源 |
|---|---|---|---|
| 007 | 写 TASK 前 | 重复造 TASK | v3 plan TASK 表 |
| 008 | Beta 期决策 | 过早架构 commit | 真实痛点 |
| 009 | 立 ADR 前 | 重复治理 | v3 plan + Stages |
| 010 | 起 SQL 前(schema) | 错位列 / 表假设 | `information_schema.columns` |
| 011 | deploy 后 | git 与 prod 偏离 | 改名入仓 + DEPLOYED header |
| **012** | **deploy 前(RPC)** | **同名 RPC 撞 ambiguity** | **`pg_proc` WHERE proname** |

## 检查清单(每次新 RPC deploy 前)

- [ ] grep prod `pg_proc` 同名 RPC 命中?
  ```sql
  SELECT proname, pg_get_function_arguments(oid) FROM pg_proc WHERE proname = '<NAME>';
  ```
- [ ] 命中 0 → 直接 deploy
- [ ] 命中 ≥ 1 → 默认重命名为 v1 / 业务前缀
- [ ] 例外 · 已知是自己写的旧版 · CREATE OR REPLACE 覆盖前 grep 调用方(`grep -rn 'rpc(...<NAME>...' src/` 跨仓)
- [ ] deploy 后 LESSON-011 改名入仓 + DEPLOYED header

任一未做 → ambiguity 风险 / 命名污染。

## 同类扩展(未来 LESSON-013 候选)

- table 名空间(LESSON-010 已覆盖)
- index 名空间(若多个 schema 有同名 index 触发警告)
- trigger 名空间(prod 跨 schema 同名 trigger)
- view 名空间(view + table 同名冲突)

每次发现新命名空间冲突 → 起新 LESSON。
