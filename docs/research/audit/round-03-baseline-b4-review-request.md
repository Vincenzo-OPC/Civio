# Round 03 baseline audit, batch B4: Numerical word problems (32), review request for Chief of Staff

Grok Bot, 2026-10-18. Source: Oct 17 export (MSI not queried). Base `main` f2766db. **Nothing applied.**

## Summary

- KEEP 20, FIX 4, REJECT 6, HOLD 2.
- **Keys:** 32/32 recomputed with exact fractions and matching exactly one option. **0 key errors.**
- **Malformed option:** #349 ' sixty-four' (user-visible), fixed in the draft.
- **Duplicates:** #48≈#203, #49≈#202, #197⊂#351, #198≈#494, #50 discount frame. No exact match to the approved bank. #205 and #350 share frames with approved 000330 and 000921 (different numbers).
- **Percent cap:** #199, #350, #495 are discount/percent items (#199 is REJECTED as a frame duplicate; #350 and #495 are HOLD) while the bank holds 78 percent-change items against a proposed cap of 40, so they're HOLD for CoS.
- **Drafts:** 5 full-schema drafts (#201, #206, #209, #349 FIX; #495 HOLD) in `audit/fixes/round-03-baseline-b4-drafts.json`. `qa_file.py` and `explanation_lint.py` results are in the tracker.
- **Needs CoS:** all REJECT/FIX and the two HOLDs.

## Per item

| ID | Key now | Verdict | Issue / evidence | Proposal | Draft |
|---|---|---|---|---|---|
| 48 | ₱52 | REJECT | Placeholder explanation ('Local practice item for Docker study.'). Same fare-times-passengers task as #203. | Retire; keep #203. |  |
| 49 | ₱4,000 | REJECT | Placeholder explanation ('Local practice item for Docker study.'). Same daily-wage task as #202. | Retire; keep #202. |  |
| 50 | ₱450 | REJECT | Placeholder explanation ('Local practice item for Docker study.'). Discount frame duplicated by #199/#495 and the bank's 78 percent-change items. | Retire. |  |
| 197 | 60 km/h | REJECT | Average speed 180 km / 3 h is the first step of #351 (same numbers). | Retire; keep #351. |  |
| 198 | 10 | REJECT | Same clerks-forms-per-hour frame as #494 (5 clerks/100 forms/2 h vs 4/160/2). | Retire; keep #494. |  |
| 199 | 1020 pesos | REJECT | Percent-change/discount item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78 (NUM-WP-PCT-CHANGE). qa_file also finds the same frame already approved ('office chair ... 15% off', different price). | Retire under the cap. |  |
| 200 | 240 L | KEEP | Key 240 recomputed (1/4 of capacity = 60). Distinct from #497 (complement fraction vs. given fraction). |  |  |
| 201 | 29 | FIX | Key 29 recomputed ((50+8)/2). Explanation 'Larger is 29.' gives no method. | Draft with the sum-difference method. | yes |
| 202 | 9000 pesos | KEEP | Key 9,000 recomputed. | Note: options lack thousands separators (8000) — fix on migration. |  |
| 203 | 120 pesos | KEEP | Key 120 recomputed. |  |  |
| 204 | 14 | KEEP | Key 14 recomputed (one part = 7). |  |  |
| 205 | 600 pesos | KEEP | Key 600 recomputed. Same frame as approved CIVIO-NUM-WP-PCT-CHANGE-000330 (6%, 2 years) with a different principal — acceptable variant, flag for the frame cap. |  |  |
| 206 | 34 m | FIX | Key 34 recomputed. Explanation 'Perimeter 34 m.' gives no method; '60 m' (area) is a good trap but uncoded. | Draft with method and coded traps. | yes |
| 207 | 4.5 kg | KEEP | Key 4.5 recomputed. |  |  |
| 208 | 30% | KEEP | Key 30% recomputed (60% left, half done → 30%). Percent-of-remaining, not percent change. |  |  |
| 209 | 300 pesos | FIX | Key 300 recomputed. Explanation 'Middle share 300.' gives no method. | Draft with the parts method. | yes |
| 210 | 15 | KEEP | Key 15 recomputed. |  |  |
| 269 | 20 | KEEP | Key 20 recomputed (2 pages/min per printer). |  |  |
| 270 | ₱3,214 | KEEP | Key ₱3,214 recomputed (30,000 − 30,000/1.12 = 3,214.29). '₱3,600' is the classic 12%-of-gross trap. |  |  |
| 271 | 2.5 hours | KEEP | Key 2.5 hours recomputed. |  |  |
| 272 | 16% | KEEP | Key 16% recomputed (0.8 L solute in 5 L). |  |  |
| 349 | 72 | FIX | Key 72 correct, but option B is malformed: ' sixty-four' (spelled out, leading space) among numerals — user-visible. | Draft with '64' (18 × 4 misread as 16 × 4). | yes |
| 350 | 648 | HOLD | Percent-change/discount item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78 (NUM-WP-PCT-CHANGE). Same frame as approved 000921 (₱600 base). | CoS decision as #199. |  |
| 351 | 300 km | KEEP | Key 300 km recomputed. |  |  |
| 352 | 15 | KEEP | Key 15 recomputed. |  |  |
| 353 | 25 | KEEP | Key 25 recomputed. |  |  |
| 494 | 20 | KEEP | Key 20 recomputed. Cosmetic: boilerplate missing period. |  |  |
| 495 | 2,040 | HOLD | Percent-change/discount item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78 (NUM-WP-PCT-CHANGE). | CoS decision as #199. Draft supplied. | yes |
| 496 | 120 km | KEEP | Key 120 km recomputed. Same skill as #351 with different numbers (3.5 h) — acceptable. |  |  |
| 497 | 120 liters | KEEP | Key 120 L recomputed. |  |  |
| 498 | 2 | KEEP | Key 2 recomputed. |  |  |
| 542 | 360 | KEEP | Key 360 recomputed. Cosmetic: boilerplate missing period. |  |  |
