# Civio Launch Checklist (review of 2026-10-23)

Code-only review of `main` at 052438a. Nothing was deployed and no host, Netlify or billing settings were read or changed. Classes:
**Confirmed defect** (wrong in code today), **Launch blocker** (must be resolved before public traffic), **Accepted residual risk** (known, tolerable, monitor).

> Bots and scrapers **can** incur hosting costs: every request consumes bandwidth, PHP CPU time and database reads/writes (sessions, cache, rate-limit counters and exam sessions are all database-backed by default). Rate limits cap the damage per client; they do not make traffic free.

| # | Area | Finding | Class |
|---|------|---------|-------|
| 1 | Trusted proxies | `bootstrap/app.php` never calls `$middleware->trustProxies(...)`. Behind any CDN/load balancer `$request->ip()` is the proxy address, so every per-IP limiter (`global-views`, `global-mutations`, `bank-access`, `exam-progress`, `support-submission`, `pdf-export`, login) buckets *all guests together*. Fix needs the host's proxy ranges/header, so it was not changed here. | Confirmed defect · Launch blocker |
| 2 | Turnstile | `VerifyTurnstile` skips verification when keys are missing (fails **open**), in every environment. Only login, register and password-reset POSTs are covered. Production must set `TURNSTILE_SITE_KEY`/`TURNSTILE_SECRET_KEY`; consider failing closed when `APP_ENV=production` and keys are absent. | Launch blocker (config) |
| 3 | Env defaults | `APP_DEBUG` defaults false; `CIVIO_GUEST_UNLIMITED` defaults false outside local/testing (1b58f7a). `SESSION_SECURE_COOKIE` has no default; set `true` in production. | Accepted residual risk (verify env at deploy) |
| 4 | Per-route limits | `global-views` 120/min, `global-mutations` 30/min, `ai-generation` 5/min are `Limit::none()` outside production, so they are only active when `APP_ENV=production` exactly. `bank-access` 30/min, `exam-progress` 180/min, offline packs/sync and PDF 1/day are always on. | Accepted residual risk (verify `APP_ENV`) |
| 5 | DB usage per request | Sessions, cache and rate-limit counters default to the `database` store, so every throttled request performs DB writes. Under bot load the DB is the first cost/limit hit. Prefer Redis/memcached for cache and limiter if the host offers it. | Accepted residual risk |
| 6 | Abandoned exam sessions | `exam_sessions` rows (with `question_ids` JSON and `saved_answers`) are never pruned; there is no scheduled task in `routes/console.php`. Each started-but-unfinished mock leaves a row forever. A `civio:prune-exam-sessions` command (delete rows with no `exam_attempt_id` and `deadline_at`/`created_at` older than N days) plus a scheduler entry is recommended; not added here to keep this change docs-only. | Confirmed defect (growth), not a blocker |
| 7 | Database session/cache tables | `sessions` and `cache` tables grow with bot traffic; Laravel's lottery GC handles sessions, expired cache rows are not swept. | Accepted residual risk |
| 8 | Spending alerts | No spend/usage alerting exists in code. Set billing alerts and bandwidth/function-invocation caps on the host and DB provider before launch. | Launch blocker (account setting, GT) |
| 9 | Shared-IP false positives | Once #1 is fixed, guests on carrier-grade NAT, school or office Wi-Fi share one IP: 30 bank accesses/min and 1 support request/day per IP can block legitimate students. Authenticated users are keyed by user id and unaffected. | Accepted residual risk (monitor 429s) |
| 10 | AI cost | AI kill switch stays closed; no paid AI calls at launch. | Accepted |
| 11 | Client retry storms | Fixed in c6c7b5b (#25): the browser only retries GET/HEAD and never replays writes, so 429/5xx no longer multiply write load. | Resolved |

## Before go-live
1. Configure trusted proxies for the chosen host (#1).
2. Set Turnstile keys, `APP_ENV=production`, `APP_DEBUG=false`, `SESSION_SECURE_COOKIE=true` (#2–#4).
3. Enable host and DB spending alerts (#8).
4. Add exam-session pruning soon after launch (#6).
