# fialr (public) skills

This is the public community repo: issues, README, CHANGELOG, SECURITY,
CONTRIBUTING, and a vendored `feature-manifest.json` the docs-parity check
validates against. Skills here are the small set of recurring procedures, in
the same self-maintaining shape as the other fialr repos.

- **Deterministic scripts:** `scripts/check_docs_parity.py` (README/CHANGELOG
  reference only real commands), `scripts/check_skills.py` (this system's drift
  guard).
- **Hook:** `.claude/settings.json` runs `scripts/hooks/post_edit.py` after an
  edit and nudges the owning skill.

| Skill | Use it when |
|-------|-------------|
| [ship-change](ship-change/SKILL.md) | Landing a change here via branch -> PR -> squash-merge (required checks: docs parity, scan, review). |
| [sync-from-app](sync-from-app/SKILL.md) | The app's command surface changed -> re-vendor the manifest and fix README/CHANGELOG refs. |
| [maintain-skills](maintain-skills/SKILL.md) | A script or skill source changed -> re-audit the skills for drift. |
