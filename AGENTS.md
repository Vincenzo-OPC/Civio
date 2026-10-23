# Civio repository rules

> **22 Oct 2026 GT VISUAL DIRECTIVE (dashboard):** Read [`docs/design/CIVIO_DASHBOARD_VISUAL_CONTRACT_2026-10-22.md`](docs/design/CIVIO_DASHBOARD_VISUAL_CONTRACT_2026-10-22.md) before any learner-dashboard UI work. Owner preferences: Title Case on headings/labels/actions, limited intentional ALL CAPS for short editorial tags, deliberate optical typography, flat surfaces **without decorative gradients/glass/glow**, equal-row card geometry, mobile-first legibility, actual screenshot measurements. Compare PRO2000, Grip-PH, Undercor; chief-of-staff delegation and independent QA. This specific owner instruction supersedes older generic typography advice. No deployment, MSI mutation, paid AI, bank changes or Rescue activation.

> **22 Oct 2026 GT roadmap: deterministic Dexter 2.0.** Read [open-source-informed scoped implementation plan](docs/DEXTER_OPEN_SOURCE_IMPLEMENTATION_PLAN_2026-10-22.md) and [tracking Epic #19](https://github.com/Vincenzo-OPC/Civio/issues/19); dependent gates [BKT evidence #20](https://github.com/Vincenzo-OPC/Civio/issues/20), [Strict selection #21](https://github.com/Vincenzo-OPC/Civio/issues/21), [approved metadata #22](https://github.com/Vincenzo-OPC/Civio/issues/22), [Rescue pilot #23](https://github.com/Vincenzo-OPC/Civio/issues/23). This is a **plan awaiting Astra ADR and GT approvals**, not permission to code every gate, alter bank, deploy or activate paid inference. Keep `docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md` as the canonical order, code/tests as truth, and currently implemented FSRS/Review Mistakes/Today's Focus intact. **No new modes, flashcards, generation services or heavyweight UI libraries.**


> **22 Oct 2026 OWNER-SPEND STOP RULE (GT directive):** Read [Dexter zero-owner-cost activation gate](docs/DEXTER_ZERO_COST_ACTIVATION_GATE_2026-10-22.md). A free Civio user may issue thousands of model calls; even fractions of a cent per call accumulate into **GT's bill**, which is unacceptable. **Maximum approved GT-funded AI inference spend: ₱0.** No owner-funded API calls, paid overages, shared production inference key, paid automatic failover, public free-tier proxy or activation of an in-app LLM. Continue improving disabled Dexter logic, safe deterministic MCQ teaching and optional external user-account handoff, without paid calls. A nominal per-request cost is NOT acceptable. Only GT may explicitly approve a legally compliant user-funded or truly zero-GT-exposure production path after evidence. Do not confuse a user logging in with granting model tokens.

> **Issue #18 status (22 Oct 2026): DONE on main (dfa8fd7, a44bc0e + follow-up).** All owner-key AI goes through `App\Services\Ai\OwnerAiSpendLock`. It is closed by default and opens only when `CIVIO_OWNER_FUNDED_AI` is exactly `true`, and never in production; credentials alone do nothing. The only path to an AI host is `AiGatewayService`, which checks the lock first in every network method. The architecture test `tests/Unit/Architecture/AiEgressTest.php` fails if app code names an AI host or uses an HTTP client elsewhere (Turnstile is the only allowed non-AI exception) or reads AI keys with `env()`. **New AI code must go through the gateway and keep these tests green. Do not open the lock without GT's explicit approval.**

> **22 Oct 2026 GT scope correction: ADAPTIVE MCQs ONLY.** Read [StudyStash competitive analysis and MCQ-first brief](docs/research/STUDYSTASH_MCQ_ADAPTIVE_LEARNING_REVIEW_2026-10-22.md) with the current Dexter plan and Issue #17. Keep Civio's teaching, adaptive selection, explanations, fresh transfer and spaced review **inside multiple-choice questions**. Do not add flashcards, matching, podcasts, drag/drop exam formats or mini-games. This is a product-research handoff for Grok Bot (independent scout), Astra (architecture) and Codex (later code), not a background start signal. Preserve all existing bank, security, no-cost, no-deploy and Lite gates.


> **COPY/PASTE HANDOFF SOURCE OF TRUTH:** [docs/DEXTER_CODEX_PROMPT_CURRENT.md](docs/DEXTER_CODEX_PROMPT_CURRENT.md). This supersedes previous prompts. Codex must consult it at session startup along with the master Dexter plan and Astra-reviewed pacing/evals brief. Keep the user's older instructions and the current security roadmap intact.


## Current GT directive: Dexter adaptive tutor and 100%-practice roadmap (21 Oct 2026)

## Latest addition: Astra-reviewed pacing and AI evaluations (21 Oct 2026)

Mandatory read: [docs/DEXTER_TIMING_AND_EVALS_2026-10-21.md](docs/DEXTER_TIMING_AND_EVALS_2026-10-21.md). GT proposes an optional pacing bar, tracked timing improvement on independent fresh questions, and a rigorous educational AI evaluation harness with human calibration. Astra decides architecture after research, not by blindly implementing this spec. Do not conflate speed with mastery; 10s and 60s are illustrative, not CSC official. Preserve current security-first gates, Lite performance, no spend, no deployment. **Previous Codex paste prompt is superseded by the integrated new prompt in this brief and Issue #17.**



**Codex must read [docs/DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md](docs/DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md) and its three linked specialist documents at startup.** This records GT's goal of near-perfect independent CSE practice (Subprofessional first, with math and spelling as priority), a real memory-driven tutor, safer Ask ChatGPT scaffolding, and **zero surprise AI costs**. Execute in small verified slices only **after** completing/confirming the existing security and bank-import gates. No paid API connection, customer billing, hosted SIWC flow, deployment, question-bank approval/import or protected live-study DB mutation is authorized by this note. See the current next-agent plan for ordering. Keep existing rules below.


## Future self-improvement experiments (2026-10-08)

When working on agent-assisted coding quality or Dexter tutor experimentation, read [`docs/AI_SELF_IMPROVEMENT.md`](docs/AI_SELF_IMPROVEMENT.md). Civio is an opt-in **evaluation target**, not an independent RSI engine. THE-MACHINE owns agent/meta-agent evolution; keep grading, questions, answer keys, Lite/offline safeguards and held-out evaluations independent. First deliver the current product roadmap; do not launch autonomous mutations or deployments based on this note. Claude agents must read the matching note in `CLAUDE.md`.


> **Pending Astra handoff: read [`docs/ASTRA_PENDING_HANDOFF.md`](docs/ASTRA_PENDING_HANDOFF.md) first** (17 Oct 2026: security and exam-integrity fixes first, then learning features; research context, not a spec).
>
> **Codex: read [`docs/CODEX_HANDOFF_PLAN.md`](docs/CODEX_HANDOFF_PLAN.md) first.**
> It has the full record, the security invariants, open decisions and the ranked
> next phases.

Codex, Grok Build and Grok Bot read this file. Claude Code reads `CLAUDE.md`
and often skips this one. Keep both aligned. Cursor is not used for Civio: there
is no `.cursor/` folder (hooks or rules); do not add one.

## Read first, every Session 0. `docs/CODEX_HANDOFF_PLAN.md` — start here: record, invariants, gaps, next phases.
0a. `docs/HANDOFF_ANY_AI.md` — how ChatGPT or any AI takes over every Grok Bot job (audits, question pipeline, Sentinel).
1. This file (`AGENTS.md`) — locked product and workflow rules.
2. `docs/CIVIO_CODEX_BUILD_BRIEF.md` — phased build plan (Gate 0 → Phase 0 → 0.5 → 1 → Bank).
3. `docs/ARCHITECTURE.md` — system shape (create/update if missing; do not invent hosting).
4. `docs/DESKTOP_PATCHES_TO_PORT.md` — MSI UX patches still to port.
4a. `docs/CHANGES_SINCE_BASELINE.md` — every difference from the baseline (`d3f0368`), with commits.
4b. `CHANGELOG.md` — release notes generated from commits (`npm run changelog`).
5. `docs/CODE_STANDARD.md` — coding standard and the modernization backlog.
6. Durable notes: Obsidian Intersect vault (GT). Question design spec also lives at
   `Projects\CIVIO\CSE-Question-Design-Spec.md` in Intersect; a copy is in
   `docs/CSE-Question-Design-Spec.md`.

Do not treat old chat handoffs as operating instructions.

## What Civio is

**Civio** (Title Case) is a Philippine Civil Service Exam study app.
Dexter is a stored-key check, not a chat tutor. It is **not** official CSC software and must never claim affiliation.

- Lowercase `civio` / `civio.ph` only in identifiers, URLs, package names, env prefixes.
- Avoid all-caps **CIVIO** in UI, metadata, README, and docs.
- The product is Civio everywhere: no other app names in code, UI, docs or seeds.

## Stack

- Backend: PHP 8.4, Laravel 13, Inertia v3, Fortify, Socialite, Wayfinder, Pest 4, Pint
- Frontend: React 19, TypeScript, Vite, Tailwind 4, shadcn/Radix
- DB: Postgres preferred (hosting provider undecided); SQLite in-memory for tests
- AI: optional server-side providers (stub default). **Never** put provider keys in `VITE_*`
- Current MSI Civio: app 8090 / PostgreSQL 5434 (civio-local-app / civio-local-db), configured by docker-compose.local.yml. No study-service operations or database access during development. The older protected application uses 8080/5433; Hermes uses 8642.

## How to run / test / lint / build

```bash
composer install
npm ci
cp .env.example .env && php artisan key:generate
# sqlite or pgsql per .env
php artisan migrate
npm run build          # or npm run dev
php artisan test       # Pest, sqlite memory via phpunit.xml
npm run types:check    # tsc --noEmit
npm run lint:check     # eslint
npm run format:check   # prettier
npm run test:js        # tsx --test tests/Js/*.test.ts
vendor/bin/pint --test
```

Before each push: types, lint, build, and `php artisan test` must be green.
Formatting fixes go in a **separate commit** from functional changes.

## Docker / MSI protection (non-negotiable)

- Never touch GT's MSI Docker study containers (app `:8090`, Postgres `:5434`; names
  in `docs/DESKTOP_PATCHES_TO_PORT.md`).
- Never touch Hermes on port **8642**.
- Local MSI study app on `localhost:8090` stays the stable study surface.
- Do not break guest unlimited study (`CIVIO_GUEST_UNLIMITED`) without GT approval.

## Branch and commit rules

- Work on **`main`**. Normal `git push origin main` only.
- **Never force-push.** If rejected, stop and report.
- Small logical commits (one concern each). Suggested Phase 0 sequence is in the build brief.
- Push periodically after green checkpoints, not every commit.
- No secrets in commits. Spot-check built assets for leaked keys.
- Conventional Commits (`feat`, `fix`, `perf`, `refactor`, `test`, `docs`, `style`,
  `chore`, `security`, optional scope). `CHANGELOG.md` is generated from them with
  git-cliff (`cliff.toml`); do not hand-edit it.
- **Baseline diff rule:** every commit or PR that changes behaviour compared with the
  baseline (`d3f0368`, tag `baseline`) must update
  `docs/CHANGES_SINCE_BASELINE.md` in the same change.
- Release tags are annotated, pushed with `git push origin <tag>` (never forced).
  Never push to the local read-only `upstream-baseline` remote.
- Bundle budgets: `npm run build && npm run size` (size-limit, brotli). Raise a
  budget only on purpose, and say why in the commit.
- **Low-end and cost review (Issue #27).** Before merging anything user-facing,
  ask: does it add bytes before the first question (budget in
  `tests/Perf/budget.spec.ts`, run by `npm run test:perf-budget`),
  per-answer bytes during a mock (target: full mock under 250 KB), DB queries
  per request (`tests/Feature/Performance/QueryBudgetTest.php`), or a paid
  service / Redis? Does it still work with no animation, no hover, Lite Mode
  and offline? See `docs/PERFORMANCE_REPORT.md`.

## Question bank rule

**Do not add question items to any bank** unless GT has approved the design against
`docs/CSE-Question-Design-Spec.md` (Intersect canonical copy). Seed/move scripts may
exist for existing content; do not invent new stems.

**No filler clones.** Never pad the bank or a mock with "(variant N)" copies or
other repeats. Mocks draw unique items only (`resources/js/pages/user/exams/utils/mock-pool.ts`);
if the bank is short, the mock is shorter and the user is told the real count.
Full mocks (Exam Simulation: Study Mock or Strict Mock, `ExamMode`) are picked on the server (`app/Services/Exam/MockPoolSelector.php`) and
never include `offline_eligible` items or exact copies of them: those keys ship in
offline drill packs. Only `php artisan civio:mark-offline-eligible` marks items;
never mark by hand without re-checking that full 150/145 mocks still fill.
Old clones are removed with `php artisan civio:remove-variant-clones [--dry-run]`
(deletes unreferenced clones, sets referenced ones to `draft`). The MSI desktop DB
still needs this run once: see `docs/DESKTOP_PATCHES_TO_PORT.md` for the command and
the equivalent Postgres SQL (`scripts/seeds/remove_variant_clones.sql`).

## Current phase status (update as you finish)

- **Done:** Gate 0 — `main` tip is desktop baseline `d3f0368`.
- **Done:** Phase 0 — security scoring, withhold keys, shuffle fix, remove
  dangerous routes, draft custom questions, nullOnDelete, remove ads, CI green,
  code-split, Civio rebrand, repo junk cleanup, docs, agent setup (Entire + AGENTS).
- **Done:** Phase 0.5 — MSI UX ported: exam/item clocks with urgency colours,
  tutor loop + weak-topic study bias (server-graded), no redundant Mock button,
  `??` math-symbol root cause fixed (`php artisan civio:repair-bank-encoding`).
  See `docs/DESKTOP_PATCHES_TO_PORT.md`.
- **Done:** "(variant N)" clones removed: seeder makes one copy per item, mocks
  use unique items only (no variant fill), `civio:remove-variant-clones` cleans
  existing rows. MSI DB cleanup still pending (desktop patches doc).
- **Done:** Copy for AI MVP (`docs/EXTERNAL_AI_HANDOFF.md`).
- **Done:** Lite L0 (items 1–5; Item 6 nginx cache config pending) and Lite L1:
  server-picked mocks (`POST /exams/sessions`, `MockPoolSelector`,
  `exam_sessions`), Lite mode flag (`lib/lite-mode.ts`, `useLiteMode()`,
  `civio_lite` cookie), text-first exam/drill screens, server-side prop
  trimming. See `docs/LITE_MODE_PLAN.md`.
- **Done:** Lite L2, offline drill packs: `questions.offline_eligible`,
  `civio:mark-offline-eligible`, `/offline/packs` + `/offline/attempts`
  (server re-grade, `offline_practice_results`), drills hub download panel,
  `/offline` runner, worker served at `/sw.js`. See `docs/LITE_MODE_PLAN.md`.
- **Next:** Learning Features (next), see `docs/CODEX_HANDOFF_PLAN.md` §0; then modernization backlog (`docs/CODE_STANDARD.md`) → Phase 1
  foundation → Phase Bank.

## Hosting intent (undecided)

Hosting is pending GT's selection. Cloud Run and Koyeb/Neon/Netlify are historical proposals, not an approved target. No deployment, paid service, billing activation or Netlify credits are authorized. Keep existing Netlify build-skip settings. Every new commit must include [skip netlify].

## Agent tooling

- Entire CLI: see `ENTIRE.md` and `.entire/README.md`. Codex + Claude Code hooks and `.githooks/` are committed; capture starts after the one-time MSI steps in `ENTIRE.md` (`git config core.hooksPath .githooks`, approve Codex hooks).
- Changelog: `npm run changelog` (git-cliff). Baseline diff: `docs/CHANGES_SINCE_BASELINE.md`.
- Lite mode plan for cheap phones / slow data: `docs/LITE_MODE_PLAN.md`.
- Laravel Boost guidelines remain in `GEMINI.md` for framework conventions.

## Libraries (Phase 0 extras)

See `docs/LIBRARIES.md` for researched options and verdicts.

Adopted now:

- **vite-plugin-pwa** — generated SW (`resources/js/sw.ts`), NetworkOnly for `/exams`, prompt update
- **ts-fsrs** — server scheduling via `scripts/fsrs-apply.mjs` and `App\Services\Exam\FsrsScheduler` (policy `civio-fsrs-policy-1`). The browser wrapper `resources/js/lib/review/fsrs.ts` stays for unit tests. Online only.
- **prism-php/prism** — installed; `App\Ai\Contracts\TutorProvider` + `NullTutorProvider` default
- **sentry/sentry-laravel** — no-op unless `SENTRY_LARAVEL_DSN` is set

Never put provider keys in `VITE_*`.

## Bank state 2026-10-22 (exact-flat)

Unique stems on official scope: **2,100** after residual drafts + trim lists.  
Every domain on clean hundred target (Numerical 400, Analytical 400, Verbal EN 400, Verbal Fil 300, Clerical 300, GI 300).  
122 new drafts in `docs/research/civio-exact-flat-cleaned-2026-10-22.json`. All `status: draft`.  
See `docs/research/AUDIT_TRACKER.md` (2026-10-22 section) and `docs/research/civio-exact-flat-review-request-2026-10-22.md`.  
Do not activate. Independent review + GT Ed25519 approval required.
