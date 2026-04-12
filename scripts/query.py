#!/usr/bin/env python3
"""
Interactive knowledge registry query tool.

Usage:
  python3 scripts/query.py node kn_0042          # full node info
  python3 scripts/query.py route cie-core-number  # route summary
  python3 scripts/query.py section s2.3           # all nodes in section
  python3 scripts/query.py domain algebra         # all nodes in domain
  python3 scripts/query.py search fractions       # text search titles
  python3 scripts/query.py prereqs kn_0097        # prerequisite chain
  python3 scripts/query.py path kn_0001 kn_0097   # learning path
  python3 scripts/query.py stats                  # registry overview
"""

import json, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'scripts'))


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def load_all():
    meta = load('dist/meta-nodes.json')
    edges = load('graph/dag-edges.json')
    routes = load('dist/routes-compiled.json')
    return meta, edges, routes


def cmd_node(args):
    """Show full info for a kn_id."""
    if not args:
        print("Usage: query.py node <kn_id>")
        return
    kn_id = args[0]
    meta, edges, routes = load_all()
    mn = next((m for m in meta if m['kn_id'] == kn_id), None)
    if not mn:
        print(f"Node {kn_id} not found.")
        return

    print(f"=== {mn['kn_id']} ===")
    print(f"  Title:    {mn['title_en']} / {mn['title_zh']}")
    print(f"  Domain:   {mn['domain']} ({mn['subdomain']})")
    print(f"  Board:    {mn['primaryBoard']}")
    print(f"  Difficulty: {mn['learning']['difficultyRange']}")
    em = mn['learning']['estimatedMinutes']
    print(f"  Time:     {em['concept']}min concept + {em['practice']}min practice")
    print(f"  Foundational: {mn['learning']['isFoundational']}")
    if mn.get('variantOf'):
        print(f"  Variant of: {mn['variantOf']}")

    # Exam boards
    print(f"\n  Exam boards:")
    for board, data in mn['examBoards'].items():
        print(f"    {board}: {json.dumps(data, ensure_ascii=False)}")

    # Prerequisites
    if mn['prerequisites']:
        print(f"\n  Prerequisites ({len(mn['prerequisites'])}):")
        meta_map = {m['kn_id']: m for m in meta}
        for p in mn['prerequisites']:
            pm = meta_map.get(p['kn_id'], {})
            print(f"    [{p['type']}] {p['kn_id']} \"{pm.get('title_en', '?')}\"")

    # Leads to
    if mn['leadsTo']:
        print(f"\n  Leads to ({len(mn['leadsTo'])}):")
        meta_map = {m['kn_id']: m for m in meta}
        for lt in mn['leadsTo']:
            lm = meta_map.get(lt, {})
            print(f"    → {lt} \"{lm.get('title_en', '?')}\"")

    # Routes
    if mn['routes']:
        print(f"\n  In routes: {', '.join(mn['routes'])}")


def cmd_route(args):
    """Show route summary."""
    if not args:
        print("Usage: query.py route <route-id>")
        print("Available:", ', '.join(sorted(load('dist/routes-compiled.json').keys())))
        return
    rid = args[0]
    meta, edges, routes = load_all()
    route = routes.get(rid)
    if not route:
        print(f"Route {rid} not found.")
        print("Available:", ', '.join(sorted(routes.keys())))
        return
    meta_map = {m['kn_id']: m for m in meta}

    nodes = [n for n in route['nodes'] if not n.get('milestone')]
    milestones = [n for n in route['nodes'] if n.get('milestone')]

    print(f"=== {route['id']} ===")
    print(f"  Title:    {route['title_en']} / {route['title_zh']}")
    print(f"  Board:    {route['board']} (filter: {route.get('boardFilter', [])})")
    print(f"  Tier:     {route['tier']}")
    print(f"  Nodes:    {len(nodes)} + {len(milestones)} milestones")
    print(f"  Time:     ~{route['estimatedHours']}h")

    # Domain breakdown
    domains = defaultdict(int)
    for n in nodes:
        mn = meta_map.get(n['kn_id'], {})
        domains[mn.get('domain', '?')] += 1
    print(f"\n  Domains: {dict(domains)}")

    # Node list
    print(f"\n  Learning path:")
    for n in route['nodes']:
        if n.get('milestone'):
            print(f"    [{n['order']:3d}] ★ {n['title_en']}")
        else:
            mn = meta_map.get(n['kn_id'], {})
            diff = mn.get('learning', {}).get('difficultyRange', [])
            req = "●" if n.get('isRequired') else "○"
            print(f"    [{n['order']:3d}] {req} {n['kn_id']} \"{mn.get('title_en', '?')}\" L{diff}")


def cmd_section(args):
    """Show all nodes in a CIE section."""
    if not args:
        print("Usage: query.py section <section>  (e.g. s2.3)")
        return
    section = args[0]
    meta = load('dist/meta-nodes.json')
    matches = [m for m in meta
               if m['examBoards'].get('cie_0580', {}).get('section') == section]
    if not matches:
        print(f"No nodes in section {section}.")
        return
    print(f"=== Section {section} ({len(matches)} nodes) ===")
    for m in matches:
        v = f" (variant of {m['variantOf']})" if m.get('variantOf') else ""
        r = f" [{', '.join(m['routes'])}]" if m['routes'] else " [no route]"
        print(f"  {m['kn_id']} \"{m['title_en']}\" L{m['learning']['difficultyRange']}{v}{r}")


def cmd_domain(args):
    """Show all nodes in a domain."""
    if not args:
        print("Usage: query.py domain <domain>  (number|algebra|geometry|statistics|probability)")
        return
    domain = args[0]
    meta = load('dist/meta-nodes.json')
    matches = [m for m in meta if m['domain'] == domain]
    if not matches:
        print(f"No nodes in domain {domain}.")
        return
    print(f"=== Domain: {domain} ({len(matches)} nodes) ===")
    # Group by section
    by_section = defaultdict(list)
    for m in matches:
        sec = m['examBoards'].get('cie_0580', {}).get('section', m['subdomain'])
        by_section[sec].append(m)
    for sec in sorted(by_section.keys()):
        nodes = by_section[sec]
        primary = [n for n in nodes if not n.get('variantOf')]
        print(f"\n  {sec} ({len(nodes)} nodes, {len(primary)} primary):")
        for m in primary:
            print(f"    {m['kn_id']} \"{m['title_en']}\" L{m['learning']['difficultyRange']}")


def cmd_search(args):
    """Text search across node titles."""
    if not args:
        print("Usage: query.py search <keyword>")
        return
    keyword = ' '.join(args).lower()
    meta = load('dist/meta-nodes.json')
    matches = [m for m in meta
               if keyword in m['title_en'].lower() or keyword in m['title_zh']]
    if not matches:
        print(f"No nodes matching '{keyword}'.")
        return
    print(f"=== Search: \"{keyword}\" ({len(matches)} results) ===")
    for m in matches:
        board = m['primaryBoard']
        routes_str = ', '.join(m['routes'][:3]) if m['routes'] else 'no route'
        print(f"  {m['kn_id']} [{board}] \"{m['title_en']}\" ({m['domain']}) → {routes_str}")


def cmd_prereqs(args):
    """Show prerequisite chain for a node."""
    if not args:
        print("Usage: query.py prereqs <kn_id>")
        return
    kn_id = args[0]
    from dag_utils import get_prerequisites_chain
    edges = load('graph/dag-edges.json')
    meta = load('dist/meta-nodes.json')
    meta_map = {m['kn_id']: m for m in meta}

    chain = get_prerequisites_chain(kn_id, edges, depth=5)
    mn = meta_map.get(kn_id, {})
    print(f"=== Prerequisites for {kn_id} \"{mn.get('title_en', '?')}\" ===")
    if not chain:
        print("  (no prerequisites)")
        return
    for item in chain:
        pid = item['kn_id']
        depth = item['depth']
        pm = meta_map.get(pid, {})
        indent = "  " * depth
        print(f"  {indent}L{depth}: {pid} \"{pm.get('title_en', '?')}\"")


def cmd_path(args):
    """Find learning path between two nodes."""
    if len(args) < 2:
        print("Usage: query.py path <from_kn_id> <to_kn_id>")
        return
    from dag_utils import get_learning_path
    edges = load('graph/dag-edges.json')
    meta = load('dist/meta-nodes.json')
    meta_map = {m['kn_id']: m for m in meta}

    path = get_learning_path(args[0], args[1], edges)
    if not path:
        print(f"No path from {args[0]} to {args[1]}.")
        return
    total_min = 0
    print(f"=== Path: {args[0]} → {args[1]} ({len(path)} steps) ===")
    for i, kn_id in enumerate(path):
        mn = meta_map.get(kn_id, {})
        em = mn.get('learning', {}).get('estimatedMinutes', {})
        mins = em.get('concept', 0) + em.get('practice', 0)
        total_min += mins
        print(f"  {i+1}. {kn_id} \"{mn.get('title_en', '?')}\" (~{mins}min)")
    print(f"\n  Total: ~{total_min}min ({round(total_min/60,1)}h)")


def cmd_stats(args):
    """Show registry overview."""
    meta, edges, routes = load_all()
    meta_map = {m['kn_id']: m for m in meta}

    print("=== Knowledge Registry Stats ===\n")
    print(f"  Nodes:     {len(meta)}")
    print(f"  Edges:     {len(edges)}")
    print(f"  Routes:    {len(routes)}")

    # Board
    boards = defaultdict(int)
    for m in meta:
        boards[m['primaryBoard']] += 1
    print(f"\n  Board: cie={boards['cie']} edx={boards['edx']} both={boards['both']}")

    # Domain
    domains = defaultdict(int)
    for m in meta:
        domains[m['domain']] += 1
    print(f"  Domain: {dict(sorted(domains.items()))}")

    # Difficulty spread
    from collections import Counter
    diffs = Counter(tuple(m['learning']['difficultyRange']) for m in meta)
    print(f"  Difficulty levels: {len(diffs)} ranges")

    # Variants
    variants = len([m for m in meta if m.get('variantOf')])
    print(f"  Variants: {variants} (primary: {len(meta) - variants})")

    # Routes summary
    print(f"\n  Routes:")
    total_nodes = 0
    for rid, route in sorted(routes.items()):
        kn = len([n for n in route['nodes'] if not n.get('milestone')])
        total_nodes += kn
        print(f"    {rid:30s} {kn:3d} nodes  ~{route['estimatedHours']}h")
    print(f"\n  Total assignments: {total_nodes}")

    # Coverage
    in_routes = set()
    for route in routes.values():
        for n in route['nodes']:
            if not n.get('milestone'):
                in_routes.add(n['kn_id'])
    non_variant = [m for m in meta if not m.get('variantOf')]
    eff = len(in_routes & {m['kn_id'] for m in non_variant})
    print(f"  Coverage: {len(in_routes)}/{len(meta)} ({round(100*len(in_routes)/len(meta))}%)")
    print(f"  Effective: {eff}/{len(non_variant)} ({round(100*eff/len(non_variant))}%)")


COMMANDS = {
    'node': cmd_node,
    'route': cmd_route,
    'section': cmd_section,
    'domain': cmd_domain,
    'search': cmd_search,
    'prereqs': cmd_prereqs,
    'path': cmd_path,
    'stats': cmd_stats,
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Knowledge Registry Query Tool")
        print()
        print("Commands:")
        print("  node <kn_id>            Full node info")
        print("  route <route-id>        Route summary + learning path")
        print("  section <section>       All nodes in CIE section (e.g. s2.3)")
        print("  domain <domain>         All nodes by domain")
        print("  search <keyword>        Text search titles")
        print("  prereqs <kn_id>         Prerequisite chain (up to 5 levels)")
        print("  path <from> <to>        Learning path between nodes")
        print("  stats                   Registry overview")
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
