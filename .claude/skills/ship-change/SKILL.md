---
name: ship-change
description: Land a change on the public fialr repo via branch -> PR -> squash-merge, as the fialr-com bot identity. Use automatically and proactively whenever a change is ready to merge to main here. Never push straight to main; this repo's ruleset enforces required checks.
---

# ship-change

Never push to `main` — the ruleset requires the checks `docs parity`, `scan`,
and `review` to pass on a PR.

## Procedure

1. Confirm the bot identity: `git config user.name` is `fialr-com`,
   `commit.gpgsign` is `false` (never a personal GPG key).
2. `gh auth switch --user fialr-com`; verify `gh api user --jq .login`.
3. `git switch -c <type>/<slug>`; commit (end with the `Co-Authored-By: Claude`
   line); push the branch.
4. `gh pr create --repo fialr-app/fialr ...`; wait for the three required
   checks green (`gh pr checks <n> --watch`); `gh pr merge <n> --squash
   --delete-branch`. Do not `--admin`-bypass the required checks.
5. Verify `gh api repos/fialr-app/fialr/commits/main` shows author `fialr-com`,
   `verified: true`.

## Keep current

Sources: the repo ruleset (required contexts), CONTRIBUTING.md.
