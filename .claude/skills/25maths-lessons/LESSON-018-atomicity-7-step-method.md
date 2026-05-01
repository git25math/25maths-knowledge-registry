---
name: 元单位拆解 7 步法 · 心法 24-31
description: 2026-04-29 NZH 立法 + AI 单 session 100+ commits · Practice 79 generators atomic 拆完 + META + master-index + query API + invariants 全栈 ship · 沉淀供未来类似工程
type: feedback
auto_load: true
---

# LESSON-018 · 元单位拆解 7 步法

> 2026-04-29 NZH 立法 4 步深化 + AI 单 session 100+ commits · 25maths-practice 全栈兑现 · 元单位铁律 + 7 层 ID Ontology 跨产品宪法立完
> 真相源:[25maths-practice/docs/ATOMICITY-PROGRESS.md](https://github.com/git25math/25maths-practice/blob/main/docs/ATOMICITY-PROGRESS.md)
> 关联:[ADR-0074](https://github.com/git25math/25maths-os/blob/main/decisions/0074-atomic-meta-7-layer-ontology.md) · [ATOMICITY_MILESTONE](../ATOMICITY_MILESTONE_2026-04-29.md)

---

## 0 · 战绩(单 session)

| 维度 | 起 | 终 |
|---|---|---|
| Composite violator | 10 | **0 ✅** |
| Practice KN coverage | 73% | **97%** |
| Atomic generators | 763 | 797 |
| **META export** | 0 | **767/767 (100% atomic)** |
| **Master-index** | n/a | 336KB · 187 KN · 317 patterns |
| **Query API** | n/a | 10/10 tests |
| **Invariants I1-I7** | 0 | 7/7 ✅ |
| **Pattern labels** | 0 | 317 |

---

## 1 · 7 步法(沉淀 SOP)

### 步骤 1 · 立 audit (违规可见)

**先写守门器 · 再修违规**:`audit:atomicity` 输出 violator 数 + 详情。

```bash
# Anti-pattern 检测 · switch on problemType + ≥3 case + ≥3 sub-functions
npm run audit:atomicity   # 0 violators target
```

→ **心法 19 真兑现**:不可见的违规 = 不存在

### 步骤 2 · 写 plan + 3 轮自审

**大工程必写计划 · 不可动手前打磨完否则中途返工**。

3 轮自审分别看:
- Round 1 · 结构完整性
- Round 2 · 边界 / edge cases
- Round 3 · 序列依赖 / 全局一致性

→ Practice atomic 工程 652 行作战手册 · 3 轮自审通过后才动手。

### 步骤 3 · MEU 拆分(每元单位 1 commit)

**最小执行单位 = 1 atomic 提取 = 18 步 SOP = 1 commit · 可独立 revert**。

每 commit 含:
- 新文件 + variants-index entry + _exam-refs paper 重分配
- audit:atomicity 数字记录(预期 -0 violator · close-all 阶段才 -1)
- gate G1-G7 全过

→ 39 atomic 39 commits · 中途任何 1 commit 失败 · 单 revert 即可。

### 步骤 4 · close-all(统一 deprecate)

**不在 MEU 阶段删 composite · 全部 atomic ship 后才统一删**。原因:

- MEU 中途若回滚需要 composite 数据
- close 是单独 commit · 集中处理跨引用 sweep + mastery alias map

### 步骤 5 · META 注入(auto-derive 80%)

**别叫 NZH 手填 797 × 50 字段**:80% META 字段(uri/kn_id/pattern_id 等)可从 variants-index.json + 文件路径 + seed v3 自动派生。

```bash
npm run inject:meta   # 自动 derive · 单次 ship 767 atomic
```

NZH 后续仅补 §D APPLICATION (recommended_contexts · 6.5h 一次性补完)。

### 步骤 6 · master-index + query API(单一查询入口)

**所有 generator 查询走单一 API · UI/Recommendation/Audit 不重写过滤逻辑**。

```typescript
queryGenerators({ pattern, kn, style, difficulty })  // pure filter
findGeneratorsForKn(kn_id)                           // 跨产品聚合
buildPaper(spec)                                     // 组卷
```

→ 心法 26 真兑现:跨产品共享 L3 (kn_id) · 不共享实现。

### 步骤 7 · build-time invariants(防漂移)

**runtime warning > silent error · build-time gate > runtime warning**。

```bash
npm run audit:meta:strict   # CI gate · 失败 exit 1
```

7 不变量(I1-I7):
- META 完整性 / 元单位唯一性(7-tuple) / URI 一致性
- variant_id 格式 / kn_id ∈ registry / style ∈ enum / pattern_id ↔ variant_id

→ CI 加 strict mode 后 · 任何后续违规自动 block merge。

---

## 2 · 心法 24-31

| # | 心法 | 触发情景 |
|---|---|---|
| 24 | ID 是 ontology 物理表示 · 不是字符串 | 7 层 schema 设计时 |
| 25 | 同知识点 ≠ 同 generator · 风格不同必拆 | NZH 第 3 步立法 |
| 26 | **同题型同风格 · 跨产品也不合并** · 共享 L3 不共享实现 | NZH 第 4 步立法 |
| 27 | 元单位 META 是 6 答 4 问 · 任一缺则不能元单位级独立调用 | META schema 设计 |
| 28 | 80% META 字段可自动 derive · 别叫 NZH 手填 | 注入策略 |
| 29 | "switch on problemType" = 元单位违规信号 | audit:atomicity 守门 |
| 30 | 大工程拆 MEU + 多轮自审 + 单元独立可回滚 | Wave 1-8 真兑现 |
| 31 | **build-time invariants > runtime warning** | CI gate 立后 0 漂移 |

---

## 3 · 反例避坑(不要重蹈覆辙)

### 反例 1 · "1 generator 多 sub-pattern 是 OK 的"

```typescript
// ❌ 反例 (FRA_MULTIPLY_DIVIDE.ts · 已删)
type ProblemType = 'frac_times_whole' | 'frac_times_frac' | 'mixed_multiply' | 'frac_divide' | 'mixed_divide';
switch (problemType) { case '...': return generateXxx(...); }

// ✅ 正例 (拆 5 文件)
cie.1.4.02.frac_times_whole.ts
cie.1.4.02.frac_times_frac.ts
cie.1.4.02.mixed_multiply.ts
cie.1.4.02.frac_divide.ts
cie.1.4.02.mixed_divide.ts
```

### 反例 2 · "数据丢失 = 数据缺失"

```bash
# ❌ 反例
NZH 1-2h 手填 61 KN description (我说: registry 没 description)

# ✅ 正例
grep seed v3 archive → 61/61 都有 → 写恢复脚本 1 commit 解
```

→ 心法 21 真兑现 · 永远先查 ETL 上游

### 反例 3 · "ship lib 不立 ratchet 守门"

```bash
# ❌ 反例
写 cool generator 框架 · 0 caller 用了 6 个月 · plan v23 sprint 46

# ✅ 正例 (本 LESSON 步骤 1)
audit:atomicity 立 + audit:meta:strict 加 CI · ship lib + ratchet 同 commit
```

→ 心法 20 真兑现:ship lib ≠ ship adoption

---

## 4 · 16 命令工具栈(本 session 立完)

```bash
# 元单位级守门(本 LESSON 步骤 1+7)
npm run audit:atomicity         # 0 violators
npm run audit:meta              # I1-I7 invariants
npm run audit:meta:strict       # CI gate

# 7 层 ID 树审计(本 LESSON 步骤 6)
npm run audit:hierarchy [s1.4]
npm run audit:kn-split

# 数据层 audit
npm run audit:coverage          # 97% KN coverage
npm run audit:cross
npm run audit:adoption
npm run audit:kn-desc

# 派生 / 注入(本 LESSON 步骤 5+6)
npm run derive:bindings
npm run propose:pattern-labels
npm run build:master-index
npm run inject:meta
npm run restore:kn-desc
npm run locate <vid>
```

---

## 5 · 跨仓 sync 闭环

```
NZH 立法
   ↓
25maths-os ADR-0074 (L1 宪法)
   ↓
25maths-practice 100+ commits (L4 实施)
   ├─ docs/ATOMICITY-PROGRESS.md (真相源)
   ↓                              ↑ 真相源指针
25maths-planning ATOMICITY_MILESTONE (L3 战略归档)
   ↓
25maths-knowledge-registry seed restore (L2 数据)
   ↓ sync
25maths-practice (consume)
```

4 repo 全 push · 完整闭环。

---

## 6 · 适用范围(下次类似工程触发条件)

本 LESSON 7 步法适用于:

- ✅ 跨多 file 的 schema/ID 系统重构(本 session 案例)
- ✅ 大量 metadata 字段统一注入(META schema)
- ✅ 跨产品共识立法(7 层 ontology · 元单位铁律)
- ✅ Build-time invariants 守门
- ⚠️ 不适用纯 UI 改动 · 纯 bug fix(MEU 粒度过小)

下次类似规模工程(50+ commits · 多 repo 影响)启动前 · 必读本 LESSON。
