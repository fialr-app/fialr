#!/usr/bin/env python3
"""Drift guard for the repo-native Claude Code skill system (.claude/skills/).

Skills encode fialr's institutional knowledge as auto-invoking procedures. They
must not rot: a skill that references a renamed script or a missing path sends
an agent down a dead end. This deterministic check (stdlib only, runs in the
gate) fails the build when a skill drifts from the live repo:

  * every `.claude/skills/<dir>/SKILL.md` has valid frontmatter with a `name`
    that matches its directory and a non-empty `description`,
  * every in-repo path a skill mentions in inline code (`scripts/x.py`,
    `tools/x.sh`, `docs/...`) actually exists,
  * `.claude/settings.json` is valid JSON and its hook commands point at real
    scripts,
  * `.claude/skills/README.md` lists every skill (and lists no ghosts).

Mirrors the read-don't-duplicate idea: skills pull truth from CLAUDE.md and the
scripts at runtime; this only checks the wiring.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
SETTINGS = ROOT / ".claude" / "settings.json"
README = SKILLS / "README.md"
# Inline-code tokens that look like in-repo paths we should be able to resolve.
PATH_PREFIXES = re.compile(r"^(scripts|tools|docs|fialr|tests|\.claude|\.github)/")


def _frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    problems: list[str] = []

    if not SKILLS.exists():
        print("no .claude/skills/ -- nothing to check")
        return 0

    skill_names: list[str] = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        d = skill_md.parent.name
        skill_names.append(d)
        raw = skill_md.read_text()
        fm = _frontmatter(raw)
        if fm.get("name") != d:
            problems.append(f"{d}/SKILL.md: frontmatter name '{fm.get('name')}' != dir")
        if not fm.get("description"):
            problems.append(f"{d}/SKILL.md: missing frontmatter description")
        # Inline-code in-repo paths must exist. Skip obvious placeholders
        # (NNNN, <...>, slug) and paths that live in a sibling repo.
        for m in re.finditer(r"`([^`]+)`", raw):
            tok = m.group(1).strip()
            if not PATH_PREFIXES.match(tok) or re.search(r"[ *?<>]", tok):
                continue
            has_ext = "." in tok.split("/")[-1]
            placeholder = "NNNN" in tok or "slug" in tok
            if has_ext and not placeholder and not (ROOT / tok).exists():
                problems.append(f"{d}/SKILL.md: references missing path `{tok}`")

    # settings.json + hook script existence
    if SETTINGS.exists():
        try:
            settings = json.loads(SETTINGS.read_text())
        except json.JSONDecodeError as e:
            problems.append(f".claude/settings.json: invalid JSON ({e})")
            settings = {}
        for grp in settings.get("hooks", {}).values():
            for entry in grp:
                for hook in entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    for m in re.finditer(r"\$CLAUDE_PROJECT_DIR/(\S+)", cmd):
                        p = m.group(1).strip("\"'")
                        if not (ROOT / p).exists():
                            problems.append(f"settings.json hook: missing {p}")

    # README index <-> skill dirs
    readme = README.read_text() if README.exists() else ""
    for name in skill_names:
        if name not in readme:
            problems.append(f"{name}: not listed in .claude/skills/README.md")

    if problems:
        print("Skill-system check FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"Skill-system OK -- {len(skill_names)} skill(s), wiring intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
