---
id: LESSON-001
title: Charter sync awk multiline failure → use Python instead
date: 2026-04-26
category: sync
severity: 🟡 important
related_ADR: 0029
related_TASK: charter sync v3.X
keywords: [charter, sync, awk, python, multiline, unicode]
auto_load: true
---

## Trigger context
Stage 5.11-C: charter sync to 6 repos using `scripts/sync-claude-charter.sh` with awk. Charter content contains `═══` Unicode separators and Chinese multiline strings.

## Symptom / error observed
- awk reported "newline in string" errors
- Sync script claimed success but CLAUDE.md files still had old charter content (silent failure)
- Verification grep showed v3 content not actually replaced

## Root cause
- awk's `-v` variable assignment doesn't handle multiline strings cleanly
- Heredoc with `═══` Unicode + Chinese multiline content broke awk's string parsing
- Script reported `"replaced"` based on awk's exit code 0, but the actual file content wasn't updated

## Fix applied
- Wrote `scripts/sync-claude-charter.py` (Python with proper regex + UTF-8 handling)
- Re-synced; verified replacements by grep

## Lesson
- For multiline Unicode + i18n content, prefer Python over shell + awk
- Always **verify** file content after script claims success (don't trust exit code)
- Charter sync class scripts should have a verification step:
  ```bash
  grep -c "expected_marker" target_file
  ```

## Auto-detection
- Future charter syncs: include `verify_sync()` function that grep-checks each target repo for expected new charter version string
- If grep fails, error out loudly (don't claim success)
