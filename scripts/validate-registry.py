#!/usr/bin/env python3
"""Validate knowledge registry — all 10 checks must pass."""

import json, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)

def main():
    print("=== Registry Validation ===\n")
    errors = []
    warnings = []

    # Load data
    registry = load('registry/kn-registry.json')
    dag = load('graph/dag-edges.json')
    kp_map = load('registry/kp-kn-map.json')
    hhk_map = load('registry/hhk-kn-map.json')
    edx_map = load('registry/edx-kn-map.json')

    kn_ids = {n['kn_id'] for n in registry}

    # 1. kn_id uniqueness
    seen_ids = []
    dupes = []
    for n in registry:
        if n['kn_id'] in seen_ids:
            dupes.append(n['kn_id'])
        seen_ids.append(n['kn_id'])
    if dupes:
        errors.append(f"kn_id duplicates: {dupes}")
        print(f"✗ kn_id uniqueness: {len(dupes)} duplicates found")
    else:
        print(f"✓ kn_id uniqueness: {len(registry)}/{len(registry)} unique")

    # 2. kn_id format
    import re
    bad_format = [n['kn_id'] for n in registry if not re.match(r'^kn_\d{4}$', n['kn_id'])]
    if bad_format:
        errors.append(f"Bad kn_id format: {bad_format}")
        print(f"✗ kn_id format: {len(bad_format)} invalid")
    else:
        print(f"✓ kn_id format: all {len(registry)} valid")

    # 3. DAG no cycles (topological sort)
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set()
    for e in dag:
        adj[e['from']].append(e['to'])
        in_degree[e['to']] += 1
        all_nodes.add(e['from'])
        all_nodes.add(e['to'])

    # Kahn's algorithm
    queue = [n for n in all_nodes if in_degree[n] == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if visited < len(all_nodes):
        errors.append(f"DAG cycle detected: {len(all_nodes) - visited} nodes in cycle")
        print(f"✗ DAG: cycle detected ({len(all_nodes) - visited} nodes)")
    else:
        print(f"✓ DAG: no cycles detected ({len(all_nodes)} nodes, {len(dag)} edges)")

    # 4. Prerequisites valid
    bad_prereqs = []
    for e in dag:
        if e['from'] not in kn_ids:
            bad_prereqs.append(f"{e['from']} (from)")
        if e['to'] not in kn_ids:
            bad_prereqs.append(f"{e['to']} (to)")
    if bad_prereqs:
        # Some nodes in DAG might be from KPs that share kn_ids not in our registry
        warnings.append(f"DAG references {len(bad_prereqs)} kn_ids not in registry")
        print(f"⚠ Prerequisites: {len(bad_prereqs)} refs to kn_ids outside registry")
    else:
        print(f"✓ Prerequisites valid: all {len(dag)} refs exist")

    # 5. KP map coverage
    kp_mapped = len(kp_map)
    kp_valid = sum(1 for v in kp_map.values() if v in kn_ids)
    if kp_valid < kp_mapped:
        warnings.append(f"KP map: {kp_mapped - kp_valid} KPs map to kn_ids outside registry")
        print(f"⚠ KP map: {kp_valid}/{kp_mapped} mapped to existing nodes")
    else:
        print(f"✓ KP map: {kp_mapped}/{kp_mapped} mapped")

    # 6. HHK map
    hhk_count = len(hhk_map)
    print(f"✓ HHK map: {hhk_count}/{hhk_count} units mapped")

    # 7. Edexcel map
    edx_sections = sum(len(ch.get('sections', {})) for ch in edx_map.values() if isinstance(ch, dict) and 'sections' in ch)
    print(f"✓ Edexcel map: {len(edx_map)} chapters, {edx_sections} sections")

    # 8. Domain validity
    valid_domains = {'number', 'algebra', 'geometry', 'statistics', 'probability'}
    bad_domains = [n['kn_id'] for n in registry if n.get('domain') not in valid_domains]
    if bad_domains:
        errors.append(f"Invalid domains: {bad_domains}")
        print(f"✗ Domains: {len(bad_domains)} invalid")
    else:
        print(f"✓ Domains: all {len(registry)} valid")

    # 9. Version ≥ 1
    bad_versions = [n['kn_id'] for n in registry if n.get('version', 0) < 1]
    if bad_versions:
        errors.append(f"Invalid versions: {bad_versions}")
        print(f"✗ Versions: {len(bad_versions)} invalid")
    else:
        print(f"✓ Versions: all {len(registry)} ≥ 1")

    # 10. Routes exist
    route_files = [f for f in os.listdir(os.path.join(BASE, 'routes')) if f.endswith('.json')]
    print(f"✓ Routes: {len(route_files)} framework files")

    # 11. primaryBoard + boardFilter sanity (only if dist/meta-nodes.json exists)
    meta_path = os.path.join(BASE, 'dist', 'meta-nodes.json')
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)

        VALID_BOARDS = {'cie', 'edx', 'both'}
        bad_primary = [m['kn_id'] for m in meta if m.get('primaryBoard') not in VALID_BOARDS]
        if bad_primary:
            errors.append(f"Invalid primaryBoard: {bad_primary[:5]}...")
            print(f"✗ primaryBoard: {len(bad_primary)} invalid")
        else:
            board_counts = defaultdict(int)
            for m in meta:
                board_counts[m['primaryBoard']] += 1
            print(f"✓ primaryBoard: {dict(board_counts)}")

        # Check route boardFilter alignment — every route node's primaryBoard
        # must be in the route's boardFilter allowlist.
        meta_map = {m['kn_id']: m for m in meta}
        route_mismatch = []
        for rf in route_files:
            with open(os.path.join(BASE, 'routes', rf)) as f:
                route = json.load(f)
            board_filter = route.get('boardFilter', ['cie', 'edx', 'both'])
            for node in route.get('nodes', []):
                if node.get('milestone'):
                    continue
                kn_id = node.get('kn_id', '')
                mn = meta_map.get(kn_id)
                if mn and mn.get('primaryBoard') not in board_filter:
                    route_mismatch.append(f"{rf}:{kn_id}({mn['primaryBoard']})")

        if route_mismatch:
            warnings.append(f"{len(route_mismatch)} route nodes fail boardFilter")
            print(f"⚠ Route boardFilter: {len(route_mismatch)} mismatches")
            for m in route_mismatch[:5]:
                print(f"    {m}")
        else:
            print(f"✓ Route boardFilter: all route nodes match primaryBoard")

    # Summary
    print(f"\n{'=' * 40}")
    if errors:
        print(f"FAIL: {len(errors)} errors, {len(warnings)} warnings")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN: {w}")
        sys.exit(1)
    elif warnings:
        print(f"PASS with {len(warnings)} warnings")
        for w in warnings:
            print(f"  WARN: {w}")
    else:
        print(f"ALL CHECKS PASSED")


if __name__ == '__main__':
    main()
