# Civio

**Civio** is a Philippine Civil Service Exam study app: Professional and
Subprofessional mocks, practice drills, learn modules, and the Dexter tutor.
**Civio is not an official Civil Service Commission (CSC) product.**

## Features

- Server-graded mocks (150 Professional / 145 Subprofessional items) picked on
  the server; answer keys stay on the server until Reveal or submit.
- Practice drills by topic, with Reveal, explanations and Copy for AI.
- Lite mode for cheap phones and slow data (auto on Save-Data / 2G / 3G).
- Offline drill packs: download a topic, practise with no connection, sync
  when back online (the server re-checks every answer; offline items never
  appear in mocks).
- Guest study without an account (`CIVIO_GUEST_UNLIMITED`).

## Stack

Laravel 13 · Inertia 3 / React 19 / TypeScript · Vite · Tailwind 4 ·
Postgres (SQLite in tests) · optional server-side AI (stub by default).

## Quick start

```bash
composer install
npm ci
cp .env.example .env && php artisan key:generate
php artisan migrate --seed
npm run dev        # or: npm run build && php artisan serve
```

Docker: `docker compose up --build` (app on `:8080`, Postgres on `:5433`).

## Checks (run before every push)

```bash
php artisan test         # Pest
npm run types:check      # tsc
npm run lint:check       # eslint
npm run test:js          # node:test via tsx
npm run build
npm run size             # bundle budgets (size-limit)
vendor/bin/pint --test
npm run format:check
```

## Docs

- `AGENTS.md` / `CLAUDE.md` — rules for agents and contributors
- `docs/CODE_STANDARD.md` — coding standard and modernization backlog
- `docs/ARCHITECTURE.md` · `docs/DEPLOY.md` · `docs/LIBRARIES.md`
- `docs/LITE_MODE_PLAN.md` — Lite mode and offline drill packs
- `docs/CSE-Question-Design-Spec.md` — question design (no bank items without approval)
- `docs/QUESTION_SOURCE_GROUPS.md` — question source groups and the re-parameterize workflow
- `docs/EXTERNAL_AI_HANDOFF.md` · `docs/AI_STUDY_AND_SPELLING_SYSTEM.md` · `docs/2026_AI_PRODUCT_STANDARD.md`
- `ENTIRE.md` — agent session capture
- `CHANGELOG.md` — generated with `npm run changelog`

## Origin

Civio started from a baseline codebase at commit `d3f0368`; every change since is
listed in `docs/CHANGES_SINCE_BASELINE.md`.
