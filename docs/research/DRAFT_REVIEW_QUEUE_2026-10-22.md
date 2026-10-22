# Draft review queue (22 Oct 2026, updated after clone retirement and baseline GI fix)

Mechanical QA of every non-approved item in the bank JSON. **No status was changed to approved and no content was rewritten.** GT-approved changes in this pass:

- **Retired 195 filler clones** to `docs/research/bank/retired/filler-clones-2026-10-22.json` (status `retired`, reason `filler_clone`, `clone_of` recorded). One representative per group stays in its source file.
- **Baseline GI (134 rows):** HOLD-screened against all 9 HOLD files, with `CSE Reviewer.pdf` read by OCR. No verbatim match. 2 rows are flagged `hold_phrase_overlap`. Difficulty and est_seconds were added by rule: 114 easy at 30 s and 20 medium at 45 s, within the approved GI range of 20–70 s. Fact spot-check: SALN timing (30 days, April 30, 30 days after separation), 15 working days, three signatories and Art. VII §19 impeachment all match R.A. 6713 §§5 and 8 and the 1987 Constitution. Status stays draft. Result: 132 pass, 2 flag.

Script: `scripts/batches/qa/draft_review_queue_2026_10_22.py`, rendered by `draft_review_report_2026_10_22.py`. Per-item CSV: `docs/research/bank/draft-review-queue-2026-10-22.csv` (GI, then Clerical, then the rest).

## Scope

1829 non-approved rows reduce to **1754 unique stems**. The approved unique count is **1477** (GI 236, Clerical 207, Numerical 309, Analytical 251, Verbal EN 286, Verbal Fil 188).

## Pass/flag by subject

| Subject | Unique drafts | Pass | Flag | new | revision | rev. of approved | baseline |
|---|---|---|---|---|---|---|---|
| GI | 287 | 273 | 14 | 84 | 24 | 45 | 134 |
| Clerical | 297 | 200 | 97 | 164 | 15 | 38 | 80 |
| Numerical | 259 | 167 | 92 | 141 | 27 | 0 | 91 |
| Analytical | 390 | 273 | 117 | 205 | 5 | 66 | 114 |
| Verbal EN | 347 | 119 | 228 | 137 | 5 | 77 | 128 |
| Verbal Fil | 174 | 160 | 14 | 127 | 24 | 22 | 1 |

## Open defects

- `missing_est_seconds` (420): Baseline-550 rows outside GI still have no difficulty or est_seconds (metadata only).
- `near_dup_approved` (246): Lint-fix revisions close to the approved item they fix. Expected, and not blocking for revisions.
- `previously_rejected` (99): Already rejected in the ChatGPT batch 002/003 reviews.
- `near_dup_draft` (23): Near-duplicate of another draft.
- `passage_missing_or_unlinked` (19): Baseline reading item with no linked passage.
- `percent_change_topic` (18): Information only: the bank is already over the percent-change cap of 40.
- `duplicate_options` (11): Two identical options, e.g. CIVIO-CLEAN-0060 with "liaison" twice.
- `template_stem_place_name` (10): "…for use in an official <City> document": the place name adds nothing.
- `key_not_in_reveal` (10): Numerical baseline items whose explanation never states the answer.
- `difficulty_vs_time` (9): Information only: the label and the time disagree.
- `superseded_by_lintfix` (4): A baseline row has a lint-fixed revision. Review that instead.
- `hold_phrase_overlap` (2): Baseline GI 0006 (the R.A. 6713 title) and 0056 (the Art. II §1 quote) share 20–30% of their 5-grams with a HOLD file. That is public statutory text, but a human must confirm.

Not found: mojibake, "(variant N)", keys outside the options, HOLD-source markers, or arithmetic key errors in the computable items.

## By file

| File | Pass | Flag |
|---|---|---|
| baseline-550-spec-2026-10-18.json | 132 | 417 |
| gap-fill-2000-06-lintfix.json | 203 | 14 |
| civio-flat-2100-2026-10-22.json | 121 | 1 |
| civio-final-rewrite-2026-10-22.json | 121 | 0 |
| gap-fill-2000-02.json | 108 | 0 |
| gap-fill-2000-03.json | 101 | 0 |
| gap-fill-2000-01.json | 99 | 0 |
| chatgpt-batch-002.json | 0 | 88 |
| gap-fill-2000-04.json | 83 | 0 |
| gap-fill-2000-05-lintfix.json | 70 | 11 |
| batch-subpro-num-001.json | 50 | 0 |
| civio-fixed-flat-final-2026-10-22.json | 26 | 19 |
| round-03-baseline-b3-drafts.json | 44 | 0 |
| gap-fill-2000-05.json | 15 | 0 |
| chatgpt-batch-003.json | 0 | 11 |
| original-foundations-10-draft.json | 10 | 0 |
| round-03-baseline-b4-drafts.json | 5 | 0 |
| civio-exact-flat-cleaned-2026-10-22.json | 4 | 0 |
| civio-syllabus-aligned-final-drafts-2026-10-22.json | 0 | 1 |

## Recommended 'ready for CoS/GT sign-off' set (GT split)

Order: gap-fill-2000 files, then round-03 replacements, then baseline GI, then flat/rewrite files. Verbal takes English first. Rows are marked `recommended=yes`.

| Subject | Approved | Passing adds available | Recommended | Projected if signed | Target | Shortfall |
|---|---|---|---|---|---|---|
| Verbal (EN+Fil) | 474 | 176 | 126 | 600 | 600 | 0 |
| Numerical | 309 | 167 | 91 | 400 | 400 | 0 |
| GI | 236 | 226 | 164 | 400 | 400 | 0 |
| Analytical | 251 | 203 | 49 | 300 | 300 | 0 |
| Clerical | 207 | 147 | 93 | 300 | 300 | 0 |
| **Total** | **1477** | | **523** | **2000** | **2,000** | **0** |

Verbal split: EN 49 + Fil 77. GI draws on baseline rows: about 107 of the 164 recommended GI items.

## Next

1. Fix the R.A. 6713 citations and circular explanations (`civio-final-rewrite`, `civio-flat-2100`).
2. A human checks the 2 `hold_phrase_overlap` rows.
3. CoS reviews the recommended set by subject, then GT signs per batch. Nothing is activated before that.
4. Baseline rows outside GI still need metadata before they can count.
