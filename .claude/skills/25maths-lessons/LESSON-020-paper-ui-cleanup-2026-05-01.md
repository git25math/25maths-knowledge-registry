---
id: LESSON-020
title: 真题 UI 净化 5 类 + 多渲染路径纪律 + 全栈数据 shape 一致性
date: 2026-05-01
category: workflow + red-line
severity: 🔴
related_ADR: ADR-0040(灵魂)/ ADR-0061(Design System)/ LESSON-013(可见性)/ LESSON-017(7 类 bug)
keywords: [paper-ui, full-stack-audit, multi-renderer, data-shape, NZH-legislation]
auto_load: true
cross_ref:
  practice_repo: 25maths-practice @ v2.98.0 · commits 2effdcc79..7e2c7dfb7 (~50 commits, 2026-04-30→05-01)
---

## 1. 触发上下文

NZH 真账号验收 CIE 0580 + EDX 4MA1 真题视图,连续发现:
- 题干 chip 噪声(topic / kn / dim 三类)残留
- 答题虚线 + 图片边框污染纸感
- headless `(a)` 与 subparts `(i)(ii)` 双 prefix(`(b)(b)(i)`)
- 单题视图却显示 self-mark / answer 输入(违和)
- 修一处一处不见效 — **因为同一逻辑在 5 个 renderer 各跑一份**

## 2. 5 类 UI 卫生违规清单(NZH 真题 UI 立法 · 2026-05-01)

| # | 类别 | 反面 | 正面 |
|---|---|---|---|
| C1 | **Topic chip / 标签** | 题干贴 `1.4` `KP-0142` `dim:skill` 三色 chip | 学生侧 0 chip · 仅 `*.*` 简码 · 教师 `/practice-by-tags` 可见全 dim |
| C2 | **Answer space** | dashed 虚线占位 / self-mark 复选 | 单题视图纯只读 · 套卷预览也撤 self-mark |
| C3 | **图片边框** | `border rounded` 套真题 figure | 0 border · 0 rounded · 让 figure 自呈纸感 |
| C4 | **Part prefix 重复** | `(b)(b)(i)` · headless `(a)` 与 `(a)(i)` 不合并 | empty stem 时 `(a)` + `(i)` → `(a)(i)` 合并;否则去外层 |
| C5 | **垂直对齐落差** | 题干为空时 `(a)` 缩进 | qNum 与 `(a)` 顶对齐 · 0 落差 · 即使配图也对齐 |

每类对应 commit:`d20f3d483` `e1ff2e574` `2a56a4197` `5d1ff71d9` `c17626e9b` `5dfe51457` `dafe9e48c` `5b0ccbed7` `7f1f2e7f7`

## 3. 数据 shape 不一致清单(全栈隐患)

| 字段 | 双形态 / 缺失 | 影响 | 修法 |
|---|---|---|---|
| `stem` vs `Stem` | 大小写两套同时存在 | renderer 二选一 → 50% 题白屏 | renderer 兼容两种 + 入仓清洗脚本 |
| `type` vs `paperType` | meta.json 字段名漂移 | 路由判定错 → 跳错视图 | 统一 `meta.type` · legacy 兼容读 |
| `by-topic.json` vs `by-topics.json` | 复数/单数 | 索引 404 | 统一 `by-topic` + alias |
| `qId` / `board` / `code` 缺失 | legacy 真题缺 anchor | deeplink 失效 | derive 工具补齐 + audit 报告 |
| IAL p1/p2 数据 | 0 数据但路由可达 | 404 噪声 | 立 empty stub 而非 hidden |

## 4. **多渲染路径纪律**(本 session 最大教训)

> "我已经修了啊 · 怎么还显示?" 因为 PaperViewerPage / PaperQuestionPage / TopicQuestionsPage / PastPapers.tsx / BlockRenderer 都在各自渲染 chip · 各自画 dashed 框。**同一语义 5 个 caller**。

### 4.1 反 anti-pattern 清单(违 = 病灶必复发)

- ❌ "我改了 QuestionContent · 应该全站生效"(实际只覆盖 1/5 入口)
- ❌ "legacy 文件不动"(legacy 仍跑 prod · 不动 = 学生还看到旧 UI)
- ❌ "新组件抽出来 · 旧 caller 慢慢迁"(慢慢迁 = 永远不迁)
- ❌ 单 grep 一个关键词就以为穷尽(同语义有多个 token:chip / Tag / Pill / Label)

### 4.2 修法 SOP(下次遇到 UI 不一致必走)

```
1. grep 所有 renderer 入口
   - rg -l "TopicChip|<Pill|topic-chip|kn-chip|dim-chip"
   - rg -l "answer-dashed|answer-dots|answer-solid"
   - rg -l "border rounded.*<img"

2. 列出 caller 表 · 标 ✓/✗ 状态

3. 一次 PR 全改 · 不放过 legacy

4. 跑 audit 脚本验证 0 残留
   - npm run audit:cie-pages
   - npm run audit:tag-coverage
   - npm run audit:orphan-values

5. NZH 真账号 5 入口都过(不只 1 入口)
```

### 4.3 共享组件原则强化

凡 ≥ 2 caller 复用的渲染逻辑 → **必须抽 component**(不是抽 util)。
component 名内含语义:`<PaperFigureImage>` 而非 `<Image>` · `<PartLabel>` 而非 `<span>{label}</span>`。

## 5. 全栈 audit 调用模式(可复用任意 board 卫生检查)

```bash
# 数据完整性
npm run audit:cie-pages          # CIE 228 套 · 4109 题 · 字段齐
npm run audit:orphan-values      # 找不到归属的 dim 值
npm run audit:tag-coverage       # tag 覆盖率 + 缺失分布

# UI 一致性(全 renderer 入口)
rg "topic-chip|kn-chip|dim-chip" src/  # 学生侧应 0 命中
rg "answer-dashed|answer-dots" src/    # 单题视图应 0
rg "<img.*rounded" src/                # 真题 figure 应 0

# 路由门禁(教师 vs 学生)
grep -r "practice-by-tags" src/routes/  # gate 应有 teacher-only
```

## 6. 灵魂自检(本 session 通过)

- 温度问 ✅ 学生看到的是干净纸感 · 不是被 chip 评判
- 老师问 ✅ 像把试卷递到学生面前 · 不是"很酷的标签云"
- 走人问 ✅ 学生回来仍是熟悉的纸面 · 0 红点 / 0 焦虑标签

## 7. Cross-ref

- 主仓 commits: `2effdcc79..7e2c7dfb7` @ 25maths-practice main
- 实践 DEV-PLAN: `25maths-practice/docs/DEVELOPMENT-PLAN.md` v2.98.0
- 关联 LESSON: 013(可见性)· 017(7 类 bug 探针)· 018(原子化 SOP)
- 下一步: SUBPLAN-2026-05-01-NEXT.md(本 lesson 衍生 sprint 列表)
