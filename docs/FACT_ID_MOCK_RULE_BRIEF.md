# Brief for Astra or Codex: one item per fact in each mock

Requested by: Chief of Staff, round 03 verdict, 2026-10-17. Written by Grok Bot. I touched no app code.

## Why

CoS accepted 8 GI items from `docs/research/chatgpt-batch-003.json` as **variants**: each is an applied scenario on a fact the approved bank already tests as a recall item. CoS keeps both formats so they can be used in different mocks. They must never appear in the same mock, because one would give the other away.

## What is already done (data only)

- Each pair (or trio) shares a `fact_id` in the batch JSON:

| fact_id | Items |
|---|---|
| FACT-CONST-II-3-CIVILIAN-SUPREMACY | GI-SCENARIO-APPLY-060001, GI-TERM-MATCH-000507 |
| FACT-CONST-IXB-2-2-MERIT-APPOINTMENT | 060017, 000909 |
| FACT-CONST-IXB-2-4-NO-PARTISAN-POLITICS | 060019, 000303 |
| FACT-CONST-IXB-2-5-SELF-ORGANIZATION | 060020, 000902 |
| FACT-RA6713-4A-G-ACCOUNTABILITY | 060057, 001003 |
| FACT-RA6713-9-DIVESTMENT-60-DAYS | 060075, 000502, 001008 |
| FACT-RA9003-SEGREGATION-AT-SOURCE | 060076, CIVIO-GI-20261013-0002 |
| FACT-RA8749-2-PRINCIPLE | 060084, CIVIO-GI-20261013-0008 |

- `scripts/batches/fixes/b3/verdict.py` writes these tags. The tags exist only in JSON. **The DB has no column for them, and `civio:import-batch` ignores `fact_id`.**

## What to build

1. Add a migration for a nullable, indexed `questions.fact_id` column (string, 100).
2. In `ImportBatchCommand::upsert`, save `$item['fact_id'] ?? null`. Re-importing the batch files listed above should then backfill the bank twins, because the importer matches on stem.
3. Make `MockPoolSelector` / `MockPoolState` keep a set of fact_ids already picked for the session and skip any candidate whose non-null `fact_id` is in that set. This applies in both `pickBalanced` and `pickFlat` and works like the existing stem-prefix spread. A null `fact_id` means no constraint.
4. Expose `fact_id` in the selector row (server-side only, like `correct`) so the rule can run.
5. Add a Pest test: build a pool where two items share a fact_id and are the only items in their subcategory quota, then assert that a mock never contains both, including when the quota falls back.

## Not in scope

- No change to approved item text.
- No deploy.

Until this ships, the 8 variants can land in the same mock as their twins. That is a low risk: there are 8 pairs in a GI pool of about 400.
