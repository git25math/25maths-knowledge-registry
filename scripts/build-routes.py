#!/usr/bin/env python3
"""
Build 13 learning routes from meta-nodes.json + dag-edges.json.

Each route filters meta nodes by exam board, tier, domain, weight etc.
Nodes are topologically sorted and milestones inserted every 5-8 nodes.

Outputs: routes/*.json (13 files updated with nodes)
"""

import json, os, sys, math
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from dag_utils import topological_sort


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def load_meta_nodes():
    return load('dist/meta-nodes.json')


def load_edges():
    return load('graph/dag-edges.json')


def load_hhk_map():
    return load('registry/hhk-kn-map.json')


def make_route_node(kn_id, order, is_required=True, est_minutes=25, milestone=False):
    return {
        'kn_id': kn_id,
        'order': order,
        'isRequired': is_required,
        'unlockCondition': {
            'type': 'prerequisite_mastered',
            'threshold': 0.8,
        },
        'estimatedMinutes': est_minutes,
        'milestone': milestone,
    }


def make_milestone(milestone_id, order, title_en, title_zh, covers):
    return {
        'kn_id': milestone_id,
        'type': 'milestone',
        'order': order,
        'title_en': title_en,
        'title_zh': title_zh,
        'covers': covers,
        'isRequired': False,
        'milestone': True,
    }


def insert_milestones(nodes, route_id):
    """Insert milestone nodes every 5-8 knowledge nodes."""
    if not nodes:
        return nodes
    result = []
    milestone_batch = []
    milestone_count = 0
    order = 1

    for node in nodes:
        node['order'] = order
        result.append(node)
        milestone_batch.append(node['kn_id'])
        order += 1

        if len(milestone_batch) >= 6:
            milestone_count += 1
            ms = make_milestone(
                f"milestone-{route_id}-{milestone_count}",
                order,
                f"Checkpoint {milestone_count}",
                f"检查点 {milestone_count}",
                list(milestone_batch),
            )
            result.append(ms)
            order += 1
            milestone_batch = []

    # Final milestone if remaining nodes >= 3
    if len(milestone_batch) >= 3:
        milestone_count += 1
        ms = make_milestone(
            f"milestone-{route_id}-{milestone_count}",
            order,
            f"Checkpoint {milestone_count}",
            f"检查点 {milestone_count}",
            list(milestone_batch),
        )
        result.append(ms)

    return result


def get_est_minutes(meta_node):
    em = meta_node.get('learning', {}).get('estimatedMinutes', {})
    return em.get('concept', 10) + em.get('practice', 20)


def topo_sort_nodes(kn_ids, edges):
    """Topologically sort a subset of kn_ids."""
    return topological_sort(kn_ids, edges)


def estimate_hours(nodes, meta_map):
    total_min = 0
    for n in nodes:
        if n.get('milestone'):
            continue
        mn = meta_map.get(n['kn_id'])
        if mn:
            total_min += get_est_minutes(mn)
    return round(total_min / 60, 1)


# ══════════════════════════════════════════
# Route builders
# ══════════════════════════════════════════

def limit_per_section(kn_ids, meta_map, max_per_section=2):
    """Limit nodes per CIE section, preferring higher weight."""
    WEIGHT_RANK = {'highest': 0, 'high': 1, 'medium': 2, 'low': 3, 'rare': 4}
    section_counts = defaultdict(int)
    result = []
    # Sort by weight priority first
    ranked = sorted(kn_ids, key=lambda k: WEIGHT_RANK.get(
        meta_map[k]['examBoards'].get('cie_0580', {}).get('weight', 'medium'), 4))
    for kn_id in ranked:
        sec = meta_map[kn_id]['examBoards'].get('cie_0580', {}).get('section', '')
        if section_counts[sec] < max_per_section:
            section_counts[sec] += 1
            result.append(kn_id)
    return result


def build_cie_core_number(meta_nodes, meta_map, edges):
    """Route 1: CIE Core Number + Statistics + Probability."""
    selected = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        if cie['tier'] not in ('core', 'both'):
            continue
        if mn['domain'] not in ('number', 'statistics', 'probability'):
            continue
        weight = cie.get('weight', 'medium')
        if weight in ('low', 'rare'):
            continue
        selected.append(mn['kn_id'])

    # Supplement: important uncovered number/statistics nodes
    SUPPLEMENT_NUMBER = [
        'kn_0046', 'kn_0047', 'kn_0048', 'kn_0050', 'kn_0051',  # Limits of accuracy
        'kn_0385', 'kn_0386',  # Cumulative frequency
        'kn_0388',  # Histograms
    ]
    selected_set = set(selected)
    for kn_id in SUPPLEMENT_NUMBER:
        if kn_id not in selected_set and kn_id in meta_map:
            selected.append(kn_id)

    selected = limit_per_section(selected, meta_map, max_per_section=3)
    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        is_req = mn['examBoards']['cie_0580'].get('weight', 'medium') in ('highest', 'high')
        nodes.append(make_route_node(kn_id, 0, is_req, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-core-number')


def build_cie_core_geometry(meta_nodes, meta_map, edges):
    """Route 2: CIE Core Geometry — s4.x/s5.x geometry nodes, all tiers."""
    selected = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        if mn['domain'] != 'geometry':
            continue
        # Include core, both, AND extended geometry (s4.x/s5.x)
        sec = cie.get('section', '')
        if not any(sec.startswith(s) for s in ['s4', 's5']):
            continue
        weight = cie.get('weight', 'medium')
        if weight in ('low', 'rare'):
            continue
        selected.append(mn['kn_id'])

    # Supplement: explicitly add uncovered geometry nodes
    SUPPLEMENT_GEO = [
        'kn_0364',  # Surface area and volume
        'kn_0374', 'kn_0377',  # Transformations
        'kn_0148',  # Angles
    ]
    selected_set = set(selected)
    for kn_id in SUPPLEMENT_GEO:
        if kn_id not in selected_set and kn_id in meta_map:
            selected.append(kn_id)

    selected = limit_per_section(selected, meta_map, max_per_section=4)
    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        is_req = mn['examBoards'].get('cie_0580', {}).get('weight', 'medium') in ('highest', 'high')
        nodes.append(make_route_node(kn_id, 0, is_req, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-core-geometry')


def build_cie_extended_algebra(meta_nodes, meta_map, edges):
    """Route 3: CIE Extended Algebra + Trig (s6.x) + Vectors (s7.x).

    Excludes pure geometry (s4.x/s5.x) which belongs in cie-core-geometry.
    Keeps: s2.x (algebra), s3.x (graphs/sequences), s6.x (trig), s7.x (vectors).
    """
    # Sections that belong in this algebra route
    ALGEBRA_SECTIONS = ['s2', 's3', 's6', 's7']

    selected = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        if cie['tier'] not in ('extended', 'both'):
            continue
        sec = cie.get('section', '')
        domain = mn['domain']

        # Include if: algebra domain OR section is s2/s3/s6/s7
        if domain == 'algebra':
            pass  # always include algebra
        elif any(sec.startswith(s) for s in ALGEBRA_SECTIONS):
            pass  # trig, vectors, graphs
        else:
            continue  # skip pure geometry (s4.x/s5.x)

        weight = cie.get('weight', 'medium')
        if weight in ('low', 'rare'):
            continue
        selected.append(mn['kn_id'])

    # Supplement: important uncovered algebra-adjacent nodes
    SUPPLEMENT_ALG = [
        'kn_0161',  # Conditional probability (uses algebra)
        'kn_0346',  # Surds
    ]
    selected_set = set(selected)
    for kn_id in SUPPLEMENT_ALG:
        if kn_id not in selected_set and kn_id in meta_map:
            selected.append(kn_id)

    selected = limit_per_section(selected, meta_map, max_per_section=3)
    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        is_req = mn['examBoards'].get('cie_0580', {}).get('weight', 'medium') in ('highest', 'high')
        nodes.append(make_route_node(kn_id, 0, is_req, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-extended-algebra')


def build_cie_recovery_algebra(meta_nodes, meta_map, edges):
    """Route 4: CIE Recovery Algebra — basic difficulty only."""
    # Group by section
    section_counts = defaultdict(int)
    selected = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        if mn['domain'] != 'algebra':
            continue
        diff = mn['learning'].get('difficultyRange', [1, 3])
        if diff[0] != 1:
            continue
        sec = cie.get('section', '')
        if section_counts[sec] >= 2:
            continue
        section_counts[sec] += 1
        selected.append(mn['kn_id'])

    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-recovery-algebra')


def build_cie_recovery_fractions(meta_nodes, meta_map, edges):
    """Route 5: CIE Recovery Fractions — s1.4 and s2.3 nodes."""
    selected = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        sec = cie.get('section', '')
        if sec not in ('s1.4', 's2.3'):
            continue
        selected.append(mn['kn_id'])

    # Sort by difficulty ascending
    selected.sort(key=lambda kn_id: meta_map[kn_id]['learning'].get('difficultyRange', [1, 3])[0])
    # Then topo sort within same difficulty
    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-recovery-fractions')


def build_cie_sprint_2weeks(meta_nodes, meta_map, edges):
    """Route 6: CIE Sprint 2 Weeks — top weight nodes, max 28."""
    WEIGHT_ORDER = {'highest': 0, 'high': 1, 'medium': 2, 'low': 3, 'rare': 4}
    candidates = []
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if not cie:
            continue
        weight = cie.get('weight', 'medium')
        if weight in ('low', 'rare'):
            continue
        candidates.append((WEIGHT_ORDER.get(weight, 4), mn['kn_id']))

    candidates.sort()
    selected = [kn_id for _, kn_id in candidates[:28]]
    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, 'cie-sprint-2weeks')


def build_edx_foundation(meta_nodes, meta_map, edges):
    """Route 7: Edexcel Foundation."""
    selected = []
    for mn in meta_nodes:
        edx = mn['examBoards'].get('edexcel_4ma1')
        if not edx:
            continue
        if edx.get('tier') not in ('foundation', 'both'):
            continue
        selected.append(mn['kn_id'])

    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, 'edx-foundation')


def build_edx_higher(meta_nodes, meta_map, edges):
    """Route 8: Edexcel Higher — higher-exclusive + Edexcel-only nodes (kn_0289-kn_0298)."""
    WEIGHT_RANK = {'highest': 0, 'high': 1, 'medium': 2, 'low': 3, 'rare': 4}
    selected = []
    for mn in meta_nodes:
        edx = mn['examBoards'].get('edexcel_4ma1')
        if not edx:
            continue
        kn_num = int(mn['kn_id'].split('_')[1])
        is_edx_only = 289 <= kn_num <= 298
        if edx.get('tier') == 'higher' or is_edx_only:
            selected.append(mn['kn_id'])

    # Limit by weight, pick top 20
    selected.sort(key=lambda k: WEIGHT_RANK.get(
        meta_map[k]['examBoards'].get('cie_0580', meta_map[k]['examBoards'].get('edexcel_4ma1', {})).get('weight', 'medium'), 4))
    selected = selected[:20]

    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map[kn_id]
        nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, 'edx-higher')


def build_hhk_year(year, meta_nodes, meta_map, edges, hhk_map):
    """Build HHK route for a specific year. Pick 1 representative node per unit."""
    WEIGHT_RANK = {'highest': 0, 'high': 1, 'medium': 2, 'low': 3, 'rare': 4}
    # Get all HHK units for this year
    year_units = []
    for unit_id, unit_data in sorted(hhk_map.items()):
        if unit_data.get('year') == year:
            year_units.append((unit_id, unit_data))

    # Build section -> kn_id index
    section_to_kn = defaultdict(set)
    for mn in meta_nodes:
        cie = mn['examBoards'].get('cie_0580')
        if cie:
            section_to_kn[cie['section']].add(mn['kn_id'])

    selected = []
    seen = set()
    for idx, (unit_id, unit_data) in enumerate(year_units):
        # Collect all candidate kn_ids for this unit
        candidates = set()
        for sec in unit_data.get('cieSections', []):
            for kn_id in section_to_kn.get(sec, []):
                if kn_id not in seen:
                    candidates.add(kn_id)
        # Pick top 1-2 by weight
        ranked = sorted(candidates, key=lambda k: WEIGHT_RANK.get(
            meta_map[k]['examBoards'].get('cie_0580', {}).get('weight', 'medium'), 4))
        for kn_id in ranked[:2]:
            selected.append(kn_id)
            seen.add(kn_id)

    # For Y11: add CIE-only supplement nodes
    if year == 11:
        all_hhk_sections = set()
        for uid, ud in hhk_map.items():
            for s in ud.get('cieSections', []):
                all_hhk_sections.add(s)

        supplement_candidates = []
        for mn in meta_nodes:
            cie = mn['examBoards'].get('cie_0580')
            if not cie:
                continue
            sec = cie.get('section', '')
            weight = cie.get('weight', 'medium')
            if sec not in all_hhk_sections and weight in ('highest', 'high', 'medium'):
                if mn['kn_id'] not in seen:
                    supplement_candidates.append(mn['kn_id'])

        # Pick up to 22 supplement nodes, prefer higher weight
        supplement_candidates.sort(key=lambda k: WEIGHT_RANK.get(
            meta_map[k]['examBoards'].get('cie_0580', {}).get('weight', 'medium'), 4))
        for kn_id in supplement_candidates[:22]:
            selected.append(kn_id)
            seen.add(kn_id)

    sorted_ids = topo_sort_nodes(selected, edges)
    nodes = []
    for kn_id in sorted_ids:
        mn = meta_map.get(kn_id)
        if mn:
            nodes.append(make_route_node(kn_id, 0, True, get_est_minutes(mn)))
    return insert_milestones(nodes, f'hhk-y{year}')


def update_route_file(route_id, nodes, meta_map):
    """Update existing route JSON file with nodes and computed hours."""
    path = os.path.join(BASE, 'routes', f'{route_id}.json')
    with open(path) as f:
        route = json.load(f)

    route['nodes'] = nodes
    route['estimatedHours'] = estimate_hours(nodes, meta_map)

    with open(path, 'w') as f:
        json.dump(route, f, indent=2, ensure_ascii=False)
    return route


def main():
    print("=== Building Routes ===\n")

    meta_nodes = load_meta_nodes()
    edges = load_edges()
    hhk_map = load_hhk_map()

    meta_map = {mn['kn_id']: mn for mn in meta_nodes}

    # Build all routes
    routes = {
        'cie-core-number': build_cie_core_number(meta_nodes, meta_map, edges),
        'cie-core-geometry': build_cie_core_geometry(meta_nodes, meta_map, edges),
        'cie-extended-algebra': build_cie_extended_algebra(meta_nodes, meta_map, edges),
        'cie-recovery-algebra': build_cie_recovery_algebra(meta_nodes, meta_map, edges),
        'cie-recovery-fractions': build_cie_recovery_fractions(meta_nodes, meta_map, edges),
        'cie-sprint-2weeks': build_cie_sprint_2weeks(meta_nodes, meta_map, edges),
        'edx-foundation': build_edx_foundation(meta_nodes, meta_map, edges),
        'edx-higher': build_edx_higher(meta_nodes, meta_map, edges),
    }

    # HHK routes
    for year in [7, 8, 9, 10, 11]:
        route_id = f'hhk-y{year}'
        routes[route_id] = build_hhk_year(year, meta_nodes, meta_map, edges, hhk_map)

    # Update route files and populate meta-node routes field
    kn_routes = defaultdict(list)  # kn_id -> [route_id]
    for route_id, nodes in routes.items():
        route_data = update_route_file(route_id, nodes, meta_map)
        kn_count = len([n for n in nodes if not n.get('milestone')])
        ms_count = len([n for n in nodes if n.get('milestone')])
        print(f"  {route_id}: {kn_count} nodes + {ms_count} milestones, ~{route_data['estimatedHours']}h")

        for node in nodes:
            if not node.get('milestone'):
                kn_routes[node['kn_id']].append(route_id)

    # Update meta-nodes.json with routes field
    for mn in meta_nodes:
        mn['routes'] = sorted(kn_routes.get(mn['kn_id'], []))

    meta_path = os.path.join(BASE, 'dist', 'meta-nodes.json')
    with open(meta_path, 'w') as f:
        json.dump(meta_nodes, f, indent=2, ensure_ascii=False)

    print(f"\n  Total routes: {len(routes)}")
    total_kn = sum(len([n for n in nodes if not n.get('milestone')]) for nodes in routes.values())
    print(f"  Total node assignments: {total_kn}")
    unique_kn = len(kn_routes)
    print(f"  Unique nodes in routes: {unique_kn}/{len(meta_nodes)}")


if __name__ == '__main__':
    main()
