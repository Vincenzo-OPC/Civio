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
