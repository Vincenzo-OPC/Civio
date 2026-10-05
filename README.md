# Civio

**Civio** is a Philippine Civil Service Exam study app (mocks, drills, learn modules,
Dexter tutor). **Not an official Civil Service Commission product.**

## Stack

Laravel 13 · Inertia/React 19 · Vite · Tailwind 4 · Postgres/SQLite · optional AI (Prism / stub)

## Quick start

```bash
composer install
npm ci
cp .env.example .env && php artisan key:generate
php artisan migrate
npm run dev   # or: npm run build && php artisan serve
```

Docker: `docker compose up --build` (app on `:8080`).

## Checks

```bash
php artisan test
npm run types:check
npm run lint:check
npm run build
npm run test:js          # FSRS wrapper
vendor/bin/pint --test
```

## Docs

- `AGENTS.md` — agent / Codex rules
- `docs/ARCHITECTURE.md` · `docs/DEPLOY.md` · `docs/LIBRARIES.md`
- `docs/CIVIO_CODEX_BUILD_BRIEF.md` · `docs/DESKTOP_PATCHES_TO_PORT.md`
- Question design: `docs/CSE-Question-Design-Spec.md` (do not add bank items without approval)

## Acknowledgements

Civio reuses the open Hiraya Review codebase originally by Kenth / codebykenth.
