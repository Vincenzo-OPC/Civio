# Legacy / one-off seed scripts

These scripts and SQL dumps came with the desktop baseline (`d3f0368`).
They are kept for local bank rebuilds.

**Do not run against production without review.**
**Do not add new question stems here without an approved pass of**
`docs/CSE-Question-Design-Spec.md`.

Preferred long-term home for repeatable seeds is `database/seeders/`.

## Importing SQL safely (UTF-8)

The `.sql` files here are UTF-8 and contain symbols such as × ÷ − √ ² ≤ ≥ ₱
and curly quotes. Each file starts with `SET client_encoding = 'UTF8';`.

- Linux / macOS / WSL: `psql -v ON_ERROR_STOP=1 -d <db> -f scripts/seeds/<file>.sql`
- Windows: `.\scripts\import-sql-utf8.ps1 -SqlFile <file> -Container <db-container> -Database <db> -User <user>`
- **Never** `Get-Content <file>.sql | docker exec -i <db> psql ...` in Windows
  PowerShell 5.1. It reads BOM-less UTF-8 as Windows-1252 and pipes it as
  US-ASCII, turning every non-ASCII byte into `?`. That pipe is the root cause
  of the desktop bank's `??` math-symbol bug.

## Repairing rows that already lost symbols

```bash
php artisan civio:repair-bank-encoding --dry-run   # report only
php artisan civio:repair-bank-encoding             # apply (idempotent)
```

It restores text only from an exact match against these UTF-8 seed files (or
`--reference=<file.sql|.php|.json>`), or when arithmetic such as `12 ?? 3 = 36`
allows exactly one operator. Rows it cannot repair safely are listed by ID.

## Removing "(variant N)" clones

Older copies of `seed_real_practice.php` saved each item 8 times with
" (variant N)" on the stem. The script now saves one copy per item. To clean a
bank that already has clones:

```bash
php artisan civio:remove-variant-clones --dry-run   # report only
php artisan civio:remove-variant-clones             # delete or archive (idempotent)
```

Unreferenced clones are deleted. Clones used by attempts, saved drills or
feedback are set to `draft`, so they leave the active pool. For a database whose
app lacks the command, `remove_variant_clones.sql` does the same in Postgres
(see `docs/DESKTOP_PATCHES_TO_PORT.md`).


## Source groups

Items from these seeds are `questions.source_group = baseline`. The PHP seed
scripts set it; for the raw SQL files run `php artisan civio:tag-source-groups`
after importing. See `docs/QUESTION_SOURCE_GROUPS.md`.
