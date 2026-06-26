---
name: maintain-skills
description: Re-audit this repo's .claude/skills against the live repo and fix any skill that drifted. Use automatically and proactively whenever scripts/**, the CI workflow, or .claude/skills itself changed.
---

# maintain-skills

## Procedure

1. Run `python scripts/check_skills.py` (also in CI): flags frontmatter drift,
   references to missing paths, an invalid `.claude/settings.json`, and skills
   missing from the index.
2. Update any SKILL.md whose referenced scripts/procedures drifted, and keep
   `.claude/skills/README.md`'s table in sync.
3. Re-run until clean.

## Keep current

Sources: `scripts/check_skills.py`, `.claude/skills/README.md`,
`scripts/hooks/post_edit.py`.
