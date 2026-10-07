# Civio repository rules

Codex, Grok Build and Grok Bot read this file. Claude Code reads `CLAUDE.md`
and often skips this one. Keep both aligned. Cursor is not used for Civio: there
is no `.cursor/` folder (hooks or rules); do not add one.

## Read first, every session

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

**Civio** (Title Case) is a Philippine Civil Service Exam study app. Tutor name:
**Dexter**. It is **not** official CSC software and must never claim affiliation.

- Lowercase `civio` / `civio.ph` only in identifiers, URLs, package names, env prefixes.
- Avoid all-caps **CIVIO** in UI, metadata, README, and docs.
- The product is Civio everywhere: no other app names in code, UI, docs or seeds.

## Stack

- Backend: PHP 8.4, Laravel 13, Inertia v3, Fortify, Socialite, Wayfinder, Pest 4, Pint
- Frontend: React 19, TypeScript, Vite, Tailwind 4, shadcn/Radix
- DB: Postgres preferred (Neon in deploy plan); SQLite in-memory for tests
- AI: optional server-side providers (stub default). **Never** put provider keys in `VITE_*`
- Docker: `Dockerfile` + `docker-compose.yml` (app `:8080`, Postgres `:5433`)

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

- Never touch GT's MSI Docker study containers (app `:8080`, Postgres `:5433`; names
  in `docs/DESKTOP_PATCHES_TO_PORT.md`).
- Never touch Hermes on port **8642**.
- Local MSI study app on `localhost:8080` stays the stable study surface.
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

## Question bank rule

**Do not add question items to any bank** unless GT has approved the design against
`docs/CSE-Question-Design-Spec.md` (Intersect canonical copy). Seed/move scripts may
exist for existing content; do not invent new stems.

**No filler clones.** Never pad the bank or a mock with "(variant N)" copies or
other repeats. Mocks draw unique items only (`resources/js/pages/user/exams/utils/mock-pool.ts`);
if the bank is short, the mock is shorter and the user is told the real count.
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
- **Done:** Lite L0 (items 1–5; item 6 nginx cache config pending) and Lite L1:
  server-picked mocks (`POST /exams/sessions`, `MockPoolSelector`,
  `exam_sessions`), Lite mode flag (`lib/lite-mode.ts`, `useLiteMode()`,
  `civio_lite` cookie), text-first exam/drill screens, server-side prop
  trimming. See `docs/LITE_MODE_PLAN.md`.
- **Next:** Lite L2 (offline drill packs, needs GT decisions) → Phase 1
  foundation → Phase Bank.

## Hosting intent (not yet executed)

Google Cloud Run (scale to zero, instance cap, budget alert) + Neon free Postgres +
Cloudflare (DNS/CDN, Turnstile, analytics). See `docs/DEPLOY.md`.

## Agent tooling

- Entire CLI: see `ENTIRE.md` and `.entire/README.md`. Codex + Claude Code hooks and `.githooks/` are committed; capture starts after the one-time MSI steps in `ENTIRE.md` (`git config core.hooksPath .githooks`, approve Codex hooks).
- Changelog: `npm run changelog` (git-cliff). Baseline diff: `docs/CHANGES_SINCE_BASELINE.md`.
- Lite mode plan for cheap phones / slow data: `docs/LITE_MODE_PLAN.md`.
- Laravel Boost guidelines remain in `GEMINI.md` for framework conventions.

## Libraries (Phase 0 extras)

See `docs/LIBRARIES.md` for researched options and verdicts.

Adopted now:

- **vite-plugin-pwa** — generated SW (`resources/js/sw.ts`), NetworkOnly for `/exams`, prompt update
- **ts-fsrs** — `resources/js/lib/review/fsrs.ts` (scheduler only; UI later); `npm run test:js`
- **prism-php/prism** — installed; `App\Ai\Contracts\TutorProvider` + `NullTutorProvider` default
- **sentry/sentry-laravel** — no-op unless `SENTRY_LARAVEL_DSN` is set

Never put provider keys in `VITE_*`.
