#!/usr/bin/env python3
"""
Build all registry files from Play kp-registry.ts source data.
Outputs: kn-registry.json, dag-edges.json, kp-kn-map.json
"""

import json, re, os, sys
from datetime import datetime, timezone

PLAY_DIR = '/Users/zhuxingzhe/Project/ExamBoard/25maths-games-legends/src/data/curriculum'
EDX_DIR = '/Users/zhuxingzhe/Project/ExamBoard/25maths-edx4ma1-json'
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# ══════════════════════════════════════════
# 1. Parse kp-registry.ts
# ══════════════════════════════════════════

def parse_registry(path):
    """Parse KP registry TS file → chapters, topics, kpIds, KP_KN_MAP"""
    with open(path) as f:
        src = f.read()

    # Extract chapters
    chapters = []
    # Pattern: { id: 'chX', title: '...', titleZh: '...',
    ch_pattern = re.compile(
        r"id:\s*'(ch\d+)',\s*title:\s*'([^']+)',\s*titleZh:\s*'([^']+)'",
    )
    # Pattern for topics within each chapter
    topic_pattern = re.compile(
        r"\{\s*id:\s*'([\d.]+)',\s*title:\s*'([^']+)',\s*titleZh:\s*'([^']+)',\s*tier:\s*'(\w+)',\s*\n?\s*kpIds:\s*\[([^\]]+)\]",
    )

    for ch_match in ch_pattern.finditer(src):
        ch_id = ch_match.group(1)
        ch_title = ch_match.group(2)
        ch_title_zh = ch_match.group(3)
        chapters.append({
            'id': ch_id,
            'title': ch_title,
            'titleZh': ch_title_zh,
            'topics': [],
        })

    for t_match in topic_pattern.finditer(src):
        topic_id = t_match.group(1)
        title = t_match.group(2)
        title_zh = t_match.group(3)
        tier = t_match.group(4)
        kp_ids_raw = t_match.group(5)
        kp_ids = re.findall(r"'(kp-[\d.]+-\d+)'", kp_ids_raw)

        ch_num = topic_id.split('.')[0]
        ch_id = f'ch{ch_num}'
        for ch in chapters:
            if ch['id'] == ch_id:
                ch['topics'].append({
                    'id': topic_id,
                    'title': title,
                    'titleZh': title_zh,
                    'tier': tier,
                    'kpIds': kp_ids,
                })
                break

    # Extract KP_KN_MAP
    kp_kn_map = {}
    map_pattern = re.compile(r"'(kp-[\d.]+-\d+)':\s*'(kn_\d+)'")
    for m in map_pattern.finditer(src):
        kp_kn_map[m.group(1)] = m.group(2)

    return chapters, kp_kn_map


def parse_graph(path):
    """Parse kp-graph.ts → edges list. Uses 'strength' field, not 'type'."""
    with open(path) as f:
        src = f.read()

    edges = []
    # Pattern: { from: 'kp-X', to: 'kp-Y', strength: 'hard'|'soft', reason: ... }
    edge_pattern = re.compile(
        r"\{\s*from:\s*'(kp-[\d.]+-\d+)',\s*to:\s*'(kp-[\d.]+-\d+)',\s*strength:\s*'(\w+)'"
    )
    for m in edge_pattern.finditer(src):
        edges.append({
            'from': m.group(1),
            'to': m.group(2),
            'type': m.group(3),
        })

    return edges


# ══════════════════════════════════════════
# 2. Domain mapping
# ══════════════════════════════════════════

CHAPTER_TO_DOMAIN = {
    'ch1': 'number',
    'ch2': 'algebra',
    'ch3': 'geometry',
    'ch4': 'geometry',
    'ch5': 'geometry',
    'ch6': 'geometry',
    'ch7': 'geometry',
    'ch8': 'probability',
    'ch9': 'statistics',
}

TIER_MAP = {
    'both': 'both',
    'ext': 'extended',
    'core': 'core',
}


# ══════════════════════════════════════════
# 3. Build kn-registry.json
# ══════════════════════════════════════════

def build_registry(chapters, kp_kn_map):
    """Build unified kn-registry from Play data + Edexcel-only nodes"""

    # Collect unique kn_ids with their source data
    kn_nodes = {}  # kn_id → node data

    for ch in chapters:
        domain = CHAPTER_TO_DOMAIN.get(ch['id'], 'number')
        for topic in ch['topics']:
            tier = TIER_MAP.get(topic['tier'], 'both')
            for kp_id in topic['kpIds']:
                kn_id = kp_kn_map.get(kp_id)
                if not kn_id:
                    continue

                if kn_id not in kn_nodes:
                    kn_nodes[kn_id] = {
                        'kn_id': kn_id,
                        'version': 1,
                        'title_en': topic['title'],
                        'title_zh': topic['titleZh'],
                        'domain': domain,
                        'subdomain': f"s{topic['id']}",
                        'tags': [],
                        'examBoards': {
                            'cie_0580': {
                                'section': f"s{topic['id']}",
                                'kpId': kp_id,
                                'tier': tier,
                                'weight': 'medium',
                            }
                        },
                        'prerequisites': [],
                        'leadsTo': [],
                        'difficultyRange': [1, 3],
                        'estimatedMinutes': {'concept': 10, 'practice': 15},
                        'content': {'variants': {'cie': [], 'edexcel': [], 'generic': []}, 'missions': [], 'glGeneratorId': None, 'examRefs': {'cie': 0, 'edexcel': 0}},
                        'noFigure': True,
                        'isFoundational': tier in ('core', 'both'),
                        'deprecated': False,
                        'createdAt': NOW,
                        'updatedAt': NOW,
                        '_kpIds': [kp_id],
                    }
                else:
                    # Add additional KP reference
                    if kp_id not in kn_nodes[kn_id]['_kpIds']:
                        kn_nodes[kn_id]['_kpIds'].append(kp_id)

    # Add 10 Edexcel-only nodes
    edx_only = [
        {'kn_id': 'kn_0289', 'title_en': 'Sum of Arithmetic Series', 'title_zh': '等差数列求和', 'domain': 'algebra', 'section': '3.1'},
        {'kn_id': 'kn_0290', 'title_en': 'Calculus Kinematics', 'title_zh': '微积分运动学', 'domain': 'algebra', 'section': '3.4'},
        {'kn_id': 'kn_0291', 'title_en': 'Imperial Unit Conversions', 'title_zh': '英制单位换算', 'domain': 'number', 'section': '4.4'},
        {'kn_id': 'kn_0292', 'title_en': 'Plans and Elevations', 'title_zh': '三视图', 'domain': 'geometry', 'section': '4.10'},
        {'kn_id': 'kn_0293', 'title_en': 'Frustum Volume', 'title_zh': '锥台体积', 'domain': 'geometry', 'section': '4.10'},
        {'kn_id': 'kn_0294', 'title_en': 'Negative Scale Factor Enlargement', 'title_zh': '负缩放因子放大', 'domain': 'geometry', 'section': '5.2'},
        {'kn_id': 'kn_0295', 'title_en': 'Box Plots', 'title_zh': '箱线图', 'domain': 'statistics', 'section': '6.1'},
        {'kn_id': 'kn_0296', 'title_en': 'Geometrical Reasoning', 'title_zh': '几何推理', 'domain': 'geometry', 'section': '4.7'},
        {'kn_id': 'kn_0297', 'title_en': 'Change Subject (appears twice)', 'title_zh': '主元出现两次的变形', 'domain': 'algebra', 'section': '2.3'},
        {'kn_id': 'kn_0298', 'title_en': 'Applied Number Operations', 'title_zh': '综合数字应用', 'domain': 'number', 'section': '1.10'},
    ]

    for node in edx_only:
        kn_nodes[node['kn_id']] = {
            'kn_id': node['kn_id'],
            'version': 1,
            'title_en': node['title_en'],
            'title_zh': node['title_zh'],
            'domain': node['domain'],
            'subdomain': f"edx-{node['section']}",
            'tags': ['edexcel-only'],
            'examBoards': {
                'edexcel_4ma1': {
                    'section': node['section'],
                    'tier': 'both',
                    'weight': 'medium',
                }
            },
            'prerequisites': [],
            'leadsTo': [],
            'difficultyRange': [2, 4],
            'estimatedMinutes': {'concept': 15, 'practice': 20},
            'content': {'variants': {'cie': [], 'edexcel': [], 'generic': []}, 'missions': [], 'glGeneratorId': None, 'examRefs': {'cie': 0, 'edexcel': 0}},
            'noFigure': True,
            'isFoundational': False,
            'deprecated': False,
            'createdAt': NOW,
            'updatedAt': NOW,
            '_kpIds': [],
        }

    # Sort by kn_id and clean internal fields
    result = []
    for kn_id in sorted(kn_nodes.keys(), key=lambda x: int(x.split('_')[1])):
        node = kn_nodes[kn_id]
        node.pop('_kpIds', None)
        result.append(node)

    return result


# ══════════════════════════════════════════
# 4. Build dag-edges.json
# ══════════════════════════════════════════

def build_dag(raw_edges, kp_kn_map):
    """Convert KP-based edges to kn_id-based edges, deduplicate"""
    seen = set()
    dag = []

    for e in raw_edges:
        from_kn = kp_kn_map.get(e['from'])
        to_kn = kp_kn_map.get(e['to'])
        if not from_kn or not to_kn:
            continue
        if from_kn == to_kn:
            continue  # skip self-loops

        key = (from_kn, to_kn)
        reverse_key = (to_kn, from_kn)
        if key in seen:
            continue
        # Skip if reverse edge already exists (would create cycle)
        if reverse_key in seen:
            continue
        seen.add(key)

        dag.append({
            'from': from_kn,
            'to': to_kn,
            'type': e['type'],
        })

    # Add Edexcel-only node prerequisites
    edx_prereqs = [
        ('kn_0289', 'kn_0115', 'soft', 'nth term linear needed for series sum'),
        ('kn_0290', 'kn_0347', 'hard', 'differentiation needed for kinematics'),
        ('kn_0292', 'kn_0350', 'soft', '3D shapes needed for plans/elevations'),
        ('kn_0293', 'kn_0363', 'hard', 'volume of cone needed for frustum'),
        ('kn_0294', 'kn_0375', 'hard', 'enlargement needed for negative SF'),
        ('kn_0295', 'kn_0386', 'soft', 'quartiles needed for box plots'),
        ('kn_0296', 'kn_0149', 'soft', 'polygon angles needed for reasoning'),
        ('kn_0297', 'kn_0095', 'hard', 'rearrange formulae needed for subject-twice'),
        ('kn_0298', 'kn_0034', 'soft', 'decimal arithmetic needed for applied number'),
    ]

    for to_kn, from_kn, etype, reason in edx_prereqs:
        key = (from_kn, to_kn)
        if key not in seen:
            seen.add(key)
            dag.append({
                'from': from_kn,
                'to': to_kn,
                'type': etype,
                'reason': reason,
            })

    # Remove cycles: iteratively remove back-edges using Kahn's algorithm
    from collections import defaultdict as dd
    adj = dd(list)
    in_deg = dd(int)
    all_nodes_set = set()
    for e in dag:
        adj[e['from']].append(e)
        in_deg[e['to']] += 1
        all_nodes_set.add(e['from'])
        all_nodes_set.add(e['to'])

    queue = [n for n in all_nodes_set if in_deg[n] == 0]
    visited_set = set()
    acyclic_edges = []

    while queue:
        node = queue.pop(0)
        visited_set.add(node)
        for edge in adj[node]:
            acyclic_edges.append(edge)
            in_deg[edge['to']] -= 1
            if in_deg[edge['to']] == 0:
                queue.append(edge['to'])

    # Nodes still not visited are in cycles — drop their back-edges
    removed = len(dag) - len(acyclic_edges)
    if removed > 0:
        dag = acyclic_edges

    return dag


# ══════════════════════════════════════════
# 5. Build mapping files
# ══════════════════════════════════════════

def build_hhk_map():
    """Build HHK unit → kn_id mapping"""
    hhk = {
        "Y7.1":  {"title": "Multiplication of Fractions", "cieSections": ["s1.4"], "year": 7},
        "Y7.2":  {"title": "Division of Fractions", "cieSections": ["s1.4"], "year": 7},
        "Y7.3":  {"title": "Negative Numbers", "cieSections": ["s1.1", "s1.6"], "year": 7},
        "Y7.4":  {"title": "Position and Direction", "cieSections": ["s3.1", "s4.3"], "year": 7},
        "Y7.5":  {"title": "Ratio and Proportion", "cieSections": ["s1.11", "s1.12"], "year": 7},
        "Y7.6":  {"title": "Percentage", "cieSections": ["s1.13"], "year": 7},
        "Y7.7":  {"title": "Circle", "cieSections": ["s5.3"], "year": 7},
        "Y7.8":  {"title": "Cylinders and Cones", "cieSections": ["s5.4", "s5.5"], "year": 7},
        "Y7.9":  {"title": "Linear Sequences", "cieSections": ["s2.7"], "year": 7},
        "Y7.10": {"title": "Probability", "cieSections": ["s8.3"], "year": 7},
        "Y7.11": {"title": "Constructions", "cieSections": ["s4.1"], "year": 7},
        "Y8.1":  {"title": "Review of Numbers", "cieSections": ["s1.1", "s1.3", "s1.6"], "year": 8},
        "Y8.2":  {"title": "Rational/Factors/Primes", "cieSections": ["s1.1", "s1.6"], "year": 8},
        "Y8.3":  {"title": "Algebraic Formula", "cieSections": ["s2.1", "s2.4"], "year": 8},
        "Y8.4":  {"title": "Inequalities", "cieSections": ["s2.6"], "year": 8},
        "Y8.5":  {"title": "Pythagoras", "cieSections": ["s6.1"], "year": 8},
        "Y8.6":  {"title": "Intersecting/Parallel Lines", "cieSections": ["s4.6"], "year": 8},
        "Y8.7":  {"title": "Further Algebra", "cieSections": ["s2.1", "s2.2", "s2.3"], "year": 8},
        "Y8.8":  {"title": "Coordinates/Linear Graphs", "cieSections": ["s3.1", "s3.2"], "year": 8},
        "Y8.9":  {"title": "Further Statistics", "cieSections": ["s9.1", "s9.2", "s9.3"], "year": 8},
        "Y9.1":  {"title": "Irrational Numbers", "cieSections": ["s1.3", "s1.7"], "year": 9},
        "Y9.2":  {"title": "Working with Expressions", "cieSections": ["s2.1", "s2.2"], "year": 9},
        "Y9.3":  {"title": "Algebraic Functions", "cieSections": ["s2.13"], "year": 9},
        "Y9.4":  {"title": "Mastery of Angles", "cieSections": ["s4.6", "s4.7"], "year": 9},
        "Y9.5":  {"title": "Pythagoras Theorem", "cieSections": ["s6.1"], "year": 9},
        "Y9.6":  {"title": "2D Shape", "cieSections": ["s5.2", "s5.3"], "year": 9},
        "Y9.7":  {"title": "Percentages", "cieSections": ["s1.13"], "year": 9},
        "Y9.8":  {"title": "Statistical Sampling", "cieSections": ["s9.1"], "year": 9},
        "Y9.9":  {"title": "Graphical Statistical Data", "cieSections": ["s9.3", "s9.4", "s9.5"], "year": 9},
        "Y9.10": {"title": "Algebraic Fractions", "cieSections": ["s2.3"], "year": 9},
        "Y9.11": {"title": "Constructions", "cieSections": ["s4.1", "s4.2"], "year": 9},
        "Y9.12": {"title": "Congruence/Similarity", "cieSections": ["s4.4"], "year": 9},
        "Y10.1":  {"title": "Real Numbers", "cieSections": ["s1.7", "s1.8"], "year": 10},
        "Y10.2":  {"title": "Algebraic Fractions", "cieSections": ["s2.3"], "year": 10},
        "Y10.3":  {"title": "Quadratic Equations", "cieSections": ["s2.10"], "year": 10},
        "Y10.4":  {"title": "Simultaneous Equations", "cieSections": ["s2.9"], "year": 10},
        "Y10.5":  {"title": "Functions", "cieSections": ["s2.13"], "year": 10},
        "Y10.6":  {"title": "Further Trigonometry", "cieSections": ["s6.2", "s6.3", "s6.4"], "year": 10},
        "Y10.7":  {"title": "Circles", "cieSections": ["s4.7", "s5.3"], "year": 10},
        "Y10.8":  {"title": "Constructions", "cieSections": ["s4.1", "s4.2"], "year": 10},
        "Y10.9":  {"title": "Congruence/Similarity", "cieSections": ["s4.4"], "year": 10},
        "Y10.10": {"title": "Transformations", "cieSections": ["s7.1"], "year": 10},
        "Y10.11": {"title": "Probability", "cieSections": ["s8.3", "s8.4"], "year": 10},
        "Y10.12": {"title": "3D Geometry", "cieSections": ["s5.4", "s6.5"], "year": 10},
        "Y11.1":  {"title": "Estimation/Bounds", "cieSections": ["s1.9", "s1.10"], "year": 11},
        "Y11.2":  {"title": "Sets/Venn Diagrams", "cieSections": ["s1.2", "s8.1"], "year": 11},
        "Y11.3":  {"title": "Simultaneous Equations", "cieSections": ["s2.9"], "year": 11},
        "Y11.4":  {"title": "Quadratic Sequences", "cieSections": ["s2.7"], "year": 11},
        "Y11.5":  {"title": "Functions", "cieSections": ["s2.13"], "year": 11},
        "Y11.6":  {"title": "Differentiation", "cieSections": ["s2.12"], "year": 11},
        "Y11.7":  {"title": "Further Trig", "cieSections": ["s6.2", "s6.4"], "year": 11},
        "Y11.8":  {"title": "Trig Graphs", "cieSections": ["s3.5"], "year": 11},
        "Y11.9":  {"title": "Regions/Inequalities", "cieSections": ["s2.6"], "year": 11},
        "Y11.10": {"title": "Vectors", "cieSections": ["s7.2"], "year": 11},
        "Y11.11": {"title": "Statistics/Probability", "cieSections": ["s8.3", "s9.2", "s9.4"], "year": 11},
    }
    return hhk


def build_edx_map():
    """Build Edexcel section → kn_id mapping from syllabus-edx.json"""
    syllabus_path = os.path.join(EDX_DIR, 'syllabus-edx.json')
    if not os.path.exists(syllabus_path):
        return {"_note": "syllabus-edx.json not found, placeholder"}

    with open(syllabus_path) as f:
        syllabus = json.load(f)

    # Format: { chapters: [ { id, title, teachingUnits: [ { unit, title, tier, sections: ["1.1"] } ] } ] }
    result = {}
    chapters = syllabus.get('chapters', [])
    for chapter in chapters:
        ch_id = chapter.get('id', '')
        ch_title = chapter.get('title', '')
        units = {}
        for tu in chapter.get('teachingUnits', []):
            unit_key = f"{ch_id}-u{tu.get('unit', 0)}"
            units[unit_key] = {
                'title': tu.get('title', ''),
                'tier': tu.get('tier', 'both'),
                'sections': tu.get('sections', []),
                'kn_ids': [],  # to be populated
            }
        result[ch_id] = {'title': ch_title, 'sections': units}

    return result


# ══════════════════════════════════════════
# 6. Build route frameworks
# ══════════════════════════════════════════

ROUTES = [
    {"id": "cie-core-number", "title_en": "CIE Core — Number", "title_zh": "CIE Core — 数字", "board": "cie_0580", "tier": "core", "desc": "CIE 0580 Core 数字章节完整学习路线"},
    {"id": "cie-core-geometry", "title_en": "CIE Core — Geometry", "title_zh": "CIE Core — 几何", "board": "cie_0580", "tier": "core", "desc": "CIE 0580 Core 几何章节完整学习路线"},
    {"id": "cie-extended-algebra", "title_en": "CIE Extended — Algebra", "title_zh": "CIE Extended — 代数", "board": "cie_0580", "tier": "extended", "desc": "CIE 0580 Extended 代数章节完整学习路线"},
    {"id": "cie-recovery-algebra", "title_en": "CIE Recovery — Algebra", "title_zh": "CIE 补救 — 代数", "board": "cie_0580", "tier": "core", "desc": "代数基础补救路线，只选L1-L2"},
    {"id": "cie-recovery-fractions", "title_en": "CIE Recovery — Fractions", "title_zh": "CIE 补救 — 分数", "board": "cie_0580", "tier": "core", "desc": "分数补救路线，s1.4→s2.3"},
    {"id": "cie-sprint-2weeks", "title_en": "CIE Sprint — 2 Weeks", "title_zh": "CIE 冲刺 — 两周", "board": "cie_0580", "tier": "both", "desc": "考前两周高频考点冲刺"},
    {"id": "edx-foundation", "title_en": "Edexcel Foundation", "title_zh": "Edexcel 基础卷", "board": "edexcel_4ma1", "tier": "foundation", "desc": "Edexcel Foundation 必考点学习路线"},
    {"id": "edx-higher", "title_en": "Edexcel Higher", "title_zh": "Edexcel 高级卷", "board": "edexcel_4ma1", "tier": "higher", "desc": "Edexcel Higher 额外内容学习路线"},
    {"id": "hhk-y7", "title_en": "HHK Year 7", "title_zh": "哈罗七年级", "board": "hhk", "tier": "both", "desc": "哈罗七年级课纲学习路线"},
    {"id": "hhk-y8", "title_en": "HHK Year 8", "title_zh": "哈罗八年级", "board": "hhk", "tier": "both", "desc": "哈罗八年级课纲学习路线"},
    {"id": "hhk-y9", "title_en": "HHK Year 9", "title_zh": "哈罗九年级", "board": "hhk", "tier": "both", "desc": "哈罗九年级课纲学习路线"},
    {"id": "hhk-y10", "title_en": "HHK Year 10", "title_zh": "哈罗十年级", "board": "hhk", "tier": "both", "desc": "哈罗十年级课纲学习路线"},
    {"id": "hhk-y11", "title_en": "HHK Year 11", "title_zh": "哈罗十一年级", "board": "hhk", "tier": "both", "desc": "哈罗十一年级课纲学习路线"},
]


# ══════════════════════════════════════════
# Main
# ══════════════════════════════════════════

def main():
    print("=== Building Knowledge Registry ===")

    # Parse source data
    registry_path = os.path.join(PLAY_DIR, 'kp-registry.ts')
    graph_path = os.path.join(PLAY_DIR, 'kp-graph.ts')

    print(f"Reading {registry_path}...")
    chapters, kp_kn_map = parse_registry(registry_path)

    total_kps = sum(len(kp) for ch in chapters for t in ch['topics'] for kp in [t['kpIds']])
    print(f"  Chapters: {len(chapters)}, Topics: {sum(len(ch['topics']) for ch in chapters)}, KPs: {total_kps}")
    print(f"  KP→kn_id mappings: {len(kp_kn_map)}")

    print(f"Reading {graph_path}...")
    raw_edges = parse_graph(graph_path)
    print(f"  Raw edges: {len(raw_edges)}")

    # Build outputs
    print("\n--- Building kn-registry.json ---")
    registry = build_registry(chapters, kp_kn_map)
    reg_path = os.path.join(OUT_DIR, 'registry', 'kn-registry.json')
    with open(reg_path, 'w') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"  Nodes: {len(registry)}")

    # Count unique kn_ids from CIE vs Edexcel-only
    cie_count = len([n for n in registry if 'cie_0580' in n.get('examBoards', {})])
    edx_only = len([n for n in registry if 'edexcel-only' in n.get('tags', [])])
    print(f"  CIE nodes: {cie_count}, Edexcel-only: {edx_only}")

    print("\n--- Building dag-edges.json ---")
    dag = build_dag(raw_edges, kp_kn_map)
    dag_path = os.path.join(OUT_DIR, 'graph', 'dag-edges.json')
    with open(dag_path, 'w') as f:
        json.dump(dag, f, indent=2, ensure_ascii=False)
    hard = len([e for e in dag if e['type'] == 'hard'])
    soft = len([e for e in dag if e['type'] == 'soft'])
    print(f"  Edges: {len(dag)} (hard: {hard}, soft: {soft})")

    print("\n--- Building kp-kn-map.json ---")
    map_path = os.path.join(OUT_DIR, 'registry', 'kp-kn-map.json')
    with open(map_path, 'w') as f:
        json.dump(kp_kn_map, f, indent=2, ensure_ascii=False)
    print(f"  Mappings: {len(kp_kn_map)}")

    print("\n--- Building hhk-kn-map.json ---")
    hhk = build_hhk_map()
    hhk_path = os.path.join(OUT_DIR, 'registry', 'hhk-kn-map.json')
    with open(hhk_path, 'w') as f:
        json.dump(hhk, f, indent=2, ensure_ascii=False)
    print(f"  HHK units: {len(hhk)}")

    print("\n--- Building edx-kn-map.json ---")
    edx = build_edx_map()
    edx_path = os.path.join(OUT_DIR, 'registry', 'edx-kn-map.json')
    with open(edx_path, 'w') as f:
        json.dump(edx, f, indent=2, ensure_ascii=False)
    sec_count = sum(len(ch.get('sections', {})) for ch in edx.values() if isinstance(ch, dict) and 'sections' in ch)
    print(f"  Edexcel chapters: {len(edx)}, sections: {sec_count}")

    print("\n--- Building route frameworks ---")
    routes_dir = os.path.join(OUT_DIR, 'routes')
    for r in ROUTES:
        route = {
            'id': r['id'],
            'title_en': r['title_en'],
            'title_zh': r['title_zh'],
            'board': r['board'],
            'tier': r['tier'],
            'description': r['desc'],
            'estimatedHours': 0,
            'nodes': [],
            'version': 1,
            'createdAt': NOW,
        }
        rpath = os.path.join(routes_dir, f"{r['id']}.json")
        with open(rpath, 'w') as f:
            json.dump(route, f, indent=2, ensure_ascii=False)
    print(f"  Routes: {len(ROUTES)}")

    print("\n=== BUILD COMPLETE ===")
    print(f"  Registry: {len(registry)} nodes")
    print(f"  DAG: {len(dag)} edges")
    print(f"  Maps: kp({len(kp_kn_map)}) + hhk({len(hhk)}) + edx")
    print(f"  Routes: {len(ROUTES)} frameworks")


if __name__ == '__main__':
    main()
