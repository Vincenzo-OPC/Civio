# Round 03 baseline audit, batch B3 (independent): GI R.A. 6713 + Environment, Numerical Basic operations + Number sequence — review request for Chief of Staff

Grok Bot, 2026-10-18. Source: `docs/research/audit/data/baseline-550-2026-10-17.json` (read-only MSI export of 17 Oct; MSI not queried). Repo base `f2766db`. **Nothing applied, imported or activated.**

ChatGPT's preliminary audit files (audit/fixes/milestone, 2026-10-18) were **not received**; this is an independent audit. ChatGPT columns in the CSV read `pending file`.

## Summary

| Group | Items | KEEP | FIX | REJECT | HOLD |
|---|---:|---:|---:|---:|---:|
| GI-6713 | 37 | 0 | 9 | 27 | 1 |
| GI-ENV | 27 | 0 | 13 | 13 | 1 |
| NUM-OPS | 31 | 12 | 14 | 2 | 3 |
| NUM-SEQ | 28 | 9 | 6 | 13 | 0 |
| **Total** | **123** | **21** | **42** | **55** | **5** |

- **0 key errors.** R.A. 6713 keys checked against LawPhil text (Secs. 3(i), 3(j), 4(A), 5, 7, 8, 9, 10, 12); environment keys against R.A. 9003 (incl. R.A. 11898 amendments), 8749, 9275, 9729, 7586/11038. All 59 Numerical keys recomputed by code (`numcheck`), each matching exactly one option.
- **Missed defects:** #343 option B reads ' von 760' (malformed, user-visible) and its fact duplicates approved bank 000528, so #343 is retired. Approved 000528 reads 'A electric fan' (grammar; flagged, not edited).
- **Duplicates dominate R.A. 6713:** 23 of 37 repeat facts already in the approved bank (000020, 000203, 000302, 000309, 000402, 000403, 000405, 000511, 000610, 000807, 000810, 000908; 060051-060072). Same precedent as B2: retire the baseline row to draft.
- **Wrong law for the subtopic:** #223 (property disposal → P.D. 1445/COA), #224 (nepotism → E.O. 292 Book V Sec. 59, HOLD), #73 (whistleblowing, not in R.A. 6713), #72 (relative-owned bidder is not R.A. 6713's Sec. 3(i) conflict of interest; rewritten).
- **Length giveaway:** in the GI subjects the key is the uniquely longest option in 52 of 64 items (median key/distractor length ratio about 1.7). The drafts balance option lengths and replace joke distractors with sibling-term traps.
- **Positions:** stored keys are A/B only in all 64 GI items (A 49, B 15). Mocks and offline drills shuffle choices at display (`mock-pool.ts` shuffleOptionsForQuestion; `lib/offline/grader.ts`). **Online drills do not shuffle choices** (see below), so stored position IS user-facing there.
- **Percent-change cap:** #181, #265, #489 are percent-change items while the bank already exceeds the proposed cap of 40 (78). HOLD for a CoS category/cap decision.
- **Number sequence:** 13 of 28 are duplicates or same-rule repeats (squares x4, doubling x4, ÷3 x2, halving x2, ...). Rejecting them widens the sequence gap (MILESTONE §5); new original sequence items should use other rules (alternating, two interleaved series, cubes).

## Online drill choice shuffling (code check)

- `app/Services/DrillService.php` orders questions with `inRandomOrder()` only and serves `options` as stored.
- `resources/js/pages/user/drills/**` never calls `shuffleOptionsForQuestion` or any option shuffle; `custom-builder-view.tsx` shuffles question IDs only. `originalOptionIndices` exists in `drills/types.ts` but is never set on the online path.
- Only `mock-session.ts`, `use-exam-hydration.ts` (mocks) and `lib/offline/grader.ts` (offline drills) shuffle choices.
- **Conclusion:** in online drills the stored answer position is shown, so the baseline A/B skew is a real giveaway. Fix is app code → Codex Astra brief (apply `shuffleOptionsForQuestion` on the drill path), not an editorial change.

## Needs CoS approval

- All REJECT (retire to draft) and FIX (replace with the full-schema draft in `docs/research/audit/fixes/round-03-baseline-b3-drafts.json`).
- HOLD decisions: #224 (recategorize to civil-service law or retire), #86 (needs P.D. 705 anchor), #181/#265/#489 (percent cap).
- Two drafts (#83 P.D. 1586, #414 E.O. 192) carry `source_quote: TO BE QUOTED`; I did not fetch those texts this session. Approve only after the quote is filled.

## Per item

| Group | ID | Key now | Verdict | Issue / evidence | Proposal | Draft |
|---|---|---|---|---|---|---|
| GI-6713 | 6 | Code of Conduct and Ethical Standards for Public Officials and Employees | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000302 (short title, Sec. 1). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 7 | Public interest over personal interest | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000810 (Sec. 4(A)(a)); also placeholder explanation. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 8 | Transparency and accountability | REJECT | Placeholder explanation ('Local practice item for Docker study.'). Vague ('an example of transparency'); its key restates #72's topic, so the pair discloses each other. No statutory anchor: R.A. 6713 has no 'disclosure of conflict' norm as such (conflict is handled by Sec. 9 divestment). | Retire; conflict of interest is covered by #388 (Sec. 3(i)) and #72 (rewritten). |  |
| GI-6713 | 66 | Public interest | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000810 (Sec. 4(A)(a)); same as baseline #7 and #379. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 67 | Upon assumption of office, annually, and upon separation | FIX | Key correct (Sec. 8(A): within 30 days after assumption, on or before April 30 every year, within 30 days after separation). Explanation uncited; key is the only long, statute-worded option (length giveaway); 'Only if salary exceeds a fixed threshold' is a fair trap but the other two are weak. | Draft: same triad fact, balanced options built from real wrong combinations (wrong deadline numbers), cite Sec. 8(A)(a)-(c). Not a duplicate of 000403/000511/060072, which test one deadline each. | yes |
| GI-6713 | 68 | Accepting gifts in connection with official duties | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000405 and 060070 (Sec. 7(d) gifts). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 69 | Making information accessible as required by law and policy | REJECT | Duplicate of approved bank item CIVIO-GI-SCENARIO-APPLY-060064 (Sec. 5(e) documents accessible); explanation uncited and 'Keeping all procurement secret until after award forever' is a joke option. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 70 | Transferring conflicting financial interests within a required period | REJECT | Overlaps #389 (definition, Sec. 3(j)) and approved 000502/060075 (60-day period, Sec. 9). Key 'within a required period' is vague. | Retire; keep #389. |  |
| GI-6713 | 71 | Lead modest lives appropriate to their positions and income | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000402 and 060058 (simple living, Sec. 4(A)(h)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 72 | An official deciding a bid where a close relative owns a bidder | FIX | Key is defensible as common usage, but the scenario (a relative owns a bidder) is NOT R.A. 6713's definition of conflict of interest, which is about the official's own board seat, office, substantial stock or business interest (Sec. 3(i)); relatives fall under Sec. 4(A)(c) and R.A. 3019. Distractors are joke options. Discloses #8. | Draft: scenario where the official is a substantial stockholder of a bidder; cite Sec. 3(i) and Sec. 9. | yes |
| GI-6713 | 73 | Consistent with the duty to uphold public interest | REJECT | R.A. 6713 has no whistleblowing provision; the key ('consistent with the duty to uphold public interest') is an inference, distractors are joke options. Not testable against the statute. | Retire. Whistleblower protection is outside R.A. 6713. |  |
| GI-6713 | 223 | Proper authority and legal basis | REJECT | Disposal of government property is governed by P.D. 1445 (Government Auditing Code) and COA rules, not R.A. 6713. Joke distractors ('Social media announcement', 'Family consent'). | Retire (wrong law for this subtopic). |  |
| GI-6713 | 224 | Favoritism in appointing relatives within prohibited degrees | HOLD | Anti-nepotism in appointments is E.O. 292 (Administrative Code of 1987), Book V, Sec. 59, not R.A. 6713; R.A. 6713 only bars undue favors to relatives (Sec. 4(A)(c)), already tested by #395. 'Merit-based promotions' and 'Use of email' are weak. | CoS: recategorize to a civil-service-law item (needs E.O. 292 text check) or retire. No draft until decided. |  |
| GI-6713 | 225 | Competence, courtesy, and dedication to duty | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000309 and 060052 (professionalism, Sec. 4(A)(b)); joke distractors. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 379 | Public interest | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000810 (Sec. 4(A)(a)); same as baseline #7 and #66. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 380 | A prohibited gift connected with official duties | REJECT | Duplicate of approved bank item CIVIO-GI-SCENARIO-APPLY-060070 (gift tied to a pending transaction, Sec. 7(d)); joke distractors ('wrapped'). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 381 | Fifteen working days | REJECT | Duplicate of approved bank item CIVIO-GI-DEADLINE-NUMBER-000020 and 000708 (15 working days, Sec. 5(a)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 382 | On or before April 30 | REJECT | Duplicate of approved bank item CIVIO-GI-DEADLINE-NUMBER-060072 (April 30, Sec. 8(A)(b)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 383 | Thirty days | REJECT | Duplicate of approved bank item CIVIO-GI-DEADLINE-NUMBER-000403 and 060071 (30 days after assumption, Sec. 8(A)(a)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 384 | Thirty days after separation | REJECT | Duplicate of approved bank item CIVIO-GI-DEADLINE-NUMBER-000511 (30 days after separation, Sec. 8(A)(c)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 385 | Serve people without unfair discrimination based on party affiliation | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000807 and 060054 (political neutrality, Sec. 4(A)(d)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 386 | Lead modest lives appropriate to position and income | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000402 and 060058 (simple living). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 387 | Discharging duties with excellence, skill, and dedication | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000309 (professionalism). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 388 | Opposed to or affected by faithful performance of official duty | FIX | Key correct (Sec. 3(i) 'may be opposed to or affected by the faithful performance of official duty'). Stem omits that the interest is a board seat, office, substantial stock or business interest; key is the only long, statute-worded option (length giveaway); 'A public holiday' is a joke option. | Draft with the full Sec. 3(i) trigger and sibling distractors (Sec. 7(a) financial interest, Sec. 4(A)(c) relatives, Sec. 9 divestment). | yes |
| GI-6713 | 389 | Voluntarily and completely disposing of a conflicting interest | FIX | Key correct (Sec. 3(j)): transfer of title voluntarily, completely and actually, to someone other than spouse and relatives. The key omits the spouse/relatives limit, which is the testable point; joke distractors ('Borrowing a colleague's ID'). | Draft: options contrast transfer to spouse/relative (not divestment), listing in the SALN, resignation (Sec. 9 resign rule) — cite Sec. 3(j), Sec. 9. | yes |
| GI-6713 | 390 | Disclosure or misuse of confidential information | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000908 and 060069 (confidential information, Sec. 7(c)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 391 | Making public documents accessible during reasonable working hours | REJECT | Duplicate of approved bank item CIVIO-GI-SCENARIO-APPLY-060064 (Sec. 5(e)); same fact as baseline #69. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 392 | Three signatories | REJECT | Duplicate of approved bank item CIVIO-GI-DEADLINE-NUMBER-000203 and 060062 (three signatories, Sec. 5(c)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 393 | Civil Service Commission | FIX | Key correct (Sec. 12: CSC has primary responsibility for administration and enforcement). Not in the approved bank (000202 tests the awards committee). Distractors 'Department of Tourism', 'A private contractor' are implausible; boilerplate missing period. | Draft with real sibling bodies: Office of the Ombudsman (receives SALN copies / prosecutes), COA, Sandiganbayan. | yes |
| GI-6713 | 394 | A prohibited outside-employment-related act | REJECT | Duplicate of approved bank item CIVIO-GI-SCENARIO-APPLY-060068 (recommending a person to a firm with a pending transaction, Sec. 7(b)(4)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 395 | Officials must avoid undue favors to relatives because of office | FIX | Key correct (Sec. 4(A)(c) undue favors to relatives) but the testable exception (confidential positions and coterminous personal staff) is missing; joke distractors ('award every contract to relatives'). | Draft: test the statutory exception; cite Sec. 4(A)(c). | yes |
| GI-6713 | 396 | Assets, liabilities, net worth, and business interests | FIX | Key correct (Sec. 8 opening paragraph); joke distractors ('favorite books'); the family scope (spouse, unmarried children under 18 living in the household) is the better testable fact. | Draft on whose interests must be declared; cite Sec. 8. | yes |
| GI-6713 | 397 | Of nominal value and received as a souvenir or mark of courtesy | FIX | Key correct (Sec. 7(d), Congress consents to a foreign-government gift of nominal value received as souvenir or mark of courtesy; also scholarships/medical treatment and certain travel grants). Distractors are bribes, so the key is obvious. | Draft listing real Sec. 7(d) categories vs. non-consented ones. | yes |
| GI-6713 | 398 | Provides the same service to supporters and opponents | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000807 (political neutrality); same as baseline #385. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 524 | Efficient, honest, and economical use of government resources | REJECT | Duplicate of approved bank item CIVIO-GI-SCENARIO-APPLY-060051 (official vehicle for a private holiday, Sec. 4(A)(a)); distractors are unrelated constitutional topics. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 525 | Explaining procedures clearly and attending to a transaction promptly | REJECT | Duplicate of approved bank item CIVIO-GI-TERM-MATCH-000610 and 060055 (responsiveness, Sec. 4(A)(e)); the key is the only competent-sounding option. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-6713 | 526 | Correct and resubmit it through the required review process | FIX | Defensible but uncited; R.A. 6713 Sec. 10(a) says the reviewing body informs the filer and directs corrective action. Joke distractors. | Draft anchored to Sec. 10(a). | yes |
| GI-ENV | 11 | Compromising future generations' ability to meet theirs | FIX | Placeholder explanation ('Local practice item for Docker study.'). Distractors are absurd ('Scientific research'). | Draft citing the Brundtland definition as adopted in R.A. 9003, Sec. 2(c) 'ecologically sustainable development principles'; sibling distractors (conservation-only, zero use, growth-first). | yes |
| GI-ENV | 12 | Significantly affect the environment | REJECT | Duplicate of baseline #83 (EIA purpose); placeholder explanation; joke distractors. | Retire; keep #83. |  |
| GI-ENV | 82 | Ecological solid waste management | REJECT | Duplicate of baseline #405 (R.A. 9003 subject). | Retire; keep #405. |  |
| GI-ENV | 83 | Assesses potential environmental effects before major projects proceed | FIX | Key correct (P.D. 1586, Philippine EIS System). Explanation uncited; 'Applies only to residential backyard gardens' is a joke option. | Draft citing P.D. 1586 (EIS System); distractors: replaces ECC? no — use real confusions (post-construction audit, LGU permit, tax incentive). Source text to be checked on LawPhil (P.D. 1586) before CoS. | yes |
| GI-ENV | 84 | Action to prevent harm may be taken even if scientific certainty is incomplete | REJECT | Duplicate of baseline #410 (precautionary principle). | Retire; keep #410. |  |
| GI-ENV | 85 | Disaster risk reduction planning and resilient infrastructure | REJECT | Duplicate of approved bank item CIVIO-GI-ENV-PRINCIPLE-060095 (adaptation, R.A. 9729); joke distractors. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-ENV | 86 | Forest ecosystems and biodiversity | HOLD | Common-sense item, joke distractors ('Stock market indexes', 'Postal delivery'). Needs a P.D. 705 (Revised Forestry Code) anchor that I have not verified on LawPhil in this session. | Rewrite after P.D. 705 text check, or retire. |  |
| GI-ENV | 87 | Separating recyclables, biodegradables, and residuals at the household or establishment | REJECT | Duplicate of approved bank item CIVIO-GI-20261013-0002 and 060076 (segregation at source, R.A. 9003 Sec. 21). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-ENV | 88 | Conserve biodiversity and ecological processes | REJECT | Duplicate of baseline #413 (protected areas). | Retire; keep #413. |  |
| GI-ENV | 89 | Department of Environment and Natural Resources (DENR) | REJECT | Duplicate of baseline #414 (DENR). | Retire; keep #414. |  |
| GI-ENV | 228 | Supply and regulate freshwater resources | FIX | Key correct; 'Only produce oil', 'Block all rainfall' are joke options; no source. | Draft citing R.A. 9275 Sec. 5 (water quality management areas use watersheds/river basins as units); sibling distractors. | yes |
| GI-ENV | 229 | Risks pollution, disease vectors, and environmental harm | FIX | Key correct (R.A. 9003 Sec. 37 prohibits open dumps; Sec. 3(t) defines them). 'Improves groundwater always' is a joke; 'Is required by R.A. 9003' is a good GI-OLD-RULE-style trap. | Draft citing Secs. 3(t), 37, 48(9). | yes |
| GI-ENV | 405 | Ecological Solid Waste Management Act of 2000 | FIX | Key correct (R.A. 9003 Sec. 1). Note: R.A. 9003 was amended by R.A. 11898 (EPR Act of 2022); short title unchanged. Distractors 'Data Privacy Act', 'Civil Service Law' are off-domain giveaways. | Draft with environmental sibling laws only (R.A. 8749, 9275, 6969). | yes |
| GI-ENV | 406 | Where it is generated | REJECT | Duplicate of approved bank item CIVIO-GI-20261013-0002 (segregation at source); same as baseline #87. | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-ENV | 407 | Biodegradable organic material | REJECT | Duplicate of approved bank item CIVIO-GI-20261013-0003 and 060082 (composting). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-ENV | 408 | Philippine Clean Air Act of 1999 | FIX | Key correct (R.A. 8749 Sec. 1). Distractors 'Anti-Graft', 'Cybercrime' are off-domain giveaways. | Draft with environmental siblings (R.A. 9003, 9275, 9729). | yes |
| GI-ENV | 409 | Examines likely environmental effects before a covered project proceeds | REJECT | Duplicate of baseline #83 (EIA purpose). | Retire; keep #83. |  |
| GI-ENV | 410 | A serious risk exists even though scientific certainty is incomplete | FIX | Key correct; R.A. 9729 Sec. 2 adopts the Precautionary Principle for climate risk decisions (also Rule 20, Rules of Procedure for Environmental Cases, A.M. 09-6-8-SC). Joke distractors ('Harm is certain to be harmless'). | Draft citing R.A. 9729 Sec. 2. | yes |
| GI-ENV | 411 | Collects and channels water through a drainage area | REJECT | Duplicate of baseline #228 (watershed); 'Stores only marine passwords' is a joke option. | Retire; keep #228. |  |
| GI-ENV | 412 | Reduce unnecessary plastic, segregate waste, and recover recyclables | FIX | Key correct but joke/absurd distractors make the key obvious; uncited. | Draft citing R.A. 9003 Sec. 21 (segregation at source) and Sec. 48(1) (littering/dumping in canals and esteros is prohibited). | yes |
| GI-ENV | 413 | Biodiversity and ecological processes | FIX | Key correct (R.A. 7586 Sec. 2 as amended by R.A. 11038 (E-NIPAS Act of 2018)). Joke distractors. | Draft citing R.A. 11038 Sec. 2 (amending R.A. 7586 Sec. 2). | yes |
| GI-ENV | 414 | Department of Environment and Natural Resources | FIX | Key correct; off-domain distractors (BIR, LTO, PSA) make it trivial. | Draft with environment-adjacent agencies (EMB is a DENR bureau, DA-BFAR, MMDA, NWRB) asking which department is primary. Cite E.O. 192 (1987) — text check pending. | yes |
| GI-ENV | 417 | Keep materials useful through reuse, repair, and recycling | FIX | Key correct; R.A. 11898 (2022) inserted a 'circular economy' definition into R.A. 9003 Sec. 3(d-1). Joke distractors. | Draft citing R.A. 9003 Sec. 3(d-1) as amended by R.A. 11898. | yes |
| GI-ENV | 418 | Release harmful smoke and pollutants | REJECT | Duplicate of approved bank item CIVIO-GI-ENV-PRINCIPLE-060083 (open burning, R.A. 9003 Sec. 48(3)). | Retire the baseline row to draft (history kept); the bank item already has full spec metadata. |  |
| GI-ENV | 527 | Prevent waste first, then reuse and recover materials before final disposal | FIX | Key correct (R.A. 9003 Sec. 2(c): avoidance and volume reduction through source reduction, reuse, recycling and recovery before disposal). Joke distractors; uncited. | Draft citing Sec. 2(c). | yes |
| GI-ENV | 528 | Providing habitat and reducing wave and erosion impacts | FIX | Key correct (ecology concept, no statute needed); joke distractors. | Draft with plausible ecological siblings (carbon only, freshwater recharge, fisheries ban). | yes |
| GI-ENV | 529 | Use an approved digital workflow with backups and retention rules | REJECT | Records-management office practice, not Environment Management and Protection; reads as a Clerical item. | Retire. |  |
| NUM-OPS | 41 | 42 | FIX | Placeholder explanation ('Local practice item for Docker study.'). One-step addition is below CSE difficulty but valid as an easy warm-up. | Draft with coded distractors (carry error, off by one). | yes |
| NUM-OPS | 42 | 12 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft with coded distractors. | yes |
| NUM-OPS | 43 | 63 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft with coded distractors. | yes |
| NUM-OPS | 44 | 63 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft with coded distractors (borrow error). | yes |
| NUM-OPS | 173 | 81 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft; same frame as #340/#486/#184 — keep but vary stems. | yes |
| NUM-OPS | 174 | 17/12 | KEEP | Key 17/12 recomputed; explanation correct. | Migrate to schema later (codes, why_wrong). |  |
| NUM-OPS | 175 | 100 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 176 | 32 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft (16 = 2^4 off-by-one, 10 = 2x5). | yes |
| NUM-OPS | 177 | 3,800 | KEEP | Key recomputed; explanation correct. | Migrate to schema later. |  |
| NUM-OPS | 178 | 24 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft (48 = product, 12 = common multiple of 6 only). | yes |
| NUM-OPS | 179 | 18 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 180 | 1/8 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 181 | 30% | HOLD | Placeholder explanation ('Local practice item for Docker study.'). Percent-change item; MILESTONE_2000_PLAN caps percent change at 40 and the bank already has 78. | CoS: count it under Basic operations (one-step percent) or retire under the cap. Draft supplied. | yes |
| NUM-OPS | 182 | 9 | KEEP | Key 9 recomputed; explanation correct. | Migrate later. |  |
| NUM-OPS | 183 | 3/8 | FIX | Placeholder explanation ('Local practice item for Docker study.'). Stem wording is awkward ('equals which fraction for the first part over total'). | Draft with a clear stem. | yes |
| NUM-OPS | 184 | 20 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 262 | 56 | REJECT | Duplicate of baseline #487 (7/8 of 64, same numbers). | Retire; keep #487. |  |
| NUM-OPS | 263 | 14 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 264 | 210 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft. | yes |
| NUM-OPS | 265 | 150 | HOLD | Placeholder explanation ('Local practice item for Docker study.'). Reverse-percent item; percent-change cap applies. | CoS decision as #181. Draft supplied. | yes |
| NUM-OPS | 339 | 22 | KEEP | Key 22 recomputed. |  |  |
| NUM-OPS | 340 | 36 | KEEP | Key 36 recomputed. |  |  |
| NUM-OPS | 341 | 150 | KEEP | Key 150 recomputed. |  |  |
| NUM-OPS | 342 | 4.35 | KEEP | Key 4.35 recomputed. |  |  |
| NUM-OPS | 343 | 720 | REJECT | Key 720 correct, but option B is malformed (' von 760', user-visible), and qa_file finds the same fact already approved as CIVIO-NUM-WP-PCT-CHANGE-000528 (₱800 at 10% off; that item itself reads 'A electric fan', a grammar slip to flag, not edited). | Retire the baseline row (removes the malformed option from users); bank 000528 covers the fact. |  |
| NUM-OPS | 485 | 30 | KEEP | Key 30 recomputed. Cosmetic: boilerplate missing period ('... is 30 Therefore'). | Add the period on migration. |  |
| NUM-OPS | 486 | 45 | KEEP | Key 45 recomputed. Same frame as #173 with different numbers (acceptable). |  |  |
| NUM-OPS | 487 | 56 | KEEP | Key 56 recomputed; kept over #262. |  |  |
| NUM-OPS | 488 | 3.65 | KEEP | Key 3.65 recomputed. |  |  |
| NUM-OPS | 489 | 1,320 | HOLD | Key 1,320 recomputed; percent-decrease item under the percent-change cap. | CoS decision as #181. |  |
| NUM-OPS | 540 | 41 | KEEP | Key 41 recomputed. |  |  |
| NUM-SEQ | 45 | 15 | FIX | Placeholder explanation ('Local practice item for Docker study.'). Very easy (+3). | Draft. | yes |
| NUM-SEQ | 46 | 80 | REJECT | Duplicate of baseline #190 (doubling; #46 and #186 are the same sequence 5,10,20,40). | Retire; keep #190. |  |
| NUM-SEQ | 47 | 26 | REJECT | Duplicate of baseline #345 (#47's sequence 2,5,10,17 is a prefix of #345). | Retire; keep #345. |  |
| NUM-SEQ | 185 | 36 | REJECT | Duplicate of baseline #193 (squares, same answer 36). | Retire; keep #193. |  |
| NUM-SEQ | 186 | 80 | REJECT | Duplicate of baseline #190 (doubling; exact duplicate of #46). | Retire; keep #190. |  |
| NUM-SEQ | 187 | 13 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft (Fibonacci). | yes |
| NUM-SEQ | 188 | 1 | REJECT | Duplicate of baseline #346 (81, 27, 9, 3 — same sequence). | Retire; keep #346. |  |
| NUM-SEQ | 189 | 42 | KEEP | Key 42 recomputed (n(n+1)); kept over #491. |  |  |
| NUM-SEQ | 190 | 112 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft; representative doubling item. | yes |
| NUM-SEQ | 191 | 63 | KEEP | Key 63 recomputed (x2+1). |  |  |
| NUM-SEQ | 192 | 50 | KEEP | Key 50 recomputed; kept over #541. |  |  |
| NUM-SEQ | 193 | 36 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft; representative squares item. | yes |
| NUM-SEQ | 194 | 17 | KEEP | Key 17 recomputed; kept over #266. |  |  |
| NUM-SEQ | 195 | 4 | REJECT | Duplicate of baseline #492 (halving). | Retire; keep #492. |  |
| NUM-SEQ | 196 | 29 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft (consecutive primes). | yes |
| NUM-SEQ | 266 | 25 | REJECT | Duplicate of baseline #194 (same rule: differences +1, +2, +3, ...). | Retire; keep #194. |  |
| NUM-SEQ | 267 | 120 | FIX | Placeholder explanation ('Local practice item for Docker study.'). | Draft (factorials). | yes |
| NUM-SEQ | 268 | 49 | REJECT | Duplicate of baseline #193 (consecutive squares again). | Retire; keep #193. |  |
| NUM-SEQ | 344 | 64 | REJECT | Duplicate of baseline #190 (doubling). | Retire; keep #190. |  |
| NUM-SEQ | 345 | 37 | KEEP | Key 37 recomputed. |  |  |
| NUM-SEQ | 346 | 1 | KEEP | Key 1 recomputed; kept over #188. |  |  |
| NUM-SEQ | 347 | 66 | KEEP | Key 66 recomputed (x2-2). |  |  |
| NUM-SEQ | 348 | 25 | REJECT | Duplicate of baseline #193 (consecutive squares). | Retire; keep #193. |  |
| NUM-SEQ | 490 | 65 | REJECT | Duplicate of baseline #191 (x2+1 vs x2-1, same rule family; keep one). | Retire; keep #191. |  |
| NUM-SEQ | 491 | 30 | REJECT | Duplicate of baseline #189 (2, 6, 12, 20, same sequence). | Retire; keep #189. |  |
| NUM-SEQ | 492 | 6 | KEEP | Key 6 recomputed. |  |  |
| NUM-SEQ | 493 | 48 | KEEP | Key 48 recomputed (missing middle term, a distinct format). |  |  |
| NUM-SEQ | 541 | 30 | REJECT | Duplicate of baseline #192 (growing subtraction, same rule). | Retire; keep #192. |  |
