---
id: LESSON-019
title: UI 一致性迁移 7 条金标准 · DashboardLayoutV2 单一 wrapper + PageGuardState 守门 + flex-wrap 移动端 + 路由限教师红线
date: 2026-05-01
category: red-line + workflow
severity: 🔴
related_ADR: ADR-0040(灵魂)/ AUDIT_FRAMEWORK § 2 UI 一致性 / LESSON-018(姐妹 · 后端 generator 金标准)
keywords: [ui-consistency, layout-primitive, dashboard-layout, page-guard, mobile-responsive, soul-redline]
auto_load: true
cross_ref:
  - 25maths-practice/src/layouts-v2/DashboardLayoutV2.tsx
  - 25maths-practice/src/components/ui-v2/PageGuardState.tsx
  - 25maths-planning/SESSION_SUMMARY_2026-05-01_UI_CONSISTENCY.md
---

# LESSON-019 · UI Consistency Migration Gold Standard

> **Date**: 2026-05-01
> **Origin**: Practice 仓 8 轮 UI 一致性审查会话(commits 06b962d7b → 7e2c7dfb7 + 1b5c44f08)
> **Scope**: 18 个页面 + 1 个 layout primitive + 1 个新 ui-v2 组件 · 跨 student / teacher / admin / courses / paper / print 五类页面
> **Soul tie**: ADR-0040 § 3 "温度问 / 老师问" — 老师视角的产品不能让学生在某个角落突然撞上一段未译英文 + 灰色 div

---

## TL;DR · 一句话原则

> **任何登录后页面 = `DashboardLayoutV2 title=… subtitle=… actions=…` + `Stack gap="md"` 包内容;不要自己造 `<div className="mx-auto max-w-Xxl p-Y">` wrapper。**
>
> **任何"看不见 / 进不去"的守门 = `<PageGuardState kind="…" />` · 不要写裸英文 `<div className="p-6">Unknown board.</div>` 。**

不读这条 = 你正在制造下一个"页面长得不像 25Maths"的 site,以及下一个学生撞上后内疚自责的英文 dead-end。

---

## 一、产生这条 lesson 的背景

Practice 仓在 2026-04-26 ~ 2026-04-30 期间快速新增了 NZH 立法的多个页面(`/courses/:board`、`/courses/:board/learning-path`、`/courses/:board/past-papers`、`/courses/:board/topical`、`/courses/:board/practice-by-tags`、`/practice-by-tags-global`、`/teacher/papers/:board/overview`、`/teacher/papers/:board/class-errors`、`/teacher/papers` 等)。每个页面 reviewer 都"求一个能跑就行",于是:

- 每页面自带一个 `<div className="mx-auto max-w-{4xl|5xl|6xl|7xl|3xl} p-{4|6}">` wrapper · max-width 5 个不同值
- 标题字号、字体、颜色每页面不一样(`text-xl` / `text-2xl` / `text-3xl` / serif / sans 混杂)
- "Back to ..." 链接位置每页面不一样(顶上 / header 内 / 标题左 / 标题右)
- 守门状态(unknown board / teacher-only)是 14 处英文裸 div · 学生看到一闪而过的"Teacher access only."就走了
- 移动端窄屏 actions 区域控件溢出 · 没有人测过 < 768px 的视口

**症状**:三分钟从 `/learning` 走到 `/teacher/papers/edx-4ma1/class-errors` 体感经过 4 个不同产品 · 信任感断档。

---

## 二、金标准 7 条

### 1. 单一 layout primitive · 不要自己造 wrapper

**铁律**: 登录后任何 dashboard-style 页面只允许用 `DashboardLayoutV2`。 `Login` / `Practice 答题卡`等单页特例用 `centered="sm"` / `centered="md"`。

```tsx
import DashboardLayoutV2 from '@/layouts-v2/DashboardLayoutV2';
import Stack from '@/components/ui-v2/Stack';

return (
  <DashboardLayoutV2
    title={`📝 ${t({ en: 'Past Papers', zh: '历年真题' })}`}
    subtitle={`${t(meta.shortLabel)} · ${total} ${t({ en: 'papers', zh: '套真题' })}`}
    actions={<Link to="..." className="text-sky-700 underline text-sm">← Back</Link>}
  >
    <Stack gap="md">
      {/* page content */}
    </Stack>
  </DashboardLayoutV2>
);
```

**禁止**:`<div className="mx-auto max-w-Xxl p-Y space-y-Z">`、`<div className="min-h-screen bg-gray-50 py-8"><div className="max-w-6xl mx-auto px-4">`、`<header className="space-y-1"><h1 className="text-2xl font-semibold">…`。

**例外**(三类只能这三类 · 添加新例外要在本 lesson § 7 登记):
1. **Print-mode 页**(`PaperViewerPage` / `PaperQuestionPage` / `PaperPreview*`)— 必须保留 `paper-print-root mx-auto max-w-4xl flex flex-col h-full` · 因为 `@media print` CSS 锁这些 selector
2. **Exam-attempt 计时流**(`PaperAttempt` / `PaperAttemptResults` / `StudentErrorBook`)— 全屏沉浸 · 不要侧边栏分心
3. **复杂 blueprint editor**(`PaperBuilder`)— 双栏 split-pane · DashboardLayoutV2 的固定 padding 会挤压编辑区

### 2. 标题副标题语法 · 三段式

```
title    = `<emoji 1 字符> <核心动作动词>` · 不挂学校 / board / class 名
subtitle = `<board shortLabel> · <动作描述> · <数据计数>` · 用 ` · ` 分割
actions  = 一个 <Link> 或一组 <select>+<button> · 不超过 5 个元素
```

**反例**:
- `title = "📊 Multi-Paper Overview · CIE 0580 · 26 students"` ❌ 太挤 · 学生信息进了 title
- `subtitle = undefined` ❌ 浪费 chrome · 不告诉学生现在在哪
- `actions = 6 个 button + 2 个 select` ❌ 移动端必爆

**正例**:见上 § 1 代码块。

### 3. 守门状态 · `PageGuardState` 单一组件

**铁律**: 任何 `if (!meta) return …` / `if (!isTeacher) return …` 必须用 `<PageGuardState kind="unknown-board" />` 或 `<PageGuardState kind="teacher-only" />`。

```tsx
import PageGuardState from '@/components/ui-v2/PageGuardState';

if (!meta) return <PageGuardState kind="unknown-board" />;
if (!isTeacher) return <PageGuardState kind="teacher-only" />;
```

**禁止**:`<div className="p-6">Unknown board.</div>`、`<div className="p-6 text-sm">Teacher access only.</div>`。

**为什么**:这两段裸英文 + 灰色文字是 14 个页面的"看不见角落",违反 ADR-0040 灵魂 #1 温度问("学生看到觉得被支持还是被追赶")· 看到只会觉得"我不该来"。新组件:DashboardLayoutV2 + EmptyStateV2 + 双语 + 回首页 link。

### 4. Header 必须 flex-wrap · actions 不能 shrink-0

`DashboardLayoutV2.tsx` 的 header 已修为 `flex flex-wrap items-start justify-between gap-x-6 gap-y-3`、`actions` 区域加 `flex-wrap max-w-full`。新增 layout primitive **不要复刻成 `flex items-center justify-between` 不带 wrap** — 5+ 控件页(PaperBoardPanel)在 < 1024px 视口 actions 必爆。

### 5. h-full flex scroll 容器 · 大概率应该删

读到 `flex-1 overflow-y-auto pr-1 -mr-1 space-y-4 min-h-0` 这种 article 时 9/10 是 copy-paste 来的 · 它要求父级 `h-full flex flex-col`,但 DashboardLayoutV2 没给 h-full · 留着 = scroll 不出来 = 学生只能看到首屏。**默认改成 `space-y-4`**(即 page-level scroll)· 除非你能说清楚为什么这页面必须独立 scroll(99% 不能)。

### 6. 双语 + 灵魂语 · 守门和空态都要

`PageGuardState` / `EmptyStateV2` 的所有文案必须 `t({ en: …, zh: … })`。零容忍:不允许"Sign in to see your errors." 这种英文 only。zh 文案要走 ADR-0040 § 4 灵魂语录 · "登录后可见错题。" 而不是 "Please sign in to access this feature." 翻译腔。

### 7. 例外注册表(本 lesson 是唯一来源)

| 页面 | 例外类型 | 理由 | 何时回正 |
|------|---------|------|---------|
| `PaperViewerPage` | print-root | `@media print` 选中 `.paper-print-root` | 重写 print pipeline 时 |
| `PaperQuestionPage` | print-root | 同上 | 同上 |
| `PaperPreview` / `PaperPreviewCompare` | print-root | 同上 | 同上 |
| `PaperAttempt` / `PaperAttemptResults` | 全屏计时 | 沉浸答题 · 不要侧边栏 | 不回 |
| `StudentErrorBook` | print 导出 | 学生导 PDF 用 | 同上 |
| `PaperBuilder` | split-pane | 编辑器 + 预览双栏 | 设计专用 layout |

新增例外必须 PR 改本表 · 否则 reviewer block。

---

## 三、整体优化成果(2026-04-30 ~ 2026-05-01 七轮)

| 轮次 | Commit | 范围 | 文件数 |
|------|--------|------|--------|
| Round 1 | 已合 | AfterClass / CourseBoardPage / CourseTopicPage / PapersList / ClassHottestErrorsPanel | 5 |
| Round 2 | `06b962d7b` | LearningPath / PastPapers / Topical / MultiDim / GlobalPractice | 5 |
| Round 3 | `225ae915e` | PaperErrors / PaperFavorites / PaperOverviewPanel / PaperBoardPanel | 4 |
| Round 4 | `a06f3ea7f` | ABTestAnalysis / PaperTagAdmin / PaperQuestionEditor | 3 |
| Round 5 | `97c43f801` | TopicQuestionsPage(h-full → page scroll) | 1 |
| Round 6 | `5179bf1b9` | DashboardLayoutV2 header `flex-wrap` 移动端 | 1 (layout primitive) |
| Round 7 | `67f1a0bba` | PageGuardState 14 处守门统一 | 15 |
| Round 8 | `7e2c7dfb7` | GlobalPractice / MultiDim 限教师(灵魂红线 #6) | 2 |

**累计**:18 页面迁移、1 layout primitive 升级、1 新 ui-v2 组件、14 守门统一。

---

## 四、教训(后人不要重蹈)

### 4.1 写新页面前先 grep 一次 layout primitive

`grep -l 'mx-auto max-w-' src/pages/` 任何新 PR 必跑 · 多写一个 raw wrapper = 多 1 个未来要清理的坑。

### 4.2 守门状态不是顺手写一行的事

每写一个 `if (!meta) return …`,问自己:学生 / 老师 / 路由错配 / 网络抖动 时谁会撞到这里 · 撞到了产生什么情绪 · 怎么走出去。这一秒的成本 << 学生静默流失的成本。

### 4.3 移动端不是"以后再说"

DashboardLayoutV2 一个 `flex-wrap` 改动惠及 17 个已迁移页 · **但** PaperBoardPanel(5 控件)的 actions 在该改动前已经在 768-1023px 视口溢出了 4 周 · 没人 report 是因为 NZH 在 macbook 上看 · 用户当时没有 mobile 用户。**不要等用户报告 · grep `actions=` 看每页 children 数 ≥ 4 的就要测窄屏。**

### 4.4 "灵魂红线 #6" 隐藏在路由配置里

`/practice-by-tags-global` 和 `/courses/:board/practice-by-tags` 是教师内部工具(查题 / 对比 board)· 学生进了反而看到不会做的 1500+ 题 → 焦虑 → 走人。本次 Round 8 用 `<Navigate to="/" replace />` 限教师 · 这是 ADR-0040 § 5 灵魂红线 #1("反向论证为 KPI 必加焦虑特性")的对偶面 — **路由开放即默认违反 · 必须主动关 · 不主动关 = 默认违反**。

### 4.5 跨账号交接的"无缝" = 单一文件能让接手者 30 秒上下文

本仓 SESSION-STATE.md(根目录)+ 本 lesson + planning/PROJECT_FUSION_PLAN_V3.md 三件套是接手协议。新增工作量大于 3 commit 的任务,必须更新 SESSION-STATE.md 的"当前活跃 session"段落 · push 之前。否则下一个 Claude session 接手只能从 git log 倒推 · 倒推不到产品意图。

---

## 五、技术资产快查

| 资产 | 路径 | 用途 |
|------|------|------|
| `DashboardLayoutV2` | `src/layouts-v2/DashboardLayoutV2.tsx` | 唯一 dashboard wrapper |
| `Stack` | `src/components/ui-v2/Stack.tsx` | 内容区垂直间距 |
| `EmptyStateV2` | `src/components/ui-v2/EmptyStateV2.tsx` | 空态 / 0 数据 |
| `PageGuardState` | `src/components/ui-v2/PageGuardState.tsx` | 守门 / 不可见 |
| `Banner` | `src/components/ui-v2/Banner.tsx` | inline 警告 / 错误 |
| `BOARD_META` | `src/lib/boardContext.ts` | board.shortLabel / longLabel |
| `t({ en, zh })` | `src/lib/i18n.ts` | 双语必须 |

---

## 六、下一步推进方向(七轮已闭合 · 不再连续 push)

七轮 chrome consistency 已经把"新页面看起来一致"做完了。**继续往下做的边际收益开始递减**。下一步候选(优先级降序):

1. **数据真相校对** · `subtitle` 里的 `5960 questions` / `4109 题` 等硬编码计数和现行 index.json 是否一致 · 偏差 1+ 即被学生当 "你也不靠谱" 信号
2. **空态文案灵魂审** · 每个 EmptyStateV2 走一次 ADR-0040 § 4 灵魂语录池 · 移除翻译腔
3. **mobile 真测** · iPhone 13 mini(375px)开 DevTools 跑过 18 页 · 发现就修
4. **Loading 状态统一** · 抽 `<LoadingLine />` 替 ~30 处自写 `<p className="text-sm text-stone-500">Loading…</p>`

**停止条件**:任一以下成立 → 暂停 chrome 工作 · 转产品功能。
- 学生 NPS ≥ 8(Beta 内问卷)
- NZH 主动说"够了 · 看下去做内容"
- 出现新页面违规 / 7 天 0 个

---

## 引用

- ADR-0040 § 3-5 灵魂宪章 5 灵魂问 + 7 红线
- ADR-0058 Beta 期注册即会员 · 全员免费(为什么必须双语 · 必须有 Chinese 默认家长群)
- LESSON-014 错题瞬间只做 3 件事(灵魂兑现起点)
- LESSON-015 不要给学生超载 5 条铁律
- 本 lesson 与 LESSON-018 元单位 7 步法形成"前端 chrome × 后端 generator"双金标准
