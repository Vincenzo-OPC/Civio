# Draft review queue (22 Oct 2026)

Mechanical QA of every non-approved item in the bank JSON on `main` (a0123fb). **No status was changed, nothing was approved, and no content was rewritten.** Every finding is a flag for CoS/GT review.

- Script: `scripts/batches/qa/draft_review_queue_2026_10_22.py` (reproducible).
- Per-item CSV: `docs/research/bank/draft-review-queue-2026-10-22.csv`. Order: GI, Clerical, Numerical, Analytical, Verbal EN, Verbal Fil. Columns: result, reasons, adds_unique, recommended.
- Summary JSON: `docs/research/bank/draft-review-queue-2026-10-22.json`.

## Scope

2024 non-approved rows deduped to **1943 unique stems**. The raw legacy dump `baseline-550-2026-10-17.json` is excluded because its converted copy (`-spec`) is reviewed instead. Kinds:

- **new**: adds a stem not yet in the bank.
- **revision**: a lint fix or baseline replacement that changes the stem.
- **revision_of_approved**: a fix to an approved item with the same stem. It replaces that item and adds nothing.
- **baseline**: the 550 converted legacy rows, served today but never approved under the spec.

True approved unique count: **1477** (GI 236, Clerical 207, Numerical 309, Analytical 251, Verbal EN 286, Verbal Fil 188).

## Pass/flag by subject

| Subject | Unique drafts | Pass | Flag | new | revision | rev. of approved | baseline |
|---|---|---|---|---|---|---|---|
| GI | 320 | 120 | 200 | 117 | 24 | 45 | 134 |
| Clerical | 361 | 200 | 161 | 228 | 15 | 38 | 80 |
| Numerical | 259 | 167 | 92 | 141 | 27 | 0 | 91 |
| Analytical | 472 | 266 | 206 | 287 | 5 | 66 | 114 |
| Verbal EN | 357 | 119 | 238 | 147 | 5 | 77 | 128 |
| Verbal Fil | 174 | 160 | 14 | 127 | 24 | 22 | 1 |

## Defects found (blocking unless noted)

- `missing_est_seconds` (554): Baseline-550 rows have no difficulty or est_seconds. This is metadata only, but they can't go active until it is filled in.
- `near_dup_approved` (246): Lint-fix revisions sit 0.9 or more token-Jaccard from the approved item they fix. That is expected, so it doesn't block them.
- `place_or_amount_swap_clone` (143): **Filler clones**: the same stem with only a city, amount or "Session/Set/Item N" changed, and the same key. Almost all are in `civio-exact-flat-cleaned` (118 of its 122 items), then `civio-fixed-flat-final` (24) and `civio-flat-2100` (1). Examples: CIVIO-EXACT-0051..0053 "Select the opposite of \"abundant\" (vocabulary Set 51/52/53)"; CIVIO-CLEAN-0075..0092 "offered ₱3,000…₱15,750 to speed up a permit" in 18 cities.
- `near_dup_draft` (107): Near-duplicate of another draft (mostly the flat files copying each other).
- `previously_rejected` (99): Already rejected in the ChatGPT batch 002/003 reviews.
- `place_swap_clone` (53): Identical stem skeleton and identical options, with only the place name different (`civio-fixed-flat-final`).
- `duplicate_options` (20): Two identical options, for example CIVIO-CLEAN-0060 with "liaison" twice (19 in `civio-fixed-flat-final`, 1 baseline).
- `passage_missing_or_unlinked` (19): Reading item with no linked passage (baseline).
- `percent_change_topic` (18): Information only: percent-change topic. The bank is already over the cap of 40 (56 approved plus 5 reviewed).
- `circular_reveal` (17): The explanation only restates the key ("R.A. 6713 §x requires: <key>"); 17 in `civio-final-rewrite`.
- `template_stem_place_name` (15): "Select the correctly spelled word for use in an official <City> document": the city adds nothing.
- `key_not_in_reveal` (10): Numerical baseline items whose explanation never states the answer (empty reveal).
- `difficulty_vs_time` (9): Information only: labelled hard at 25 s or less, or easy at 90 s or more. The reviewer sets the level.
- `gi_citation_doubt` (8): R.A. 6713 section cited wrongly: nepotism cited as §7(a) (it is EO 292 Bk V §59), share conflicts as §7(b) (that is §9 divestment), and late SALN with a remedy §8 does not give (CIVIO-2100-0111/0112/0114/0119 and FINAL equivalents).
- `superseded_by_lintfix` (4): A baseline row already has a lint-fixed revision. Review the revision instead.
- `gi_fact_doubt` (1): CIVIO-FINAL-0118: late-SALN remedy attributed to §8.
- `options_shape` (1): CIVIO-FINAL-2000-0001 uses `id` instead of `option_id`, and its math is wrong (527.4 sacks).
- `track_noncanonical` (1): One track label is not professional/subprofessional/both.

Not found: mojibake, "(variant N)" text, keys outside the options, HOLD-source markers (Mutia-Tayone, CSEReviewer.com, recalled items), or arithmetic key errors in the computable items.

GI fact spot-check: rules for 15 Constitution and R.A. 6713 facts were checked against the official texts (1987 Constitution Arts. III, V, VI, VII, VIII, IX-B; R.A. 6713 §§5, 7, 8, 9). Doubts are flagged above. Every flagged item still needs a human check.

## By file

| File | Pass | Flag |
|---|---|---|
| baseline-550-spec-2026-10-18.json | 0 | 549 |
| gap-fill-2000-06-lintfix.json | 203 | 14 |
| civio-flat-2100-2026-10-22.json | 117 | 5 |
| civio-fixed-flat-final-2026-10-22.json | 25 | 97 |
| civio-exact-flat-cleaned-2026-10-22.json | 4 | 118 |
| civio-final-rewrite-2026-10-22.json | 98 | 17 |
| gap-fill-2000-02.json | 108 | 0 |
| gap-fill-2000-03.json | 101 | 0 |
| gap-fill-2000-01.json | 99 | 0 |
| chatgpt-batch-002.json | 0 | 88 |
| gap-fill-2000-04.json | 83 | 0 |
| gap-fill-2000-05-lintfix.json | 70 | 11 |
| batch-subpro-num-001.json | 50 | 0 |
| round-03-baseline-b3-drafts.json | 44 | 0 |
| gap-fill-2000-05.json | 15 | 0 |
| chatgpt-batch-003.json | 0 | 11 |
| original-foundations-10-draft.json | 10 | 0 |
| round-03-baseline-b4-drafts.json | 5 | 0 |
| civio-syllabus-aligned-final-drafts-2026-10-22.json | 0 | 1 |

## Recommended 'ready for CoS/GT sign-off' set (GT split)

Picked from passing items that add a unique stem, in this order: CoS-pipeline gap-fill-2000 files first, then round-03 replacements, then the flat/rewrite files. Within Verbal, English comes first. Rows are marked `recommended=yes` in the CSV.

| Subject | Approved | Passing adds available | Recommended | Projected if signed | GT target | Shortfall |
|---|---|---|---|---|---|---|
| Verbal (EN+Fil) | 474 | 176 | 126 | 600 | 600 | 0 |
| Numerical | 309 | 167 | 91 | 400 | 400 | 0 |
| GI | 236 | 73 | 73 | 309 | 400 | 91 |
| Analytical | 251 | 196 | 49 | 300 | 300 | 0 |
| Clerical | 207 | 147 | 93 | 300 | 300 | 0 |
| **Total** | **1477** | | **432** | **1909** | **2,000** | **91** |

Verbal split: EN 49 + Fil 77.

**General Information is the only shortfall (91).** The 134 baseline GI rows fail only on missing difficulty/est_seconds metadata. Filling that metadata and reviewing them could cover the gap. Their author is unknown (legacy import), so they need a provenance check against the HOLD list first. Otherwise, new GI items must be written and approved against the design spec.

## Recommendations

1. Retire `civio-exact-flat-cleaned-2026-10-22.json` and the cloned part of `civio-fixed-flat-final-2026-10-22.json` (filler clones break the no-clones rule).
2. Fix the R.A. 6713 citations and circular explanations in `civio-final-rewrite` / `civio-flat-2100` before review.
3. CoS reviews the recommended set by subject, then GT signs per batch. Nothing is activated before that.
4. Decide on the GI gap: add metadata to and review the baseline GI rows, or commission new GI items.
