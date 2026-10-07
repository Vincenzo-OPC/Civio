# Claude instructions for Civio

> Substantive entry for Claude (Claude Code CLI, Claude.ai projects, Claude Cowork).
> Pair with `AGENTS.md`. Claude Code often loads this file and skips `AGENTS.md` —
> keep the locked rules duplicated here.

## Provenance

Civio builds on the baseline codebase at `d3f0368` (CSE mocks, drills, Dexter tutor).
Work continues across Codex, Grok Build, Grok Bot, Claude and human contributors.
GitHub `Vincenzo-OPC/Civio` is the durable record — not any one chat history.

## Read order before acting

1. `AGENTS.md` — product locks, MSI Docker protection, branch/push rules, phase status.
2. This file.
3. `docs/CIVIO_CODEX_BUILD_BRIEF.md` — phased execution order.
4. `docs/ARCHITECTURE.md`, `docs/DEPLOY.md`, `docs/DESKTOP_PATCHES_TO_PORT.md`,
   `docs/CHANGES_SINCE_BASELINE.md` (what differs from the baseline), `CHANGELOG.md`.
5. `docs/CSE-Question-Design-Spec.md` before any bank content work.
6. Obsidian Intersect vault for GT durable notes (`Projects\CIVIO\...`).

When documents conflict: live code/tests → build brief → AGENTS.md → historical docs.

## What Civio is

Philippine Civil Service Exam study app. Brand **Civio** (Title Case). Tutor
**Dexter**. **Not** official CSC. Lowercase `civio` only in identifiers/URLs/env.

## Non-negotiable

- Never force-push `main`. Never touch Hermes `:8642` or the MSI Docker study
  containers (app `:8080`, Postgres `:5433`).
- Never expose API keys client-side (`VITE_*` secrets forbidden).
- Never add bank questions without an approved design-spec pass.
- Server grades exam attempts; do not trust client `cat_scores`.
- Do not ship `correct_option` / `explanation` in live exam JSON before submit.
- No secrets in commits.
- Behaviour change vs the baseline → update `docs/CHANGES_SINCE_BASELINE.md` in the same commit.

## Stack one-liner

Laravel 13 + Inertia/React 19 + Postgres/SQLite + optional server AI (Dexter stub default).

## Verify before claiming done

`vendor/bin/pint --test`, `npm run types:check`, `npm run lint:check`, `npm run build`,
`php artisan test`.
