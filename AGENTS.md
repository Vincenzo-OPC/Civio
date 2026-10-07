# Civio repository rules

Codex, Copilot, Cursor, and Grok CLI read this file. Claude Code reads `CLAUDE.md`
and often skips this one. Keep both aligned.

## Read first, every session

1. This file (`AGENTS.md`) — locked product and workflow rules.
2. `docs/CIVIO_CODEX_BUILD_BRIEF.md` — phased build plan (Gate 0 → Phase 0 → 0.5 → 1 → Bank).
3. `docs/ARCHITECTURE.md` — system shape (create/update if missing; do not invent hosting).
4. `docs/DESKTOP_PATCHES_TO_PORT.md` — MSI UX patches still to port.
5. `docs/CIVIO_AUDIT_AND_PLAN.md` — audit map (paths may have shifted; re-verify in tree).
6. Durable notes: Obsidian Intersect vault (GT). Question design spec also lives at
   `Projects\CIVIO\CSE-Question-Design-Spec.md` in Intersect; a copy is in
   `docs/CSE-Question-Design-Spec.md`.

Do not treat old chat handoffs as operating instructions.

## What Civio is

**Civio** (Title Case) is a Philippine Civil Service Exam study app. Tutor name:
**Dexter**. It is **not** official CSC software and must never claim affiliation.

- Lowercase `civio` / `civio.ph` only in identifiers, URLs, package names, env prefixes.
- Avoid all-caps **CIVIO** in UI, metadata, README, and docs.
- Rebrand from Hiraya is allowed; credit original author in README acknowledgements.

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

- Never touch GT's MSI Docker containers `hiraya-review-app` / `hiraya-review-db`.
- Never touch Hermes on port **8642**.
- Local MSI study app on `localhost:8080` stays the stable study surface.
- Do not break guest unlimited study (`CIVIO_GUEST_UNLIMITED`) without GT approval.

## Branch and commit rules

- Work on **`main`**. Normal `git push origin main` only.
- **Never force-push.** If rejected, stop and report.
- Small logical commits (one concern each). Suggested Phase 0 sequence is in the build brief.
- Push periodically after green checkpoints, not every commit.
- No secrets in commits. Spot-check built assets for leaked keys.

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
- **In progress:** Copy for AI MVP (`docs/EXTERNAL_AI_HANDOFF.md`).
- **Then:** Phase 1 foundation → Phase Bank.

## Hosting intent (not yet executed)

Google Cloud Run (scale to zero, instance cap, budget alert) + Neon free Postgres +
Cloudflare (DNS/CDN, Turnstile, analytics). See `docs/DEPLOY.md`.

## Agent tooling

- Entire CLI: see `ENTIRE.md` and `.entire/README.md`.
- Laravel Boost guidelines remain in `GEMINI.md` for framework conventions.

## Libraries (Phase 0 extras)

See `docs/LIBRARIES.md` for researched options and verdicts.

Adopted now:

- **vite-plugin-pwa** — generated SW (`resources/js/sw.ts`), NetworkOnly for `/exams`, prompt update
- **ts-fsrs** — `resources/js/lib/review/fsrs.ts` (scheduler only; UI later); `npm run test:js`
- **prism-php/prism** — installed; `App\Ai\Contracts\TutorProvider` + `NullTutorProvider` default
- **sentry/sentry-laravel** — no-op unless `SENTRY_LARAVEL_DSN` is set

Never put provider keys in `VITE_*`.
