# Bank milestone — 2026-10-22 (CONTINUE directive, BANK section)

Recounted from source files via `scripts/batches/audit/master_audit_2026_10_22.py` and `scripts/batches/qa/validate_flat_2100_manifest.py`.

| Tier | Count |
|---|---|
| Manifest rows (raw) | 2,100 |
| Unique (id + content) | 2,100 |
| Mechanically QA-valid (audit 0 unresolved issues) | 2,100 |
| Content-reviewed (status reviewed) | 42 |
| Approved (by GT, unchanged) | 1,377 |
| Active | 0 changed by this worker (no activation) |

Domains: Numerical 400, Analytical 400 (all professional), Verbal EN 400, Verbal FIL 300, Clerical 300 (all subprofessional), GI 300.

Replaced in manifest this cycle: 268 (231 weak/no explanation, 23 GI template padding, 9 numeric/analytical twins, 5 disputed ARMA filing variants).
New draft files (489 items): analytical-professional 127, gi-applied 90, numerical-series 13, subpro-clerical 50, subpro-filipino 50, subpro-math 60, verbal-en-organization-reading 99. Draft review queue: 489/489 pass.

Audit now also enforces: Analytical professional-only, Clerical subprofessional-only, difficulty/est_seconds present, why_correct + 3 why_wrong on every row. Two syllogism near-dup pairs (945/247, 956/253) were hand-checked and recorded as distinct (different premises/conclusions).

Pending human review: 723 non-approved rows (681 draft + 42 reviewed). Nothing self-approved.

## Update — 2026-10-22 afternoon

- **Legacy rows now checked inside `qa.check_item`** (`qa.legacy_errors`): GI rows must match a verbatim lawphil quote
  (`audit/gi_legacy_evidence_2026_10_22.py`, 90 hand-located quotes; `audit/verified_keys_2026_10_22.py`; or the row's own
  `source_quote`), numerical/verbal_en rows must match a hand-checked key (`audit/legacy_keys_2026_10_22.py`, 109 rows re-solved).
  The lawphil texts are committed under `docs/research/sources/lawphil/` so QA no longer depends on a box-local cache.
  217 of 217 legacy rows in the manifest pass.
- **Replaced 2** legacy GI drafts that could not be verified (no statute cited; placeholder "TO BE QUOTED" quote) with gi-applied drafts.
- **Deeper content QA on the 489 new drafts:** every math key re-solved by hand (73), all 7 syllogisms and 12 ordering/conditional
  items checked for validity, all 90 GI quotes found in the lawphil text, all 72 analogies read for a single same-order relation.
  Fixed: 1 analogy with no clean relation (seed : orchard, rebuilt), 1 analogy distractor that shared the stem relation (judge : court),
  1 table title (three vs four precincts), 1 GI key reworded to match its quote, 1 GI quote replaced with the clause that supports the key,
  decimal distractors on 6 whole-count word problems replaced with integer misconceptions.
- **Review packets:** 723 non-approved rows in 28 independent packets (`docs/research/review/packets-2026-10-22/`):
  P1 42, P2 84, P3 258, P4 339. Key and explanation sit in a separate answer sheet; decisions go in `decisions.csv`.
