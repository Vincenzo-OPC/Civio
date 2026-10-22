# P1 Subprofessional Numerical: independent AI review recommendation (2026-10-22)

**Source:** `docs/research/review/packets-2026-10-22/P1-numerical-01.md` (40), `P1-numerical-02.md` (2), and canonical `docs/research/batch-subpro-num-001.json`.

**Reviewer:** ChatGPT GPT-6, additional AI content check. **This is NOT GT's human approval, signature, status change or a completed independent-human review.** Do not enter ACCEPT as GT in `decisions.csv`, mark approved, import, or activate based solely on this memo.

## Findings

- All 42 keyed answers agree with an independent arithmetic working shown below. Each has four different answer options, a `reveal.shortcut`, `why_correct`, and three `why_wrong` entries in the canonical source. The supplied values admit one correct listed answer.
- **41 ACCEPT recommendations; 1 minor REVISE** (`CIVIO-NUM-WP-ALGEBRA-926041`). Its answer of 12 is mathematically correct, but a 12-year-old "speech therapist trainee" is an implausible real-world setting. Suggest changing the relationship to "A teacher is 21 years older than a student" with age relations unchanged. Recheck the explanations after that edit. This is a quality edit, not a wrong key.
- The separate **seven English reading passages below 150 words** remain a bank-wide specification gap. Add a word-count check that fails CI/QA for all applicable new/pending reading passages, then repair those passages without changing answer validity or duplicating material. This does not block review of this numerical P1 group.
- Existing review/approval gate stays intact. No production deployment, no DB activation, no status mutation.

## Per-item key verification

| ID | Key | Independent working | Recommendation |
|---|---|---|---|
| `CIVIO-NUM-FRAC-DEC-926001` | 5/8 meter | 7/8 − 1/4 = 5/8 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926002` | 27 seats | 72 × 3/8 = 27 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926003` | 3/5 | 3/5 = 0.6 > 7/12, 4/7, 5/9 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926004` | 17/7 | 2 + 3/7 = 17/7 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926005` | 8 bags | 6 ÷ (3/4) = 8 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926006` | 72 blankets | 45 ÷ (5/8) = 72 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926007` | 4 servings | (3/2) ÷ (3/8) = 4 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926008` | 3 5/6 kilograms | 1 2/3 + 2 1/6 = 3 5/6 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926009` | 1/2 | 1 − 3/10 − 1/5 = 1/2 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926010` | 5/8 | 0.625 = 625/1000 = 5/8 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926011` | 18 seedlings | 45 × 2/3 × 3/5 = 18 | ACCEPT recommendation |
| `CIVIO-NUM-FRAC-DEC-926012` | 2 kilometers | (8/3) × (3/4) = 2 | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926013` | 54 notebooks | 360 × 15/100 = 54 | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926014` | 30% | 18/60 = 30% | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926015` | 288 files | 72 ÷ 25% = 288 | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926018` | 68% | (20 × 80% + 30 × 60%)/50 = 68% | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926019` | 90% | 72/80 = 90% | ACCEPT recommendation |
| `CIVIO-NUM-PCT-BASIC-926022` | 20 children | 400 × 30% − 250 × 40% = 20 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926033` | 32 folders | 49 − 17 = 32 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926034` | 11 beads | 3(x + 4) = 45 ⇒ x = 11 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926035` | 41 kilometers | longer route = (68 + 14)/2 = 41 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926036` | 40 | consecutive even 38 + 40 = 78 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926038` | 8 booklets | (400 − 120)/35 = 8 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926039` | 30 kilograms | x − 12 = x/2 + 3 ⇒ x = 30 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926040` | 10 beads | 2(x + 6) + x = 42 ⇒ x = 10 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926041` | 12 years | (t + 21 − 5) = 4(t − 5) ⇒ t = 12 | REVISE (context only) |
| `CIVIO-NUM-WP-ALGEBRA-926042` | 17 years | today sum = 48 − 8 = 40; (40 − 6)/2 = 17 | ACCEPT recommendation |
| `CIVIO-NUM-WP-ALGEBRA-926048` | ₱240 | 1200 − 18 × 45 − 6 × 25 = 240 | ACCEPT recommendation |
| `CIVIO-NUM-WP-AVERAGE-926049` | ₱51 per kilogram | (3 × 45 + 2 × 60)/5 = 51 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926029` | ₱650 | 390 ÷ 6 × 10 = 650 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926030` | 10 hours | 8 × 15 / 12 = 10 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926031` | 30 kilometers | 7.5 × 4 = 30 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926043` | 400 kits | 360/(3 × 6) × 5 × 4 = 400 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926044` | 4 4/5 hours | 1/(1/8 + 1/12) = 24/5 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926045` | 2 1/2 hours | 120/(72 ÷ 1.5) = 2.5 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926046` | 33 1/3 km/h | 100/(50/50 + 50/25) = 100/3 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATE-926047` | ₱234 | 18 × (35 − 22) = 234 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATIO-926025` | 35 stools | 55/(4 + 7) × 7 = 35 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATIO-926026` | 48 sacks | 30/5 × 8 = 48 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATIO-926027` | 8 cups | 20/5 × 2 = 8 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATIO-926028` | 50 kits | 100/(2 + 3 + 5) × 5 = 50 | ACCEPT recommendation |
| `CIVIO-NUM-WP-RATIO-926032` | 4 crates | 36/(4 + 5) × (5 − 4) = 4 | ACCEPT recommendation |

## Next steps

1. Apply the single wording repair as a draft revision, then re-review that item's stem/distractors.
2. An authorized **independent human reviewer / GT** should record final decisions separately under the project's current governance. Prior Astra/Grok AI checks do not substitute for final human approval.
3. Run the existing QA scripts after repairs. Maintain the 2,100 candidate selection, preserve signatures/review history, and make no automatic approvals.

*Method:* Reviewed the two published P1 review packets and canonical item fields, recomputed the numerical results independently, then cross-checked the keyed answer text. Did **not** run repository PHP/JS tests or re-execute its Python QA in this connector session.
