# Civio Codex takeover checkpoint — 2026-10-23 (Asia/Manila)

**Purpose:** Compact, current handoff after Grok Bot reached its usage cap. This is a **task entrypoint**, not a replacement for `AGENTS.md` or permission to activate anything. Always revalidate `git rev-parse HEAD`, GitHub CI, and live code first. At creation, verified `main` is `ecb1e477b7763a3a6712df1a372edd50d2a50808`; Actions **e2e / tests / linter** green.

## Instruction precedence and context hygiene

1. Current owner task and safety boundaries; live code/tests/GitHub CI.
2. `AGENTS.md` non-negotiable product/safety/test rules, plus `CLAUDE.md` where applicable.
3. The specific open GitHub issue being implemented; `docs/PERFORMANCE_REPORT.md` for current low-end evidence.
4. Historical plans/handoffs (`docs/CODEX_HANDOFF_PLAN.md`, `docs/CIVIO_CODEX_BUILD_BRIEF.md`, `docs/ASTRA_PENDING_HANDOFF.md`, `docs/DEXTER_CODEX_PROMPT_CURRENT.md`, etc.) **only if relevant**, and never over present instructions.

**Important:** `docs/CIVIO_CODEX_BUILD_BRIEF.md` still says to replace GitHub main with a desktop MSI baseline: this is **obsolete**. Do not replace main, restore an old tree, reset history, or operate on MSI. Historical documents have several mutually superseding "read first" instructions; do not recursively ingest them all at session start. Read the smallest applicable sections.

## What has shipped

- `8316646` and `c6c7b5b`: Strict Mock answer-recovery regression tests; only GET/HEAD globally retried; writes never blindly replayed.
- `1b58f7a`: guest free-attempt URL bypass closed; safe production defaults.
- `052438a` and `8fa533a`: responsive flat dashboard and independent visual QA.
- `2dfcff6`: guarded guest abandoned-session cleanup (default 45 days); signed-in exposure-history sessions retained.
- `097d093`: `civio:launch-check` and Turnstile/proxy configuration groundwork.
- `a34d783`, `ab4bc2f`, `f2018ce`, `ffb2c5c`, `ecb1e477`: Issue #27 low-end performance fixes, test harness, and measured report. CDN/server environment not deployed.

## Current task order (do not parallelize overlapping writes)

**P0 — GitHub Issue #28: reproducible JS-chunk/download failure affecting Strict Mock sync.** `docs/PERFORMANCE_REPORT.md` reports a dropped `import('../utils/progress-save')` about 1s after Begin leaves subsequent imports rejecting even after reconnect. In one isolated test, **0/6 answers reached the server after 60s**, but **localStorage retained them and reload recovered**. This is not proven irreversible answer loss. A naive re-import retry failed and was reverted. Verify with Playwright network interception and implement a safe UI/readiness and recovery path. Do not accept answers without a durable local write path; preserve server deadlines and pending merge. Never retry non-idempotent writes globally. Keep Strict scenarios 1a/1b, data security, and local-storage failure handling.

**P1 — GitHub Issue #27: measured old-device/low-data and cost work.** Baseline after optimizations: cold exam **401 KB**, 400 kbps/4x first question **11.9 s**, 250 kbps/4x **17.5 s**, 150-answer mock increment **245.3 KB**; these are Chromium emulation, not physical-device or deployed CDN numbers. Warm visits are fast. Large first-load shared JS (~330 KB gzip) remains bottleneck. Local `npm run test:perf-budget` exists but **is not in Actions** due to the previous token lacking `workflow` permission. Inspect permissions and wire CI if authorized; do not falsely claim it already runs. Never meet speed goals by losing answer safety, breaking offline/Lite or hiding real work. Keep size budgets.

**P2 — Dexter only after P0/P1:** #22 approved metadata audit, #20 honest mastery calibration; #21 representative Strict integrity; #23 Rescue requires approvals. No bank approval/import, no AI activation, no false pass forecast.

## Locked boundaries

No deployment/hosting changes, billing/paid APIs, real learner data, protected MSI app/database, Hermes, signed bank changes, keys in build output, question-answer leakage or destructive actions. Owner-funded AI inference spend remains **₱0** and production AI kill switch closed. Lite/old-phone support and Subprofessional study quality matter. Keep `main` history; no reset/force-push. Isolated SQLite/E2E only.

## Working cadence and durable state

- First inspect `git status --short`, `git branch --show-current`, `git rev-parse HEAD` and remote; preserve any existing user changes. Verify issue states and Actions. Follow local repo rules.
- Implement **one scoped slice**, run focused test, then PHP/JS, types, lint, formatting, build, `npm run size`, Strict E2E, and `npm run test:perf-budget` as applicable. CI green before marking completed.
- Commit small meaningful changes with `[skip netlify]`; update `docs/CHANGES_SINCE_BASELINE.md` for behavior changes. Push normally only when permitted and green, never force.
- End each independent slice with brief durable notes: SHA, tests and actual results, unresolved issue, exact next action. Use a fresh Codex session per issue/major slice rather than carrying megabytes of logs or old chat history forward.
