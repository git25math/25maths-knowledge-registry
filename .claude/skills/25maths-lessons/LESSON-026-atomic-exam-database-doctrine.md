---
name: 真题数据库原子化 5 教义
description: v35 6 天 ship 沉淀 · 真题驱动 + 原生编号 + part-level + 灵魂兑现 + 启发式 backfill
type: feedback
auto_load: true
---

# LESSON-026 · 真题数据库原子化 5 教义

> 立法日期:2026-05-03 · 来源:Plan v35 6 天落地实战
> Sealed by:22/26 sprint ship + 4 NZH-blocking + 5 联文档 ~3000 行
> 取代立场:plan v32 v8 强制跨板 kn_id · 改为各板原生编号 + concept 仅 join

---

## 0 · 触发故事

NZH 反思海南中考 SyllabusTreePage 真用反馈:
> "学生在大考纲下钻进小考纲 · 看下挂真题 · 体验直接超过 cross-board 概念抽象"
> "对于综合题 · 通过分析拆分 · 共享题干 / 独立"
> "经常出错的题 · 针对性训练 · 而不是盲目刷题"
> "标签足够细致 · 变式 / generator 自然清晰 · 这就是专题专练的教研"

---

## 教义 1 · 真题驱动 generator 设计 (心法 24)

### 旧范式(凭想象 · 易跑偏)
```
教研员想:"二次方程应该有什么变式?"
  ↓
拍脑袋列:基础解 / 含负根 / 完全平方 ...
  ↓
造 generator → ship → 真题没考的题型在练
```

### 新范式(数据驱动 · 临摹真题)
```
真题标 L3 + 共享题干 + 子标签
  ↓
聚合到 L3 节点(2.5.04 · 7 道)
  ↓
肉眼分组 · 这 7 道分 K 个变式套路
  ↓
generator 设计 = 80% 临摹真题型 + 20% 派生
```

**铁律**:**Generator backlog 必从真题数据反推 · 不能凭工程师 / 教研员直觉**。

### 工具兑现
- `scripts/generate-generator-backlog.py` · 4 优先级算法(urgent / high / medium / low)
- `/admin/syllabus/:board/:l3` · L3 模式预览(教研工具 · 导 markdown)

---

## 教义 2 · 原生编号优先 + concept 仅 join (心法 25)

### 跨板统一编号是错方向
- 教师/学生术语错位:学生说"今天讲 CIE 1.4" 不说"kn_0107"
- 跨板协商成本高:CIE 改一处 · 影响全板
- 限制新板 onboard:海南中考、AMC 各有原生编号

### 正确做法
```
cie-igcse-0580-kn-#.#.#  · CIE 0580 原生
edx-igcse-4ma1-kn-#.#.#  · EDX 4MA1 原生
edx-ial-wma11-kn-#.#.#   · IAL Pure 1 原生
hnzk-kn-#.#.#            · 海南中考原生
   ↓
kn-registry concept(kn_0107)· 跨板 join 标 · 不主显
```

**铁律**:**主键 = 原生编号** · concept 是侧向 join · 跨产品 mastery 走 concept · UI 不以 concept 为主。

### Sprint 兑现
- ADR-073 立法
- 4 板独立 syllabus.json
- `_kn_concept` 字段(可选 · 不强同步)

---

## 教义 3 · part-level 错题颗粒 (心法 26)

### qId 整题 5 连对修复 = 浪费 80% 力气
- 学生 12 marks 题答错 part (b)
- 修复 = 重做整题 5 次 · 80% 力气重做已会的 part (a) (c)

### partId + atomicity-aware 修复
```
错题 record:
  qId + partId + l3_subtopic + atomicity + is_repairable
   ↓
错题专练显示按 atomicity 决策:
  independent → 仅 part(简洁)
  shared_scenario/data → 共享情境跟随(不丢上下文)
  chained → 锁 · 跳整题练(不可单抽)
   ↓
修复 = 跨真题 / 变式同 L3 5 连对(不限同 qId)
chained → 整题 5 连对(强制)
```

**铁律**:**错题颗粒 = 学生真出错的最小单位**(part)· 修复颗粒 = 同 L3 任意题(灵活)。

### 数据 schema
- `practice_attempts` 加 4 字段:`q_id` / `part_id` / `l3_subtopic` / `atomicity`
- 兼容老路径:全 NULL → 走 qId 整题 5-correct(0 回归)

---

## 教义 4 · 灵魂兑现到每 surface (心法 27)

### 学生侧 5 灵魂问(每 UI 必过)
1. 温度 · 学生感到被支持还是被追赶?
2. 声音 · 替学生说没说出口的内心 OS
3. 老师 · 像中国老师而非酷工具
4. 三学生 · 差/中/优 3 视图分层
5. 走人 · 一周回看温暖 vs 内疚

### 禁忌文案 vs 对的文案

| 禁忌(违反 ADR-0040)| 对的 |
|---|---|
| "你错了 N 道" | "再练 5 道 · 完全通了" |
| "答错率 60%" | "上次卡这 · 现在再来一次" |
| "比 X% 同学差" | "不急 · 这一档大家都需要练几次" |
| "0% 完成" | "📚 7 真题 · ⚙️ 2 generator" |

### chained 锁定文案
- ❌ "🚫 cannot be repaired"(冷字)
- ✅ "🔒 这一问要先做 (a)(b) · 一起练才有意义 [▶ 来本题视图]"

### 自主感铁律
3 入口让学生自己选:
- 📜 真题(看真考过的样子)
- 🌱 变式(按自己节奏练熟)
- 📋 综合题(完整应用 · 锻炼建模)

---

## 教义 5 · 启发式 backfill > NZH 全人工标 (本 plan 实战)

### 全人工标 = 慢 + 易卡 SOP
NZH 标 1 题 5 min · 全板 9923 题 = 800h · 不可能

### Smart-suggest + 校对 = 快 + 准
6 启发式规则 · 派生 6780 part 默认值:
- 单 part → independent
- "use your answer" 模式 → chained
- 整题含表格 + part 不重复 → shared_data
- 整题含应用情境关键词 → shared_scenario
- 默 → independent

### NZH 校对工作流
1. 跑启发式 → /tmp/atomicity-suggestions.json(全板派生)
2. NZH 起手标 50 题 pilot(走 7 屏 SOP)
3. 命中率 ≥ 70% 时 · 全板自动 backfill
4. NZH 后续仅校对 30% 不准的

**铁律**:**机器派生 80% + 人校对 20%** · 不强求 NZH 全人工。

### 工具兑现
- `scripts/smart-suggest-atomicity.py`(6 启发式 · 200 词字典)
- `/admin/atomicity` 7 屏 wizard(智能默认值已填)
- `/admin/data-quality` 进度仪表盘(NZH 看校对覆盖率)

---

## 5 教义 总览

```
1 · 真题驱动 generator      → 临摹真题型 · 不拍脑袋
2 · 原生编号 + concept join → 教师术语正确 · 跨板各保各
3 · part-level 错题颗粒     → 修复精准 · 不浪费力气
4 · 灵魂兑现到每 surface    → 自主感 · 不评价 / 催促 / 对比
5 · 启发式 + 校对           → 机器派生 80% + 人校对 20%
```

5 条任一断裂 · 整个架构失灵。

---

## 应用 SOP(下次推类似 plan 直接套)

### Step 1 · 数据真相先于 UI
派生 / 标注 / audit 在前 · 学生侧 UI 后 · 0 回归靠默路径兼容。

### Step 2 · 4 层立法骨架(L1 Board → L4 Subtopic)
任何课程领域 · 都按 4 层嵌套 · 不强求统一编号。

### Step 3 · CI guard 5 道
- syllabus-tree(L3 真题/gen 数)
- atomicity(part 标注)
- shared-stem(复合题配套)
- l3-ref(引用合法)
- coverage-stats(KPI 汇总)
全 informational 起 · NZH 标完阈值后改 strict。

### Step 4 · NZH 工作量精算
不让 NZH 全人工标 · 启发式承接 80%。
NZH 投入 ≤ 6h 一次性 + N 周持续 · 不绑死。

### Step 5 · 灵魂自检每 PR
5 灵魂问 · 任一答错 = block。
学生侧 surface = 自主选 · 老师面板 = 推荐而非要求。

---

## 与其他 LESSON 的关系

- LESSON-024(协议 vs 直觉)· 本 lesson 是协议化标准在"真题数据库"领域的具象
- LESSON-025(LaTeX 渲染 SOP)· 同 7 步全栈验收原则
- LESSON-019(UI 一致性迁移)· part-level 错题颗粒升级方法论同
- ADR-040(灵魂宪章)· 教义 4 直接兑现

---

## 数据基线(Day 6 ship 时)

| 数据 | 数 |
|---|---|
| CIE 0580 真题 | 9923 |
| 派生 L3 三级考点 | 329(72 L2 / 9 ch)|
| 复合题 | 2932 |
| 待标 atomicity part | 10309 |
| smart-suggest 派生 part | 6780(58/37/4.6/0.2 分布)|
| 紧急 generator 缺口 | 23(0 gen + 真题 ≥ 5)|

---

## 文档 5 联

```
planning/PLAN-V35-ATOMIC-EXAM-DB.md       骨架 (475)
planning/PLAN-V35.1-CONCRETE.md           具象 (691)
planning/PLAN-V35.2-POLISH.md             终版打磨 (585)
planning/PLAN-V35.3-EXECUTABILITY-AUDIT.md 可执行审计 (618)
planning/PLAN-V35-SHIP-COMPLETE.md        ship 完结 (258)
practice/public/data/kp/_adrs/ADR-073-...md 立法 ADR
```

下次推类似课题 · 直接走此 5 联模板 + 5 教义。
