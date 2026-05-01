---
name: Lesson Distribution Pipeline Discipline
description: lesson 文件存在 ≠ 跨账号 active · 必经 5 步 pipeline(frontmatter / INDEX / sync 脚本 / 8 仓 commit / 8 仓 push)· 任一步漏 = 全 8 仓接手者读不到 · 加自动化 lint 防回归
type: feedback
auto_load: true
---

# LESSON-022 · Lesson Distribution Pipeline Discipline

> 立法日期:2026-05-01
> 来源:**同 session 内连续 2 次"sealed"声明都漏 lesson** — LESSON-019 + LESSON-021 各自被声明已 sync,实际 8 仓无文件
> 姊妹 lesson:LESSON-013(backend deploy ≠ user experience ship)· **本 lesson 是 LESSON-013 的"内部协作层"对偶**
> Severity:🔴 红线类 — 跨账号无缝衔接是 ADR-0067 核心承诺,违反 = 下一个 Claude session 接手时 lesson 不在 context

---

## TL;DR · 一句话原则

> **lesson 文件写完 ≠ 跨账号 active**。`git commit + push planning` ≠ "8 仓 Claude session 启动时能读到"。
>
> 必经 5 步 pipeline · 任一步漏 = silent fail · **接手者完全看不到这条 lesson 存在**。

---

## 一、产生这条 lesson 的两次踩坑(同 session 连续犯)

### 1.1 LESSON-019(UI 一致性金标准)— round 1 漏

**症状**:声明"8 仓 sealed in sync"后,接手者审计发现 `LESSON-019=N` 在所有 8 仓。

**根因**:
1. 我写文件时**漏了 YAML frontmatter**(用了 `# LESSON-019 · UI...` 直接进 H1 · 0 metadata)
2. 跑 `sync-skills-and-lessons.py` 时,`is_auto_load()` 返回 False · **silent skip**
3. 我没读 sync 输出的"Found N auto_load lessons"数字与 INDEX 是否对得上
4. 我用"文件 commit 进 planning"当成"sync 完成"宣布 sealed

**修复轨迹**(round 1 audit):
- 加 frontmatter(name / description / type / auto_load: true)
- 重 sync · 输出从 "19 auto_load" → "20 auto_load"(对上)
- 8 仓 commit + push

### 1.2 LESSON-021(Paper data + multi-claude)— round 2 才发现

**症状**:LESSON-019 修完后再 audit,发现 LESSON-021 文件存在但**完全没 frontmatter** + **不在 INDEX** + **不在任何仓的 .claude/skills/** 下。

**根因**:
1. 并行 session 写 LESSON-021 时同样漏了 frontmatter(犯了和我 LESSON-019 一样的错)
2. 并行 session 也没 register 到 INDEX.md
3. 第一次 round 1 audit 我**只检查 LESSON-019 + LESSON-020**(我"知道的两个"),没扫整个 lessons/ 目录
4. **Round 1 sealed 声明 = 二次 silent fail** · LESSON-021 在所有 8 仓都不存在

**修复轨迹**(round 2):
- 补 frontmatter
- 加 INDEX
- 重 sync · 8 仓 commit + push

---

## 二、5 步 Pipeline · 缺一步即 silent fail

```
┌──────────────────────────────────────────────────────────────────┐
│ Step 1 · 写 lesson 文件 + YAML frontmatter                       │
│   必须含:name / description / type / auto_load: true            │
│   verify:`grep -L 'auto_load:' lessons/LESSON-*.md` 必空        │
├──────────────────────────────────────────────────────────────────┤
│ Step 2 · 加 INDEX.md 对应 severity 章节                          │
│   verify:`grep -L 'LESSON-NNN' lessons/INDEX.md` 必为空(对该 NNN)│
├──────────────────────────────────────────────────────────────────┤
│ Step 3 · commit + push planning 仓                               │
│   verify:`git log origin/main -1 --name-only \| grep LESSON-NNN` │
├──────────────────────────────────────────────────────────────────┤
│ Step 4 · 跑 `python3 scripts/sync-skills-and-lessons.py`         │
│   verify:输出的"Found N auto_load lessons" 数字 == INDEX 行数   │
├──────────────────────────────────────────────────────────────────┤
│ Step 5 · 8 仓各自 commit + push .claude/skills/25maths-lessons/  │
│   verify:cross-repo audit 脚本(下文 § 4)所有仓 LESSON-NNN=Y    │
└──────────────────────────────────────────────────────────────────┘
```

**任何一步漏** → 下一个 Claude session 在该仓启动时,`auto_load` 机制扫不到此 lesson → **接手者完全看不到这条 lesson 存在** → 重蹈被 lesson 防的覆辙。

---

## 三、为什么会反复发生(根因分析)

### 3.1 "文件存在" 是错的 progress signal

我 / 并行 session 都把"`git status` clean + commit pushed in planning" 当成 "sealed"。
**这是错的 mental model**。

实际真相:**lesson 必须在 8 仓的 `.claude/skills/25maths-lessons/` 下都有文件 + 都已 push 到 origin**,接手者 clone 后才看得到。这是 ADR-0067 的承诺。

### 3.2 sync 脚本静默跳过

`is_auto_load()` 返回 False 时**只跳过 · 不报警**。20 auto_load lessons 但 lessons/ 下有 22 个 LESSON-* 文件 — 这个差是**致命信号**,但脚本不打印。

### 3.3 audit 范围太窄(round 1 教训)

第一次"再继续审查是否还有遗漏"时,我**只 audit 我手写的两个 lesson**(LESSON-019 + LESSON-020),没扫整个 lessons/ 目录。所以 LESSON-021 第一次 audit 漏了。

### 3.4 双标 frontmatter schema

planning/lessons/ 里两套 frontmatter schema 并存:
- 旧 schema(LESSON-001..018 + 020):`name / description / type / auto_load`
- 新 schema(我写的 LESSON-019 originally):`id / title / category / severity / related_ADR / keywords / auto_load`
- LESSON-021:**两套都不用** — 0 frontmatter

`is_auto_load()` 不挑 schema · 只看是否有 `auto_load: true` 一行。但人写的时候不注意,容易漏。

---

## 四、自动化防线(立 + 跑)

### 4.1 lessons/ 目录预检脚本(本 lesson 同步立)

`scripts/audit-lessons-pipeline.sh`(下面立)· 跑出 5 类问题任一即 exit 1:

```bash
#!/usr/bin/env bash
# audit-lessons-pipeline.sh — 5 步 pipeline 自检
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

# Check 1: 每个 LESSON-*.md 必含 auto_load: true
echo "[1/5] frontmatter 自检..."
for f in lessons/LESSON-*.md; do
  if ! grep -q '^auto_load: *true' "$f"; then
    echo "  ❌ $f 缺 auto_load: true frontmatter"
    fail=1
  fi
done

# Check 2: 每个 LESSON-NNN 必在 INDEX
echo "[2/5] INDEX 注册自检..."
for f in lessons/LESSON-*.md; do
  nnn=$(basename "$f" | grep -oE 'LESSON-[0-9]+')
  if ! grep -q "$nnn" lessons/INDEX.md; then
    echo "  ❌ $nnn 不在 INDEX.md"
    fail=1
  fi
done

# Check 3: planning 仓本身已 push
echo "[3/5] planning push 自检..."
unpushed=$(git log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "$unpushed" != "0" ]; then
  echo "  ❌ planning 仓有 $unpushed 个 unpushed commit"
  fail=1
fi

# Check 4: auto_load 数 == INDEX 引用数
echo "[4/5] count match 自检..."
auto_n=$(grep -l '^auto_load: *true' lessons/LESSON-*.md | wc -l | tr -d ' ')
idx_n=$(grep -oE 'LESSON-[0-9]+' lessons/INDEX.md | sort -u | wc -l | tr -d ' ')
if [ "$auto_n" != "$idx_n" ]; then
  echo "  ⚠️  auto_load=$auto_n vs INDEX 引用=$idx_n(允许 INDEX 多 · 不允许少)"
  [ "$auto_n" -gt "$idx_n" ] && fail=1
fi

# Check 5: 跨仓 active 自检(cross-repo audit)
echo "[5/5] 跨仓 active 自检..."
for repo in 25Maths-Keywords 25maths-games-legends 25maths-knowledge-registry \
            25maths-os 25maths-practice 25maths-website Teaching math-video-engine; do
  d="$HOME/Project/ExamBoard/$repo"
  [ -d "$d" ] || continue
  for f in lessons/LESSON-*.md; do
    name=$(basename "$f")
    if [ ! -f "$d/.claude/skills/25maths-lessons/$name" ]; then
      echo "  ❌ $repo 缺 $name"
      fail=1
    fi
  done
done

[ $fail = 0 ] && echo "✅ 5/5 pipeline checks pass" || { echo "❌ pipeline 有漏 · 跑 sync-skills-and-lessons.py 修"; exit 1; }
```

**何时跑**:每次"sealed"声明前必跑 · CI 也跑(planning 仓 push 后)。

### 4.2 sync 脚本输出强化(本 lesson 后续 PR 改进)

`sync-skills-and-lessons.py` 启动时打印:
```
Found 22 LESSON-*.md files
Found 22 with auto_load: true   ← 必相等
Found 22 in INDEX.md             ← 必相等
```

任何不等 · 红字 + exit 1 · 不 silent。

---

## 五、How to apply(写 lesson 流程)

```
1. 写 LESSON-NNN-slug.md
   · 第一行必为 `---`(YAML frontmatter 开头)
   · 含 4 字段:name / description / type / auto_load: true
   · 第二个 `---` 后才写 H1 # LESSON-NNN ·

2. 加 INDEX.md 对应 severity 章节(🔴/🟡/🟢)+ 末尾"Last updated"行

3. cd ~/Project/ExamBoard/25maths-planning

4. bash scripts/audit-lessons-pipeline.sh
   · 必通过 · 否则修

5. git add lessons/ && git commit && git push

6. python3 scripts/sync-skills-and-lessons.py
   · 必出 "Found N auto_load lessons" · N 必含本次新 lesson

7. 在 8 仓循环 commit + push(参 LESSON-022 § 4.1 第 5 步脚本逻辑)

8. 再跑 audit-lessons-pipeline.sh
   · 5/5 pass 才能宣布 "sealed"
```

**严禁**:跳过任一步说"sealed" · 后续 audit 必返工 + 浪费 ≥ 5 min token。

---

## 六、引用

- LESSON-013 backend deploy ≠ user experience ship(本 lesson 协作层对偶)
- LESSON-006 跨账号可移植 = repo-committed skills(承诺源)
- ADR-0067 跨仓 sync 协议
- AUDIT_FRAMEWORK § 8 DRY 强约束
- 同 session 案例:LESSON-019(round 1 漏)+ LESSON-021(round 2 漏)

---

## 七、并行 session 推 import 漏 implementation(2026-05-01 案例)

**症状**:并行 session 在 `ui/year-picker-polish` 分支立 `useCrossBoardTotals` hook + 改 2 页 import · 但只把 2 页改动推 main · `src/lib/papers/totals.ts` 实现留在分支 → main `npx vite build` 报 "Cannot resolve @/lib/papers/totals" → 全站 build broken。

**和本 lesson 主题(lesson distribution)的关联**:
本质是同类错 — **"我以为已经全栈交付了" 但实际只交付了一半**。lesson 主题是"frontmatter / INDEX / sync / 8 仓 commit 任一步漏 = silent fail";本案例是"分支 import 推 main 但 implementation 留分支 = build fail"。

**修复**:
- 当场 cherry-pick `ui/year-picker-polish` 的 totals.ts 到 main(commit `6aa03bbe3`)

**新增防线**(本 lesson § 五 8 步流程之外的并行 session 协作纪律):

```bash
# 任何分支推 main 之前 · 必跑:
git checkout main
git pull
npx vite build       # 必 0 错误
# 或 check-only(更快):
git fetch origin main && git diff origin/main --name-only | grep -E '\.(ts|tsx)$' | \
  while read f; do
    grep -h "^import.*from '@/" "$f" 2>/dev/null
  done | sort -u | while read line; do
    # 验证每个 @/path 真存在
    p=$(echo "$line" | sed -E "s|.*from '@/([^']+)'.*|src/\1|")
    [ -f "$p.ts" ] || [ -f "$p.tsx" ] || [ -f "$p/index.ts" ] || echo "MISSING: $p"
  done
```

**根因**:并行多 Claude session 各自 push 到不同分支,人工合并时容易漏文件。
**长期对策**:CI 加 `audit-missing-imports.sh`(已有 · 2026-04-27 立)+ 每个分支 push 前自跑。

事故 commit 链:`f95bfdf5e`(import 推 main 漏 file)→ `6aa03bbe3`(救火补 file)。
