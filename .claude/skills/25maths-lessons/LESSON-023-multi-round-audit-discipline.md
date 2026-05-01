---
name: 多轮审计纪律 R1/R2/R3
description: 任一全栈整改 sealed 前必经 ≥ 3 轮深审 · R1 视觉/数据残留 · R2 dead code/unused/single-ref · R3 边缘 schema/a11y/cache/mobile/print
type: feedback
auto_load: true
---

# LESSON-023 · 多轮审计纪律 · "每轮加 1 维 · 老问题不回归"

> 2026-05-01 sealed · 配 LESSON-020 真题 UI 净化 + R2/R3 审计闭环

## 立法

任一全栈净化 / 立法整改后 · **必须跑 ≥ 3 轮深审**:
- **R1**: 立法对应的视觉 / 数据残留扫
- **R2**: dead code / unused identifier / single-ref import 扫
- **R3**: 边缘数据 schema / a11y / cleanup hooks / cache invalidate / mobile / print 扫

每轮加 1 维 · 不重复扫已 clean 维度 · 下轮假设前轮成立。

## R1 → R2 → R3 实例(本 session 真题 UI 净化)

### R1(2026-04-30 22:00 UTC)· 视觉残留扫
- ✅ `border-l-2 border-dashed border-stone-200` 答题虚线
- ✅ `border border-stone-200 rounded bg-white` 图片边框
- ✅ chip 渲染 (kn_id / DimensionChips / 类似题 CTA)
- ✅ self-mark 按钮 / answer panel
- 漏:dead JS imports + unused functions

### R2(2026-05-01 00:30 UTC)· dead code 扫
新增维度:
- `单 ref import = dead 死引用`(grep -c == 1)
- `0 ref function/component = unused`
- 教师 gate(/practice-by-tags + global)`isTeacher` 守门 entry

发现 + 修:
- `PaperQuestionPage.tsx` SelfMarkValue / QuestionAnswerPanel / DimensionChips · 3 dead imports
- `PaperViewerPage.tsx` SelfMarkButtons function 0 callers · 1 dead func
- caller-aware `?from=tags` `?from=global-tags` 未在 callerList resolver(非阻 · fallback OK)

### R3(2026-05-01 01:00 UTC)· 边缘 schema + a11y + hooks 扫
新增维度:
- 复合数据 key 模式(`(a)(ii)` 多层 label)
- useEffect cleanup leak(setTimeout / setInterval)
- img alt(a11y)
- block 类型 fall-through(`image` / `figure` 视为占位)
- cache invalidation 路径(admin override 改后清不清)

发现 + 修:
- `partLabelToFigKey('(a)(ii)')` 只取首 paren · CIE 数据 5 figs key 是 `Suba(ii)` / `Subb(i)` 等复合 · 不渲染
- 修:`partLabelToFigKeys()` 返候选 list · PartCard 遍历取第 1 非空
- 0 setTimeout/setInterval 漏 cleanup
- 全 img 有 alt={fn}
- 0 cache invalidate 漏

## 核心教训

### 第 N+1 轮总比第 N 轮少修 · 但少得越来越快

| 轮 | 检测维度 | 找到问题数 | 用时 |
|---|---|---|---|
| R1 | CSS 字符串(7 维) | 18+ commits | 数小时 |
| R2 | dead code(3 维) | 5 处 | 30 min |
| R3 | 边缘 schema(5 维) | 1 处 | 15 min |

### 每轮 grep pattern 清单

```bash
# R1 视觉残留
grep -rn "border-l-2 border-dashed\|border border-stone-200 rounded bg-white\|max-w-full h-auto.*border\|my-3 flex flex-wrap" src/

# R2 dead code
for f in <file>; do
  for ident in <suspect-list>; do
    [ "$(grep -c $ident $f)" = "1" ] && echo "DEAD: $f · $ident"
  done
done

# R3 复合 key + a11y + cleanup
grep -rn "useEffect.*setTimeout" src/      # cleanup 漏
grep -rn "<img" src/ | grep -v "alt="     # alt 漏
grep -rn "block.type === 'image'" src/    # fall-through
grep -rn "questionCache\|invalidateQuestionCache" src/  # cache invalidate
```

### 灵魂金句

> "审计是迭代的 · 不是一次性的。每轮假设前轮成立 · 加 1 维深度 · 直到 R-N 找不到问题。"

## SOP · 任何整改 sealed 前必跑 3 轮

1. **R1 立法对应扫**(立法本身要解决的问题)
2. **R2 死代码 + gate 扫**(整改后留下的破碎引用 / 漏 gate 路径)
3. **R3 边缘 + a11y + cleanup 扫**(数据 schema 边角 / a11y / hooks / cache)
4. R-N 直到 0 命中 · sealed
5. 每轮失败维度入 `LESSON-023` · 下次整改首查

## 配套立法

- **LESSON-020** · 真题 UI 净化金标准(本批整改 R1 主修复)
- **LESSON-019** · UI 一致性迁移(并行 session · 同期 sealed)
- **LESSON-018** · 元单位原子化 7 步法
- **CHANGE_GOVERNANCE.md** · 任一 sealed 立法须经 3 轮深审 · 否则不入 archive

## 跨账号衔接 · skills 集成

- `25maths-rectification-protocol/SKILL.md` 加 R1/R2/R3 三轮 SOP
- `25maths-context-loader/SKILL.md` 加 LESSON-023 入索引
- 任一新账号接手 · 读 LESSON-023 即知"我现在该跑哪轮"
