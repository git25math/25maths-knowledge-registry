#!/usr/bin/env python3
"""
Auto-populate kn_ids in registry/edx-kn-map.json.

Matches Edexcel sections (e.g. "1.3") to CIE sections (e.g. "s1.3")
via kn-registry.json, filling the empty kn_ids arrays.
"""

import json, os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)


def save(path, data):
    with open(os.path.join(BASE, path), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print("=== Populating edx-kn-map kn_ids ===\n")

    registry = load('registry/kn-registry.json')
    edx_map = load('registry/edx-kn-map.json')

    # Build CIE section → kn_ids index
    section_to_kn = defaultdict(list)
    for node in registry:
        cie = node.get('examBoards', {}).get('cie_0580', {})
        sec = cie.get('section', '')
        if sec:
            section_to_kn[sec].append(node['kn_id'])

    filled = 0
    total_kn = 0
    for ch_id, ch_data in edx_map.items():
        if not isinstance(ch_data, dict) or 'sections' not in ch_data:
            continue
        for sec_id, sec_data in ch_data['sections'].items():
            edx_sections = sec_data.get('sections', [])
            matched = set()
            for es in edx_sections:
                cie_sec = f"s{es}"
                for kn_id in section_to_kn.get(cie_sec, []):
                    matched.add(kn_id)
            sec_data['kn_ids'] = sorted(matched, key=lambda x: int(x.split('_')[1]))
            if matched:
                filled += 1
                total_kn += len(matched)
                print(f"  {sec_id} ({sec_data['title']}): {len(matched)} kn_ids")

    save('registry/edx-kn-map.json', edx_map)

    empty = sum(
        1 for ch in edx_map.values()
        if isinstance(ch, dict)
        for sd in ch.get('sections', {}).values()
        if not sd.get('kn_ids')
    )
    print(f"\nFilled: {filled} sections, {total_kn} kn_id assignments")
    print(f"Empty: {empty} sections (no matching CIE section)")


if __name__ == '__main__':
    main()
