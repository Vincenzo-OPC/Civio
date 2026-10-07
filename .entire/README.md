# What "Entire" is (read this before searching for it)

If you are an AI session that looked for "Entire" among plugins, skills or MCP
servers and found nothing: that is expected. **Entire is not a plugin, skill or
MCP server**, and it never shows up in those lists.

Entire ([entire.io](https://entire.io), `entireio/cli`) is a **standalone CLI**.
It records which agent prompts and transcripts led to which commits:

1. **Agent hooks** call `entire hooks <agent> <event>` while an agent works.
   In Civio these are committed for **Codex** (`.codex/hooks.json`) and
   **Claude Code** (`.claude/settings.json`). Every hook exits quietly when the
   `entire` binary is not installed.
2. **Git hooks** (`.githooks/`, enabled per clone with
   `git config core.hooksPath .githooks`) add the `Entire-Checkpoint` trailer on
   commit and push checkpoints on `git push`.
3. **Checkpoints** are stored as git refs (`refs/entire/checkpoints/...`, the
   `git-refs` strategy), pushed to `origin` next to your normal push. No cloud
   login is needed for this; `entire login` only adds the entire.io web view.

## Files

| File                                 | Committed | Purpose                                                                                  |
| ------------------------------------ | --------- | ---------------------------------------------------------------------------------------- |
| `.entire/settings.json`              | yes       | enabled, telemetry off, git-refs checkpoints, secret redaction patterns                  |
| `.entire/.gitignore`                 | yes       | keeps `tmp/`, `settings.local.json`, `metadata/`, `logs/`, `redactors/local/` out of git |
| `.codex/hooks.json`                  | yes       | 7 Codex hooks (Windows `cmd.exe` wrappers)                                               |
| `.claude/settings.json`              | yes       | Claude Code hooks (`sh -c` wrappers) + deny reading `.entire/metadata/**`                |
| `.githooks/*`                        | yes       | commit-msg, prepare-commit-msg, post-commit, post-rewrite, pre-push                      |
| `.entire/metadata/`, `logs/`, `tmp/` | **never** | local session data                                                                       |

Setup and activation steps: see `ENTIRE.md` in the repo root.

Redaction is best-effort. Do not paste secrets into agent sessions.
