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

## Late-afternoon update (22 Oct 2026, after 2:55 PM directive)

- **Verbal EN:** 12 new original passages (158–185 words), 4 questions each = 48 drafts (`verbal-en-reading-set2-2026-10-22.json`) covering main idea, detail, inference, vocabulary in context, author's purpose and relation between parts. The 7 short-passage drafts (CIVIO-GF2K05-RCD-0001/0002, RCI-0001/0002, RCM-0001/0002, RCV-0001) were swapped out for RC2 items; 41 RC2 items stay as spares.
- **Clerical:** 40 Subpro-only spare drafts (`subpro-clerical-set2-2026-10-22.json`): 12 spelling, 12 alphabetic filing (ARMA Rules 1, 2, 8), 6 chronological, 4 numeric filing (Rule 7), 6 copy-check. Spec proposals pending CoS: archetypes CLR-CHRONOLOGICAL and CLR-COPY-CHECK, distractor code CLR-COPY-MISMATCH.
- **Numerical method-first:** `reveal.method_steps` (asked, givens, method, why, solve by hand, check, distractors, shortcut) added in place to all 76 non-D1022 numerical draft rows (the 25 D1022 drafts already had them). Hashes refreshed by the swap script, now for every draft row. 59 approved rows got -R1 proposals only (`audit/fixes/method-first-r1-proposals-2026-10-22.json`, content and key unchanged, not in the manifest). Not yet covered: 42 reviewed rows (batch-subpro-num-001) and about 240 other approved rows (no template yet).
- **Flags for review:** signoff-replacements-2026-10-22 has template padding (5 near-identical rectangle-edging items, 3 near-identical chair-discount items), and gap-fill-2000-02 has 20 templated order-of-operations items. These are drafts only.
- **Manifest:** 2,100 (Num 400, Ana 400, VEN 400, VFIL 300, CLR 300, GI 300); percent-change rows 40/40; validator 0 problems; master audit Counter().
