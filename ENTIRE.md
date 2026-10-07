# Entire on Civio

Entire ([entire.io](https://entire.io), `entireio/cli`) is a standalone CLI that
links AI agent sessions (prompts, transcripts) to the commits they produced. It
is not a plugin or MCP server; see `.entire/README.md`.

- GitHub repo: `Vincenzo-OPC/Civio` (Entire follows the repo, not the folder name)
- Checkpoints: **git-refs** strategy, `refs/entire/checkpoints/...`, pushed to `origin`
- Agents wired: **Codex** and **Claude Code**
- Telemetry: off. Secret redaction: `.entire/settings.json`
- Canonical MSI study app: the Docker study container on `localhost:8080` (do not
  break it; never touch Hermes on `:8642`). Box build tree: `/workspace/civio-build`.

## How a checkpoint gets recorded

1. A supported agent (Codex or Claude Code) works in a clone of Civio. Its
   committed hooks (`.codex/hooks.json`, `.claude/settings.json`) call
   `entire hooks <agent> <event>`, and Entire keeps the session in local shadow
   branches (`entire/<hash>`) and `.entire/metadata/` (never committed).
2. A commit is made in that clone. The git hooks in `.githooks/` add an
   `Entire-Checkpoint:` trailer and condense the session into a checkpoint ref
   `refs/entire/checkpoints/...`.
3. `git push` runs `.githooks/pre-push`, which pushes the checkpoint refs to
   `origin` next to your branch.

All three are needed. Without agent hooks there is no session; without the git
hooks there is no trailer and nothing is pushed.

**No login is needed for git-refs checkpoints.** They are ordinary git refs on
GitHub. `entire login` is only for the entire.io web view.

## Committed files

| File                    | What it does                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.entire/settings.json` | `enabled`, `absolute_git_hook_path`, `telemetry: false`, git-refs checkpoints, redaction for GitHub classic and fine-grained PATs, Google API keys and Telegram bot tokens                                                                                                                                                                                                                          |
| `.entire/.gitignore`    | ignores `tmp/`, `settings.local.json`, `metadata/`, `logs/`, `redactors/local/`                                                                                                                                                                                                                                                                                                                     |
| `.codex/hooks.json`     | 7 Codex hooks: SessionStart, UserPromptSubmit, PostToolUse, Stop, SubagentStart, SubagentStop, SessionEnd. Each is a `cmd.exe` wrapper that runs `entire hooks codex <event>` only if `where.exe entire` finds it, and otherwise exits 0 quietly                                                                                                                                                    |
| `.claude/settings.json` | Claude Code hooks: SessionStart, UserPromptSubmit, Stop, SubagentStop, SessionEnd, PreToolUse(Agent) → pre-task, PostToolUse(Agent) → post-task, PostToolUse(TaskCreate\|TaskUpdate) → post-todo. Each is an `sh -c` wrapper that exits quietly if `entire` is not on PATH. Also denies `Read(./.entire/metadata/**)`                                                                               |
| `.githooks/`            | `commit-msg`, `prepare-commit-msg`, `post-commit`, `post-rewrite`, `pre-push`. They use `entire` from PATH, else `%USERPROFILE%\scoop\apps\entire\current\entire.exe` (or `$SCOOP`), and exit 0 quietly when Entire is missing, so the box, CI and other machines never break. `pre-push` runs `entire hooks git pre-push "$1"`, then chains to `.githooks/pre-push.pre-entire` if that file exists |

`.githooks/` only runs in a clone that has `core.hooksPath` set to it. That is
local git config, so it is a one-time step per clone (below).

A failing `entire hooks git pre-push` stops the push, as in Entire's own hook:
Entire fails on purpose when it detects a privacy-critical problem (for example
a diverged checkpoint ref on the remote). A transient checkpoint upload failure
is only logged and does not stop the push.

Cursor is not used for Civio, so the old `.cursor/hooks.json` was removed and
there is no `.cursor/` folder (no hooks, no rules). GT works with Codex, Grok
Build and Grok Bot. Only Codex (and Claude Code, if used) has Entire hooks; Grok
Build and Grok Bot sessions are not captured by Entire.

## Activate on GT's MSI (GT does these steps)

Entire 0.10.5 is installed with Scoop at
`C:\Users\GT\scoop\apps\entire\current\entire.exe`.

```powershell
# 1. The Civio clone on the MSI is C:\Users\GT\Desktop\Claude\Civio
cd C:\Users\GT\Desktop\Claude\Civio
git pull --ff-only origin main
#    (first time only: git clone https://github.com/Vincenzo-OPC/Civio.git C:\Users\GT\Desktop\Claude\Civio)

# 2. Use the committed git hooks (local git config, once per clone)
git config core.hooksPath .githooks

# 3. Check Entire sees the repo
entire status        # expect: Enabled, checkpoints sync to origin
```

4. Open the Civio folder in **Codex** and **approve the project hooks** when the
   Codex UI asks. Codex does not run project hooks until they are trusted.

Then work through Codex (or Claude Code), commit, and push as usual. Check:

```powershell
git log -1 --format=%B                 # the commit ends with an Entire-Checkpoint: trailer
entire checkpoint list                 # the checkpoint is listed
git ls-remote origin "refs/entire/*"   # after git push: the checkpoint refs are on GitHub
```

Notes:

- Do **not** run `entire enable` again in this clone. It rewrites the committed
  hooks with machine-specific paths. If it happens, restore them with
  `git checkout -- .githooks .codex .claude .entire`.
- Known CLI bug: `entire doctor` shows **REVIEW NEEDED** for the Codex hooks
  (entireio/cli#1803, Codex hook-trust detection). Ignore it. Do **not** run
  `entire doctor --force`.
- Optional web view: `entire login` opens a browser. On a machine without a
  browser it switches to a device code by itself (`entire login --device` forces
  it); without an OS keyring use `ENTIRE_TOKEN_STORE=file entire login`. Not
  needed for checkpoints.
- Optional upgrade: `scoop update entire` (the box runs 0.11.4).

## Box status (7 Oct 2026, Asia/Manila)

- Official CLI 0.11.4 at `~/.local/bin/entire` (release archive from
  `github.com/entireio/cli`, checksum verified), replacing the old npm wrapper.
- The box clone does not set `core.hooksPath`: the box agent is not a supported
  Entire agent, so there is nothing to capture there.
- Recorded so far: nothing (no sessions, no `refs/entire/*` on `origin`). Capture
  starts once the MSI steps above are done and Codex or Claude Code commits.

## Related

- `docs/CHANGES_SINCE_BASELINE.md`: every difference from the baseline (`d3f0368`).
- `CHANGELOG.md`: generated with `npm run changelog` (git-cliff).
