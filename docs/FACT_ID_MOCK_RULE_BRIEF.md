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

## Addendum (CoS 2026-10-17): more fact IDs and a theme cap

**More fact IDs.** The 10 gap-fill-004 items (`docs/research/gap-fill-004.json`) each carry a `FACT-RA…` fact_id. None has a twin yet, but the importer should save them.

**Theme cap.** CoS ruled that no mock may serve more than 2 items with the same `theme`. Today one theme is tagged: `first-measure-misleads`, on 8 of the 12 approved chatgpt-batch-002 RC items (050002, 050005, 050011, 050012, 050015, 050020, 050022, 050023). Spec v0.1.9 §10.8 defines the field.

6. Add a migration for a nullable, indexed `questions.theme` column (string, 100), and have `civio:import-batch` save `$item['theme'] ?? null`. Re-importing chatgpt-batch-002 backfills it, because the importer matches on stem.
7. In `MockPoolSelector` / `MockPoolState`, count picks per non-null theme and skip a candidate once its theme has 2 picks in the session. The rule applies to every mock and to the quota fallback, the same way as the fact_id rule. A null theme means no constraint.
8. Add a Pest test: in a pool with 5 same-theme RC items, every mock holds at most 2 of them.

Until this ships, a Verbal mock could draw more than 2 of the 8 themed items. They are among about 590 active Verbal items, so the risk is low.

## Addendum 2 (CoS 2026-10-17, 3:43 PM): a real `passage_id` field

Reading passages now come in sets of 2–3 questions (spec v0.1.9, §10.8). Each item carries the full passage in its stem, and today siblings are tagged only in `notes` ("Passage gap-fill-005-P01, question 1 of 3"). gap-fill-005 has 7 sets, all active on the MSI.

9. Add a migration for a nullable, indexed `questions.passage_id` column (string, 100). `civio:import-batch` should save `$item['passage_id'] ?? null`, and, until the batch files carry the field, parse it from the `notes` tag `Passage <id>, question k of m`.
10. Mock rule: serve at most one question per `passage_id` per mock, so a reader never sees the same passage twice in one session. Alternatively, serve the whole set together, if the UI can show a shared passage. The simpler version is one per mock. Drills can serve whole sets.
11. Add a Pest test: in a pool with one 3-question set, a mock contains at most 1 of the 3.

Grok Bot keeps the `notes` tag until this ships, then backfills `passage_id` into the batch JSON.

## Not in scope

- No change to approved item text.
- No deploy.

Until this ships, the 8 variants can land in the same mock as their twins. That is a low risk: there are 8 pairs in a GI pool of about 400.
