---
name: sync-from-app
description: Keep this repo's vendored feature-manifest.json and command references in sync with the app in fialr-private. Use automatically and proactively whenever the app's command surface changed, or when scripts/check_docs_parity.py fails because README/CHANGELOG names a command that no longer exists.
---

# sync-from-app

The app's command surface lives in `fialr-app/fialr-private`. This repo vendors
the code-derived `feature-manifest.json` and checks README/CHANGELOG against it.

## Procedure

1. In `fialr-private`, regenerate the manifest (`gen_feature_manifest.py`) and
   copy the resulting `feature-manifest.json` into this repo's root.
2. Update any stale command names in `README.md` / `CHANGELOG.md`.
3. Run `python scripts/check_docs_parity.py` until clean.
4. Land it via the ship-change skill.

## Keep current

Sources: `feature-manifest.json`, `scripts/check_docs_parity.py`.
