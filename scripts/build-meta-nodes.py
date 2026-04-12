#!/usr/bin/env python3
"""
Build meta-nodes.json — enriched knowledge nodes with DAG, HHK, Edexcel mappings.

Reads:
  registry/kn-registry.json   (203 knowledge nodes)
  graph/dag-edges.json         (272 dependency edges)
  registry/kp-kn-map.json     (KP -> kn_id)
  registry/hhk-kn-map.json    (HHK -> cieSections)
  registry/edx-kn-map.json    (Edexcel chapters -> sections)

Outputs:
  dist/meta-nodes.json
"""

import json, os, sys
from collections import defaultdict
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from dag_utils import topological_sort

NOW = "2026-04-07T00:00:00Z"

# Domain-based estimated minutes
DOMAIN_MINUTES = {
    'number':      {'concept': 5,  'practice': 20},
    'algebra':     {'concept': 8,  'practice': 25},
    'geometry':    {'concept': 10, 'practice': 30},
    'statistics':  {'concept': 7,  'practice': 20},
    'probability': {'concept': 6,  'practice': 18},
}


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def build_section_to_kn(registry):
    """Build mapping: CIE section -> list of kn_ids."""
    section_map = defaultdict(list)
    for node in registry:
        cie = node.get('examBoards', {}).get('cie_0580')
        if cie:
            section_map[cie['section']].append(node['kn_id'])
        # Also index by subdomain
        sd = node.get('subdomain', '')
        if sd and sd != cie.get('section', '') if cie else True:
            section_map[sd].append(node['kn_id'])
    return section_map


def build_hhk_mapping(hhk_map, section_to_kn):
    """For each kn_id, find which HHK units reference it via cieSections."""
    kn_to_hhk = defaultdict(list)  # kn_id -> [{"unit": "Y7.1", "year": 7}]
    for unit_id, unit_data in hhk_map.items():
        cie_sections = unit_data.get('cieSections', [])
        year = unit_data.get('year', 0)
        matched_kns = set()
        for sec in cie_sections:
            for kn_id in section_to_kn.get(sec, []):
                matched_kns.add(kn_id)
        for kn_id in matched_kns:
            kn_to_hhk[kn_id].append({
                'unit': unit_id,
                'year': year,
            })
    return kn_to_hhk


def build_edx_mapping(edx_map, section_to_kn):
    """For each kn_id, find Edexcel section info."""
    kn_to_edx = {}  # kn_id -> {"section": ..., "tier": ..., "chapter": ...}
    for ch_id, ch_data in edx_map.items():
        if not isinstance(ch_data, dict) or 'sections' not in ch_data:
            continue
        for sec_id, sec_data in ch_data['sections'].items():
            tier = sec_data.get('tier', 'both')
            edx_sections = sec_data.get('sections', [])
            # Map edx sections (like "1.3") to CIE sections (like "s1.3")
            for es in edx_sections:
                cie_sec = f"s{es}"
                for kn_id in section_to_kn.get(cie_sec, []):
                    if kn_id not in kn_to_edx:
                        kn_to_edx[kn_id] = {
                            'section': es,
                            'tier': tier,
                            'chapter': ch_id,
                            'weight': 'medium',
                        }
    return kn_to_edx


def main():
    print("=== Building meta-nodes.json ===\n")

    # Load all data sources
    registry = load('registry/kn-registry.json')
    dag_edges = load('graph/dag-edges.json')
    kp_map = load('registry/kp-kn-map.json')
    hhk_map = load('registry/hhk-kn-map.json')
    edx_map = load('registry/edx-kn-map.json')

    kn_by_id = {n['kn_id']: n for n in registry}
    kn_ids = set(kn_by_id.keys())

    # Build prerequisites and leadsTo from DAG
    prereqs = defaultdict(list)   # kn_id -> [{kn_id, type}]
    leads_to = defaultdict(list)  # kn_id -> [kn_id]
    for edge in dag_edges:
        fr, to, etype = edge['from'], edge['to'], edge['type']
        if fr in kn_ids and to in kn_ids:
            prereqs[to].append({'kn_id': fr, 'type': etype})
            leads_to[fr].append(to)

    # Build section index and mappings
    section_to_kn = build_section_to_kn(registry)
    kn_to_hhk = build_hhk_mapping(hhk_map, section_to_kn)
    kn_to_edx = build_edx_mapping(edx_map, section_to_kn)

    # Compute in-degree for weight assignment
    in_degree = defaultdict(int)
    for edge in dag_edges:
        if edge['to'] in kn_ids:
            in_degree[edge['to']] += 1

    def compute_weight(kn_id):
        """Assign weight based on graph connectivity."""
        lt_count = len(leads_to.get(kn_id, []))
        in_count = in_degree.get(kn_id, 0)
        if lt_count >= 5:
            return 'highest'
        elif lt_count >= 3 or in_count >= 4:
            return 'high'
        elif lt_count >= 1 or in_count >= 1:
            return 'medium'
        else:
            return 'low'

    # Build variant map: for nodes sharing same (title_en, section),
    # the lowest kn_id is the "primary" and others are variants.
    section_groups = defaultdict(list)
    for node in registry:
        cie = node.get('examBoards', {}).get('cie_0580', {})
        sec = cie.get('section', node.get('subdomain', ''))
        key = (node.get('title_en', ''), sec)
        section_groups[key].append(node['kn_id'])

    variant_of = {}  # kn_id → primary kn_id (or None)
    for (title, sec), kn_ids in section_groups.items():
        if len(kn_ids) <= 1:
            continue
        sorted_ids = sorted(kn_ids, key=lambda x: int(x.split('_')[1]))
        primary = sorted_ids[0]
        for kn_id in sorted_ids[1:]:
            variant_of[kn_id] = primary

    # Build meta nodes
    meta_nodes = []
    for node in registry:
        kn_id = node['kn_id']
        domain = node.get('domain', 'number')
        est_min = DOMAIN_MINUTES.get(domain, DOMAIN_MINUTES['number'])
        weight = compute_weight(kn_id)

        # Exam boards
        exam_boards = {}

        # CIE 0580
        cie = node.get('examBoards', {}).get('cie_0580')
        if cie:
            cie_entry = {
                'section': cie.get('section', ''),
                'tier': cie.get('tier', 'both'),
                'weight': weight,
            }
            # Add paperCodes based on tier
            tier = cie.get('tier', 'both')
            if tier == 'core':
                cie_entry['paperCodes'] = ['P11', 'P12', 'P31', 'P32']
            elif tier == 'extended':
                cie_entry['paperCodes'] = ['P21', 'P22', 'P41', 'P42']
            else:
                cie_entry['paperCodes'] = ['P11', 'P12', 'P21', 'P22', 'P31', 'P32', 'P41', 'P42']
            exam_boards['cie_0580'] = cie_entry

        # Edexcel 4MA1
        edx_existing = node.get('examBoards', {}).get('edexcel_4ma1')
        if edx_existing:
            exam_boards['edexcel_4ma1'] = {
                'section': edx_existing.get('section', ''),
                'tier': edx_existing.get('tier', 'both'),
                'weight': edx_existing.get('weight', 'medium'),
            }
        elif kn_id in kn_to_edx:
            edx_info = kn_to_edx[kn_id]
            exam_boards['edexcel_4ma1'] = {
                'section': edx_info['section'],
                'tier': edx_info['tier'],
                'weight': edx_info['weight'],
            }

        # HHK
        if kn_id in kn_to_hhk:
            hhk_entries = kn_to_hhk[kn_id]
            units = sorted(set(e['unit'] for e in hhk_entries))
            years = sorted(set(e['year'] for e in hhk_entries))
            exam_boards['hhk'] = {
                'units': units,
                'year': years[0] if len(years) == 1 else years[0],
            }

        # Prerequisites and leadsTo
        node_prereqs = prereqs.get(kn_id, [])
        node_leads_to = sorted(set(leads_to.get(kn_id, [])))

        # isFoundational: true if leadsTo >= 5
        is_foundational = len(node_leads_to) >= 5

        # Difficulty range
        diff_range = node.get('difficultyRange', [1, 3])

        # Primary board classification:
        #   'cie'  — CIE only (no Edexcel mapping)
        #   'edx'  — Edexcel only (tagged edexcel-only OR kn_0289-kn_0298)
        #   'both' — Present in both CIE and Edexcel
        kn_num = int(kn_id.split('_')[1])
        has_cie = 'cie_0580' in exam_boards
        has_edx = 'edexcel_4ma1' in exam_boards
        is_edx_only = 'edexcel-only' in node.get('tags', []) or 289 <= kn_num <= 298

        if is_edx_only or (has_edx and not has_cie):
            primary_board = 'edx'
        elif has_cie and has_edx:
            primary_board = 'both'
        elif has_cie:
            primary_board = 'cie'
        else:
            primary_board = 'cie'  # default fallback

        meta_node = {
            'kn_id': kn_id,
            'title_en': node.get('title_en', ''),
            'title_zh': node.get('title_zh', ''),
            'domain': domain,
            'subdomain': node.get('subdomain', ''),
            'primaryBoard': primary_board,
            'variantOf': variant_of.get(kn_id),

            'examBoards': exam_boards,

            'prerequisites': node_prereqs,
            'leadsTo': node_leads_to,

            'content': {
                'variants': {
                    'cie': [],
                    'edexcel': [],
                    'generic': [],
                },
                'missions': [],
                'glGeneratorId': node.get('content', {}).get('glGeneratorId'),
                'examRefs': node.get('content', {}).get('examRefs', {'cie': 0, 'edexcel': 0}),
            },

            'learning': {
                'estimatedMinutes': est_min,
                'difficultyRange': diff_range,
                'noFigure': node.get('noFigure', True),
                'isFoundational': is_foundational,
            },

            'routes': [],
            'version': 1,
            'createdAt': NOW,
        }
        meta_nodes.append(meta_node)

    # Sort by kn_id
    meta_nodes.sort(key=lambda n: int(n['kn_id'].split('_')[1]))

    # Output
    dist_dir = os.path.join(BASE, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    out_path = os.path.join(dist_dir, 'meta-nodes.json')
    with open(out_path, 'w') as f:
        json.dump(meta_nodes, f, indent=2, ensure_ascii=False)

    # Stats
    total = len(meta_nodes)
    with_hhk = len([n for n in meta_nodes if 'hhk' in n['examBoards']])
    with_edx = len([n for n in meta_nodes if 'edexcel_4ma1' in n['examBoards']])
    foundational = len([n for n in meta_nodes if n['learning']['isFoundational']])
    with_prereqs = len([n for n in meta_nodes if n['prerequisites']])

    # Primary board breakdown
    board_counts = defaultdict(int)
    for n in meta_nodes:
        board_counts[n['primaryBoard']] += 1

    print(f"Total meta nodes: {total}")
    print(f"With CIE mapping: {len([n for n in meta_nodes if 'cie_0580' in n['examBoards']])}")
    print(f"With HHK mapping: {with_hhk}")
    print(f"With Edexcel mapping: {with_edx}")
    print(f"Primary board breakdown:")
    for board in ('cie', 'edx', 'both'):
        print(f"  {board}: {board_counts.get(board, 0)}")
    variants = len([n for n in meta_nodes if n.get('variantOf')])
    print(f"Variants (variantOf set): {variants}")
    print(f"Foundational (leadsTo >= 5): {foundational}")
    print(f"With prerequisites: {with_prereqs}")
    print(f"\nOutput: {out_path}")


if __name__ == '__main__':
    main()
