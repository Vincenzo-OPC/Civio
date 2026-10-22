# Civio Bank Reconciliation Report (2026-10-22)

## Crosscheck
- GitHub unique stems inventoried: 1,627
- CSE bot crosschecked the plan
- Exam engine (MockPoolSelector) blueprints and unique-item rules reviewed
- Approval gate confirmed (GT Ed25519 required)

## CSE bot flags (addressed where possible)
1. Domain split (GI 300 / Analytical 400) needs GT decision
2. Unique stems ≠ approved items (~1,478 approved this morning)
3. Prior stub commits had empty arrays — this commit records the reconciled batch
4. Avoid more pure percent-change; prefer applied GI
5. Tracks normalized to professional / subprofessional / both
6. Clerical kept on subprofessional or both

## Result
- 473 new draft items generated
- Projected unique total: ~2,110
- Domains land on clean hundreds
- All status = draft
- No import or activation performed

Full item JSON prepared locally. Independent review + GT signed approval still required.