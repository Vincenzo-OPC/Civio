# Strict mock browser E2E (Playwright, Chromium)

`tests/E2E/playwright/strict-mock.spec.ts` drives a real headless Chromium against a local app server (`php artisan serve` on port 8123). Each scenario starts as a fresh guest:

1. **Offline reload:** answer item 1 online, go offline and answer item 2, close the tab, reconnect and reopen `/exams`. Item 2 is restored with a notice and saved, item 1 is kept, and the local copy is cleared.
2. **Two tabs:** both tabs resume the same mock. Tab A saves, then tab B's stale save gets a 409, re-reads, retries once and shows the merge notice. Both answers end up on the server.
3. **Deadline while offline:** the deadline is moved to 4 s ahead and passes while offline. On reconnect the late save is refused with 409 and "Time is up" shows. A final submit that still carries the late answer is graded on saved answers only.
4. **Double submit:** two concurrent submits give exactly one 200 and one refusal, and only one attempt exists. A later retry and any further save return 409. A refresh does not resume the exam and the local resume copy is cleared.
5. **Withdrawn mid-mock:** an item retired during the mock is marked "withdrawn, not scored" on the exam screen as soon as a save reports it, and again after a reload. Its answer is never saved and no key is sent.

Every scenario also checks that no key or explanation reaches the browser before submit.

## Database isolation (required)

The E2E only ever uses a **throwaway SQLite file in a temp directory**. It is never run against the production database, the local study app database (Postgres on :5433, app on :8080), or Civio's local database on :5434.

- `playwright.config.ts` sets `DB_CONNECTION=sqlite`, `DB_DATABASE=$E2E_DB` and a blank `DB_URL` for the app server and PHP helpers only. `E2E_DB` defaults to `<os temp dir>/civio-e2e.sqlite`; CI uses `$RUNNER_TEMP/civio-e2e.sqlite`.
- `tests/E2E/db-guard.mjs` **aborts the run** unless all of these hold:
    - `DB_CONNECTION` is `sqlite`;
    - `DB_DATABASE` equals `E2E_DB`;
    - the file is named `civio-e2e*.sqlite` and lives inside the OS temp dir or `RUNNER_TEMP`;
    - `DB_URL` is empty;
    - none of `DB_PORT`, `BASE_URL` or `APP_URL` points at 5432, 5433, 5434 or 8080.
- The guard runs when the config loads, in `setup-db.mjs` before the file is deleted and migrated, and before every PHP helper call. `tests/Js/e2e-db-guard.test.ts` covers the guard.
- `setup-db.mjs` deletes and recreates the file on every run, migrates it and seeds 24 active questions.
- The server is never reused (`reuseExistingServer: false`). If something is already on port 8123, the run fails rather than testing against an unknown database.

**Pest cannot inherit the E2E settings.** `phpunit.xml` forces in-memory SQLite and array session/cache, in both `<env>` and `<server>` (Laravel reads `$_SERVER` first). `tests/Feature/TestDatabaseIsolationTest.php` fails if that ever stops holding. Before this change, a Pest run in a shell that exported the E2E variables wiped the E2E file.

## Run locally

```bash
npm ci
npx playwright install chromium     # once
npm run build
npm run test:e2e                    # starts the server, seeds the throwaway DB, runs Chromium
```

Do not `export` any `DB_*` variables for this. The config sets them for its own processes.

## CI

`.github/workflows/e2e.yml` runs on pushes and pull requests to `main`, and also manually. Its setup:

- Chromium only, with the browser cached by Playwright version.
- PHP 8.4 and the throwaway SQLite file in `$RUNNER_TEMP`.
- No secrets, no external database, no Netlify and no deploy.
- Traces are uploaded only on failure.

`@playwright/test` is a devDependency only, and nothing under `resources/` imports it, so the production bundle does not change.
