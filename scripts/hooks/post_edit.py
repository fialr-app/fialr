#!/usr/bin/env python3
"""PostToolUse router for the public fialr repo. Read-only, fail-open, stdlib."""

from __future__ import annotations

import json
import re
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    rel = (payload.get("tool_input") or {}).get("file_path", "") or ""
    if not rel:
        return 0
    msgs: list[str] = []
    if re.search(r"README\.md$|CHANGELOG\.md$|feature-manifest\.json$", rel):
        msgs.append(
            "README/CHANGELOG/manifest changed -> run scripts/check_docs_parity.py; "
            "if the app's commands changed, re-vendor feature-manifest.json from "
            "fialr-private (the sync-from-app skill)."
        )
    if re.search(r"scripts/|\.github/workflows/|\.claude/skills/", rel):
        msgs.append("A script or skill source changed -> invoke the maintain-skills skill.")
    if msgs:
        print("\n".join(msgs))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
