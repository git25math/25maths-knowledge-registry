#!/usr/bin/env node
/**
 * restore-kn-descriptions-from-seed.mjs
 *
 * 从 seed v3 draft 把 lost description / lu_id / topics 字段
 * 注回 meta-nodes.json · 解决 61 neither kn 同 title 无法区分问题
 *
 * 设计为可在 25maths-knowledge-registry 仓直接跑(只改 meta-nodes.json)
 *
 * 用法 (from this repo):
 *   node scripts/restore-kn-descriptions-from-seed.mjs --dry-run    # 预览
 *   node scripts/restore-kn-descriptions-from-seed.mjs              # 应用
 *
 * 用法 (from registry repo):
 *   cp scripts/restore-kn-descriptions-from-seed.mjs ../25maths-knowledge-registry/scripts/
 *   cp docs/data-backlogs/seed-archives/canonical_nodes_seed_v3_draft.json ../25maths-knowledge-registry/seed-archives/
 *   cd ../25maths-knowledge-registry
 *   node scripts/restore-kn-descriptions-from-seed.mjs
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const DRY_RUN = process.argv.includes('--dry-run');

// 路径 · 自适应 (this repo vs registry repo)
const META_PATH = existsSync('public/data/kn-registry/meta-nodes.json')
  ? 'public/data/kn-registry/meta-nodes.json'
  : 'dist/meta-nodes.json';
const SEED_PATH = existsSync('docs/data-backlogs/seed-archives/canonical_nodes_seed_v3_draft.json')
  ? 'docs/data-backlogs/seed-archives/canonical_nodes_seed_v3_draft.json'
  : 'seed-archives/canonical_nodes_seed_v3_draft.json';

const seedRaw = JSON.parse(readFileSync(SEED_PATH, 'utf8'));
const seedNodes = Array.isArray(seedRaw) ? seedRaw : (seedRaw.nodes || []);
const seedById = new Map();
for (const n of seedNodes) {
  const id = n.id || n.kn_id || n.node_id;
  if (id) seedById.set(id, n);
}

const metaRaw = JSON.parse(readFileSync(META_PATH, 'utf8'));
const metaNodes = Array.isArray(metaRaw) ? metaRaw : (metaRaw.nodes || []);

let touched = 0;
for (const n of metaNodes) {
  const id = n.kn_id || n.id;
  const sd = seedById.get(id);
  if (!sd) continue;
  const seedTitle = sd.title || {};
  const seedTitleEn = typeof seedTitle === 'string' ? seedTitle : seedTitle.en;
  const seedTitleZh = typeof seedTitle === 'string' ? null : seedTitle.zh;
  if (seedTitleEn && seedTitleEn !== n.title_en) {
    n.title_en = seedTitleEn;
    if (seedTitleZh) n.title_zh = seedTitleZh;
    n.description = seedTitleEn;
    if (sd.tags) n.topics = sd.tags;
    if (sd.lu_id) n.lu_id = sd.lu_id;
    touched++;
  }
}

console.log(`📦 ${touched} nodes patched (${DRY_RUN ? 'dry-run · 未写入' : 'written'})`);
if (!DRY_RUN) {
  const out = Array.isArray(metaRaw) ? metaNodes : { ...metaRaw, nodes: metaNodes };
  writeFileSync(META_PATH, JSON.stringify(out, null, 2) + '\n');
  console.log(`✅ ${META_PATH} updated`);
}
