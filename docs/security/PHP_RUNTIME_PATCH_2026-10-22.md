# PHP runtime patch: CVE-2026-109618 / CVE-2026-109619 (22 Oct 2026)

## Advisory (independently verified)

| CVE | GHSA | Issue |
| --- | --- | --- |
| CVE-2026-109618 | GHSA-w8hw-w9fx-j79w | Out-of-memory bailout leaves request state partly initialised; memory corruption, RCE |
| CVE-2026-109619 | GHSA-6wmf-4rv5-p3rp | Stale request state after a fatal error; use-after-free in a later request on the same worker |

First fixed: **8.5.12, 8.4.27, 8.3.36, 8.2.35**. 8.1 and older get no fix. RCE was confirmed on PHP-FPM through application code paths, so Civio's FPM image was affected while it ran 8.4.0 to 8.4.26.

Sources: https://www.php.net/ChangeLog-8.php, https://github.com/php/php-src/blob/PHP-8.3/NEWS, https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/

## Repository remediation (this PR)

- `Dockerfile` pins `serversideup/php:8.4.27-fpm-nginx-v4.5.3@sha256:f6768762…a512`. The registry config for that digest says `PHP_VERSION=8.4.27`.
- At build time, `scripts/security/assert-patched-php.php` makes the build fail if the base image runs a vulnerable PHP.
- The `tests` (8.4 and 8.5) and `lint` workflows check the PHP version on their runners.
- `tests/Unit/Security/PatchedPhpRuntimeTest.php` fails if the Dockerfile loses its pin, digest or guard, or if a workflow drops the check.
- The `php runtime security` workflow builds the image against 8.4.26 and expects the build to fail. It then builds the pinned image, smoke-tests it and runs migrations against a throwaway Postgres on the runner.

Merging this does **not** patch a running container.

## Runtime remediation on the MSI (NOT executed; needs GT's go-ahead)

This procedure touches only the `civio-local` project (app on 8090, db on 5434). It never touches 8080/5433, Hermes on 8642, or the `civio_local_pgdata` volume. Run it in PowerShell or a shell in the Civio checkout.

1. **Check the current state (read-only).**
   `docker exec civio-local-app php -v` shows whether it runs 8.4.26 or older.
   `docker image inspect civio-local-app --format '{{.Id}}'` gives you the image ID; note it down.
2. **Back up the database** (logical dump; the database keeps running):
   `docker exec civio-local-db pg_dump -U civio -d civio_local -Fc > civio_local_2026-10-22_prepatch.dump`
   Confirm the file isn't empty, then run `docker exec -i civio-local-db pg_restore -l < civio_local_2026-10-22_prepatch.dump` to list its contents.
3. **Tag the current image so you can roll back:** `docker tag civio-local-app civio-local-app:pre-php-8.4.27`
4. **Update the code:** `git fetch && git checkout main && git pull` (after the PR merges).
5. **Rebuild the app only. Leave the db alone.**
   `docker compose -p civio-local -f docker-compose.local.yml build app`
   If the guard fails here, the old container keeps running.
   `docker compose -p civio-local -f docker-compose.local.yml up -d --no-deps app`
   Note: the entrypoint `scripts/00-laravel-deploy.sh` may run migrations on start. This PR adds no migrations.
6. **Verify.**
   - `docker exec civio-local-app php -v` should show `PHP 8.4.27`.
   - `docker exec civio-local-app php scripts/security/assert-patched-php.php`
   - `docker exec civio-local-app php artisan --version`
   - Open http://localhost:8090 and check that your study progress is still there.
   - `docker volume ls` should still list `civio-local_civio_local_pgdata`.
7. **Roll back if anything is wrong.**
   `docker tag civio-local-app:pre-php-8.4.27 civio-local-app && docker compose -p civio-local -f docker-compose.local.yml up -d --no-deps app`
   Restore the database only if its data was damaged: `docker exec -i civio-local-db pg_restore -U civio -d civio_local --clean --if-exists < civio_local_2026-10-22_prepatch.dump`

Never run `down -v`, `volume rm` or `system prune`.
