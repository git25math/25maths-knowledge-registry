# 25maths Knowledge Registry

## 当前版本：v1.0.0（Phase 2 完成）

Unified knowledge node registry for the 25Maths ecosystem — a single source of truth for knowledge points across all products (Play, Practice, ExamHub) and exam boards (CIE 0580, Edexcel 4MA1, HHK).

## Quick Start

```bash
# Phase 2 full build pipeline
python3 scripts/build-all.py

# Validate (must pass before commit)
python3 scripts/validate-registry.py

# Coverage report
python3 scripts/check-coverage.py

# Phase 3 verification
python3 scripts/verify-phase3.py
```

## 知识节点

- 203 个原子知识节点（kn_id）
- 193 个 CIE 0580 节点
- 10 个 Edexcel-only 节点
- 272 条依赖边（DAG 无环）

## 考试局覆盖

- CIE 0580：72 sections，288 KP
- Edexcel 4MA1：42 sections，完整真题库
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
│   ├── meta-nodes.json             # 203 enriched meta nodes
│   ├── routes-compiled.json        # All 13 routes compiled
│   └── coverage-report.json        # Coverage analysis
├── routes/                         # 13 learning routes (filled)
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
│   ├── build-all.py                # Phase 2 build pipeline
│   ├── build-meta-nodes.py         # Generate meta-nodes.json
│   ├── build-routes.py             # Fill 13 routes
│   ├── build-registry.py           # Phase 1 source builder
│   ├── dag-utils.py                # DAG utilities (topo sort, paths)
│   ├── check-coverage.py           # Coverage report
│   ├── validate-registry.py        # 10-check validation
│   └── verify-phase3.py            # Phase 3 data flow verification
└── .github/workflows/validate.yml  # CI validation
```

## 学习路线（13条）

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

| 产品 | kn_id | 进度写入 | 路线引擎 |
|------|-------|---------|---------|
| Play | 294 KP | 9处 | 隐含DAG |
| ExamHub | 55 HHK | FLM | 课纲 |
| Practice | 647 variant | 答题后 | RouteEngine |

## MetaNode Schema

Each meta node contains:
- `kn_id`, `title_en/zh`, `domain`, `subdomain`
- `examBoards` — CIE 0580 / Edexcel 4MA1 / HHK mappings with tier, weight, paperCodes
- `prerequisites` / `leadsTo` — DAG relationships with hard/soft types
- `content` — variants, missions, generator IDs, exam refs
- `learning` — estimatedMinutes, difficultyRange, isFoundational
- `routes` — which learning routes include this node

See `schema/knowledge-node.schema.json` for the full type definition.

## 下一步（Phase 3-5）

- Phase 3：弱点路线动态生成验证
- Phase 4：Edexcel variants 建立
- Phase 5：综合节点 + 跨产品成就

---

*Phase 2 complete — 2026-04-07*
