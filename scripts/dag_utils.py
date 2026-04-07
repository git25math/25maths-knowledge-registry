#!/usr/bin/env python3
"""DAG utility functions for topological sort, path finding, and analysis."""

import json, os
from collections import defaultdict, deque

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_edges(path=None):
    if path is None:
        path = os.path.join(BASE, 'graph', 'dag-edges.json')
    with open(path) as f:
        return json.load(f)


def build_adjacency(edges):
    """Build adjacency list and reverse adjacency from edge list."""
    adj = defaultdict(list)       # from -> [to]
    rev = defaultdict(list)       # to -> [from]
    for e in edges:
        adj[e['from']].append(e['to'])
        rev[e['to']].append(e['from'])
    return adj, rev


def topological_sort(nodes, edges):
    """Return nodes in topological order (Kahn's algorithm).

    Args:
        nodes: list of kn_id strings
        edges: list of {"from": ..., "to": ..., "type": ...}
    Returns:
        list of kn_id in dependency-respecting order
    """
    node_set = set(nodes)
    # Only consider edges within our node set
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    for e in edges:
        if e['from'] in node_set and e['to'] in node_set:
            adj[e['from']].append(e['to'])
            in_degree[e['to']] += 1

    # Initialize in_degree for all nodes
    for n in node_set:
        if n not in in_degree:
            in_degree[n] = 0

    queue = deque(sorted([n for n in node_set if in_degree[n] == 0]))
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for nb in sorted(adj[node]):
            in_degree[nb] -= 1
            if in_degree[nb] == 0:
                queue.append(nb)

    # Any remaining nodes (in cycles) appended at end
    remaining = [n for n in sorted(node_set) if n not in set(result)]
    result.extend(remaining)
    return result


def get_learning_path(start_kn_id, target_kn_id, edges):
    """Return shortest learning path from start to target using BFS."""
    adj, _ = build_adjacency(edges)
    visited = {start_kn_id}
    queue = deque([(start_kn_id, [start_kn_id])])
    while queue:
        node, path = queue.popleft()
        if node == target_kn_id:
            return path
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return []


def get_prerequisites_chain(kn_id, edges, depth=3):
    """Return complete prerequisite chain up to `depth` levels."""
    _, rev = build_adjacency(edges)
    result = []
    current_level = [kn_id]
    visited = {kn_id}
    for d in range(depth):
        next_level = []
        for node in current_level:
            for parent in rev[node]:
                if parent not in visited:
                    visited.add(parent)
                    next_level.append(parent)
                    result.append({'kn_id': parent, 'depth': d + 1})
        current_level = next_level
        if not current_level:
            break
    return result


def find_bottleneck_nodes(edges):
    """Find nodes with highest in-degree (most students need as prerequisite)."""
    in_degree = defaultdict(int)
    for e in edges:
        in_degree[e['to']] += 1
    # Sort by in-degree descending
    ranked = sorted(in_degree.items(), key=lambda x: -x[1])
    return ranked[:20]


def estimate_route_time(route_nodes, meta_nodes_map):
    """Estimate total learning time for a route in minutes.

    Args:
        route_nodes: list of route node dicts (with kn_id)
        meta_nodes_map: dict of kn_id -> meta node
    Returns:
        total minutes
    """
    total = 0
    for rn in route_nodes:
        kn_id = rn.get('kn_id', '')
        if kn_id.startswith('milestone'):
            continue
        mn = meta_nodes_map.get(kn_id)
        if mn:
            em = mn.get('learning', {}).get('estimatedMinutes', {})
            total += em.get('concept', 0) + em.get('practice', 0)
    return total


if __name__ == '__main__':
    edges = load_edges()
    adj, rev = build_adjacency(edges)
    all_nodes = set()
    for e in edges:
        all_nodes.add(e['from'])
        all_nodes.add(e['to'])

    print(f"Nodes in DAG: {len(all_nodes)}")
    print(f"Edges: {len(edges)}")

    sorted_nodes = topological_sort(list(all_nodes), edges)
    print(f"Topological order: {len(sorted_nodes)} nodes")
    print(f"First 10: {sorted_nodes[:10]}")

    bottlenecks = find_bottleneck_nodes(edges)
    print(f"\nTop bottleneck nodes (highest in-degree):")
    for kn_id, deg in bottlenecks[:10]:
        print(f"  {kn_id}: in-degree={deg}")
