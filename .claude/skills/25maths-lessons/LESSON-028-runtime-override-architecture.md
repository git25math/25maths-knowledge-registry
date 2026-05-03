---
name: 运行时覆盖层 + 单源派生架构
description: HNZK 双源不同步事故沉淀 · localStorage→supabase→realtime 三层 · admin 在线编辑全字段 · 静态 JSON 作 fallback 真相 · 派生视图运行时合并 override
type: feedback
auto_load: true
---

# LESSON-028 · 运行时覆盖层 + 单源派生架构

> 立法日期:2026-05-03
> 来源:HNZK 模块 q17 子题未拆事故 + 双源不同步发现
> 沉淀:18 commits 一气推到端到端云端编辑闭环

---

## 0 · 触发故事(为何立此教义)

学生反馈:`hnzk-2025-q17` 单题视图正确(已拆 (1)(2) 子题),
**套卷视图却没拆**。排查发现:
- 单题视图读 `items/{year}/q*.json`(每题独立文件)
- 套卷视图读 `papers/{year}.json`(整套聚合 · 含 22 题副本)
- **同一道题数据存在两份** · 改单题文件没改聚合文件 → 不一致

更早一层事故:`hnzk-2024-q10` 考点编号错挂(`旋转 / 菱形` 但 by-type 视图归在 `抛物线`)
- 修复要改 q10.json + 重跑 derive 脚本 + 提交 + 部署 + 用户清缓存
- 一次小错位 → 5 步操作 → 再次发现错位时同样昂贵

NZH 立法:
> "可以做到自由组合,特别是作为修复技能这块应该是一个很好的工程基础"
> "云端,网页端,本地端三端同步"
> "如何架构,让以后的工作量不大"

---

## 1 · 五条铁律

### 铁律 1 · **数据真相源 ≤ 1 份**(no twin sources)

> 任何一道题、一份聚合数据,git 仓里**只能存在一份权威文件**。
> 所有派生视图(套卷/topical/by-type/by-kp/coverage)
> 在浏览器端从单源派生,不要落盘成第二份。

**违反典型**:
- ❌ `papers/{year}.json` 把 22 道题 stem 又复制了一份(已删除)
- ❌ `papers/by-hnzk-kp.json` 与 `coverage/hnzk-by-type-coverage.json` 各自命中表

**应做**:items/{year}/q\*.json 是真相;by-type / by-kp 在前端从 items + index 派生。

### 铁律 2 · **三层覆盖**(local → cloud → realtime)

```
Layer 0 · 静态 JSON(git · 部署冻结)
   ↑ 学生 fetch
Layer 1 · admin override(supabase · 三层同步)
   ↓ merge
Layer 2 · 最终视图(浏览器渲染)
```

实现栈:
- **localStorage 先**(即时反馈,offline 兜底)
- **supabase 后**(权威 · fire-and-forget upsert)
- **postgres realtime ws**(其他设备瞬间同步)

模板:`src/lib/hnzk/{kp,item}Overrides.ts`(两份 ~250 行 · 同模式可复用)

### 铁律 3 · **编辑发生在 git 之外**

学生体验侧的运营改动(打错考点、子题没拆、解答 OCR 污染)
**永远不应**让 admin 改 git push 部署。
对策:**前端编辑器 + supabase override 表**。

落地件:
- `KpEditDrawer` · 改 kp_ids 多选(从 355 kp 全大纲挑 · 含未挂题灰色)
- `ItemEditDrawer` · 改 stem / subparts / solution / 元数据 · 字段视图 + JSON 高级视图
- 撤销 = 删 supabase 行 → 自动回到静态 JSON

### 铁律 4 · **trigger SECURITY DEFINER + 主表门禁**

RLS trigger 写 history 表时被同表 RLS 挡了 = 经典坑。
解:trigger function `SECURITY DEFINER` 绕 RLS,
**主表写策略已守 admin allowlist** · 链路安全。

```sql
CREATE OR REPLACE FUNCTION foo_log_history()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER       -- ← 绕 history RLS · 链路由主表 admin 门禁守
SET search_path = public
AS $func$ ... $func$;
```

### 铁律 5 · **静态 metadata 学生不可见**

工程内部度量(`v3.0 · 8 单元 · 33 节 · 351 考点`)对学生是噪音 / 让界面像后台。
对 admin 是状态指示。

```tsx
subtitle={isAdmin ? `v${ver} · 8 单元 · ${kpCount} 考点` : undefined}
```

一个三元就分清,不必造两套页面。

---

## 2 · 实施模式(可复用 template)

### Pattern A · 静态文件读取改派生 hook

before:
```ts
useEffect(() => {
  fetch('/data/coverage/foo.json').then(setData);
}, []);
```

after:
```ts
const data = useEffectiveCoverage();  // 静态 + override 自动 merge + realtime 订阅
```

`useEffectiveCoverage` 内部:
- 单例 fetch 静态 JSON
- bootstrap kpOverrides + itemOverrides
- subscribe → setState 重 derive
- 所有页面共享 cache

### Pattern B · 双覆盖层叠加

```ts
// Layer 1: itemOverride 全替换(payload = 完整 Item JSON)
const itemOv = getItemOverride(rawItem.id);
const baseItem = itemOv?.payload ?? rawItem;

// Layer 2: kpOverride 仅覆盖 kp_ids(高频 tag 修)
const kpOv = getKpOverride(rawItem.id);
const item = kpOv ? { ...baseItem, hnzk_kp_ids: kpOv.kp_ids } : baseItem;
```

这样:
- kp tag 修复(频繁、轻量) → kp_overrides 表
- 题干结构修复(罕见、整 payload) → item_overrides 表
- 两层独立 · 不互相污染

### Pattern C · 单源派生套卷

```ts
// 旧:fetch papers/{year}.json(整套副本)
// 新:
fetch('/items/{year}/index.json')  // 题序 + 元数据
  .then(idx => Promise.all(
    idx.items.map(it => fetch(`/items/{year}/${it.file}`))
  ))
  .then(qs => qs.map(mergeItemWithOverride))
  .then(qs => buildPaperView(qs));
```

性能不降反升:HTTP/2 多路复用 22 个并行 fetch 通常比单文件还快;cache 粒度精细(改 1 题 1 个文件 miss vs 整套 miss)。

---

## 3 · 部署运维 SOP(管理员日常)

### 改一道题的 kp tag(常规)
```
1. 题卡点 ✏️ 考点
2. 选 / 反选 kp(可挑灰色未挂题考点)
3. 保存 → 三层即时同步
4. 0 git push · 0 部署
5. 全设备 0.5-1s 后看到新分布
```

### 改子题拆分 / 题干 / 解答(罕见)
```
1. 题卡点 ✏️ 题目
2. 字段视图编辑(增删 subparts / 改 stem latex / 改 solution)
   或 JSON 视图(高级)
3. 保存 → 同步链同上
```

### 撤销修正
```
点 ✏️ → 撤销修正 → 删 supabase 行 → 回到静态 JSON
```

### 新增 admin 权限
```
1. 编辑 src/lib/auth.tsx · BUILTIN_ADMIN_EMAILS 加邮箱
2. supabase SQL editor 跑:
   CREATE OR REPLACE FUNCTION public.is_hnzk_admin() ...
   (lower(auth.email()) IN ('foo@x', 'bar@y'))
3. push + 重新部署
```

---

## 4 · 跨产品移植清单

把这套架构搬到 CIE / EDX / 其他真题板需要:
1. 静态 JSON 仍按 board 存 `public/data/papers/{board}/items/{year}/q*.json`
2. supabase 加表(2 张):
   ```sql
   CREATE TABLE {board}_kp_overrides (item_id PK, kp_ids[], ...);
   CREATE TABLE {board}_item_overrides (item_id PK, payload jsonb, ...);
   ```
3. 加 admin 函数 `is_{board}_admin()`(可复用同一 allowlist)
4. 加 trigger + history + RLS + realtime publication(同 SQL 模板)
5. 前端复制 `kpOverrides.ts` / `itemOverrides.ts` 改 table_name
6. 复制 `KpEditDrawer` / `ItemEditDrawer`(0 改业务逻辑)
7. 在每个 ItemRenderer 里挂双订阅 + merge

每板 ~0.4d(基本是 search/replace board 名)。

---

## 5 · 反模式速查

| ❌ 反模式 | ✅ 正模式 |
|---|---|
| 一份数据存 git 多处 | 单源 · 派生 |
| 改完不跑 derive 脚本 | 不需要 derive 脚本 · 浏览器端实时合并 |
| admin 改要 git push | admin 改进 supabase · 实时同步 |
| trigger 写从表被 RLS 挡 | SECURITY DEFINER + 主表门禁 |
| 学生看到 v3.0 · 351 考点 | isAdmin 守 metadata |
| kp picker 只显示已挂题 kp | 显示全大纲(灰色提示未挂题) |
| 双源各存 stem 副本 | 单源 + 并行 fetch + override merge |

---

## 6 · 观测指标

后续验证此架构是否达成"工作量不大"目标的 KPI:

```
信号 X · admin 月修题数 / 月 git push 次数
  期望 X >> 1(大量修复零 push)

信号 Y · 学生从看到错位 → 修复完成的 P95 时长
  期望 < 5 分钟(admin 看到 + 改 + 全设备同步)

信号 Z · 双源不同步事故计数
  期望 = 0(架构上不可能)
```

---

## 7 · 心法

> **bug 不是修一次的事 · 是把"修一次的成本"做小的事**

q17 从被发现到全设备同步,改架构前 = 30 分钟(改两份 JSON + 重跑 derive + push + 部署 + 缓存)。
改架构后 = 30 秒(admin 浏览器点几下)。

> **真相源不能繁殖 · 派生视图不能落盘**

落盘的派生视图必然存在不同步的瞬间。
浏览器实时派生没有这个窗口。

> **能让 admin 自己修的事不要让 admin 来 push**

每一次"管理员要改 git"都是产品架构债。
