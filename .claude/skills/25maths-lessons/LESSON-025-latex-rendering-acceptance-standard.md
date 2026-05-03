---
name: LaTeX 渲染验收金标准
description: 真题数据 LaTeX 渲染 5 类盲区 + 7 步全栈验收 SOP · 2026-05-02 latex.ts 4 commit 修复后立法
type: feedback
auto_load: true
---

# LESSON-025 · LaTeX 渲染验收金标准

> 立法日期:2026-05-02
> 来源:本 session 用户连报 3 处 LaTeX 渲染 bug(`\textit{smallest}` / `40\,cm` / `-8` 短减号)
> Sealed by:数据全栈 grep + 33 tests · 修 5 commits 收口

---

## 0. 触发故事

用户在不到 30min 内连报 3 处真题 LaTeX 渲染 bug:
1. `https://practice.25maths.com/courses/cie-0580/past-papers/2025March-Paper12/q08` · `\textit{smallest}` 显字面量
2. `/courses/hainan-zhongkao/topical` · `OM=40\,cm` · `\,cm` 显字面量
3. 同上 · q03 B 选项 `-8` · ASCII hyphen 偏短

**每报一个修一个** = 反应式开发 = 永远漏。
**改成"修第一个就全栈扫"** = 一次清完同类。

---

## 一、5 类 LaTeX 渲染盲区(本 session 暴露)

| # | 盲区 | 表现 | 出现位置 |
|---|---|---|---|
| 1 | text-mode 命令落 math 外 | `\textit{X}` / `\textbf{X}` / `\underline{X}` 显字面量 | `type: "text"` content |
| 2 | spacing 命令落 math 外 | `\,` / `\;` / `\quad` 显字面量(`$OM=40$\,cm` 模式) | text 块拼 math 块缝隙 |
| 3 | ASCII hyphen vs U+2212 | `-N` 在 prose 字号短紧(plain-number 短路触发) | math 短路 + `\textbf{-N}` |
| 4 | tabular cell 内 LaTeX | `\textbf{X}` 在 `\begin{tabular}` 单元格 | 已 cell-level renderLatex 通过 |
| 5 | 嵌套 `$...$` 在 text-mode | `\textbf{$2$}` math 在 cmd 内 | stash 顺序保护 OK |

---

## 二、根因诊断

### 渲染管线分层(必须画清)

```
原始字符串 input
   ↓
[1] stash math chunks · `$...$` / `$$...$$` → token
   ↓
[2] text-mode preprocessing · `\textit/\textbf/\underline/\,...` → token  ← 本 session 加
   ↓
[3] escapeHtml 整体
   ↓
[4] 还原 textcmd token → HTML(<em>/<strong>/<u>/&thinsp;/...)
   ↓
[5] 还原 math token → KaTeX HTML
   ↓
output
```

**关键不变量**:
- text-mode preprocess 必在 escapeHtml **之前**(否则 `\` 被 escape 失效)
- text-mode preprocess 必在 math stash **之后**(否则 math 内的 `\textbf{}` 被错误处理)
- restore 顺序无关(token 互不冲突)

### Plain-number 短路设计

`$-5$` 走 KaTeX 会因 1.21em scale 在 prose 中跳出。
`PLAIN_NUMBER` regex 短路输出 `<strong>...</strong>` 保字号一致。
**但 ASCII `-` 视觉短紧** → 替前导 `-` 为 U+2212 MINUS SIGN(数学减号)。
同样规则适用 `\textbf{-N}` 通路(都 prose-level)。

---

## 三、7 步 全栈 LaTeX 验收 SOP(每次报 LaTeX bug 必跑)

### Step 1 · 报点定位
```bash
# 找到原始数据文件
grep -rln "<报点关键字>" public/data/papers/ public/data/units/
```

### Step 2 · 全数据同模式扫
```bash
# 找出该模式所有出现位置 · 决定是改数据还是改 renderer
grep -rohE '\\\\<command>\{' public/data/ | sort | uniq -c | sort -rn
```

**判别**:
- 出现 ≤ 3 处 + 数据是手敲 → 改数据
- 出现 > 3 处 OR pipeline 自动产 → **改 renderer**(此 session 选)

### Step 3 · 渲染管线分层验
```bash
# renderLatex 是唯一通路?
grep -rln "renderLatex" src/ | xargs grep -l "type === 'text'\|LatexLine\|dangerouslySetInnerHTML"
```
确认所有 caller 都走同一 renderLatex,否则需逐个修。

### Step 4 · 写测试 ≥ 1
**必须先于代码改**(测试驱动 · 防回归)。
位置:`src/lib/__tests__/latex.test.ts`
```typescript
it('<具体 bug 描述>', () => {
  expect(renderLatex('<原始问题字符串>')).toBe('<期望输出>');
});
```

### Step 5 · 修 latex.ts
- text-mode cmd → 加到 textCmd preprocessing 段
- spacing cmd → 同上 + HTML entity 映射
- prose 视觉 → 改 PLAIN_NUMBER 短路 / textCmd 内 normalize
- math-only cmd → 0 修(KaTeX 处理)

### Step 6 · 跑全 33 tests + build
```bash
npx vitest run src/lib/__tests__/latex.test.ts
npx vite build
```

### Step 7 · 全数据回扫 · 确认其他同类问题
```bash
# 同 commit 内修所有同类
grep -rohE '\\\\(text|math)[a-zA-Z]+\{' public/data/ | sort -u
grep -rE '"[^"]*\\\\<cmd>' public/data/ | grep -vE '\$[^$]*\\\\<cmd>' | head -3
```
若发现新同类 → 回 Step 4(加测试 + 修 + 测)。

---

## 四、铁律

1. **不接受"修了一个 bug"作为完成** · 同 session 内必扫同类全数据
2. **测试先于修复** · 每一个发现都先成测试再写代码
3. **`escapeHtml` 是隔离点** · 任何 stash/restore 都按它分前后
4. **prose 字号一致 = 用 plain-number 短路** · 但要 normalize ASCII hyphen → U+2212
5. **真题数据是唯一真相源** · 不允许"假设作者会写 `$...$` 包裹"
6. **数据有 ~10% pipeline artifact**(textit / 失配 dollar / 嵌套 brace)· renderer 必兜底

---

## 五、数据全扫速查命令(50s 跑完)

```bash
# 1. 所有 text-mode 命令
grep -rohE '\\\\(text|math)[a-zA-Z]+\{[^}]*\}' public/data/ 2>/dev/null | sort -u | head

# 2. 所有 LaTeX 在 math 外的形式(可能漏渲)
grep -rE '"[^"]*\\\\[a-zA-Z]+' public/data/papers/ 2>/dev/null | \
  grep -vE '\$[^$]*\\\\[a-zA-Z]+' | head -3

# 3. spacing 命令
grep -rohE '\\\\[,;:!]|\\\\(quad|qquad)' public/data/ 2>/dev/null | sort | uniq -c

# 4. 数学环境
grep -rohE '\\\\(begin|end)\{[a-z]+\*?\}' public/data/ 2>/dev/null | sort | uniq -c | sort -rn
```

---

## 六、本 session 修复实录(供后人对照)

| Commit | 修复 | 触发点 |
|---|---|---|
| `570c60f2` | `\textit/\textbf/\underline` 在 math 外 → HTML | 用户报 q08 `\textit{smallest}` |
| `0422b976` | `\,/\;/\:/\!/\quad/\qquad` spacing 命令 | 用户报 hainan q15 `40\,cm` |
| `7099193d` | 短路负数 ASCII `-` → U+2212 | 用户报 hainan q03 `-8` |
| `b7bf2af4` | 加 7 测试守门 · 32 → 33 pass | 防回归 |
| `248fcb64` | `\textbf{-N}` 同步 U+2212 normalize | grep 自查发现 s2.10 solutions 含 `\textbf{-2/-4/-8}` |

**关键洞察**:第 5 个修复(`248fcb64`)是 grep 自查在 fix 第 4 个后**主动**发现,不是用户报。这是 SOP Step 7 的真价值。

---

## 七、与其他 LESSON 的关系

- LESSON-017 7 类 pre-ship bug · 本 lesson 是其中"渲染层"的细化
- LESSON-023 multi-round audit · 本 lesson 是其中"渲染审查"的具体清单
- LESSON-024 audit protocol vs intuition · 本 lesson 兑现"protocol 必胜直觉"

下次报渲染 bug → 直接走本 lesson 的 7 步 SOP · 不靠"再扫一遍"的直觉。
