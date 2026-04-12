# 25maths Knowledge Registry

## 当前版本：v2.1.0（Phase 5A 完成）

Unified knowledge node registry for the 25Maths ecosystem — a single source of truth for knowledge points across all products (Play, Practice, ExamHub) and exam boards (CIE 0580, Edexcel 4MA1, HHK).

## Quick Start

```bash
# Phase 2 full build pipeline
python3 scripts/build-all.py

# Validate (must pass before commit)
python3 scripts/validate-registry.py

# Coverage report
python3 scripts/check-coverage.py

# Phase 3 data flow verification
python3 scripts/verify-phase3.py
```

## 知识节点

- 203 个原子知识节点（kn_id）
- 193 个 CIE 0580 节点
- 10 个 Edexcel-only 节点
- 272 条依赖边（DAG 无环）

## 考试局覆盖

- CIE 0580：72 sections，288 KP
- Edexcel 4MA1：42 units，exam-refs 74.8%（2435/3257），107 variants 映射完成
- HHK 校本：55 units，Y7-Y11

## Structure

```
25maths-knowledge-registry/
├── schema/                         # JSON Schema definitions
│   └── knowledge-node.schema.json  # KnowledgeNode type
├── registry/                       # Core data
│   ├── kn-registry.json            # 203 knowledge nodes (main registry)
│   ├── kp-kn-map.json              # Play KP → kn_id (288 mappings)
│   ├── hhk-kn-map.json             # HHK unit → kn_id (55 units)
│   └── edx-kn-map.json             # Edexcel section → kn_id (6 ch, 42 sec)
├── graph/
│   └── dag-edges.json              # 272 prerequisite edges (DAG, 0 cycles)
├── dist/                           # Build outputs
│   ├── meta-nodes.json             # 203 enriched meta nodes (with primaryBoard)
│   ├── routes-compiled.json        # All 13 routes compiled
│   ├── coverage-report.json        # Coverage analysis
│   ├── nodes-by-board.json         # Pre-filtered CIE/Edx/both views (P1)
│   ├── question-id-map.json        # kn_id → canonical URL prefix (P1)
│   └── board-stats.json            # Per-board domain breakdown (P1)
├── routes/                         # 13 learning routes (all activated)
│   ├── cie-core-number.json
│   ├── cie-core-geometry.json
│   ├── cie-extended-algebra.json
│   ├── cie-recovery-algebra.json
│   ├── cie-recovery-fractions.json
│   ├── cie-sprint-2weeks.json
│   ├── edx-foundation.json
│   ├── edx-higher.json
│   └── hhk-y7.json ... hhk-y11.json
├── scripts/
│   ├── build-all.py                # Full build pipeline orchestrator
│   ├── build-meta-nodes.py         # Generate meta-nodes.json (+ primaryBoard)
│   ├── build-routes.py             # Fill 13 routes (+ boardFilter)
│   ├── build-board-indexes.py      # P1 artifacts (nodes-by-board, qid map)
│   ├── build-registry.py           # Phase 1 source builder
│   ├── dag_utils.py                # DAG utilities (topo sort, paths)
│   ├── check-coverage.py           # Coverage report
│   ├── validate-registry.py        # Registry + primaryBoard validation
│   └── verify-phase3.py            # Three-product data flow verification
└── .github/workflows/validate.yml  # CI validation
```

## 学习路线（13条，全部激活）

| 路线 | 节点 | 时间 |
|------|------|------|
| CIE Core Number | 58 | ~24.6h |
| CIE Core Geometry | 35 | ~23.3h |
| CIE Extended Algebra | 64 | ~38.0h |
| CIE Recovery Algebra | 26 | ~14.3h |
| CIE Recovery Fractions | 8 | ~3.9h |
| CIE Sprint 2 Weeks | 28 | ~15.2h |
| Edexcel Foundation | 31 | ~19.0h |
| Edexcel Higher | 20 | ~10.0h |
| HHK Y7 | 21 | ~11.0h |
| HHK Y8 | 18 | ~9.9h |
| HHK Y9 | 23 | ~13.0h |
| HHK Y10 | 24 | ~14.0h |
| HHK Y11 | 42 | ~22.1h |

Coverage: 189/203 nodes (93%), 14 uncovered are low-frequency optional variants.

## 三产品接入状态

| 产品 | kn_id | 进度写入 | 路线引擎 | Edexcel |
|------|-------|---------|---------|---------|
| Play | ✅ 294 KP | ✅ 9处 | ✅ DAG | ✅ 复用 CIE variants |
| ExamHub | ✅ 55 HHK | ✅ 2处 | ✅ 课纲 | ✅ 真题 2435/3257 (74.8%) |
| Practice | ✅ 416 variant | ✅ 答题后 | ✅ RouteEngine | ✅ 107 variants + style层 |

## Phase 完成记录

| Phase | 内容 | 状态 |
|-------|------|------|
| Phase 0 | 知识节点注册表建立（203 nodes, 272 edges, 4 maps） | ✅ 完成 |
| Phase 1 | 源数据解析 + KP/HHK/Edexcel 映射 | ✅ 完成 |
| Phase 2 | 元节点体系 + 13条路线填充 + 覆盖率93% | ✅ 完成 |
| Phase 3 | 弱点路线动态生成验证 + 数据流通确认 | ✅ 完成 |
| Phase 4 | Edexcel 4MA1 完整接入（42 units, style layer） | ✅ 完成 |
| Phase 5A | Edexcel exam-refs 74.8% + 107 variants 映射 + 三产品融合 | ✅ 完成 |
| Phase 5B | 综合节点 + 跨产品成就 | 规划中 |

## MetaNode Schema

Each meta node contains:
- `kn_id`, `title_en/zh`, `domain`, `subdomain`
- `examBoards` — CIE 0580 / Edexcel 4MA1 / HHK mappings with tier, weight, paperCodes
- `prerequisites` / `leadsTo` — DAG relationships with hard/soft types
- `content` — variants, missions, generator IDs, exam refs
- `learning` — estimatedMinutes, difficultyRange, isFoundational
- `routes` — which learning routes include this node

See `schema/knowledge-node.schema.json` for the full type definition.
See [`CONSUMERS.md`](CONSUMERS.md) for per-product integration guide.

## 下一步（Phase 5B+）

### P1 — 多考试局分离（所有产品首要任务）
当前问题：CIE 和 Edexcel 节点在路线/地图/练习中混合显示
解决方案：
- [x] meta-nodes 加 `primaryBoard` 字段（cie=105 / edx=10 / both=88）
- [x] 路线文件加 `boardFilter` 字段（cie-*/hhk-* → [cie,both]; edx-* → [edx,both]）
- [x] validate-registry 加 primaryBoard + boardFilter 对齐检查
- [x] `dist/nodes-by-board.json` — cie_view (193) + edx_view (98) 预过滤视图
- [x] `dist/question-id-map.json` — kn_id → `cie.1.4` / `edx.ch1-u7` URL 前缀
- [x] `dist/board-stats.json` — KnowledgeMap board tab 用的领域计数
- [ ] Practice 消费 `question-id-map.json` 生成 URL 路由 (产品侧)
- [ ] KnowledgeMap 消费 `nodes-by-board.json` 渲染 board tab (产品侧)

### P2 — Phase 5B 综合节点
- [ ] 跨 section 综合节点定义（Mock 模板已验证可行）
- [ ] 知识图谱添加综合节点边

### P3 — Phase 5C 成就统一
- [ ] 三产品成就合并展示
- [ ] Mock 相关成就（首次完成/A级/满分等）

---

*v2.1.0 — Phase 5A complete — 2026-04-07*
