# PHP runtime patch: CVE-2026-109618 / CVE-2026-109619 (22 Oct 2026)

## Advisory (independently verified)

| CVE | GHSA | Issue |
| --- | --- | --- |
| CVE-2026-109618 | GHSA-w8hw-w9fx-j79w | Out-of-memory bailout leaves request state partly initialised; memory corruption, RCE |
| CVE-2026-109619 | GHSA-6wmf-4rv5-p3rp | Stale request state after a fatal error; use-after-free in a later request on the same worker |

First fixed: **8.5.12, 8.4.27, 8.3.36, 8.2.35**. 8.1 and older get no fix.

**Exposure statement.** The PHP Foundation and vendor bulletins (AWS, Google Cloud, NCSC) confirm that remote code execution affects PHP-FPM through application-level code paths. Civio's image is PHP-FPM, and before this change it used the floating `8.4-fpm-nginx` tag, so any image built on PHP 8.4.0 to 8.4.26 was in the affected range. **We did not demonstrate an end-to-end exploit against Civio.** "Affected" here means the version is in the vulnerable range and the SAPI is the one vendors confirm, not that Civio was shown to be exploitable.

Sources: https://www.php.net/ChangeLog-8.php, https://github.com/php/php-src/blob/PHP-8.3/NEWS, https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/, https://aws.amazon.com/security/security-bulletins/2026-143-aws/, https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php

## Repository remediation (this PR)

- `Dockerfile` pins `serversideup/php:8.4.27-fpm-nginx-v4.5.3@sha256:f6768762…a512`. The registry config for that digest says `PHP_VERSION=8.4.27`.
- At build time, `scripts/security/assert-patched-php.php` makes the build fail if the base image runs a vulnerable PHP.
- The `tests` (8.4 and 8.5) and `lint` workflows check the PHP version on their runners.
- `tests/Unit/Security/PatchedPhpRuntimeTest.php` fails if the Dockerfile loses its pin, digest or guard, or if a workflow drops the check.
- The `php runtime security` workflow builds the image against 8.4.26 and expects the build to fail. It then builds the pinned image, smoke-tests it and runs migrations against a throwaway Postgres on the runner.

Merging this does **not** patch a running container.

## Runtime remediation on the MSI (NOT executed; needs GT's go-ahead)

This procedure touches only the `civio-local` project (app 8090, db 5434). It never touches 8080/5433, Hermes 8642, or the `civio_local_pgdata` volume. The commands work in PowerShell and in POSIX shells. Binary data never passes through a shell redirect, because PowerShell `>` re-encodes output and corrupts `pg_dump` files.

### 0. Choose the reviewed commit (not a blind `git pull main`)

Upgrade only to a reviewed commit: the merge commit of this PR (`REVIEWED_SHA`), or a branch that cherry-picks only the security commits onto the commit the MSI already runs.

```
git -C <civio checkout> rev-parse HEAD            # DEPLOYED_SHA: what the MSI was built from
git -C <civio checkout> fetch origin
git -C <civio checkout> diff --stat DEPLOYED_SHA REVIEWED_SHA
git -C <civio checkout> diff --name-only DEPLOYED_SHA REVIEWED_SHA
```

Continue only if every listed file is one of the following:
`Dockerfile`, `.github/workflows/lint.yml`, `.github/workflows/tests.yml`, `.github/workflows/php-runtime-security.yml`, `scripts/security/assert-patched-php.php`, `scripts/security/patched-php-minimums.php`, `tests/Unit/Security/PatchedPhpRuntimeTest.php`, `docs/security/PHP_RUNTIME_PATCH_2026-10-22.md`.

If main has moved on and the list contains other files, create a security-only branch and diff it again:

```
git checkout -b msi-php-patch DEPLOYED_SHA
git cherry-pick <security commit SHAs from this PR, oldest first>
git diff --name-only DEPLOYED_SHA HEAD            # must list only the files above
```

### 1. Check the current state (read-only)

```
docker exec civio-local-app php -v
docker image inspect civio-local-app --format "{{.Id}}"     # note it as OLD_IMAGE_ID
```

### 2. Back up the database (inside the container, then copy out)

```
docker exec civio-local-db pg_dump -U civio -d civio_local -Fc -f /tmp/civio_local_prepatch.dump
docker exec civio-local-db pg_restore --list /tmp/civio_local_prepatch.dump
docker exec civio-local-db sha256sum /tmp/civio_local_prepatch.dump
docker exec civio-local-db stat -c %s /tmp/civio_local_prepatch.dump
docker cp civio-local-db:/tmp/civio_local_prepatch.dump ./civio_local_2026-10-22_prepatch.dump
```

`pg_restore --list` must print a table of contents with no error. Then check the copy on the host:
- PowerShell: `Get-FileHash .\civio_local_2026-10-22_prepatch.dump -Algorithm SHA256` and `(Get-Item .\civio_local_2026-10-22_prepatch.dump).Length`
- POSIX: `sha256sum` and `stat -c %s`

The hash and the size must match the in-container values exactly; stop if they don't. Then remove the temporary copy: `docker exec civio-local-db rm /tmp/civio_local_prepatch.dump`.

### 3. Keep the old image for rollback

```
docker tag civio-local-app civio-local-app:pre-php-8.4.27
docker image inspect civio-local-app:pre-php-8.4.27 --format "{{.Id}}"   # must equal OLD_IMAGE_ID
```

### 4. Rebuild and restart the app only

```
git checkout REVIEWED_SHA        # or the msi-php-patch branch from step 0
docker compose -p civio-local -f docker-compose.local.yml build app
docker compose -p civio-local -f docker-compose.local.yml up -d --no-deps app
```

If the guard fails during the build, the old container keeps running. The entrypoint `scripts/00-laravel-deploy.sh` runs `php artisan migrate --force` on start. The security commits add no migrations, and the diff check in step 0 proves it.

### 5. Verify

```
docker exec civio-local-app php -v                                  # PHP 8.4.27
docker exec civio-local-app php scripts/security/assert-patched-php.php
docker exec civio-local-app php artisan --version
docker exec civio-local-app php artisan migrate:status              # no new pending or ran rows
docker volume ls                                                    # civio-local_civio_local_pgdata still listed
```

Open http://localhost:8090 and check that study progress is unchanged.

### 6. Rollback (if anything is wrong)

```
docker tag civio-local-app:pre-php-8.4.27 civio-local-app
docker compose -p civio-local -f docker-compose.local.yml up -d --no-deps app
```

Restore the database **only if its data was damaged**:

```
docker cp ./civio_local_2026-10-22_prepatch.dump civio-local-db:/tmp/restore.dump
docker exec civio-local-db pg_restore -U civio -d civio_local --clean --if-exists /tmp/restore.dump
docker exec civio-local-db rm /tmp/restore.dump
```

### 7. Verify the rollback worked (run it if step 6 was used)

```
docker image inspect civio-local-app --format "{{.Id}}"      # must equal OLD_IMAGE_ID
docker exec civio-local-app php -v                          # the pre-patch version again
docker exec civio-local-app php artisan --version
```

Reload http://localhost:8090 and check that progress is present. Keep the `.dump` file and the `pre-php-8.4.27` tag until GT confirms the upgrade.

Never run `docker compose down -v`, `docker volume rm` or `docker system prune` for this procedure.
