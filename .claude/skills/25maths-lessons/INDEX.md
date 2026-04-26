# Lessons Library Index

> **机制**:ADR-0065 · 每修复必产 lesson · `auto_load: true` 同步到 7 仓 `.claude/skills/25maths-lessons/`

---

## Active Lessons(自动 load 到所有 Claude session · 9 条)

### 🔴 Red-line · 红线类(违即触灵魂宪章 / 信任红线)

| ID | Title | Date |
|---|---|---|
| [LESSON-004](LESSON-004-never-touch-user-private-workspace.md) | 用户私人工作仓(NZH Dashboard)永不主动修改 · 即使清理 charter 也不 | 2026-04-26 |
| [LESSON-005](LESSON-005-no-premature-commercialization.md) | 过早商业化设计创造反向灵魂压力 · 推迟到 post-Beta(ADR-0058)| 2026-04-26 |
| [LESSON-008](LESSON-008-defer-pre-emptive-architecture.md) | Beta 期不解决"未来痛点" · 推迟架构 commit · 优先 1 行措辞 / opt-in | 2026-04-26 |
| [LESSON-009](LESSON-009-grep-v3-plan-before-new-adr.md) | 立新 ADR 前 grep v3 plan + Stages 综合 · 防重复治理 · 优先 1 行修订指向真相源 | 2026-04-26 |
| [LESSON-010](LESSON-010-grep-prod-schema-not-just-frontend-code.md) | 起 SQL artifact 前必 grep prod migration + information_schema · 不信 frontend `.select()` · LESSON-009 schema 域强化版 | 2026-04-26 |

### 🟡 Workflow · 工作流类(防具体动作出错)

| ID | Title | Date |
|---|---|---|
| [LESSON-001](LESSON-001-charter-sync-awk-failure.md) | charter sync awk multiline 失败 → 用 Python 替代 | 2026-04-26 |
| [LESSON-002](LESSON-002-quarterly-consistency-audit.md) | 跨多 session ADR layered 加叠隐含 silent inconsistency · 季度 audit 必走 | 2026-04-26 |
| [LESSON-006](LESSON-006-cross-account-portable-skills.md) | 跨账号可移植 = repo-committed skills · 不依赖 user-level memory | 2026-04-26 |
| [LESSON-007](LESSON-007-stage-research-before-revising.md) | 多 stage 综合先做 v3 plan TASK inventory · 不要重新发明已存在的 TASK | 2026-04-26 |

### 🟢 Meta · 元认知类(对项目本质的认知校准)

| ID | Title | Date |
|---|---|---|
| [LESSON-003](LESSON-003-solo-dev-claude-25-75.md) | solo dev + Claude Max 20× = 25/75 工时拆分 · 不是 1+1 | 2026-04-26 |

---

## 防重复治理铁四角(2026-04-26 · session 沉淀)

| LESSON | 防止 | 真相源 |
|---|---|---|
| **007** | 多 stage 综合 → 重复造 TASK | v3 plan TASK 表 |
| **008** | Beta 期 → 过早架构 commit | 真实痛点(非未来想象) |
| **009** | 立新 ADR → 重复治理 | v3 plan + Stages 累积 |
| **010** | 起 SQL artifact → 错位 schema 假设 | supabase prod `information_schema.columns` |

**共同主旨**:任何 artifact 立 / 改 / deploy 前必先 grep 真相源 · git 不一定是 single source of truth(尤其 schema · 因 hot-patch / dashboard 改 / 多 worktree)。

实战印证:本 session 节省 ~10d 工程时间(防 4 个新 TASK + 防 2 个 ADR 立法 + 防 prod schema 误改)。

---

## Severity 与 Category 速查

| 标签 | 含义 |
|---|---|
| 🔴 Red-line | 违反触灵魂宪章 / 合规 / 信任红线 · 必须强制遵守 |
| 🟡 Workflow | 具体动作错误防范 · 影响效率但不触红线 |
| 🟢 Meta | 元认知校准 · 长期项目理解 |

| Category | 范围 |
|---|---|
| red-line | 灵魂宪章 / 合规 / 信任 · ADR-0040/0058/0059 联动 |
| workflow | 工具 / 流程 / 自动化 · ADR-0064-0069 联动 |
| meta | 项目本质 / 协作 / 节奏 · 跨 ADR |
| sync | charter / lessons / skills 跨仓同步 · ADR-0067 联动 |

---

## Archive(stale · 不 sync)

(空)

---

## 写新 LESSON 检查清单

- [ ] frontmatter 含 `name` / `description` / `type` / `auto_load: true`
- [ ] 触发场景写明(避免抽象规则 · 用具体事件)
- [ ] 规则段含 **Why** + **How to apply**
- [ ] 反例 + 正例 各至少一个
- [ ] 同类 LESSON 关联(若有)
- [ ] 检查清单(若是 workflow 类)
- [ ] 加入本 INDEX 对应 severity 章节
- [ ] 跑 `python3 scripts/sync-skills-and-lessons.py` 同步 8 仓

---

*Last updated: 2026-04-26 · 9 active lessons · 0 archived · 防重复治理铁三角立成(007/008/009)*
