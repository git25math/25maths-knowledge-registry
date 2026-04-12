#!/usr/bin/env python3
"""
Route progress simulator — show what's unlocked/next given mastered nodes.

Usage:
  python3 scripts/simulate-progress.py <route-id>                         # empty progress
  python3 scripts/simulate-progress.py <route-id> kn_0001 kn_0002 ...    # with mastered nodes
  python3 scripts/simulate-progress.py <route-id> --random 10            # simulate 10 random masteries
  python3 scripts/simulate-progress.py --all kn_0001 kn_0002             # show all routes

Outputs per route:
  - completion %
  - next unlocked nodes (ready to learn)
  - blocked nodes (and which prereqs they're waiting for)
  - estimated remaining time
"""

import json, os, sys, random

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def simulate_route(route, meta_map, mastered):
    """Compute progress state for a route given mastered kn_ids.

    Returns dict with: completed, unlocked, blocked, progress%, remaining_time.
    """
    nodes = [n for n in route['nodes'] if not n.get('milestone')]
    route_kns = [n['kn_id'] for n in nodes]
    mastered_set = set(mastered)

    completed = []
    unlocked = []
    blocked = []

    for n in nodes:
        kn_id = n['kn_id']
        mn = meta_map.get(kn_id, {})
        prereqs = mn.get('prerequisites', [])

        # Hard prereqs that must be mastered
        hard_unmet = [
            p['kn_id'] for p in prereqs
            if p['type'] == 'hard' and p['kn_id'] not in mastered_set
        ]

        if kn_id in mastered_set:
            completed.append(kn_id)
        elif not hard_unmet:
            unlocked.append(kn_id)
        else:
            blocked.append({'kn_id': kn_id, 'waiting_for': hard_unmet})

    # Time estimates
    remaining_min = 0
    for kn_id in [*[u for u in unlocked], *[b['kn_id'] for b in blocked]]:
        mn = meta_map.get(kn_id, {})
        em = mn.get('learning', {}).get('estimatedMinutes', {})
        remaining_min += em.get('concept', 0) + em.get('practice', 0)

    total = len(nodes)
    return {
        'route_id': route['id'],
        'total': total,
        'completed': completed,
        'unlocked': unlocked,
        'blocked': blocked,
        'progress_pct': round(100 * len(completed) / total) if total else 0,
        'remaining_hours': round(remaining_min / 60, 1),
    }


def print_route_progress(result, meta_map, verbose=True):
    """Pretty-print a route's progress state."""
    rid = result['route_id']
    pct = result['progress_pct']
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"\n=== {rid} ===")
    print(f"  Progress: [{bar}] {pct}% ({len(result['completed'])}/{result['total']})")
    print(f"  Remaining: ~{result['remaining_hours']}h")

    if result['unlocked']:
        print(f"\n  Ready to learn ({len(result['unlocked'])}):")
        for kn_id in result['unlocked'][:8]:
            mn = meta_map.get(kn_id, {})
            em = mn.get('learning', {}).get('estimatedMinutes', {})
            mins = em.get('concept', 0) + em.get('practice', 0)
            print(f"    → {kn_id} \"{mn.get('title_en', '?')}\" (~{mins}min)")
        if len(result['unlocked']) > 8:
            print(f"    ... and {len(result['unlocked']) - 8} more")

    if verbose and result['blocked']:
        print(f"\n  Blocked ({len(result['blocked'])}):")
        for b in result['blocked'][:5]:
            mn = meta_map.get(b['kn_id'], {})
            waiting = ', '.join(b['waiting_for'][:3])
            print(f"    ✗ {b['kn_id']} \"{mn.get('title_en', '?')}\" — needs: {waiting}")
        if len(result['blocked']) > 5:
            print(f"    ... and {len(result['blocked']) - 5} more")


def main():
    meta = load('dist/meta-nodes.json')
    routes = load('dist/routes-compiled.json')
    meta_map = {m['kn_id']: m for m in meta}

    if len(sys.argv) < 2:
        print("Usage:")
        print("  simulate-progress.py <route-id> [kn_0001 kn_0002 ...]")
        print("  simulate-progress.py <route-id> --random <N>")
        print("  simulate-progress.py --all [kn_0001 kn_0002 ...]")
        print(f"\nRoutes: {', '.join(sorted(routes.keys()))}")
        return

    # Parse args
    show_all = '--all' in sys.argv
    random_mode = '--random' in sys.argv
    random_n = 0

    args = [a for a in sys.argv[1:] if a not in ('--all',)]
    if random_mode:
        idx = args.index('--random')
        random_n = int(args[idx + 1]) if idx + 1 < len(args) else 10
        args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]

    if show_all:
        target_routes = sorted(routes.keys())
        mastered = [a for a in args if a.startswith('kn_')]
    else:
        if not args:
            print("Specify a route-id or --all")
            return
        target_routes = [args[0]]
        mastered = [a for a in args[1:] if a.startswith('kn_')]

    # Random mode: pick N random nodes from the target route(s)
    if random_mode:
        all_route_kns = set()
        for rid in target_routes:
            route = routes.get(rid, {})
            for n in route.get('nodes', []):
                if not n.get('milestone'):
                    all_route_kns.add(n['kn_id'])
        mastered = random.sample(sorted(all_route_kns), min(random_n, len(all_route_kns)))
        print(f"Simulating {len(mastered)} random masteries: {mastered[:5]}...")

    # Run simulation
    for rid in target_routes:
        route = routes.get(rid)
        if not route:
            print(f"Route {rid} not found.")
            continue
        result = simulate_route(route, meta_map, mastered)
        verbose = len(target_routes) == 1
        print_route_progress(result, meta_map, verbose=verbose)


if __name__ == '__main__':
    main()
