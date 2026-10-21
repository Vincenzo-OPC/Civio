# Deployment readiness — 21 October 2026

Hosting is still undecided. This note does not choose a provider, create an account, or deploy Civio. Smart Review stays **IMPLEMENTED, NOT PRODUCTION VERIFIED**.

Labels mean what was actually observed.

## Baseline

| Item | Result |
| --- | --- |
| Starting and checked HEAD | `4aeb05533a306bfe2aaf1dae425d41636c23e109` |
| `origin/main` at the start of this check | same commit |
| PHP 8.4 CI | **VERIFIED** pass. [tests run 39622949292](https://github.com/Vincenzo-OPC/Civio/actions/runs/39622949292), [job 119300829006](https://github.com/Vincenzo-OPC/Civio/actions/runs/39622949292/job/119300829006) |
| PHP 8.5 CI | **VERIFIED** pass. Same run, [job 119300828366](https://github.com/Vincenzo-OPC/Civio/actions/runs/39622949292/job/119300828366) |
| Quality CI | **VERIFIED** pass. [linter run 39622949103](https://github.com/Vincenzo-OPC/Civio/actions/runs/39622949103) |
| Published bundle on that commit | **VERIFIED** by the size step and a clean local rebuild of that tree: all JS 1,002,557 / 1,040,000 brotli bytes. Exam chunk 10,975 / 11,000. Main 45,464 / 48,000. Vendor 119,212 / 122,000. CSS 28,660 / 33,000 |
| This sandbox's host PHP | 8.4.23, no sodium. Bank-signature tests were not re-run here. **NOT VERIFIED** on this host |

No protected study database was migrated. A first server process did not receive `DB_*` from the shell and served one GET from the local `database/database.sqlite` (992 questions). That file's size and mtime were unchanged afterward. Every later check used `/tmp/civio-verify.sqlite` and fixture questions only.

## Runtime compatibility

| Check | Result |
| --- | --- |
| App timezone | **VERIFIED** `Asia/Manila`. `/ping` returned `+08:00`. A stored due instant `2026-10-21 23:36:41` rendered as "Oct 21, 2026 11:36 PM" |
| Node used by the browser checks | **VERIFIED** v22.23.2. Wrong answers scheduled. `/bin/false` left the event unscheduled |
| ts-fsrs | **VERIFIED** in the app path used by those requests (`ts-fsrs` 5.4.2 is the committed dependency). Not verified inside a built image |
| Sodium in the production image | **NOT VERIFIED**. The image was not built. The Dockerfile still requests sodium |
| Host Pest `ReviewMistakeTest` | **VERIFIED** 23 passed, 311 assertions |
| Host Pest `PdfAnswerKeyTest` | **VERIFIED** 12 passed, 62 assertions |

## Docker image

**BLOCKED.** Not an application defect.

```text
docker build -t civio-fsrs-smoke /workspace/civio
```

```text
failed to register layer: failed to Lchown "/etc/gshadow" for UID 0, GID 42
(try increasing the number of subordinate IDs in /etc/subuid and /etc/subgid):
lchown /etc/gshadow: invalid argument
```

`/proc/self/uid_map` is `0 0 1`. `scripts/fsrs-image-smoke.sh` was not run, because it starts with that build. A filesystem or chroot check was not treated as a passed image.

On a Docker host that can unpack layers:

```sh
scripts/fsrs-image-smoke.sh
```

That script builds `civio-fsrs-smoke` and runs `scripts/fsrs-image-smoke.php` inside it. It does not deploy.

## Multi-instance scheduling

| Check | Result |
| --- | --- |
| Intended cache and session | **VERIFIED** in `.env.example` and `env.docker.example`: `CACHE_STORE=database`, `SESSION_DRIVER=database`. `cache_locks` is created by `0001_01_01_000001_create_cache_table.php` |
| Two PHP processes, database lock, sqlite | **VERIFIED**. Process A held `review-schedule:41`. Process B got `LockTimeoutException` in 0.759s on `block(1)`. `review-schedule:42` was acquired in 0.001s while the first lock was held |
| Same-process lock tests | **VERIFIED** by `ReviewMistakeTest` under `CACHE_STORE=array`. That does not prove multi-instance safety |
| PostgreSQL or a second machine | **NOT VERIFIED** |
| Unbounded wait | **VERIFIED** absent in config. `CIVIO_FSRS_LOCK_WAIT` defaults to 10 seconds. Node timeout is 5 seconds. Lock TTL defaults to 20 seconds |
| Different learners | **VERIFIED** they do not share the lock key (`review-schedule:{userId}`) |
| Idempotency | **VERIFIED** by unique `(user_id, source_attempt_id, question_id)` on events and the `scheduled` flag. A failed Node run left `scheduled=0` and no card |
| File or array locks across servers | **NOT** safe. Do not use them for more than one app instance |
| Maintenance mode | **PARTIALLY VERIFIED** risk only. `.env.example` sets `APP_MAINTENANCE_DRIVER=file`, which is not shared across machines. Use the database driver before running more than one instance |

Queue, cache, and session examples are `database`. Smart Review does not use a queue worker. It runs after the grading transaction commits. `CIVIO_ALLOW_BROWSER_MIGRATIONS` must stay false. `scripts/00-laravel-deploy.sh` runs `config:cache`, `route:cache`, `view:cache`, and `migrate --force`. It does not roll migrations back.

## Browser and device

Chrome for Testing 153.0.8010.12 via the sandbox Playwright binary. Not a phone. Isolated fixture bank. No live question bank.

| Journey | Result |
| --- | --- |
| Home | **VERIFIED** at 1280px, no horizontal overflow |
| Guest drill and submit | **VERIFIED** on a fixture item |
| Register, verification link, signed-in session | **VERIFIED**. Mail driver was `log`. Nothing was sent off the machine |
| Wrong answer creates a reminder | **VERIFIED**. Rating `again`, due 11:36 PM Manila, shown under Upcoming Reviews |
| Independent correct | **VERIFIED**. Rating `good`, reps 2, due moved to 11:47 PM, item Resolved. The page said one clear does not finish the question. It did not say Review Complete |
| Show Explanation | **VERIFIED** on a numerical fixture. A first correct answer after that explanation did not create a review event |
| Assisted answer does not move an existing due date | **NOT VERIFIED** in the browser. **VERIFIED** by `ReviewMistakeTest` |
| Strict Mock | **VERIFIED**. Subprofessional, 1 of 8, timer `2:39:57`, no Show Explanation. Notice: the bank has 8 items, not 145. PDF export returned 423, "Answers stay hidden until you submit your Strict Mock." That user had 0 review rows |
| Professional and Subprofessional setup copy | **VERIFIED**. "3 Hours 10 Mins" and "2 Hours 40 Mins" |
| Full Strict Mock submit | **NOT VERIFIED**. Question 1 shows Next, not Submit |
| Scheduler failure | **VERIFIED**. With `CIVIO_FSRS_NODE=/bin/false`, the page said "Your answer was saved. The next reminder was not. Try again." and showed Save the reminder. The event stayed `scheduled=0` |
| Save the reminder after Node returned | **NOT VERIFIED**. The second visit did not reach the control (login was likely throttled). Pest covers recovery |
| Logout then login | **NOT VERIFIED** |
| Analytics wording | **PARTIALLY VERIFIED**. Visible text said "practice scores from finished mocks and drills." No pass-probability or ranking sentence was on that screen |
| Offline | **PARTIALLY VERIFIED**. `/offline` while online said no packs yet. A reload with the network cut was not completed |
| Lite Mode class | **NOT VERIFIED**. Setting `civio_lite=1` was not observed on `<html>` in that check |
| Keyboard focus audit | **NOT VERIFIED** |
| Widths 320, 360, 390, 768, 1024, 1440 on Exam Simulation | **VERIFIED** no document horizontal overflow |
| Drill at 390 and empty Review Mistakes at 320 | **VERIFIED** no document horizontal overflow. Choices were fully visible at 390 |
| 320px How it works | **VERIFIED** defect, then fixed. The label was clipped ("HOW IT WORK"). After `flex-wrap`, the full label fit, the button was not clipped, and overflow stayed false |
| Battery, prepaid data, low-end Android | **NOT VERIFIED**. No device and no measurements |

## PDF

| Check | Result |
| --- | --- |
| App calls `doc.html()` | **VERIFIED** it does not. The only mention is the comment in `resources/js/lib/html2canvas-stub.ts`. Capture uses `html2canvas-pro` and `addImage` |
| Stock `html2canvas` chunk | **VERIFIED** absent after the stub. The built chunk is `html2canvas-stub-*.js` |
| Button hidden | **VERIFIED** defect. `can_download_pdf` was true in the database and the button was absent, because the Inertia share omitted the flag. Fixed by sharing it. Regression: `PdfExportTest` "the exam screen receives the pdf permission" |
| Browser download after the fix | **VERIFIED**. Subprofessional booklet, 414,162 bytes, `%PDF-1.3`, 4 pages, 4 JPEG streams, no page errors |
| Answer-key order and Strict Mock refusal | **VERIFIED** by `PdfAnswerKeyTest`. The JPEG pages were not OCR'd, so the printed key text is **NOT VERIFIED** from the file |
| Daily throttle and guest refusal | **VERIFIED** by the existing Pest tests, not re-clicked in the browser |
| Mobile PDF | **NOT VERIFIED** |

## Mobile study

No phone was available. **NOT VERIFIED** for battery, radio data, touch latency, or a low-end Android browser. What was checked is the desktop Chrome viewport list above. Lite Mode was not confirmed in the browser. Offline packs were not downloaded.

## Deployment requirements

### A. Hosting capabilities

One or more Linux instances that can run the Dockerfile: PHP 8.4 FPM + nginx, Node 22 at runtime (not only at build), outbound HTTPS for mail and optional Turnstile. Persistent disk for `storage/` and for the SQLite file if SQLite is chosen. A reachable PostgreSQL is what `env.docker.example` expects. No provider is selected.

### B. PHP and Node

PHP 8.4 with `pdo_pgsql`, `pdo_sqlite`, `gd`, `zip`, `bcmath`, `opcache`, and `sodium`. Node 22 on `PATH` (or `CIVIO_FSRS_NODE`). `ts-fsrs` must remain in the image. npm is not required at runtime. `PHP_MAX_INPUT_VARS=1000` and `PHP_MEMORY_LIMIT=256M` must be real values. The serversideup image reads those from the environment. Unset, `max_input_vars` becomes 0.

### C. Database and cache

PostgreSQL for a multi-instance deploy, or one SQLite file for a single instance. `CACHE_STORE=database` or Redis. Do not use `array` or `file` when more than one PHP process handles learners. Sessions: `SESSION_DRIVER=database`.

### D. Durable storage and sessions

`storage/` and `bootstrap/cache` must be writable by `www-data`. Sessions live in the database in the examples. Uploaded local files use `FILESYSTEM_DISK=local`. There is no object-storage requirement in the current examples.

### E. Environment

Required before boot: `APP_KEY`, `APP_ENV=production`, `APP_DEBUG=false`, `APP_URL`. Database: `DB_CONNECTION` and the matching host or sqlite path. `CACHE_STORE`, `SESSION_DRIVER`, `QUEUE_CONNECTION`. Leave `CIVIO_TUTOR_PROVIDER` null until a tutor is approved. Leave AI keys empty. `CIVIO_ALLOW_BROWSER_MIGRATIONS=false`. `CIVIO_GUEST_UNLIMITED=false` for a public launch. Turnstile keys only if the widget should be required. Do not put secrets in `VITE_*`.

### F. Migrations

`php artisan migrate --force` from the entrypoint. Run it once per deploy against the empty or staging database. Do not point it at the protected study databases (`:5433`, `:5434`).

### G. Backup and rollback

Take a database dump before `migrate --force`. The entrypoint does not run `migrate:rollback`. Rollback is restore the dump and redeploy the previous image. Keep the previous image tag.

### H. Secrets

`APP_KEY` stays out of git. Bank approval keys stay out of this checklist. This check did not create hosting credentials.

### I. Operational risks

The image has not been built here. The exam chunk has little room (see bundle below). File maintenance mode does not coordinate instances. Smart Review holds a per-learner lock during Node, up to the lock TTL. A stuck Node is capped at 5 seconds and leaves the reminder unfinished. Login and PDF routes are throttled.

### J. Smart Review health

There is no separate scheduler health URL. `GET /ping` only proves PHP answered. A failed schedule is visible on Review Mistakes and is reported through Laravel's logger. `scheduled=0` with a non-null rating is the unfinished state.

### K. Monitoring and recovery

Log `FsrsScheduler` and lock-timeout exceptions. The learner retries with Save the reminder, or the next successful schedule run finishes older unscheduled events. Do not mark the answer unsaved when only the reminder fails.

### L. Browser evidence

Recorded above. Screenshots from this run are local artifacts, not committed.

### M. Blockers

1. **BLOCKED:** `docker build` cannot unpack layers in this sandbox.
2. **NOT VERIFIED:** sodium, Node, and `ts-fsrs` inside the actual image.
3. **NOT VERIFIED:** multi-host PostgreSQL locking.
4. **NOT VERIFIED:** phone, Lite Mode in the browser, offline reload, logout round-trip, and the Save the reminder click after a forced failure.
5. Hosting is undecided. No deploy is authorized.

### N. Staging sequence

1. On a normal Docker host, run `scripts/fsrs-image-smoke.sh`. Do not continue if it fails.
2. Start one staging instance with a new empty database, `CACHE_STORE=database`, `SESSION_DRIVER=database`, `APP_DEBUG=false`, browser migrations off.
3. Confirm `/ping`, register a staging user, miss a fixture or approved item, see a Manila due time, answer it again without an explanation, and see the due time move.
4. Stop Node, miss another item, confirm the failure sentence, restore Node, and use Save the reminder.
5. Open a Strict Mock and confirm PDF export is refused until submit. Download one PDF as an allowed account.
6. Only then ask GT which host to use. Do not enable billing, Turnstile-as-a-paid product, or a tutor provider in that step.

## Bundle after the 320px wrap

Measured in this workspace after `npm run build`. Budgets were not raised.

| Chunk | Brotli bytes | Limit |
| --- | ---: | ---: |
| Main | 45,396 | 48,000 |
| Vendor | 119,212 | 122,000 |
| CSS | 28,660 | 33,000 |
| Exam | 10,983 | 11,000 |
| All JS | 1,002,704 | 1,040,000 |

The exam chunk has 17 bytes of headroom. Do not add to that chunk casually.

## Catalog

Smart Review: **IMPLEMENTED, NOT PRODUCTION VERIFIED**. Dexter is not a chat tutor. This check does not approve question-bank content and does not promise a CSC result.
