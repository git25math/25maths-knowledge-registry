---
name: Paper Data Hygiene + Multi-Claude Coordination
description: 真题数据卫生(KaTeX-fatal narrow space / shape 双形态 / hash drift)+ 多账号协作 11 类坑(branch race / lock conflict / 远程改动)· Practice 9 PR 沉淀
type: feedback
auto_load: true
---

# LESSON-021 · Paper Data Hygiene + Multi-Claude Coordination

> 立法日期:2026-05-01 · 来源:practice 仓 9 PR + 11 次多账号踩坑
> Sealed by:Practice session 2026-04-30 → 2026-05-01

---

## 一、Paper Data 三类污染必检(KaTeX-fatal 全谱)

### 1.1 narrow space 进入 `$...$` 数学区
KaTeX 严格模式不识别 6 个 Unicode 窄空格:
```
U+00A0 (nbsp)  U+2007 (figure)  U+2008 (punctuation)
U+2009 (thin)  U+200A (hair)    U+202F (narrow nbsp)
```
**修法**:paired math 区内全部替换为 `\,`(LaTeX 合法薄空格)。

### 1.2 currency `$` 未转义 + math 混合
散文里 `$160 which is $\frac{5}{11}$` 用非贪婪 regex 把 `$160` 与 `\frac` 开头 `$` 配对吃掉散文 → 毁掉 `\frac`。
**修法**:smart preescape — `$\d` 后跟 3+ 字母英文单词且无 LaTeX 命令 → 该 `$` 是货币,转义。

### 1.3 unbalanced `$` ≥ 3 奇数
单 `$` 当字面输出无害(renderLatex regex 配对失败),≥ 3 奇数说明真断裂(math span 吃到 EOL)。

### 1.4 工具链(已上线)
- `practice/scripts/audit-paper-latex.py` · audit(`--strict` for CI)
- `practice/scripts/normalize-paper-latex.py` · 一键修复(幂等)
- `practice/scripts/_paper_latex_lib.py` · 共享判定库

### 1.5 真题导入门禁(SOP)
```bash
# PDF → JSON 后立即跑
python3 scripts/audit-paper-latex.py --strict   # 任一 > 0 → block
python3 scripts/normalize-paper-latex.py        # 自动修复
python3 scripts/audit-paper-latex.py            # 必须 0/0/0
npx vite build                                  # 零错误
```

---

## 二、运行时崩溃源 · TS grandfathered 错可崩页

### 2.1 教训(PR #622)
`MultiDimPracticePage.tsx:107` `meta?.label.zh` — BoardMeta 没有 `label` 字段。`meta?.` 防 meta undefined,但 `.label` 不存在 → `.zh` 抛 TypeError → React 整树崩。

TSC ratchet baseline 把 `TS2339` grandfathered → 用户访问该路由触发崩溃才暴露。

### 2.2 高危 TS 错代码(独立审计)
- TS2339 / TS2551(Property does not exist / typo)→ 🔴 高
- TS18047 / TS18048 / TS2531 / TS2532(possibly null/undefined)→ 🟡 中

**规则**:ratchet "新错为 0" ≠ "运行时安全"。grandfathered 错可能是沉睡炸弹。每发布前人工扫一遍 grep。

---

## 三、Mobile 抽屉永远 flex column · `100vh` 不可信

### 3.1 教训(PRs 615 → 623)
iOS Safari `100vh` 包含 URL bar 高度,即使视觉隐藏不收缩。`max-height: calc(100vh - X)` 算出来比可视区大 → `overflow-y-auto` 触不到底部。

### 3.2 正模式
```tsx
<div className={`md:hidden fixed top-0 left-0 right-0 z-50 ${
  open ? 'bottom-0 flex flex-col' : ''
}`}>
  <div className="flex items-center px-4 h-14 shrink-0">{header}</div>
  {open && (
    <nav
      className="flex-1 min-h-0 overflow-y-auto overscroll-contain"
      style={{ WebkitOverflowScrolling: 'touch' as never }}
    >
      {items}
    </nav>
  )}
</div>
```

关键:**不用 100vh** · 用 `bottom-0` 撑满 + flex column + `overscroll-contain` + iOS touch 动量。

---

## 四、多 Claude 账号并发协作协议

### 4.1 现象(本会话 11 次踩坑)
另一 Claude 账号在 main 同时跑 step 75-96(20+ commits)。表现:
- 我刚 commit 报"nothing to commit"(被 fast-forward 进 main)
- 工作树突然变空(`git stash -u` 或 `git pull --rebase`)
- baseline 跳变(别 session 已 `--update`)
- 87 个 untracked 被静默删(PR #420 历史)

### 4.2 协议
1. 任何写操作前 `git fetch origin && git status`
2. 长任务必须 feature branch + PR
3. SESSION-STATE.md 标 "intended branch" 给其他 session 看
4. 缓存策略:L0/L1/L2 分级,跨会话用 SESSION-STATE 30 秒重建上下文
5. Skills 复用:`.claude/skills/` 11 个已立,**不重复造**

### 4.3 防御性 git
- 永远 `git stash -u`(包括 untracked)
- 不用 `git reset --hard` 跨 session
- forced push 用 `--force-with-lease`

---

## 五、Route/Nav lockstep(PR #621)

`navConfig.to` 与 `App.tsx <Route path>` 必须严格一致,否则白屏。

防御方案:
1. 静态 lint(可加 CI step)
2. 主路径用 descriptive(`/teacher/question-board`),旧短路径加 `<Navigate>` redirect alias

类似场景:i18n keys ↔ 翻译、feature flags ↔ DB、API client 类型 ↔ 后端 schema。

---

## 六、Schema 迁移期 · 双字段兼容模式

PaperQuestion 加 `qNum?: number` 兼容字段:
```ts
export interface PaperQuestion {
  qnum: number;                                  // 新规范
  qNum?: number;                                 // 旧 caller 兼容,数据双写
}
```

**模式**:迁移期 JSON 双写两个 key,接口都标 optional 兼容,等所有 caller 迁完再 deprecation。

---

## 七、用户反馈系统应用要点(本批立设计)

详见 `practice/docs/sub-plans/FEEDBACK-SYSTEM-S1-S8.md`。核心铁律:
1. **题目报错不能只入 localStorage** — 学生换设备就丢
2. **admin RLS 必须开 super_admin 读** — 否则 admin 也看不到反馈
3. **被动捕获 80% 有价值反馈**(JS 异常 / chunk-load / KaTeX warn) — 不能只指望用户主动
4. **闭环回信温暖语气** — 符合 SOUL-CHARTER,不"修了 5 件事"罗列
5. **Webhook 必须 dedupe** — 同 variant_id 1h 内仅 1 次,避免风暴

---

## 八、Lesson 引用矩阵

本 lesson 与既有 lesson 关系:
- LESSON-019 UI consistency · 同期但不同主题(UI vs 数据)
- LESSON-020 paper UI cleanup · 前置(UI 净化为本批数据洁净铺路)
- LESSON-018 atomicity 7-step · 复用其"严苛验证"思路到 audit-paper-latex
- LESSON-016 hhk 8-module standard · 复用其"模板化金标准"模式

---

*LESSON-021 v1.0 · sealed 2026-05-01 · 8 类教训 · 跨 Claude 账号必读。*
