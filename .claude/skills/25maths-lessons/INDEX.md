# Lessons Library Index

> **机制**:ADR-0065 · 每修复必产 lesson · `auto_load: true` 同步到 7 仓 `.claude/skills/25maths-lessons/`

---

## Active Lessons(自动 load 到所有 Claude session · 24 条)

### 🔴 Red-line · 红线类(违即触灵魂宪章 / 信任红线)

| ID | Title | Date |
|---|---|---|
| [LESSON-004](LESSON-004-never-touch-user-private-workspace.md) | 用户私人工作仓(NZH Dashboard)永不主动修改 · 即使清理 charter 也不 | 2026-04-26 |
| [LESSON-005](LESSON-005-no-premature-commercialization.md) | 过早商业化设计创造反向灵魂压力 · 推迟到 post-Beta(ADR-0058)| 2026-04-26 |
| [LESSON-008](LESSON-008-defer-pre-emptive-architecture.md) | Beta 期不解决"未来痛点" · 推迟架构 commit · 优先 1 行措辞 / opt-in | 2026-04-26 |
| [LESSON-009](LESSON-009-grep-v3-plan-before-new-adr.md) | 立新 ADR 前 grep v3 plan + Stages 综合 · 防重复治理 · 优先 1 行修订指向真相源 | 2026-04-26 |
| [LESSON-010](LESSON-010-grep-prod-schema-not-just-frontend-code.md) | 起 SQL artifact 前必 grep prod migration + information_schema · 不信 frontend `.select()` · LESSON-009 schema 域强化版 | 2026-04-26 |
| [LESSON-011](LESSON-011-prod-deploy-then-rename-draft-to-migration.md) | prod deploy 后 _DRAFT 必须改名入仓 migration · "跑过了" ≠ "入历史了" · LESSON-009/010 闭环 | 2026-04-26 |
| [LESSON-012](LESSON-012-grep-prod-rpc-names-before-deploy.md) | deploy 前必 grep prod RPC 名 · 同名 overload + default 参数 = ambiguity 错 · 默认重命名 v1 | 2026-04-26 |
| [LESSON-013](LESSON-013-backend-deploy-is-not-user-experience-ship.md) | 🔴 backend deploy ≠ user experience ship · 前端 0 wire = 学生 0 感知 · DoD 6 步 + 第 6 灵魂问"可见性" | 2026-04-26 |
| [LESSON-014](LESSON-014-wrong-answer-moment-only-three-things.md) | 🔴 错题瞬间 = 3 件事(看答案/为什么错/再来一题)· 教学瞬间 + 推荐 留 session 总结 · 克制原则 | 2026-04-26 |
| [LESSON-015](LESSON-015-no-overload-five-rules.md) | 🔴 整站不过载 5 铁律 · 情境界面/分角色/push 白名单/纯继续语/双层数据 · 014 整站升级 | 2026-04-26 |
| [LESSON-016](LESSON-016-hhk-8-module-content-standard.md) | 哈罗课纲 8 模块内容标准(词/学/例/手把手/配套/专题/真题/延伸)· NZH 创作必查 | 2026-04-26 |
| [LESSON-017](LESSON-017-pre-ship-7-bug-categories.md) | 链路重构 ship 前 7 类 bug 探针 · 数据假设/列写入/返回链/UI重复/HTML/路由/nav覆盖 | 2026-04-27 |
| [LESSON-018](LESSON-018-atomicity-7-step-method.md) | 元单位拆解 7 步法 · 心法 24-31 · audit→plan→MEU→close→META→query→invariants · 大工程 SOP | 2026-04-29 |
| [LESSON-019](LESSON-019-ui-consistency-migration-gold-standard.md) | 🔴 UI 一致性 7 条金标准 · DashboardLayoutV2 单一 wrapper + PageGuardState 守门 + flex-wrap 移动端 + 路由限教师红线 · AUDIT § 2 UI 一致性域强化 | 2026-05-01 |
| [LESSON-020](LESSON-020-paper-ui-cleanup-2026-05-01.md) | 🔴 真题 UI 净化 5 类违规 + 多渲染路径纪律 + 数据 shape 双形态 + 全栈 audit SOP · Practice v2.98.0 | 2026-05-01 |
| [LESSON-021](LESSON-021-paper-data-hygiene-and-multi-claude-coordination.md) | 🔴 真题 KaTeX-fatal 数据卫生 + 多账号协作 11 类坑 · Practice 9 PR 沉淀 | 2026-05-01 |
| [LESSON-022](LESSON-022-lesson-distribution-pipeline-discipline.md) | 🔴 lesson distribution 5 步 pipeline · 文件存在 ≠ 跨账号 active · audit-lessons-pipeline.sh 自动化防线 · LESSON-013 协作层对偶 | 2026-05-01 |
| [LESSON-023](LESSON-023-multi-round-audit-discipline.md) | 🔴 多轮审计纪律 R1/R2/R3 · 每轮加 1 维 · 整改 sealed 前必经 ≥ 3 轮 | 2026-05-01 |
| [LESSON-024](LESSON-024-audit-protocol-vs-intuition-blind-spots.md) | 🔴 协议化 vs 直觉化 5 类盲区 · 三层 TodoList · 收尾强制 5 问 · LESSON-023 元教训层 | 2026-05-01 |

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

## 防重复治理铁七角(2026-04-26 · 7 LESSONs 立成)

| LESSON | 阶段 | 防止 | 真相源 |
|---|---|---|---|
| **007** | 写 TASK 前 | 重复造 TASK | v3 plan TASK 表 |
| **008** | Beta 期决策 | 过早架构 commit | 真实痛点 |
| **009** | 立 ADR 前 | 重复治理 | v3 plan + Stages |
| **010** | 起 SQL schema 前 | 错位列/表假设 | supabase prod `information_schema` |
| **011** | deploy 后 | git 与 prod 偏离 | 改名入仓 + DEPLOYED header |
| **012** | deploy RPC 前 | 同名 overload ambiguity | `pg_proc` WHERE proname |
| **013 🔴** | **task 标 ✅ 前** | **backend done = user happy 错觉 · DoD 漏洞** | **NZH 真账号 UI 验收 + 第 6 灵魂问** |

**共同主旨**:任何 artifact 立 / 改 / deploy / 标 done 前后必先 grep 真相源 + 把 prod 真相回流到 git + **学生真实可见才算 done**。git 不一定是 single source of truth(尤其 schema)· deploy 后必让 git 重成真相(LESSON-011)· **backend ready ≠ ship**(LESSON-013 灵魂红线)。

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

*Last updated: 2026-05-01 · 24 active lessons · 0 archived · LESSON-022/023/024 R2-R3 audit 补(distribution pipeline + 多轮纪律 + 协议化盲区 三联立法)*
