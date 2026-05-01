---
name: 链路重构 7 类 bug · ship 前预排查清单
description: 2026-04-27 NZH HHK 学习线 P1-P5 + Hotfix 累积发现 7 类高频 bug · 每类提供 grep 探针 · ship 前必跑 · 跨 session auto-load
type: feedback
auto_load: true
---

# LESSON-017 · 链路重构 7 类 bug · ship 前预排查

NZH HHK 学习线 P1-P5 + 4 hotfix · 累积发现 7 类 bug。本 LESSON 提炼为 ship 前必跑预排查清单。

---

## 7 类 bug + grep 探针

### A · 数据假设 vs 接口真实

**症状**:plan / 文档假设 variantId / API / query schema · 实际仓中**不存在** · 学生进 → silent fail / 空白 / 错跳。

**实例**:
- Y7.1.json `cie.1.4.07.frac_mult_frac` 不存(真值 `06.proper_times_proper`)
- PracticePage 假设 `?taskMode=` query(真无 · 用 mode/count)
- KnowledgeMap 假设 `?focus=` query(真无)
- PastPapers 假设 `?focus=` query(真用 `/papers/{sectionId}` path)

**预排查**:
```bash
# variantId 真否
grep -rn "VARIANT_ID = " src/engine/generators/v2/ | grep -F "{your-id}"

# 路由 query 接收
grep -nE "useSearchParams|searchParams\.get" src/pages/{Page}.tsx

# path param vs query
grep -nE "useParams|Route path=" src/App.tsx | grep "{path}"
```

### B · 数据库列 vs frontend 写入

**症状**:frontend 写新列 · supabase prod 列未部署 · POST **400 PGRST204** · 整 row 拒 · 学生答题数据 silent 丢。

**实例**:#497 hotfix:`source/unit_id/kp_id/is_repair` 列未部署 · 整 POST `practice_attempts` 失败。

**预排查**:
```bash
# 凡 supabase.from('table').insert / .update 加新列前
grep -rn "supabase.from\('{table}'\)" src/lib/sync.ts src/lib/

# 检查 supabase prod 列存在(NZH 跑)
SELECT column_name FROM information_schema.columns
WHERE table_name = 'practice_attempts' AND column_name IN ('source','unit_id','kp_id');
```

**修补铁律**:
- 加新列写入 → **localStorage feature flag** 默认 OFF
- migration 文件入仓但未部署 prod 时 · frontend 不直接写
- NZH 手动部署 + console 启 flag 验证后 · 改 default ON 单独 PR

### C · 跨域返回上下文不解耦

**症状**:跨 page 跳转后 · 返回链固定指向某默认 page(科技树 / 知识地图)· 不识别学生来源 · 返回到错误位置。

**实例**:#498 PracticePage 顶 ← Skill Tree 链固定 `to=/section/{kpSlug}` · 学生从 hhk 进 · 答完返到科技树(错)· 应返 hhk 单元。

**预排查**:
```bash
# 找所有"跨域跳转能进的 page"的返回链是否解耦
grep -nE "<Link to=\"/(map|section|practice|papers)" src/pages/{Page}.tsx
```

**修补铁律**:
- 任何跨域链接的"返回"按钮 · 必基于 `?from=` query 动态计算
- 推荐用 `getBackContext(urlFrom, fallback)` 工具函数 · 跨页复用
- 与 ReturnChip(顶 chip)并存 · 双层保险

### D · UI 标签 vs placeholder 重复

**症状**:输入框上面有 label "分子" · 输入框 placeholder 也是"分子" · **同字显 2 次** · 视觉冗余。

**实例**:#499 FractionField "分子"/"分母" 各显 2 次。

**预排查**:
```bash
grep -nE "label.*placeholder|placeholder=.*\\1" src/components/{Component}.tsx
# 检查 label 文字 vs placeholder 文字 是否相同
```

**修补铁律**:
- `<label>` 已显字面意 → 撤 input `placeholder`(留 `aria-label`)
- 或 placeholder 用真实示例(如"如 1/2")· 不重复 label

### E · 嵌套元素 HTML 合法性

**症状**:`<p>` 标签内含 `<div>` · HTML 规范禁止 · 浏览器自动闭合 p · React 渲染混乱 / 空白。

**实例**:P3 ConceptModule `<p dangerouslySetInnerHTML>` · 内容含 `$$...$$` display math · `renderLatex` 输出 `<div>` · `<p><div>` invalid → 空白。

**预排查**:
```bash
# 任何 dangerouslySetInnerHTML + 含 display math / table / list
grep -B2 -A2 "dangerouslySetInnerHTML" src/components/{Comp}.tsx
# 上下文若是 <p> · 检查渲染输出是否含块级元素(div/table/figure)
```

**修补铁律**:
- 凡 `dangerouslySetInnerHTML` 内容可能含块级元素 → 用 `<div>` 包(不 `<p>`)
- 或不 split · 整段 dangerouslySetInnerHTML(让 latex.ts 内部处理换行)

### F · 路由 query vs path 选错

**症状**:链接生成 `/foo?focus=X` 想跳具体子页 · 实际 page 不接此 query · 落整体页面。

**实例**:#496 PapersModule 链 `/papers?focus=1.4` · PastPapers 不接 `?focus` · 实际接 `/papers/:sectionId` path param。

**预排查**:
```bash
# 跳特定子页前 · 必 grep 该 page 的接口
grep -nE "useSearchParams|searchParams\.get|useParams\(" src/pages/{Page}.tsx
# 看接 query 还是 path · 选对的形式
```

**修补铁律**:
- 跳转目标页前 · 必查目标页的 `useParams` / `useSearchParams`
- 用 path param 的:`/foo/{val}`
- 用 query 的:`/foo?key=val`
- 不混

### G · nav 链 path 必有 page

**症状**:nav L1/L2 配置链 path · 但 App.tsx 没注册路由 → 404 / NotFound 兜底 · 学生迷失。

**实例**:plan v9 navConfig `/assignments`(我的作业 L1)· 但 P5 时还没 ship · 学生点 nav → 404。

**预排查**:
```bash
# 所有 nav 链 path 列表
grep -E "to: '/" src/components/nav/navConfig.ts | grep -oE "'/[^']*'" | sort -u

# vs 所有路由
grep -E "Route path=" src/App.tsx | grep -oE "path=\"[^\"]+\"" | sort -u

# diff:nav 有 · 路由无 = 404 风险
```

**修补铁律**:
- 任何 nav 路径 · 必有 path mount(即使是 Placeholder 占位)
- 用通用 `<Placeholder />` 组件:icon + 标题 + 描述 + ← 父跳

---

## ship 前必跑 7 探针(verbatim)

```bash
# A · 数据假设
grep -rn "{variantId-or-data-key}" src/engine/generators/v2/ public/data/

# B · 列写入(若涉)
grep -rn "supabase.from\('{table}'\).insert\|.update" src/lib/sync.ts
# + supabase SQL 验列存在

# C · 跨域返回链
grep -nE "<Link to=\"/(map|section|practice|papers|review)" src/pages/{Page}.tsx
# 看是否用 backContext / getBackContext / 动态 to

# D · UI 标签 vs placeholder
grep -B1 -A1 "placeholder=" src/components/{Comp}.tsx
# 比对上方 label 文字

# E · 嵌套块级元素
grep -B3 -A3 "dangerouslySetInnerHTML" src/{path}.tsx
# 父元素 <p>?内容可能含 $$display$$ / table / list?

# F · 路由 query vs path
grep -nE "useParams|useSearchParams" src/pages/{Target}.tsx

# G · nav vs route diff
diff <(grep -E "to: '/" src/components/nav/navConfig.ts | grep -oE "'/[^']*'" | sort -u) \
     <(grep -E "Route path=\"" src/App.tsx | grep -oE "path=\"[^\"]+\"" | tr -d '"' | sed 's/path=/\//' | sort -u)
```

---

## 与 LESSON-013 / LESSON-011 关系

| LESSON | 角度 |
|---|---|
| LESSON-011 deploy 后 git 入仓 | migration / 数据 deploy 纪律 |
| LESSON-013 backend ship ≠ user happy | frontend wire 必须 |
| **LESSON-017** | 链路重构 ship 前 7 探针 |

三 LESSON 串联:**ship 前 7 探针(017)→ migration 入仓(011)→ frontend wire(013)→ user happy**。

---

## 触发条件(本 LESSON auto-apply)

任一:
- 大重构(plan v{N} 跨多 sprint)
- 跨多 page 链接改造
- 加新数据库列 + frontend 写入
- 新 nav L1/L2 项加入
- 跨域跳转设计

→ ship 前必跑 7 探针 · 任一红 · 不 PR。

---

## 验收 checklist 增订(plan v15.1 入)

每 PR ship 前必加 6 项:

- [ ] **A**:variantId / 数据 key grep 仓中真存
- [ ] **B**:supabase 列(若涉)用 feature flag 默认 OFF
- [ ] **C**:跨域链返回基于 `?from=` 解耦
- [ ] **D**:UI label 与 placeholder 不重复
- [ ] **E**:dangerouslySetInnerHTML 上下文无 `<p><div>` invalid
- [ ] **F**:跳转目标页 query / path 校对
- [ ] **G**:nav 链 path 全有 route(即占位)
