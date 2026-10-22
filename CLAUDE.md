# Claude instructions for Civio

> **22 Oct 2026 GT VISUAL DIRECTIVE (dashboard):** Read [`docs/design/CIVIO_DASHBOARD_VISUAL_CONTRACT_2026-10-22.md`](docs/design/CIVIO_DASHBOARD_VISUAL_CONTRACT_2026-10-22.md) before any learner-dashboard UI work. Owner preferences: Title Case on headings/labels/actions, limited intentional ALL CAPS for short editorial tags, deliberate optical typography, flat surfaces **without decorative gradients/glass/glow**, equal-row card geometry, mobile-first legibility, actual screenshot measurements. Compare PRO2000, Grip-PH, Undercor; chief-of-staff delegation and independent QA. This specific owner instruction supersedes older generic typography advice. No deployment, MSI mutation, paid AI, bank changes or Rescue activation.

> **Future AI research:** Also read [`docs/AI_SELF_IMPROVEMENT.md`](docs/AI_SELF_IMPROVEMENT.md) when proposing agent/tutor optimization. Civio is an opt-in held-out evaluation target of THE-MACHINE, not a separate self-editing agent. Do not begin autonomous mutation loops or change grading, question-bank or deployment approvals.

> Substantive entry for Claude (Claude Code CLI, Claude.ai projects, Claude Cowork).
> Pair with `AGENTS.md`. Claude Code often loads this file and skips `AGENTS.md` —
> keep the locked rules duplicated here.

## Provenance

Civio builds on the baseline codebase at `d3f0368` (CSE mocks, drills, and a stored-key check named Dexter).
Work continues across Codex, Grok Build, Grok Bot, Claude and human contributors.
GitHub `Vincenzo-OPC/Civio` is the durable record — not any one chat history.

## Read order before acting

Pending Astra handoff (17 Oct 2026): read `docs/ASTRA_PENDING_HANDOFF.md` first (security and exam-integrity fixes, then learning features).

0. `docs/CODEX_HANDOFF_PLAN.md` — start here: record by phase, invariants, gaps, next phases.
1. `AGENTS.md` — product locks, MSI Docker protection, branch/push rules, phase status.
2. This file.
3. `docs/CIVIO_CODEX_BUILD_BRIEF.md` — phased execution order.
4. `docs/ARCHITECTURE.md`, `docs/DEPLOY.md`, `docs/DESKTOP_PATCHES_TO_PORT.md`,
   `docs/CHANGES_SINCE_BASELINE.md` (what differs from the baseline), `CHANGELOG.md`.
5. `docs/CSE-Question-Design-Spec.md` before any bank content work.
6. Obsidian Intersect vault for GT durable notes (`Projects\CIVIO\...`).

When documents conflict: live code/tests → build brief → AGENTS.md → historical docs.

## What Civio is

Philippine Civil Service Exam study app. Brand **Civio** (Title Case). Dexter
is a stored-key check, not a chat tutor. **Not** official CSC. Lowercase `civio` only in identifiers/URLs/env.

## Non-negotiable

- Never force-push `main`. Never touch Hermes `:8642` or the MSI Docker study
  containers (app `:8090`, Postgres `:5434`).
- Never expose API keys client-side (`VITE_*` secrets forbidden).
- Never add bank questions without an approved design-spec pass.
- Server grades exam attempts; do not trust client `cat_scores`.
- Do not ship `correct_option` / `explanation` in live exam JSON before submit.
- Offline drill packs carry keys, so they only contain `offline_eligible` items, which
  strict mocks never use. The sync endpoint re-grades with server keys.
- No secrets in commits.
- Behaviour change vs the baseline → update `docs/CHANGES_SINCE_BASELINE.md` in the same commit.

## Stack one-liner

Laravel 13 + Inertia/React 19 + Postgres/SQLite + optional server AI (Dexter stub default).

## Verify before claiming done

`vendor/bin/pint --test`, `npm run types:check`, `npm run lint:check`, `npm run build`,
`php artisan test`.

## Current execution boundary - 20 October 2026

Civio study services are civio-local-app / civio-local-db at 8090/5434. The separate protected application is 8080/5433; Hermes is 8642. Do not operate or query any of these services for development. Use isolated test infrastructure. GT authorizes normal verified pushes to main; pull --rebase first, never force-push or bypass hooks, stop on rejection. Every new commit includes [skip netlify]. Hosting remains undecided; no deployment or spending is authorized.
