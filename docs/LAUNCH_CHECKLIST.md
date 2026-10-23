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


## Architecture review decisions, 23 October 2026 (advisory; no paid activation)

These are recommendations for the next implementation handoff. The owner has **not** authorized setting up hosting, enabling billing, deploying, or creating paid services.

1. **Dashboard breakpoint: ACCEPT 1024px.** At 768px, retain a single column instead of forcing dense paired panels into narrow columns next to the sidebar. Accept restrained blank space inside a taller, equal-height desktop row; do not invent filler content. Preserve genuine mobile content heights and correct content hierarchy.
2. **Abandoned-session cleanup: IMPLEMENT as a guarded code-only task.** Add `civio:prune-exam-sessions` with `--dry-run`, configurable retention and bounded batch deletes. Target only `exam_sessions` without an `exam_attempt_id`, and require older-than-cutoff inactivity (default **45 days**, beyond the existing 30-day local study recovery window). Never delete graded attempts, linked exam sessions, recent Study sessions, or question-bank rows. Tests must confirm these exclusions, Strict deadlines and guest/signed-in cases. Prepare a daily scheduler entry; don't activate external cron until hosting is chosen. Confirm legacy session ownership and database foreign-key dependencies before deletion.
3. **Redis: DEFER.** Don't add Redis/Memcached merely to pass hypothetical load tests; this adds another billed component. Keep the current database-backed cache/session/rate-limit implementation for a small controlled pilot, measure DB CPU, query latency, 429 rates, active users and write volume, then migrate when supported by evidence. Avoid declaring the present setup fit for unlimited public scale.
4. **Tentative hosting preference: Railway Hobby + Postgres in Singapore, with Cloudflare Free as the public CDN/WAF and Turnstile.** Railway provides a Southeast Asia region, $5/month Hobby minimum including $5 resource usage, and billing alerts/usage limits. **This is a recommendation only** pending owner approval of any spending and a test of PHP/Laravel deploy, Postgres backup/restore, cron, IPv6/client IP, network egress, latency and actual cost. Railway usage hard limits can stop workloads, and storage/backup costs must be examined separately: a usage cap is not a guarantee of uninterrupted uptime or a universal invoice ceiling. Initial suggested thresholds: $10 alert, $15 compute hard limit, subject to a budget decision by GT.
5. **Trusted proxy setup: MUST PASS BEFORE LAUNCH.** For Cloudflare -> Railway -> Laravel, configure the chain using actual verified proxy ranges and supported forwarded headers, never unconditionally trust caller-supplied `CF-Connecting-IP` or `X-Forwarded-For`. Audit whether the origin can be accessed without Cloudflare and close bypass routes as supported by hosting. Test at least two distinct visitor IPs, a school/shared IP, malformed/spoofed headers, auth and guest rate-limit keys, HTTPS redirects and session cookies. Laravel 13 supports `trustProxies` in `bootstrap/app.php`. Host-specific configuration cannot be finalized in the repository without an actual deployment target.
6. **Turnstile: USE FREE TIER; FAIL LAUNCH READINESS IF UNCONFIGURED.** Add production readiness validation of the site and secret keys; don't allow signup, password-reset or login bot checks to silently be disabled by absent keys. Never commit secrets. Confirm the actual POST routes are covered and fallback behavior is understandable for legitimate users. Turnstile Free supports normal production applications.
7. **Cost control and backups: MUST PASS BEFORE LAUNCH.** Set the host's email spending warning and enforced usage limit, Postgres usage/storage alerts, backup schedule and one verified restoration test. Edge caching may be applied to versioned static assets, never user-specific exam/session/progress/score responses. Disallow surprise billable AI and unintended auto-scaling.

Official sources checked:
- Railway: https://docs.railway.com/pricing/cost-control and https://docs.railway.com/deployments/regions
- Cloudflare Turnstile Free: https://developers.cloudflare.com/turnstile/plans/
- Cloudflare visitor IP: https://developers.cloudflare.com/support/troubleshooting/restoring-visitor-ips/restoring-original-visitor-ips/
- Laravel 13 proxy trust: https://laravel.com/framework/docs/requests#configuring-trusted-proxies

**Release rule:** No deployment, hosting signup, paid service, DNS/proxy changes, keys, or billable activation without GT approval. Continue safe code-only fixes and tests on isolated infrastructure.

## Readiness check (Sprint 2)

`php artisan civio:launch-check` reads configuration only (no network, no writes) and exits non-zero on any failure. In production (or with `--production`) these fail: `APP_DEBUG` on, `SESSION_SECURE_COOKIE` not `true`, Turnstile keys missing, a wildcard trusted proxy without acknowledgement, `CIVIO_OWNER_FUNDED_AI=true`, `CIVIO_GUEST_UNLIMITED=true`. Warnings: no trusted proxies, Turnstile fail-closed off, an acknowledged wildcard, and not running as production. Run it before switching traffic to a new host.

Turnstile fail-closed: `CIVIO_TURNSTILE_REQUIRED=true` makes login, register and password-reset POSTs refuse with a neutral message when the keys are missing in production. Off by default so a missing key cannot lock everyone out without GT choosing that. Fixed alongside: a missing Turnstile env value used to crash `TurnstileService` (null into a typed string) and 500 the auth pages.

## Trusted-proxy strategy (anti-spoofing)

- Proxy trust is configured only through `CIVIO_TRUSTED_PROXIES` (comma-separated IPs/CIDRs). Empty, the default, trusts nobody: `X-Forwarded-For` is ignored and `$request->ip()` is the TCP peer. No ranges are configured in the repo.
- Put only the edge's published egress ranges there (for example the CDN's list), and keep it updated when the provider changes them.
- Never use `*` unless the origin accepts connections only from the edge (private network, firewall allow-list or authenticated tunnel). Then set `CIVIO_TRUSTED_PROXIES_ALLOW_WILDCARD=true`; the launch check still warns.
- Host-specific test before launch: send a request directly to the origin with a forged `X-Forwarded-For: 1.2.3.4` and confirm logs and rate limits see the real peer, not `1.2.3.4`.

## Backups and restore

- Daily automated database backups with at least 7 days of point-in-time or snapshot retention; one copy outside the hosting account.
- Restore drill before launch and monthly: restore into a scratch database, run `php artisan migrate --pretend` and the test suite against it, and check row counts for `users`, `exam_attempts`, `questions`.
- The question bank is the irreplaceable asset: keep an export of approved questions in version-controlled or offline storage separate from the app database.
- Backups contain personal data (emails, answers); encrypt at rest and restrict access to GT.

## Logging without personal data

- `LOG_LEVEL=warning` or `error` in production; never `debug`.
- Do not log request bodies, answers, emails, passwords, tokens, Turnstile tokens or full IPs. Prefer user ids and hashed or truncated IPs.
- `APP_DEBUG=false` (checked) so exception pages never show env or query bindings.
- Set log retention (for example 14–30 days) on the host's log store.
