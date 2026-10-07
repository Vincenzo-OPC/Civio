# Legacy / one-off seed scripts

These scripts and SQL dumps came from the Hiraya → Civio desktop baseline.
They are kept for provenance and local bank rebuilds.

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
