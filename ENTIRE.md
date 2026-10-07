# Entire.io on this repo

Entire follows the GitHub repo, not the Windows folder name.

- GitHub: `Vincenzo-OPC/Civio`
- Web: https://entire.io (sign in Vincenzo-OPC, open Civio)
- Checkpoints: git-refs strategy (`refs/entire/checkpoints/...`)
- Canonical MSI study app: Docker `hiraya-review-app` on `localhost:8080` (do not break; never touch Hermes `:8642`)
- Box build tree: `/workspace/civio-build` (agents). Do not reuse `/workspace/civio-audit`.

## Enable (once per clone)

```bash
# Linux / box
curl -fsSL https://entire.io/install.sh | bash
cd /path/to/Civio
entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path
entire status
```

```powershell
# GT MSI
irm https://entire.io/install.ps1 | iex
cd C:\Users\GT\Desktop\Grok\CSE\Hiraya-Review   # or the Civio clone path
entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path
entire status
```

Committed: `.entire/settings.json`, `.entire/.gitignore`, `.entire/README.md`, `.cursor/hooks.json`.
Never commit `.entire/metadata/`, logs, or `settings.local.json`.

## Notes

- Telemetry off in this repo.
- Redaction rules cover common API key / PAT shapes (best-effort).
- If `entire enable` cannot run in a headless cloud session, commit the settings
  files (already done) and run enable on the MSI so local git hooks install.

## Status (checked 7 Oct 2026, Asia/Manila)

**Entire is set up as config and docs only. It is not capturing any Civio
sessions yet.**

What exists:

- Committed config: `.entire/settings.json` (enabled, telemetry off, git-refs
  checkpoints, PAT/API-key redaction) and `.cursor/hooks.json` (Cursor agent hooks
  that call `entire hooks cursor …` only if the CLI is installed).
- On the box (`/workspace/civio-build`): `entire` CLI 0.11.3, installed through
  the npm wrapper `@yossydev/entire` 0.5.0 rather than the official install script.
  `entire status` says "Enabled · Agents: Cursor", and the box clone has Entire git
  hooks (`prepare-commit-msg`, `commit-msg`, `post-commit`, `post-rewrite`, `pre-push`).

What it has recorded: nothing. `entire session list` → no sessions;
`entire checkpoint list` → 0 checkpoints; no `refs/entire/*` locally or on
`origin`; no `Entire-Checkpoint` trailers in history; the CLI is not logged in.
`.entire/logs/entire.log` only shows "redaction configured" on each commit.

Why: Entire records a session only when a supported agent (Cursor, Claude Code,
Codex, Copilot CLI, OpenCode…) runs with its hooks in a clone where Entire is
enabled. Only the Cursor integration is installed, and the box agent sessions
that made recent commits are not one of those agents, so commits have no session
to attach. Whether the MSI clone has Entire enabled was not checked (the MSI is
read-only for agents).

To turn it on (GT, on the machine where an agent edits Civio, e.g. the MSI clone
or the Codex environment):

```powershell
irm https://entire.io/install.ps1 | iex          # official CLI (Windows)
cd <your Civio clone>                            # a git clone of Vincenzo-OPC/Civio
entire login                                     # for the entire.io web view
entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path
entire agent add codex                           # and/or: entire agent add claude-code
entire status                                    # expect the agents listed
```

Commit any hook config files `entire agent add` creates, work through that agent,
and push normally (the `pre-push` hook pushes checkpoints). Check with
`entire session list`, `entire checkpoint list`, and
`git ls-remote origin "refs/entire/*"`. Optionally swap the box's npm wrapper for
the official `curl -fsSL https://entire.io/install.sh | bash`.

## Related

- `docs/CHANGES_FROM_HIRAYA.md` — every difference from the original Hiraya.
- `CHANGELOG.md` — generated with `npm run changelog` (git-cliff).
