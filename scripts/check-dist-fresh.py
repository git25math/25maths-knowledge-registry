#!/usr/bin/env python3
"""
Check that dist/ artifacts were built from the current source files.

Maintains dist/build-manifest.json which records SHA-256 hashes of all
source inputs. On check, compares current source hashes to the manifest.
If sources changed but dist/ wasn't rebuilt, the check fails.

Usage:
  python3 scripts/check-dist-fresh.py           # check only (CI mode)
  python3 scripts/check-dist-fresh.py --update   # rebuild + update manifest
"""

import hashlib, json, os, sys, subprocess, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(BASE, 'dist')
MANIFEST_PATH = os.path.join(DIST, 'build-manifest.json')

# Source files that, if changed, require a dist rebuild
SOURCE_PATTERNS = [
    'registry/*.json',
    'graph/*.json',
    'scripts/build-meta-nodes.py',
    'scripts/build-routes.py',
    'scripts/build-board-indexes.py',
    'scripts/dag_utils.py',
]

# Dist artifacts that must exist
DIST_FILES = [
    'meta-nodes.json',
    'routes-compiled.json',
    'coverage-report.json',
    'nodes-by-board.json',
    'question-id-map.json',
    'board-stats.json',
    'build-manifest.json',
]


def file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def collect_source_hashes():
    """Hash all source files that affect dist/ output."""
    hashes = {}
    for pattern in SOURCE_PATTERNS:
        for path in sorted(glob.glob(os.path.join(BASE, pattern))):
            rel = os.path.relpath(path, BASE)
            hashes[rel] = file_hash(path)
    return hashes


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return None


def save_manifest(source_hashes):
    manifest = {
        'generatedBy': 'check-dist-fresh.py',
        'sourceHashes': source_hashes,
        'distFiles': {
            f: file_hash(os.path.join(DIST, f))
            for f in DIST_FILES if f != 'build-manifest.json'
        },
    }
    os.makedirs(DIST, exist_ok=True)
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest


def main():
    update_mode = '--update' in sys.argv

    print("=== Dist Freshness Check ===\n")

    # 1. Check all dist files exist
    missing = [f for f in DIST_FILES if not os.path.exists(os.path.join(DIST, f))]
    if missing and 'build-manifest.json' in missing and len(missing) == 1:
        # Only manifest missing — first run, generate it
        if not update_mode:
            print(f"  No build manifest found.")
            print(f"  Run 'python3 scripts/check-dist-fresh.py --update' to create one.")
            sys.exit(1)
    elif missing:
        print(f"  Missing dist files: {missing}")
        if not update_mode:
            print(f"\n  FAIL — run 'python3 scripts/build-all.py' first.")
            sys.exit(1)

    # 2. Collect current source hashes
    current_sources = collect_source_hashes()
    print(f"  Source files tracked: {len(current_sources)}")

    # 3. Compare to manifest
    manifest = load_manifest()
    if manifest is None:
        if update_mode:
            print("  No existing manifest — will create after build.")
        else:
            print("  No manifest found.")
            print("  FAIL — run with --update to generate.")
            sys.exit(1)
    else:
        old_sources = manifest.get('sourceHashes', {})
        changed = []
        for path, h in current_sources.items():
            old_h = old_sources.get(path)
            if old_h != h:
                changed.append(path)
        removed = [p for p in old_sources if p not in current_sources]

        if changed or removed:
            print(f"\n  Source changes since last build:")
            for p in changed:
                print(f"    CHANGED: {p}")
            for p in removed:
                print(f"    REMOVED: {p}")

            if not update_mode:
                print(f"\n  FAIL — {len(changed)} files changed, {len(removed)} removed.")
                print("  Run 'python3 scripts/build-all.py && python3 scripts/check-dist-fresh.py --update'")
                sys.exit(1)
        else:
            print(f"  All {len(current_sources)} source files match manifest.")
            print(f"\n  PASS — dist/ is fresh.")
            return

    # 4. Update mode: rebuild and save manifest
    if update_mode:
        print("\n  Rebuilding dist/ ...")
        result = subprocess.run(
            [sys.executable, os.path.join(BASE, 'scripts', 'build-all.py')],
            cwd=BASE,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  Build failed:\n{result.stderr[-500:]}")
            sys.exit(1)

        # Re-collect source hashes (build might have changed nothing)
        current_sources = collect_source_hashes()
        manifest = save_manifest(current_sources)
        print(f"  Manifest saved: {len(manifest['sourceHashes'])} sources, {len(manifest['distFiles'])} artifacts")
        print(f"\n  UPDATED — dist/ rebuilt and manifest saved.")


if __name__ == '__main__':
    main()
