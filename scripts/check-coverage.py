#!/usr/bin/env python3
"""
Knowledge Coverage Report — checks how many meta nodes are covered by routes.

Reads:
  dist/meta-nodes.json
  routes/*.json

Outputs:
  Coverage report to stdout
  dist/coverage-report.json
"""

import json, os, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def main():
    meta_nodes = load('dist/meta-nodes.json')
    meta_map = {mn['kn_id']: mn for mn in meta_nodes}

    # Load all routes
    route_files = sorted(glob.glob(os.path.join(BASE, 'routes', '*.json')))
    routes = {}
    for rf in route_files:
        with open(rf) as f:
            route = json.load(f)
        routes[route['id']] = route

    # Track which nodes are in routes
    nodes_in_routes = set()
    route_stats = []

    for route_id, route in sorted(routes.items()):
        nodes = route.get('nodes', [])
        kn_nodes = [n for n in nodes if not n.get('milestone')]
        ms_nodes = [n for n in nodes if n.get('milestone')]

        kn_ids = [n['kn_id'] for n in kn_nodes]
        nodes_in_routes.update(kn_ids)

        # Estimate learning time
        total_min = 0
        for kn_id in kn_ids:
            mn = meta_map.get(kn_id)
            if mn:
                em = mn.get('learning', {}).get('estimatedMinutes', {})
                total_min += em.get('concept', 0) + em.get('practice', 0)

        hours = round(total_min / 60, 1)
        route_stats.append({
            'id': route_id,
            'nodes': len(kn_nodes),
            'milestones': len(ms_nodes),
            'estimatedHours': hours,
        })

    # Nodes not in any route — classify reason
    not_in_route = []
    for mn in meta_nodes:
        if mn['kn_id'] not in nodes_in_routes:
            cie = mn['examBoards'].get('cie_0580', {})
            weight = cie.get('weight', 'N/A')
            variant_of = mn.get('variantOf')
            if variant_of:
                reason = f'variant of {variant_of}'
            elif weight in ('low', 'rare'):
                reason = 'low frequency'
            else:
                reason = 'optional'
            not_in_route.append({
                'kn_id': mn['kn_id'],
                'title_en': mn['title_en'],
                'domain': mn['domain'],
                'weight': weight,
                'reason': reason,
                'variantOf': variant_of,
            })

    variants_exempt = len([n for n in not_in_route if n.get('variantOf')])
    effective_total = len(meta_nodes) - variants_exempt
    effective_pct = round(100 * len(nodes_in_routes) / effective_total) if effective_total else 0

    # Print report
    print("=== Knowledge Coverage Report ===\n")
    print(f"Meta Nodes: {len(meta_nodes)} total")
    print(f"  In routes: {len(nodes_in_routes)}/{len(meta_nodes)} ({round(100*len(nodes_in_routes)/len(meta_nodes))}%)")
    print(f"  Not in any route: {len(not_in_route)} nodes")
    print(f"    Variants (exempt): {variants_exempt}")
    print(f"    Other: {len(not_in_route) - variants_exempt}")
    print(f"  Effective coverage: {len(nodes_in_routes)}/{effective_total} ({effective_pct}%)")

    print(f"\nRoutes Coverage:")
    for rs in route_stats:
        print(f"  {rs['id']:30s} {rs['nodes']:3d} nodes, ~{rs['estimatedHours']}h learning")

    if not_in_route:
        print(f"\nNodes not in any route:")
        for item in not_in_route:
            print(f"  {item['kn_id']}: \"{item['title_en']}\" ({item['reason']})")

    # Save report JSON
    report = {
        'totalMetaNodes': len(meta_nodes),
        'nodesInRoutes': len(nodes_in_routes),
        'coveragePercent': round(100 * len(nodes_in_routes) / len(meta_nodes), 1),
        'variantsExempt': variants_exempt,
        'effectiveCoverage': effective_pct,
        'routeStats': route_stats,
        'nodesNotInRoute': not_in_route,
    }
    report_path = os.path.join(BASE, 'dist', 'coverage-report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved: {report_path}")


if __name__ == '__main__':
    main()
