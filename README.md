# 25Maths Knowledge Registry

Unified knowledge node registry for the 25Maths ecosystem — a single source of truth for knowledge points across all products (Play, Practice, ExamHub) and exam boards (CIE 0580, Edexcel 4MA1, HHK).

## Quick Start

```bash
# Build registry from source data
python3 scripts/build-all.py

# Validate (must pass before commit)
python3 scripts/validate-registry.py
```

## Structure

```
25maths-knowledge-registry/
├── schema/                         # JSON Schema definitions
│   └── knowledge-node.schema.json  # KnowledgeNode type
├── registry/                       # Core data
│   ├── kn-registry.json            # 201 knowledge nodes (main registry)
│   ├── kp-kn-map.json              # Play KP → kn_id (288 mappings)
│   ├── hhk-kn-map.json             # HHK unit → kn_id (55 units)
│   └── edx-kn-map.json             # Edexcel section → kn_id (6 ch, 42 sec)
├── graph/
│   └── dag-edges.json              # 165 prerequisite edges (DAG, 0 cycles)
├── routes/                         # 13 learning route frameworks
│   ├── cie-core-number.json
│   ├── cie-extended-algebra.json
│   ├── edx-foundation.json
│   ├── hhk-y7.json ... hhk-y11.json
│   └── ...
├── scripts/
│   ├── build-all.py                # Build from Play + Edexcel sources
│   └── validate-registry.py        # 10-check validation
└── .github/workflows/validate.yml  # CI validation
```

## Registry Stats

| Metric | Value |
|--------|-------|
| Knowledge Nodes | 201 (191 CIE + 10 Edexcel-only) |
| DAG Edges | 165 (68 hard + 97 soft, 0 cycles) |
| KP Mappings | 288 Play KPs |
| HHK Units | 55 (Y7-Y11) |
| Edexcel Sections | 42 across 6 chapters |
| Learning Routes | 13 frameworks |

## KnowledgeNode Schema

Each node has: `kn_id`, `title_en/zh`, `domain`, `examBoards` (CIE/Edexcel/HHK), `prerequisites`, `leadsTo`, `difficultyRange`, and content references.

See `schema/knowledge-node.schema.json` for the full type definition.

---

*Phase 0 complete — 2026-04-07*
