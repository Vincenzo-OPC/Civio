# Low-end performance and cost report (Issue #27, 23 October 2026)

Goal: Civio works cheaply on a 2 GB Android phone on weak 3G and on an old
dual-core 4 GB PC. Everything below was measured on the build box in headless
Chromium. **No real devices were available.** Treat timings as emulation.

## How it was measured

- `playwright.perf.config.ts` + `tests/Perf/*` (dev only, no new dependencies).
  Throwaway SQLite (same guard as the Strict Mock E2E): 5 categories, 310
  synthetic items, Strict mock serves 150.
- `tests/Perf/gzip-proxy.mjs` stands in for production nginx: gzip, ETag and,
  with `PERF_CACHE_RULES=1`, the same Cache-Control rules as
  `conf/nginx/civio-cache.conf`. `php artisan serve` alone sends neither.
- CDP throttling: 400 kbps / 300 ms RTT and 250 kbps / 400 ms RTT (upload half),
  CPU slowdown 4x and 6x, 360x740 viewport, plus offline toggling.
- Bytes are `encodedDataLength` (response bytes on the wire incl. headers);
  memory/disk-cache and service-worker hits count as 0. Upload bytes are not
  counted.
- Vitals: LCP and CLS from PerformanceObserver, TBT from long tasks (INP proxy
  is the longest event-timing entry). JS heap from CDP.
- `measure.spec.ts` runs only with `PERF_MEASURE=1`; raw JSON is in
  `tests/Perf/results/` (`before.json`, `after.json`, `after-final.json`).
- Lighthouse was not run (it would need a new dependency fetched by npx; the
  harness above covers the same metrics).

Limitations: throttling runs over HTTP/1.1 with 6 connections, which overstates
latency for the ~70 small chunks compared with HTTP/2 or HTTP/3 behind a CDN.
CDP throttling does not change `navigator.connection`, so Lite auto-detection
was exercised by forcing the Lite preference instead. During the "before" run
two backend changes (pool cache, lazy pool) landed after ~9 minutes; byte
counts are unaffected and timings at most marginally. The "before" run had no
Cache-Control (nginx default heuristics), as in production today.

## Before and after: Strict Mock, first question usable

"First question" = from navigation to `/exams` to option A of question 1 being
enabled (accept rules, Exam Mode, Begin).

| Case | Before KB / req | After KB / req | Before first Q | After first Q | After LCP | CLS | TBT (after) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unthrottled, Lite off | 787.9 / 77 | **401.3 / 76** | 0.54 s | 0.54 s | 0.27 s | 0 | 0 ms |
| 400 kbps, 4x, Lite off | 387.2 + 398.4 later / 77 | 398.9 / 76 | 12.7 s | **11.9 s** | 10.4 s | 0 | 156 ms |
| 250 kbps, 4x, Lite off | 387.2 + 398.4 later / 77 | 398.8 / 76 | 18.7 s | **17.5 s** | 15.7 s | 0 | 174 ms |
| 400 kbps, 6x, Lite on | 386.4 + 398.4 later / 75 | 397.8 / 74 | 12.9 s | **12.3 s** | 10.6 s | 0 | 517 ms |
| 250 kbps, 6x, Lite on | 386.4 + 398.4 later / 75 | 397.9 / 74 | 19.0 s | **18.0 s** | 15.8 s | 0 | 319 ms |

Before, the two logo PNGs (398 KB) downloaded right after the first question
on throttled links, competing with the first answer saves. After: 8 KB.

Warm visit (resumes the unfinished mock): 1.4 KB / 1 wire request (Lite off),
7.4 KB / 3 (Lite on, no service worker), 0.2 to 1.0 s to the question at 4x
to 6x CPU. JS heap 7 to 9 MB on load, 14.8 MB after a 150-item mock.

## Full Strict mock and offline

| | Before | After |
| --- | --- | --- |
| 150 answers (150 progress POSTs) | 233.8 KB | 233.9 KB |
| Submit + scorecard | 11.4 KB | 11.4 KB |
| **Incremental total** | **245.2 KB** | **245.3 KB** |
| Longest interaction (6x CPU) | 40 ms | 32 ms |
| Offline pack (one category, opt-in, size shown) | – | 18 KB, 5 requests |
| Drills page cold | – | 349.8 KB |

About 1.67 KB per answer; most of it is response headers (two cookies) and the
full saved-answers map that each save returns. Lazy-loading the scorecard and
review screens was tried and **reverted**: it cut 12 KB before the first
question but moved 25 KB into the mock (prefetch so results still show after
a drop), taking the mock to 270 KB, over target.

## Targets

| Target | Result |
| --- | --- |
| First question ≈ 6 s at 400 kbps | **Missed**: 11.9 s (4x) / 12.3 s (Lite, 6x) |
| First question ≈ 10 s at 250 kbps | **Missed**: 17.5 s / 18.0 s |
| Full-mock incremental < 250 KB | Met, narrowly: 245.3 KB |
| LCP ≤ 2.5 s | Met unthrottled (0.27 s); **missed** on 3G emulation (10.4 s / 15.7 s) |
| INP ≤ 200 ms | Met by proxy: longest interaction 32 ms at 6x CPU (TBT on load 156 to 517 ms) |
| CLS ≤ 0.1 | Met: 0 everywhere |
| No bundle-budget regression | Met: app 45.82 / 48, vendor 119.21 / 122, CSS 28.65 / 33, exams 10.99 / 11, all JS 1.01 MB / 1.04 MB |

Why the first-question targets are missed: ~330 KB of gzip JS (vendor-inertia
98 KB, app 59 KB, vendor-ui 35 KB, ~30 icon chunks) must arrive before the
exam can render. At 400 kbps that alone is ~7 s of transfer before any
request latency. Meeting 6 s needs roughly halving first-load JS (e.g. a
server-rendered or no-React "exam-lite" first screen, or SSR) plus HTTP/2 at
a CDN; that is an architecture decision, not a tuning pass.

## Optimizations made

1. Logos: 320 px and 360 px quantised PNGs (4.2 KB, 7.9 KB) replace 239 KB and
   169 KB originals in the header/sidebar; correct width/height (the old
   height attribute was wrong), `decoding="async"`, the hidden collapsed icon
   is `loading="lazy"`. Originals kept in `public/images/`.
2. Removed the `questions.active` cache: it stored a 12.6 MB serialized blob
   per bank (hit ~109 ms and 137 MB peak memory versus a ~35 ms direct query).
3. `getExamSessionData` loads the bank pool only for attempt/drill branches;
   `GET /exams` now runs 0 bank queries.
4. `pending_feedback_count` is computed only for admins (also stops an admin
   count reaching guests).
5. Production static caching: `conf/nginx/civio-cache.conf` copied by the
   Dockerfile into serversideup's `server-opts.d`: hashed `/build/assets/*`
   immutable 1 year, manifests `no-cache`, images 30 days. `public/.htaccess`
   rule fixed (its `FilesMatch` never matched). Unused
   `conf/nginx/nginx-site.conf` deleted. Not yet verified in a built image.

Already good, unchanged: Lite Mode, opt-in offline packs with sizes, lazy
PDF/charts, no hover-only content, answers flushed only while pending.

### Queries per request (database session and cache drivers)

| Request | Before | After | CI budget |
| --- | --- | --- | --- |
| GET /exams | 22 | 14 (0 bank) | 17 |
| POST /exams/sessions | 15 | 12 | 16 |
| POST progress (one answer) | 9 | 8 | 11 |
| POST attempts (submit 150) | 18 | 17 | 22 |
| GET /dashboard (guest) | 6 | 4 | 8 |
| GET /drills (guest) | 11 | 8 | 11 |

## Finding: answers can stay unsaved after an early offline drop (pre-existing)

Reproduced by the intermittent test. If the connection drops in the ~1 s
after Begin, before the lazily loaded `progress-save` chunk arrives, the
dynamic import fails. Chrome keeps a failed module import failed for the
page's lifetime, so every later save also fails; the hydration request then
repeats about every 1.4 s, and in 60 s after reconnecting **0 of 6 answers
reached the server** (they stay in local storage and recover on reload). A
small retry-the-import fix was tried and did not help, because Chrome does not
re-fetch the module, so it was reverted. Fix options for GT: load `progress-save`
before Begin (costs exam-chunk budget) or reload the page once on reconnect.

## Backend cost estimate (no Redis, no paid services)

Assumptions, per daily active student: 1 full Strict mock (150 answers), 6
other page views, 30% of days are a cold cache. Database session and cache
drivers on Postgres. 20 ms PHP CPU per request (**assumed**, not measured on
production hardware). Peak hour = 20% of daily traffic.

Per student-day: ~160 requests, ~1,280 queries, ~320 DB writes (session row
on every request, two writes per answer), ~460 KB transfer
(0.3 × 401 KB cold + 245 KB mock + 6 × ~15 KB pages), ~8 KB new rows
(exam session ~2.5 KB, attempt ~3.2 KB, plus indexes).

| DAU | Requests/day | Peak req/s | Queries/day | Peak CPU (app) | Transfer/month | DB growth/month |
| --- | --- | --- | --- | --- | --- | --- |
| 100 | 16 k | ~1 | 128 k | < 0.1 core | ~1.4 GB | ~25 MB |
| 1,000 | 160 k | ~9 | 1.3 M | ~0.2 core | ~14 GB | ~240 MB |
| 10,000 | 1.6 M | ~90 | 12.8 M | ~1.8 cores | ~140 GB | ~2.4 GB |

100 to 1,000 DAU fit one small 1 to 2 vCPU box with Postgres beside it.
10,000 DAU needs ~4 vCPU for PHP-FPM plus a separate Postgres; the session
and cache tables then take ~90 to 270 writes/s at peak and need routine
vacuuming. Exam sessions are pruned after 45 days (#26); attempts are kept.
Static assets with immutable caching and a free CDN would remove most of the
transfer from the origin.

## Kept permanent

- `npm run test:perf-budget` runs `tests/Perf/budget.spec.ts`: byte and
  request-count limits only, no timings. **Not yet in CI:** adding the step to
  `.github/workflows/e2e.yml` needs a token with `workflow` scope, which the
  agent token lacks; the one-step patch is ready for GT to apply.
- `tests/Feature/Performance/QueryBudgetTest.php` (Pest) caps queries per request.
- `tests/Js/static-cache-config.test.ts` keeps nginx, `.htaccess`, the Dockerfile
  and the perf proxy in step.
- size-limit budgets unchanged.
- AGENTS.md "Low-end and cost review" item.
