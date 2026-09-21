# Hiraya Review — Local Fork Notes (GT / Cover)
Dated: 19 Sep 2026 (Asia/Manila)

Upstream: https://github.com/codebykenth/hiraya-review
Local path: `C:\Users\GT\Desktop\Grok\Hiraya-Review`
Purpose of upstream: self-hosted CSE (Civil Service Exam) mock reviewer (Laravel + Inertia/React + Postgres). There is no public hosted demo — GitHub is so people can run it themselves (Docker preferred).

Live local stack (MSI):
- App: http://localhost:8080
- Postgres host port: 5433 (container 5432)
- Containers: hiraya-review-app, hiraya-review-db
- Intentionally NOT on :8642 (Hermes uses that)

---

## Why fork later

Upstream works as a product idea but the local install hit many rough edges for study use:
1. Guest / free-attempt exam crashed (auth.user null).
2. Announcements serialized as PHP Incomplete_Class → blank/broken Inertia page.
3. Empty / thin question bank after migrate+seed (needed custom seeder).
4. Aggressive anti-cheat (no screenshot, no copy, blur on focus loss) — hostile for local studying/Google-checking.
5. Stale Vite assets + service worker / localStorage kept serving broken exam sessions ("Which option is correct?" with no stem/options).
6. Docker ports collided with Hermes; frontend npm run build timed out during compose (prebuilt assets still served).
7. Schema quirks (e.g. no is_active column on questions — status flags differ from what we guessed).

Goal of a future fork: keep the mock-exam UX, harden guest mode, ship a real practice bank, make anti-cheat optional/dev-off, and document one-command Docker for Windows.

---

## Source patches already in the working tree (git-tracked diffs)

Do NOT push these to upstream. Keep them for your fork.

### 1. app/Http/Middleware/HandleInertiaRequests.php
Bug: global_announcements shared as Eloquent collection → sometimes JSON'd as PHP_Incomplete_Class, crashing the exams page.
Fix: chain ->values()->toArray() after ->get().

### 2. resources/js/pages/user/exams/components/setup-exam-view.tsx
Bug: Guest free attempt (auth.user === null) → Cannot read properties of null (reading 'can_download_pdf').
Fix: optional chaining: auth.user?.role, auth.user?.can_download_pdf.

### 3. resources/js/pages/user/exams/hooks/use-content-shield.ts
Change: early-return no-op shield when hostname is localhost or 127.0.0.1 (study mode: screenshots + copy allowed).
Marked with comment LOCAL_SHIELD_OFF. Production / non-local host still shields.

### 4. Dockerfile
Minor local tweak (1-line diff) — review before fork; may be build-path related.

---

## Untracked / added files (keep for fork)

| File | Role |
|------|------|
| docker-compose.yml | Local compose: app 8080, db 5433, avoids Hermes 8642 |
| env.docker.example | Example env for Docker |
| seed_real_practice.php | Replaces dummy stems with ~440 readable practice Qs + options/explanations |
| seed_sample_questions.php / seed_topup_questions.php | Earlier/extra seed attempts |
| _pw/ | Playwright probes used while debugging (omit from fork or keep as scripts/debug) |
| compose-build.log | Build log noise — omit from fork |
| _*debug*.png, _debug_*.html | Debug artifacts — omit |

.env is local-only — never commit.

---

## Container-only patches (NOT in host git — rebuild loses them)

These live inside the running hiraya-review-app filesystem. Re-apply after recreate, or bake into fork properly.

1. public/build/assets/app-copyok-gt0920.js
   Patched Vite bundle: localhost shield bypass + bootstrap CSS user-select:text + capture listeners that stopImmediatePropagation on copy/cut/contextmenu/selectstart so Ctrl+C works for Google study.
   Manifest points here: assets/app-copyok-gt0920.js.

2. public/build/manifest.json
   All assets/app-*.js refs rewritten to app-copyok-gt0920.js.

3. public/sw.js
   Kill-switch service worker: unregister caches / force fresh assets (old SW kept serving broken JS).

4. public/clear-exam.html
   Clears localStorage keys (active_exam_session_v1, pending_free_exam) + sessionStorage, then redirects to /exams?free_attempt=1&start=professional.
   Use when exam shows placeholder "Which option is correct?" with no real stem.

Proper fork approach: apply the TS/PHP source fixes, run a real npm run build, drop the hand-patched app-copyok hack, and gate anti-cheat with APP_ENV=local or a config flag instead of hostname sniffing.

---

## Runtime / data notes

- After php artisan db:seed --force, categories exist; question count was raised to 440 via seed_real_practice.php.
- Stale exam UX was often browser localStorage, not DB — always try /clear-exam.html first.
- Incognito worked when normal Chrome didn't → cache / SW / old session.
- Hermes on MSI: leave port 8642 alone.

---

## Suggested fork backlog (improve later)

1. Guest-safe exam path (null auth.user everywhere, not just setup view).
2. Config flag EXAM_CONTENT_SHIELD=false for local/study builds.
3. Official seed of real CSE-style practice items (or import pipeline) — replace placeholders.
4. Harden Inertia shared props (always arrays/DTOs, never raw incomplete models).
5. Document Windows Docker Desktop one-shot: ports, .env, seed, healthcheck.
6. Disable or scope SW in local; version assets aggressively.
7. Reset exam session button in UI (same as clear-exam.html).
8. Fix report-question flow (user said report didn't work).
9. Ensure options/diagrams render when stem references them (placeholder stems were the main culprit).
10. Optional: hosted demo for non-Docker users (upstream currently expects self-host).

---

## Quick local ops (MSI)

cd C:\Users\GT\Desktop\Grok\Hiraya-Review
docker compose ps
start http://localhost:8080/clear-exam.html

Re-seed practice bank (inside app container):
docker exec hiraya-review-app php /var/www/html/seed_real_practice.php
docker exec hiraya-review-app php artisan cache:clear

---

## Decision log (GT)

- Keep using local Docker for CSE study for now.
- Do not push patches to codebykenth/hiraya-review.
- Later: fork under GT's GitHub and apply the source fixes cleanly + real build + study-mode config.
## Session resume (added 19 Sep 2026 evening)

- Exam progress already saved in browser localStorage key `active_exam_session_v1`.
- Extended TTL from 12 hours to **30 days**; flush on pagehide/beforeunload/visibility hidden.
- Hydration skips `?start=` when a valid saved session exists (so resume is not wiped).
- `SESSION_LIFETIME=43200` (30 days) for guest free-attempt PHP session.
- Use `http://localhost:8080/resume-exam.html` after reboot (keeps progress).
- `clear-exam.html` still wipes progress for a brand-new mock.
- Docker `restart: unless-stopped` + Postgres volume `hiraya_pgdata` survive PC reboot if Docker Desktop starts with Windows.
