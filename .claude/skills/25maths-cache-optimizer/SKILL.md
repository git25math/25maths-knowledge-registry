---
name: 25maths-cache-optimizer
description: Apply ADR-0066 token cache 5 ironclads. Pre-task scan for cache miss antipatterns. Invoke `/25maths-cache-optimizer` to manually self-audit current session. Cross-account portable.
---

# 25Maths Cache Optimizer

## 用途
让 Claude session 维持 cache hit rate 70-80%(默认 ~30%)· 等价 2-3x 响应速度 + 2-3x 长会话不 truncate。

## 5 铁律(ADR-0066)

### 铁律 1 · 慢变内容不 daily-edit
🚨 **不要改**:
- ADR-0040(灵魂宪章)/ ADR-0059(创立初心)
- V3_FINAL_CHEATSHEET.md
- charter v3.X(月级才升 · 不 weekly)

改 = 全 session cache 失效 · 烧 token。

### 铁律 2 · Markdown `---` 分隔
每 doc 章节 `---` 分隔 · cache 算法精准识别 prefix。

### 铁律 3 · Edit > Write
- `Edit` 替片段(cache 影响小)
- `Write` 整文件覆盖(cache 全失效)

→ 优先用 Edit · 仅新建 / 完全重写时才 Write。

### 铁律 4 · 大文档分 chunk 读
读 50K 文档时 50 行/次 · 每 chunk 独立 cache。

### 铁律 5 · 5 分钟内不重复 read
- 刚 edit 的文件 5 min 内不 re-read
- 刚 read 过的不立即 re-read
- 例外:用户明确要求 / 文件被外部改

## 慢/中/快 三档分类

| 档 | 例子 | Cache 策略 |
|---|---|---|
| 🟢 慢(月级)| ADR-0040/0059, V3_FINAL_CHEATSHEET, 战略 ADR | 顶部 · 最大化 cache hits |
| 🟡 中(周级)| TASK 列表, charter 版本, L2 ADRs | 中段 · 选择性 cache |
| 🔴 快(日级)| session 消息, handoff, 新 lessons | 末尾 · 不 cache |

## 反模式 grep 黑名单

任务前自检以下:
- ❌ "把 60 ADR 全 read 一遍"(50K+ token cache miss)
- ❌ "再读一次 V3_FINAL_CHEATSHEET 看看"(刚读过)
- ❌ "先 edit ADR-0040 一行,再 read 几个文件"(慢变 hack 改)
- ❌ "Write 全部覆盖" 当应该 Edit 时

## 触发条件

- **自动**:每个任务开始前快速自检(隐式)
- **手动**:用户输入 `/25maths-cache-optimizer` · Claude 输出当前 session 的 cache 健康度报告

## 量化检测(invoke 时输出)

```
Cache Health Report:
- Slow-change edits in last 30 min: X (target: 0)
- Repeated reads in last 5 min: X (target: 0)  
- Average chunk size on Read: X lines (target: ≤ 50)
- Edit vs Write ratio: X (target: > 5:1)
- Estimated cache hit rate: X% (target: > 70%)
```

## Cross-account 可移植

本 skill 提交 git · 任何 Claude 账号 clone 25maths-planning 即得。
铁律是结构性 · 不依赖 user-specific 设置。
