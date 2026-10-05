# What "Entire" actually is (read this before asking again)

If you are an AI session reading this because you searched for "Entire" in enabled
plugins, skills, or MCP servers and found nothing: that is correct and expected.
**Entire is not a Claude plugin, skill, or MCP server.** It will never show up in
any of those lists, in any session, on any surface.

## What it actually is

Entire (entire.io / `entireio/cli`) is a standalone command-line program that:

1. Installs hook files for AI coding tools (`.cursor/hooks.json` for Cursor,
   Codex / Claude Code hooks when those agents are enabled).
2. Installs git hooks that capture AI session transcripts as checkpoints under
   `refs/entire/checkpoints/...` (git-refs strategy).
3. Stays outside Claude's plugin / skill / MCP system.

## What it's for

Reviewability of AI-written code: later you can inspect which prompts produced
which diffs. It does **not** sync WSL, cloud sandboxes, and Codex trees.

## This repo

- Source of truth: `.entire/settings.json` (`enabled: true`, `telemetry: false`,
  `checkpoints.primary.type: "git-refs"`).
- Local-only (gitignored): `metadata/`, `logs/`, `tmp/`, `settings.local.json`.
- On a new clone (especially GT's MSI), run: `entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path`
- Install: `curl -fsSL https://entire.io/install.sh | bash` (Linux/macOS) or
  `irm https://entire.io/install.ps1 | iex` (Windows / Scoop).

Do not commit secrets into checkpoints. Redaction is best-effort.
