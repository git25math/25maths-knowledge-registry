# Consuming the Knowledge Registry

This doc explains how each product consumes `dist/` artifacts.

## Artifact Overview

| File | What | Primary Consumer |
|------|------|-----------------|
| `meta-nodes.json` | 203 enriched nodes (DAG, boards, learning) | All products |
| `routes-compiled.json` | 13 routes in one file | RouteEngine (Practice) |
| `nodes-by-board.json` | Pre-filtered CIE/Edx views | KnowledgeMap |
| `question-id-map.json` | kn_id → URL prefix | Practice URL routing |
| `board-stats.json` | Board × domain counts | KnowledgeMap tab UI |
| `coverage-report.json` | Route coverage stats | Internal dashboards |
| `build-manifest.json` | Source hashes for freshness | CI only |

## Per-Product Guide

### Practice (题目练习)

**Route loading:**
```ts
import routes from 'knowledge-registry/dist/routes-compiled.json';

// Get a specific route
const cieNumber = routes['cie-core-number'];

// Filter nodes (skip milestones)
const knNodes = cieNumber.nodes.filter(n => !n.milestone);
```

**Board-specific URL routing:**
```ts
import qidMap from 'knowledge-registry/dist/question-id-map.json';

// Generate practice URL for a node
function getPracticeUrl(knId: string, board: 'cie' | 'edx'): string {
  const prefix = qidMap[knId]?.[board];
  // prefix = "cie.1.4" → /practice/cie/1.4
  // prefix = "edx.ch1-u7" → /practice/edx/ch1-u7
  return prefix ? `/practice/${prefix.replace('.', '/', 1)}` : null;
}
```

**Prerequisite check:**
```ts
import meta from 'knowledge-registry/dist/meta-nodes.json';

const node = meta.find(n => n.kn_id === 'kn_0042');
const prereqs = node.prerequisites; // [{kn_id, type: "hard"|"soft"}]
const canUnlock = prereqs
  .filter(p => p.type === 'hard')
  .every(p => userMastery[p.kn_id] >= 0.8);
```

### KnowledgeMap (知识地图)

**Board tab filtering:**
```ts
import boardData from 'knowledge-registry/dist/nodes-by-board.json';
import stats from 'knowledge-registry/dist/board-stats.json';

// Tab: "CIE 0580" shows 193 nodes
const cieNodes = boardData.cie_view;

// Tab: "Edexcel 4MA1" shows 98 nodes
const edxNodes = boardData.edx_view;

// Domain sidebar counts
const cieDomains = stats.cie.domains;
// { number: 33, algebra: 25, geometry: 25, probability: 6, statistics: 16 }
```

**Rendering node cards:**
```ts
// Each entry in cie_view:
interface BoardNode {
  kn_id: string;
  title_en: string;
  title_zh: string;
  domain: string;
  subdomain: string;
  difficultyRange: [number, number];
}
```

### ExamHub (教师端)

**HHK unit → kn_id resolution:**
```ts
import meta from 'knowledge-registry/dist/meta-nodes.json';

// Find all nodes for Y7.1
const y7_1_nodes = meta.filter(n =>
  n.examBoards.hhk?.units?.includes('Y7.1')
);
```

**Route assignment by year group:**
```ts
import routes from 'knowledge-registry/dist/routes-compiled.json';

// Get Y7 route
const y7Route = routes['hhk-y7'];
const totalHours = y7Route.estimatedHours; // ~11.0h
```

### Play (游戏学习)

**KP → kn_id (uses kp-kn-map.json directly):**
```ts
import kpMap from 'knowledge-registry/registry/kp-kn-map.json';

// When player answers a KP question
function onKpAnswer(kpId: string) {
  const knId = kpMap[kpId]; // e.g. "kp-1.1-01" → "kn_0001"
  // Write progress to meta_node_progress
}
```

## Field Contracts

### primaryBoard
Every meta node has `primaryBoard: "cie" | "edx" | "both"`.
- `cie` (105 nodes): only in CIE 0580
- `edx` (10 nodes): Edexcel-only (kn_0289–kn_0298)
- `both` (88 nodes): present in both boards

### boardFilter
Every route has `boardFilter: string[]`.
- `cie-*` routes: `["cie", "both"]`
- `edx-*` routes: `["edx", "both"]`
- `hhk-*` routes: `["cie", "both"]` (HHK tracks CIE syllabus)

**Filtering rule:** A node belongs in a route's board view iff
`route.boardFilter.includes(node.primaryBoard)`.

### question-id-map.json
```json
{
  "kn_0042": {
    "cie": "cie.1.9",       // → /practice/cie/1.9
    "edx": "edx.ch1-u6"     // → /practice/edx/ch1-u6
  }
}
```
Not every node has both keys. CIE-only nodes lack `edx`, Edexcel-only nodes lack `cie`.

## Keeping Up To Date

1. `dist/build-manifest.json` records source hashes
2. CI runs `check-dist-fresh.py` on every push
3. If you update any script in `scripts/build-*.py`, run:
   ```bash
   python3 scripts/build-all.py
   python3 scripts/check-dist-fresh.py --update
   ```
4. Commit the updated `dist/` files
