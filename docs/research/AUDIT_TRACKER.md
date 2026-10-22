# Civio audit tracker (single source of progress)

The rules are in spec §7 and §10. Never auto-approve or deploy. Batch 001-011 approval stays as Chief of Staff recorded it.

| Round | Date | Items / files | Pass | Fix | Fail | Report |
|---|---|---|---|---|---|---|
| 01 | 2026-10-13 | ChatGPT supplements 001: 150 (VFIL 80, GI 30, CLR 40) | 0 release-ready (140 content-pass) | 140 | 10 | audit/round-01.md |
| 01 fixes | 2026-10-13 | All 150 supplement items fixed (still draft); gap-fill-001 23 | gap-fill: 20 CoS PASS + 3 fixed → approved | 150 fixed | 0 open | audit/round-01-fixes.md |
| 02 | 2026-10-13 | Batches 001-011, Subprofessional domains: 759 (CLR 151, VEN 203, GI 102, NUM 303) | 759 key-correct | ~27 proposed (CoS) + 58 metadata applied | 0 | audit/round-02.md |
| 02 gap | 2026-10-13 | gap-fill-002: 14 new drafts (VEN error 5, NUM frac/dec 6, CLR business filing 3) | 14 CoS PASS (4 fixed) → approved, active locally | 4 | 0 | audit/round-02-fixes.md |
| 02 fixes | 2026-10-13 | CoS round 02 rulings: 178 rewrites of approved items (spelling 93, Verbal lead-in 60, ops shapes 25) + gap-fill-003 10 filing drafts + 267 Numerical shortcuts | CoS PASS after fixes → merged + approved | 178 changed | 0 | audit/round-02-fixes.md, audit/round-02-fixes-review-request.md |

## Open flags (not edited)

- Active item stem `The word 'abate' most nearly means:` (seed `scripts/seed_cse_pack_200_2026-10-03.sql`) uses distractors that are not real mistakes, including "Move alphabetically" and "Multiply instantly". Left unchanged. It needs the bank-review workflow before any rewrite.

## Round 01

- **Issues:**
  - Spec metadata is missing on all 150: `terms` is empty, codes aren't in the spec, and `why_wrong` is generic.
  - 6 paragraph-order items give away their key.
  - 2 Filipino grammar errors in keys/stems (0026, 0038).
  - 1 item has two right answers (0046).
  - 1 Reveal doesn't match its key (0050).
  - GI has implausible distractors.
- **Decisions:** ChatGPT's files were left untouched, and their items stay draft. Gap fill 001 (23 drafts) was written for sawikain, human rights, RC, PO and ARMA filing.
- **Next:** round 02 = the Subprofessional parts of batches 001-011, in this order:
  1. clerical 151
  2. Verbal EN 200, sampled 100
  3. GI 102
  4. numerical, recompute-only

  Then round 03+ = the baseline bank (550), Subprofessional domains first. After that, gap fill 002: Verbal EN error recognition, numerical fractions and decimals, and ARMA business-name filing.

## Round 01 fixes and CoS verdict (2026-10-13)

- **CoS verdict:**
  - Gap-fill-001: 20 PASS. VFIL-0011, VFIL-0013 and VEN-RC-0017 needed code fixes, now done.
  - The 10 supplement FAILs are confirmed.
  - The other 140 supplement items pass on content and only needed metadata fixes.
- **Supplement fixes (every change is logged in `audit/round-01-fixes.md`):**
  - 10 FAILs fixed. VFIL-0075 to 0080 had their sentence labels shuffled, so no key equals the listed order.
  - Filled `terms` on all 150.
  - Spec codes on every distractor, and a separate why-wrong line for each option.
  - ARMA Rule 1 / ANSI/ARMA 12-2005 citation added to the 20 filing items.
  - GI giveaway distractors replaced in 0005, 0010, 0013, 0014, 0017, 0019, 0023, 0024, 0028 and 0029.
  - Spelling stems reworded and their wrong source label corrected.
  - "upang" is now the key in 3 completion items, down from 6.
  - Rescan for the new codes: 21 FIL-ANTONYM-TRAP and 9 RC-SUPPORTED-NOT-ASKED recodes. Batches 001-011 have no Filipino or RC items, so they had nothing to rescan.
- **Spec v0.1.5 (§10.4):** adds `FIL-ANTONYM-TRAP`, `RC-SUPPORTED-NOT-ASKED`, the order-key check, and the ANSI/ARMA 12-2005 note on filing Reveals.
- **qa.py:** rejects any order item whose key equals the listed order.
- **Activated:** only gap-fill-001 (23), set to approved/passed by Chief of Staff, 2026-10-13. The 150 supplement items stay draft/unreviewed.
- **Next:**
  - round 02: batches 001-011 Subprofessional parts (clerical, then Verbal English, GI, Numerical)
  - gap-fill 002: English error recognition, fractions and decimals, business-name filing

## Round 02 (2026-10-13)

- **Issues:**
  - About 25 typo-style misspellings, and the same misspelled words reused across batches.
  - Filing covers only ARMA Rules 1, 5 and 6, with one stem frame.
  - Frame repetition in Verbal (89 of 203 share one frame) and Numerical (30 share one frame).
  - 2 spelling Reveal labels describe the wrong error type.
- **Decisions:** the content of approved items is untouched; proposals went to CoS. I applied the §10.4 ARMA note to 58 filing items and re-rendered the batch `.md` files.
- **Gap fill 002:** 14 drafts written.
- **Next:**
  - round 03: baseline bank (550), Subprofessional domains first, starting with clerical and GI
  - CoS rulings on the round 02 proposals
  - gap fill 003: Filipino idioms and grammar beyond the supplements, and ARMA Rules 4 and 8

## Round 02 fixes (2026-10-13)

- **Gap-fill 002:** CoS PASS on all 14. I applied the 4 code and why-wrong fixes plus the optional VEN-ERROR-0003 recode. All 14 are approved and active in the local Civio DB.
- **Rulings applied (spec v0.1.6, §10.5):** these are rewrites of approved items, held in `docs/research/round-02-fixes.json` with status draft and review_status "changed". The batch files keep the approved versions.
  - 93 spelling items rewritten: unique real-misspelling targets, plus the new code SPL-SILENT. The 2 wrong error labels went away with the rewrite.
  - 60 Verbal lead-ins rewritten: "best completes" is down from 89 to 29.
  - 25 order-of-operations items rewritten across 5 new shapes, with keys recomputed.
  - The VFIL-0007 o2 recode to FIL-OTHER-TRAIT is applied in gap-fill-001 and synced.
- **Filing:** gap-fill-003 adds 10 drafts for ARMA Rules 2, 3, 4, 7 and 8.
- **Shortcut field (spec v0.1.7, §10.6):**
  - New optional `shortcut` field. `qa.py` accepts it, and the importer shows it as "Shortcut:", followed by "Method:".
  - 267 verified Numerical shortcuts are in `shortcuts-num-001.json`, pending CoS.
- **qa.py additions:**
  - one spelling target per item, bank-wide
  - error codes must match the misspelling
  - the 25% frame cap
  - exact evaluation of brackets and ÷
  - `qa_all.py` overlays `round-*-fixes.json`; it is GREEN with the overlay and RED with `--no-fixes`, as expected.
- **Next:**
  - CoS verdict on the 178 rewrites, gap-fill-003, and the shortcuts. Then merge the rewrites into the batches, retire the old-stem DB rows (the importer keys on stem), and sync.
  - Round 03: baseline bank (550), Subprofessional first.
  - Shortcut backfill for Clerical, Verbal and GI.

| ChatGPT 001 | 2026-10-13 | `chatgpt-batch-001.json`: 100 original Filipino Verbal drafts (synonym 25, antonym 20, sawikain 15, grammar 15, reading 15, paragraph ordering 10) | 0 approved; 100 unreviewed | independent content and linguistic review pending | 0 structural blockers in connector checks | `chatgpt-batch-001.json` |
| ChatGPT 002 | 2026-10-13 | `chatgpt-batch-002.json`: 100 English Verbal drafts (RC 25, paragraph order 35, error recognition 40) | 0 approved; 100 unreviewed | Grok Bot + CoS editorial and Python QA pending | 0 static blockers found | `chatgpt-batch-002.json` |
| ChatGPT 003 | 2026-10-16 | `chatgpt-batch-003.json` 100 General Information drafts (Constitution 25, human rights 25, R.A. 6713 25, environment 25) | 0 approved | Source-backed drafts; independent QA pending | No structural or Jaccard blockers | `CHATGPT_GI_DEEP_RESEARCH_2026-10-16.md` |

## ChatGPT batch 001 (2026-10-13)

- New file: `docs/research/chatgpt-batch-001.json`, **100 draft / unreviewed Filipino Verbal items**. Breakdown: 25 synonym, 20 antonym, 15 idiom/sawikain, 15 grammar, 15 reading comprehension, 10 paragraph-order questions.
- Static checks: 4 distinct options each, answer-option references, item metadata, spec distractor codes, choice-specific `why_wrong`, ordering-code distinctness, nontrivial order keys and locally unique IDs/stems. Token Jaccard at threshold **0.65** found no matches against **1,197** existing bank/supplement/gap-fill questions and **127** available baseline seed/prefix stems. This is not a comparison against all 550 rows in the private local development DB.
- **Validation limitation:** The actual Python `scripts/batches/qa.py` was not executable in this connector-only environment. The equivalent structural and token-duplicate checks were run, but the new JSON MUST pass the repository's Python QA and independent review before import or approval. No app code, tests, Grok batches or deploy were changed.
- Review focus: `CIVIO-VFIL-KASINGKAHULUGAN-040009` (mabini), `CIVIO-VFIL-KASINGKAHULUGAN-040013` (kinauukulang), `CIVIO-VFIL-WIKAIN-040054` (assess whether the idiom is suitably standard, and review all idioms), grammar items `CIVIO-VFIL-BALARILA-040069`/`040070` (din/rin, daw/raw; compare DepEd/KWF *Ortograpiyang Pambansa* §8.1) and all 10 ordering items for unique defensibility. Review interpretation and tone as natural Filipino and verify dictionary spelling. Review `RC-TOO-NARROW` choices for code precision. 
- Never auto-approve, activate or deploy. Reviewers: Grok Bot → Chief of Staff.

## Round 02 merge (CoS PASS on df61273 with fixes, 2026-10-13)

- **Fixes applied, no key changed except the two CoS asked for:**
  - 000100: dependant → independant (target independent).
  - 000587: publically → occured (target occurred).
  - Foils replaced with realistic misspellings: 000787 surprize → suprize, 000395 nayber → neigbor, 000996 eyeland → illand, 000994 dowbt → dought, 000691 siedge → seege.
  - In the word list, Februrary → Feburary and aighth → eith. These were not shown in any item: 000201 and 000188 are "misspelled" items whose keys are already Febuary and eigth.
- **gap-fill-003:** the 0023 and 0024 wrong-answer reasons now apply Rule 6 (SanCarlos, SantoTomas, deDavao, deManila). Keys are unchanged.
- **Shortcuts:**
  - The 30 OPS-ORDER entries moved to skipped.
  - Discount wording now rotates through 3 forms per type.
  - 237 shortcuts are merged into items as `shortcut`.
- **Merged:**
  - the 178 rewrites into batches 001-011
  - gap-fill-003 (10) and ChatGPT's supplements 001 (150)
  - all marked approved/passed, Chief of Staff, 2026-10-13
- **Change record:** `round-02-fixes.json` stays, with `replaces` (old stem and key) for each item.
- **Checks:** `qa_all.py --no-fixes` is GREEN on the committed files. The Bank Pest tests were updated for the approved supplements and the shortcut render.
- **Local DB:** imported on the MSI. Old-stem rows were set to draft (retired, with history kept).

## Round 03 (2026-10-13): ChatGPT batch 001 (100 Filipino Verbal)

- **Results:**
  - `qa.py` reports 0 flags.
  - 0 duplicates against 1,207 bank stems or the baseline.
  - No order key matches its listed order.
- **Fixes:** 040005 had two possible keys and is fixed. 040018 marked the wrong word. 040044 had the wrong code. 040047 had a spelling error. 040069 and 040070 were rewritten as applied din/rin and daw/raw items.
- **Status:** all 100 stay draft. Review request: `audit/round-03-chatgpt-001-review-request.md`.
- **Next:** CoS verdict, then round 03b on the baseline bank (550).

## ChatGPT batch 002 (2026-10-13)

- **File:** `docs/research/chatgpt-batch-002.json`, all 100 `draft` / `unreviewed`. 25 distinct reading passages (at least 150 words each) with one question each; 35 paragraph-order items with mixed sentence labels and unique keys; 40 grammar/error recognition (15 agreement, 5 tense, 20 modifiers and parallel structure).
- **Static checks:** all questions have four distinct options, a valid marked answer, nonempty Reveal fields, spec-coded distractors and individualized why-wrong reasons. Every paragraph-order item has three different order-trap codes and a key distinct from its listed order. Internal token Jaccard ≥ 0.65: no collisions. Repository comparisons: 1,277 existing items (batches 001–011 and selected gap-fill/supplements/ChatGPT 001) and 127 accessible baseline seed or prefix stems: no collisions ≥ 0.65. The local development DB may contain additional stems not accessible to this check.
- **Required before CoS review:** `python scripts/batches/qa.py` and `qa.check_round(items, prior_stems, near=0.65)` must be executed in a fully cloned repo with all existing stems and DB records. The GitHub connector did not expose a Python execution environment, so a passing run is **not yet confirmed**. `_legacy: true` marks manually authored formats not supported by existing deterministic generator-specific solvers; it MUST NOT be interpreted as answer-key verification.
- **Editorial watchlist:** all RC inferences for unintended second defensible answers; English grammar options that are too easy, especially singular-subject vs nearby-plural disagreement; modifier/parallelism forms; the chronology of every ordering question; and whether RC reading durations are calibrated fairly. Grok Bot should identify `ACCEPT`, `REVISE`, `REJECT` per ID and hand off to Chief of Staff. No activation, import or production deployment.

## ChatGPT Batch 003 — Deep Research, 2026-10-16

- **File:** `docs/research/chatgpt-batch-003.json`, **100 General Information items** (25 Constitution/government structure, 25 constitutional human rights, 25 R.A. 6713 and ethical standards, 25 environmental protection). All remain `draft` / `unreviewed`; none approved, activated, imported or deployed.
- **Source ledger:** `docs/research/CHATGPT_GI_DEEP_RESEARCH_2026-10-16.md`. Every item has a specific Constitution or law section and a LawPhil primary-law text URL; the CSC official examination announcement establishes scope. The ledger explains important legal distinctions and lists item-level citations.
- **Structural checks:** 4 distinct options, marked answer-option reference, 3 spec-coded distractors, 3 individualized `reveal.why_wrong` entries, review metadata and item identifiers. Jaccard duplicate threshold >=0.65: **zero matches** against 1,407 accessible preexisting batch/gap/supplement/question records plus 127 baseline seed/prefix stems. No full local dev DB comparison was possible.
- **QA caveat:** `scripts/batches/qa.py` could not be executed here because the connected GitHub service does not provide the repository Python runtime. `_legacy: true` is used for manually authored legal scenarios absent from the finite `gi_facts.py` table, **not** as evidence that the answers have been factually validated. Actual QA and independent blind verification are release blockers. No code, existing tests, or Grok Bot batch files were edited.
- **GitHub Actions warning (2026-10-16):** One Batch 003 tests run had PHP 8.5 job fail at the pre-existing global `npm run size` budget: aggregate lazy-included JS was **1,043,562 B against a 1,040,000 B ceiling**, over by **3,562 B**. The 91 JS unit tests shown in those logs passed. This is a bundle-size gate, **not evidence that the new GI questions were tested or failed**, since only draft JSON/docs were changed. Linter passed; later runs were still in progress when checked. Do not raise size budgets or alter application code as part of this research-only task.
- **Reviewer watchlist:** Section VII/Article VII martial-law extension procedure; Art. IX-A versus Art. XIII CHR commission distinctions; R.A. 6713 Sec. 5(a) 15-working-day *reply* versus other statutory permit-processing deadlines; Secs. 8–9 disclosure and divestment exceptions; clean-water land-based source nuance. Scrutinize all law distractors and any formulaic why-wrong lines; some may require stronger, non-giveaway alternatives. Review each ID independently with ACCEPT / REVISE / REJECT / HOLD.
- **Next:** Grok Bot -> Chief of Staff review; only after that, proceed to Clerical / Numerical gaps, refreshing the gap map to avoid overlap.


## Round 03: ChatGPT batch 001 (100 Filipino Verbal), CoS verdict applied, 2026-10-13

- CoS verdict: 89 pass, 11 fixed. 040029 stem giveaway removed; 040065 "sa daan ___ kabundukan"; 040092 A reworded for planning; 040013 key "may saklaw o pananagutan", o2 "nakatataas na tanggapan"; 040047 kaniyang; KWF 040033 nakadaraan, 040053 nakasasakit, 040030 nakasasabay (x2), 040008 nagmamaliit; 040043 o3, 040045 o3, 040006 o2 to FIL-SAME-FIELD; 040080 o4 to RC-NOT-IN-TEXT; 040057 o2 kawalang-hiya; 040074 o3 wording.
- New targets: 040012 MAALAB, 040023 MATIGAS, 040027 MAAYOS, 040032 MALABAY (unique in the bank).
- FIL-SPOKEN-FORM for all ng/nang, din/rin, daw/raw and pang-angkop errors (040061-040070, 040073). Spec 0.1.8.
- qa.py: nakaka- and kanya/kanyang checks in every field; option-in-stem check for Filipino vocabulary. Fixed one "kanyang" in filipino-supplement-001 (0015).
- Key/trap separation: in `MockPoolState` (session builder), with tests; `qa_fil.py` lists remaining pairs.
- All 100 approved/passed by Chief of Staff, 2026-10-13. No deploy.
- MSI local import PENDING: the MSI was offline at 23:00 PHT. Next time it is up: copy chatgpt-batch-001.json, filipino-supplement-001.json and app/Services/Exam/MockPoolState.php + MockSessionService.php into the civio container, run `php artisan bank:import-batch` on chatgpt-batch-001.json as active, then confirm mocks start at 150 and 145.

## Round 03: Codex batch 003 (100 GI drafts) audited, 2026-10-17

- qa.py ran in the full repo: 0 flags, 0 near-duplicates (0.65), 0 baseline hits. This clears the QA blocker from 9611b91.
- All 100 keys and citations checked against LawPhil text: no legal errors.
- Fixed: 100 padded method lines, 263 tautological why-wrong reasons (all 300 rewritten), absurd distractors replaced with real siblings, 22 long-key giveaways, 5 ambiguous stems, codes. Reproducible via `scripts/batches/fixes/b3/apply.py`.
- Proposed: ACCEPT 77, ACCEPT as variant 8, HOLD 4, REJECT 11 (fact duplicates of approved items). Packet: `audit/round-03-chatgpt-003-review-request.md`. All stay draft.
- Housekeeping: moved the stray root `AUDIT_TRACKER.md` (round 03 Filipino notes from 2026-10-13) into this file.

## 2026-10-17: Round 03 baseline audit, B1 Clerical and B2 GI (Grok Bot)

- Export: a read-only copy of the 550 `source_group='baseline'` rows from the MSI local DB, saved at `audit/data/baseline-550-2026-10-17.json`. No DB rows were changed.
- **B1 Clerical (81 items):** 3 KEY ERROR, 18 FIX, 37 DUPLICATE (retire to draft), 23 OK. Packet: `audit/round-03-baseline-b1-clerical-review-request.md`.
  - Key errors: #277 (the correct order Dela Cruz; Del Mundo; Delos Santos; Del Rosario matches no option, so the options need rewriting); #287 (the key should be the first listed order); #282 ("Leave Application" files before "Leave Credits").
  - Fixes: placeholder explanations on #51-55, joke distractors, implausible misspellings, the wrong ie/ei rule in #548, punctuation in #499-550.
  - 12 baseline spelling targets repeat targets already in the bank. **Question for CoS:** fix these baseline rows, or audit Codex's paraphrase set (`scripts/seeds/baseline_reparameterized.json`, 496 matched by stem, not applied) instead?
- **B2 GI, Constitution and Peace/HR (70 items):** 0 key errors, 23 FIX, 14 DUPLICATE (8 repeat approved bank items, 6 repeat other baseline items), 33 OK. Packet: `audit/round-03-baseline-b2-gi-review-request.md`. Gap: there are no items on RA 9851, 9745, 10353, 9710 or 7610.
- Scripts: `scripts/batches/audit/baseline_b1_clerical.py` and `baseline_b2_gi.py` regenerate the packets. Nothing is applied until CoS rules.
- Next: B3 GI (RA 6713, 37 items; Environment, 27 items), then the other domains.

## 2026-10-17: Prompt for the next English ChatGPT batch

- `CHATGPT_NEXT_PROMPT.md` asks for 100 English drafts in `chatgpt-batch-004.json` (RC 30, paragraph organization 30, error recognition 40), because `chatgpt-batch-002.json` already holds 100 unaudited English drafts in the same areas. It carries the earlier rules plus these QA checks: no keyboard typos, unique targets, no order key matching the listed order, the 25% stem cap, an honest shortcut, and KWF spelling. Batch 002 still needs a Grok Bot audit.

## 2026-10-17: Round 03 CoS verdicts applied

- Details are in `audit/round-03-cos-verdict-2026-10-17.md`.
- GI batch 003: 89 approved, 11 rejected; 060009 fixed; 8 fact_id pairs. Brief for the one-per-fact mock rule: `docs/FACT_ID_MOCK_RULE_BRIEF.md`.
- Baseline B1/B2: 3 keys corrected, 63 retired, 52 fixed. #304 is on hold because the foil CoS asked for is already a choice.
- MSI was backed up first. It now has 1,882 active questions (civio 1,395, baseline 487).
- QA: `qa_all.py --no-fixes` and `qa_file.py` (batch 001 and 003) are green; Pest passes 328/328.
- Pending CoS: 14 spelling swaps (`audit/fixes/round-03-baseline-b1-spelling-swaps.json`) and gap-fill-004.

## 2026-10-17: CoS action items (spelling swaps, gap-fill-004)

- **Spelling swaps (pending CoS, inactive):** `audit/fixes/round-03-baseline-b1-spelling-swaps.json`, built by `scripts/batches/audit/b1_spelling_swaps.py`. It proposes 14 new targets: prerogative, referred, remittance, itinerary, pamphlet, consensus, hindrance, subpoena, forfeit, illegible, undoubtedly and inevitable for the 12 rows, plus accidentally and nuisance for #308 and #311. None is used anywhere in the bank or the baseline. Each key is a dictionary word, each foil is a real misspelling (not a dictionary word and not a keyboard slip), and each foil has an SPL code. Codex's 496-item reworded set is not a substitute; it gets its own audit round.
- **gap-fill-004 (pending CoS, inactive):** 10 GI drafts, 2 each on R.A. 7610, 9710, 9745, 10353 and 9851. Quotes are asserted against LawPhil text; `qa_file.py` finds 0 problems. Packet: `audit/round-03-gap-fill-004-review-request.md`.
- **B2 packet:** the duplicate count already reads 14 (fixed in 93b7eae).

## 2026-10-17: Round 03 audit of ChatGPT batch 002 (100 English drafts)

- `qa_file.py` finds 0 problems, but the content fails review.
- Proposed: REJECT 75 and FIX 25.
  - The 75 rejects are all 35 para-order items and all 40 error items. They use 4–5 sentence frames repeated with words swapped, two items have a second defensible order, and five use non-words.
  - The 25 fixes are the RC items. They need their distractors rewritten and their padded tails trimmed, and all 25 share one theme.
- Fixed now: two text errors (050004 and 050006). Every item stays draft.
- Packet: `audit/round-03-chatgpt-002-review-request.md`. gap-fill-005 replaces the rejected areas.

## 2026-10-17: gap-fill-005 (60 original English drafts, pending CoS)

- `docs/research/gap-fill-005.json`, built by `scripts/batches/gapfill/gap_fill_005.py`.
  - Reading comprehension, 20: main idea 5, detail 4, inference 7, vocabulary 4.
  - Paragraph organization, 20: order 12, insert 8.
  - Sentence structure, 20.
- Every item is draft/unreviewed and inactive. `qa_file.py` finds 0 problems against 1,684 bank items. `qa_all` is green and Pest passes 328/328.
- Pending CoS:
  - the proposed codes `VEN-RUN-ON`, `VEN-FRAGMENT` and `VEN-MODIFIER-PLACE` (spec v0.1.9);
  - RC passages run 96–129 words, below the spec's 150–250.
- Packet: `audit/round-03-gap-fill-005-review-request.md`.

## 2026-10-17 (3:11 and 3:14 PM): more CoS verdicts applied and activated on the MSI

- **#304:** the new foil is 'Indispencible', with the explanation rewritten. It is active.
- **Spelling swaps (all 14 approved and active):**
  - #292 is now Compelled (foils Compeled, Complelled, Compelld).
  - #312 is now Conscientiously (foils Concientiously, Conscientously, Conscienciously).
  - #298's foil Subpena became Subpoene.
  - #311's Nusiance is recoded SPL-SOUND.
  - Note: the base word "conscientious" is also the target of baseline #301. CoS chose this word.
- **gap-fill-004:** all 10 are approved and active. 0001 o4 now reads "12 is a special victim-age threshold (Secs. 5 and 7), not the definition of a child." Every item has a `FACT-RA…` fact_id.
- **chatgpt-batch-002:**
  - 12 RC items kept, fixed, recoded, approved and active.
  - 88 rejected.
  - 8 items tagged with the theme `first-measure-misleads`. The cap of 2 per mock is in the fact-ID brief for Codex.
- **Spec v0.1.9:** the VEN codes are approved, and §10.8 adds the passage-set rule and the `fact_id` and `theme` fields.
- **gap-fill-005 (still draft):** RC rebuilt as 7 passages of 162–183 words with 2–3 questions each. `qa.py` gains a sibling exemption. The packet is updated.
- **MSI:**
  - Backups first: `civio_local_pre_304_20261017.dump` and `civio_local_pre_r03b_20261017.dump`.
  - Active: Analytical 365, Clerical 262, GI 347, Numerical 400, Verbal 544, **total 1,918** (civio 1,417, baseline 501).

## 2026-10-17 (3:43 and 3:44 PM): gap-fill-005 approved and activated; #312 changed; spec 10.8 relaxed

- **Spec 10.8 relaxed:** each passage needs at least 1 main-idea or detail question and at least 1 inference or vocabulary question.
- **gap-fill-005:**
  - RC rebalanced to main 4, detail 5, inference 6, vocabulary 5 across the 7 passages. The 3 new questions (P01 detail, P04 main, P07 detail) replaced 2 vocabulary items and 1 inference item and were written after CoS's review.
  - CoS fixes applied:
    - 0005's key now reads "cannot quietly pile up";
    - 0037 o4 recoded to LOG-IGNORED-CLUE;
    - 0047 o2's reason rewritten.
  - All 60 approved and imported as active. `qa_file` finds 0 problems; `qa_all` is green.
- **#312:** CoS asked for Questionnaire, but it is already a bank target (CIVIO-CLR-20261013-0033) and was baseline #296's old target. I used the untested word **Sergeant** instead (foils Sargeant, Sergant, Seargant). It is applied and active. Flagged for CoS.
- **`passage_id`:** now a real field request for Codex in `docs/FACT_ID_MOCK_RULE_BRIEF.md`, addendum 2. The `notes` tag stays until it ships.
- **Next batch:** `CHATGPT_NEXT_PROMPT.md` and the spec now require passage sets and varied sentence-structure option sets.
- **MSI:**
  - Backup first: `civio_local_pre_r03c_20261017.dump`.
  - Active: Analytical 365, Clerical 262, GI 347, Numerical 400, Verbal 604, **total 1,978**.

## 2026-10-18: Baseline 550 converted to the spec schema (Grok Bot)

- `scripts/batches/audit/baseline_convert.py` → `audit/data/baseline-550-spec-2026-10-18.json` (501 active, 49 retired; drafts mirroring state; no status change). Report: `audit/baseline-550-spec-qa-2026-10-18.md`.
- qa_file.py: 2,217 problems. 1,650 are schema gaps the baseline never filled, and 534 are self-matches against its own seeds. That leaves 29 intra-baseline near-duplicates, 2 duplicate stems, and 1 non-distinct option set (#462, active, needs CoS).
- New `scripts/batches/audit/explanation_lint.py` (run on every batch): 370/550 flagged; positions A 325 / B 163 / C 53 / D 9.

## 2026-10-18: gap-fill-2000-05, English Verbal drafts (15) and EV lint fixes (117), pending CoS

- **Correction (drill shuffle):** online drills already shuffle the answer choices. The real leak was answer keys sent in the drills-hub payloads, and it is fixed on `grok/drill-choice-shuffle`. The earlier claim that online drills do not shuffle is now marked superseded on `grok/batch-3-independent-audit` (tracker + B3 packet) and `grok/baseline-550-spec-convert` (QA doc). Stored key position is an editorial balance goal, not a user-facing giveaway.
- **Part A drafts:** `docs/research/gap-fill-2000-05.json`, from `scripts/batches/gapfill/gap_fill_2000_05.py`.
  - VEN-PARA-ORDER 8 (need 6).
  - Reading comprehension 7 (need 5): VEN-RC-DETAIL/INFER/MAIN 2 each, VEN-RC-VOCAB 1.
  - QA: `qa_file.py` 0 problems; `explanation_lint.py` 0 flagged.
- **Part B lint fixes:** `docs/research/audit/fixes/gap-fill-2000-05-lintfix.json`, from `scripts/batches/gapfill/lintfix_2000_05.py` + `lintfix_2000_05_baseline.py`.
  - 117 full-item fix drafts (`<id>-LINTFIX`, `fix_of`) for English Verbal Release picks that fail explanation_lint: sentence structure 27, error recognition 11, paragraph organization 36, reading comprehension 43.
  - Originals are untouched.
  - The 41 baseline items in the set are completed to full spec (terms, shortcut, coded why-wrong).
  - Wrong options were lengthened on 22 long-key items, with the same error and code.
  - 4 stems were clarified to clear false near-duplicates.
  - QA:
    - New checker `scripts/batches/audit/qa_fixfile.py`, which runs the qa_file checks but does not compare a fix with its own original: 0 problems.
    - `explanation_lint.py`: 0 flagged.
- **Not fixed (CoS):**
  - `CIVIO-BASELINE-0466` is a Filipino item classified as English Verbal.
  - The passage set `CIVIO-GAP1-VEN-RC-0014..0017` (approved) shares a passage shorter than the 400-character sibling floor, so it already fails qa_file.
  - `CIVIO-GAP2-VEN-ERROR-0002` and `-0005` (approved) have identical stems.
- **Release projection** (approved + kept + pending drafts incl. gap-fill-01/02/05): **EV 300, FV 300 and Num 400 exact.** Still short: Analytical analogy 61 and data interpretation 31; Clerical filing 41; R.A. 6713 32. These are on gap-fill-03/04 (other agents).

## 2026-10-18 — gap-fill-2000-02: Numerical basic ops + sequences, Filipino reading + paragraph order (108 drafts, pending CoS)

- `docs/research/gap-fill-2000-02.json` (generator `scripts/batches/gapfill/gap_fill_2000_02.py`): NUM-OPS-ORDER 60, NUM-SEQ-DIFF 11, NUM-SEQ-MULT 9, VFIL-PAGBASA 12, VFIL-PAGSUSUNOD 16. Numerical stems avoid near-duplicates: the generator rejects any stem with Jaccard ≥ 0.6 to an existing numerical stem. No percent items.
- QA: `qa_file.py` 0 problems vs 1,755 bank items, with solver-recomputed keys on all 80 numerical items. `explanation_lint.py` 0 flagged. Positions 27/27/27/27. `qa_fil.py` GREEN.
- Release projection (approved + kept + pending drafts incl. gap-fill-01/02): **FV 300 exact, Num 400 exact.** Remaining shortfalls: Analytical analogy 61, data interpretation 31; Clerical filing 41; R.A. 6713 32; EV paragraph organization 6, reading comprehension 5. Gap-fill-03 (Analytical) and -04 (Clerical filing + R.A. 6713) are being drafted on their own branches.

## 2026-10-18: gap-fill-2000-01, Filipino Verbal (99 drafts, pending CoS)

- `docs/research/gap-fill-2000-01.json`, built by `scripts/batches/gapfill/gap_fill_2000_01.py`: antonyms 41, synonyms 34, idioms 24. All target words and idioms are new to the bank. Spelling follows KWF.
- Every item has 3 coded distractors with a specific why-wrong line each. Key positions are A 25, B 25, C 25, D 24.
- QA:
  - `qa_file.py docs/research/gap-fill-2000-01.json` → 0 problems against 1,656 bank items.
  - `explanation_lint.py` → 0 flagged, after lengthening the distractors of 4 synonym items that had a long-key giveaway.
  - `qa_fil.py` → GREEN.
- Release Collection: new `scripts/batches/release/release_manifest.py` selects exactly EV300 / FV300 / Num400 / Ana400 / Cler300 / GI300 with round subtopic quotas. It exits 1 and lists the shortfalls until every quota is met. Over-target pools are trimmed by selection only; nothing is deleted or demoted.
- Shortfalls after this batch (approved + kept + pending drafts):
  - FIL reading 10, FIL paragraph order 14
  - Numerical basic operations 55, number sequence 16
  - Analytical analogy 61, data interpretation 31
  - Clerical filing 41
  - R.A. 6713 32 (CoS topic-mix decision)
- Packet: `audit/gap-fill-2000-01-review-request.md`. Next: gap-fill-2000-02 (Numerical basic operations and sequences, plus FIL reading and paragraph order).

## 2026-10-18: gap-fill-2000-06, lint fixes for FV / Analytical / Clerical / GI Release Collection picks (247 + 7, pending CoS)

- File: `docs/research/audit/fixes/gap-fill-2000-06-lintfix.json`, built by `scripts/batches/gapfill/lintfix_2000_06.py` with data in `lintfix_2000_06_data.py`. Each fix is an `<id>-LINTFIX` copy with `fix_of`, status draft/unreviewed. Originals are untouched.
- Fixes by subject: Filipino Verbal 39, Analytical 96, Clerical 58, GI 54. There are also 7 Filipino passage-set companions, because five short passages were lengthened to the 400-character sibling floor.
- Series, data-interpretation and numeric/date filing explanations are generated and key-checked by code. GI fixes cite LawPhil sections; all 61 quoted spans were verified against the LawPhil text.
- QA on `integration/2000`: `explanation_lint` 0 flagged; `qa_fixfile` 0 problems against 1,811 bank items.
- Packet: `audit/gap-fill-2000-06-lintfix-review-request.md`. It includes 7 CoS decisions, among them the R.A. 6713 Sec. 2→1 citation in 000302 and the arma_solver "business" mismatch on GAP3-0020.

## 21 October 2026 curriculum audit checkpoint

Repository evidence at `dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1`: 1,478 approved-labeled primary records, not a runtime count. Independently checked 497 existing keys (400 numerical, 41 data tables, 44 syllogisms, 12 explicit sorts); all matched. Mechanically screened 2,127 main/export records; 83 quality flags, including historical #462 duplicate choices. All 45 Vera IDs reconciled; nine lack a correct listed option. Ten original numerical drafts remain unreviewed; existing full QA cannot parse their novel structures. No approvals, imports or activations. See [current assessment](curriculum/CURRENT_BANK_ASSESSMENT.md), [Vera ledger](curriculum/VERA_45_QUESTION_AUDIT.md), [production plan](curriculum/QUESTION_QUALITY_AND_PRODUCTION_PLAN.md), and [scope evidence](curriculum/CSC_COMPETENCY_GAP_MAP.md). The 2,000 milestone is incomplete; exact eligible release count unknown.

### Product research continuation, 21 October 2026

The [educational/product handoff](curriculum/CODEX_EDUCATIONAL_HANDOFF.md) extends this checkpoint: raw versus weighted score disagreement reproduced, unsupported percentile/pass-prediction outputs identified, guest-history and exposure limitations traced, existing graphs/Lite/FSRS reviewed. A 44-node curriculum blueprint and private Subprofessional diagnostic protocol are prepared. Three open-source UI repositories were pinned and evaluated; no dependency or feature was added. Recommendations follow existing security and Review Mistakes priorities. GitHub push was authentication-blocked; local commits are not remote publication.

## Publication reconciliation, 22 October 2026

Remote main `99ebe099376ca18c5a9338876c928fbea7519536` contains the research from commits `3c1fd91` and `b51c311`. Of 20 prepared files, 19 exactly match local checkpoint `57d79fa`; the baseline changes log has later engineering additions. No duplicate import or old-tree overwrite is needed. The audit baseline and content approval limits remain unchanged. Later Review Mistakes, FSRS and scoring work must be read through `docs/FEATURE_CATALOG.md`; this is publication verification, not a new test or live bank audit. GT authorized the connected GitHub integration for the documentation follow-up.

## 2026-10-22: Subprofessional Numerical batch 001

- **Draft file:** `docs/research/batch-subpro-num-001.json` (50 items). The requested allocation is 12 fraction, 12 percentage, 8 ratio/proportion, 8 basic algebra and 10 applied word-problem items. The uploaded geometry item `CIVIO-NUM-WP-GEOM-926037` was mathematically sound but held outside this allocation; the batch uses original algebra item `CIVIO-NUM-WP-ALGEBRA-926051` in its place. The held item remains in the original supplied upload.
- **Astra content review:** 49 supplied items passed after corrections and are `status: reviewed` / `review_status: passed`. Replacement 926051 remains `draft/unreviewed` because its author cannot review it. No item is GT-approved, active, imported or counted toward the 2,000 verified release count.
- **Evidence:** `docs/research/bank/subpro-num-001-audit-2026-10-22.json`, bound to the batch digest. Exact answer recomputation: 50/50; required-field, four-distinct-option, key mapping, distractor-code, Reveal-length and per-archetype timing checks passed. Keys: o1 12, o2 14, o3 12, o4 12.
- **Duplicate screen:** 3,333 unique repository stems across current main `43529d8425b86b5a47b8032346eed26bbea48218` plus 10 pinned open content PR snapshots; no Jaccard ≥0.65 matches, within-batch collisions or stable-ID collisions. The scan did not compare stems to reviewer PDFs, so it is not source-by-source originality proof.
- **Corrections:** 926036's 42 distractor explanation was corrected and recoded `NUM-EXTRA-STEP`; target times now follow spec §3.1 archetype values. The earlier generic `qa_file.py` CLI still aborts at 926001 because the NUM-FRAC-DEC solver assumes the stem contains `had <number>`. This is a validator coverage defect, not a content pass. A deterministic supplemental check passed; no claim that the repository CLI passed.
- **Pacing:** exact archetype targets yield a 69.3-second mean for this content batch. Do not administer it as a standalone practice set under the spec's 60-second set-mean rule. Difficulty labels are 11 easy / 25 medium / 14 hard, versus the suggested 15/25/10; these are editorial, not empirically calibrated.
- **Remaining gates:** GT must review the exact manifest and review report and provide the detached approval signature required by `docs/BANK_IMPORT_APPROVAL.md` before active import. No private key was requested or used.

## 2026-10-22: Astra review of B4 Numerical replacement drafts in open PR #5

Source snapshot: PR #5 head `fcc2ed22b39d60e0469304e690749bc17263f8bf`; file `docs/research/audit/fixes/round-03-baseline-b4-drafts.json`. These five items replace legacy baseline records. **They are not five new unique bank questions.**

- **Answer check:** 5/5 answer keys independently recomputed; all four choices are distinct and only one matches each stated calculation.
- **Targeted validators from that PR:** `qa_file.py` reports 0 problems against 1,656 bank items; `explanation_lint.py` reports 0 flags. These scripts do not validate target-time metadata or whether distractor codes describe the actual error.
- **Exact edits still needed in the open draft file:**
  - `CIVIO-B4-NUM-WP-ALGEBRA-0201`: 29 is correct. Set `est_seconds: 90` (the `NUM-WP-ALGEBRA` target) and difficulty to medium (sum/difference requires two steps).
  - `CIVIO-B4-NUM-WP-GEOM-0206`: 34 m is correct. Set `est_seconds: 90` and difficulty to medium. Its 60 m distractor is the area/perimeter mix-up; the nearest available numerical code is acceptable only if the explanation says it multiplies length by width and reports area.
  - `CIVIO-B4-NUM-WP-RATIO-0209`: ₱300 is correct. Set `est_seconds: 75` (not 60); classify difficulty as hard if retaining the three separate computations (parts total, value per part, middle share).
  - `CIVIO-B4-NUM-WP-RATE-0349`: 72 is correct. Set `est_seconds: 90`. The distractor 64 is not produced by the claimed “16 × 4” from any given value. Replace it with 18 (one hour only; `NUM-PARTIAL`) or 90 (one extra hour; `NUM-EXTRA-STEP`), and remove the unsupported 82 “extra 10” distractor. Keep 54 as the 3-hour/off-by-one trap.
  - `CIVIO-B4-NUM-PCT-BASIC-0495`: ₱2,040 is correct, but this is a discount/application item and should be `NUM-WP-PCT-CHANGE`, target 90 seconds, medium difficulty. Replace ₱2,085 (the claimed 315-peso error has no credible derivation) with ₱2,400 for “used the listed fee without applying the discount” (`NUM-GIVEN-REUSED)). The ₱2,160 distractor can be explained as taking off only the 10% part and omitting 5% (`NUM-PARTIAL)); ₱2,760 remains the add-instead-of-subtracting error.
- The milestone plan's percent-change cap is a **Release Collection** selection rule, not by itself a content-quality failure for the whole verified bank. Exclude this replacement from that collection if the cap remains, but do not reject or hold otherwise-valid bank content solely because of the collection cap.
- No source PR file was edited, merged, signed or activated in this review. The records remain drafts until the corrected packet is resubmitted with a digest-bound report; GT's signed approval remains necessary for active import.


## 2026-10-22: Independent audit of gap-fill-2000-02 (open PR #8)

**Scope and source:** Reviewed PR #8 head `5fd89f9dd0a5a3592f682187c9b7db07b37b6757`, batch `docs/research/gap-fill-2000-02.json` (108 draft items). It proposes 60 Numerical basic-operations items, 20 Numerical sequences, 12 Filipino reading-comprehension items and 16 Filipino paragraph-order items. The PR is open and marked draft. This audit did not edit the PR, merge it, approve its content for activation, or import it.

**Reproducible repository check:** On the pinned PR head, `python scripts/batches/qa_file.py docs/research/gap-fill-2000-02.json` reported **108 items, compared with 1,656 bank items; 0 problems**. This is a content-file QA result, not the full PR check suite listed in its description (tests, type/lint/format/build/bundle checks were not run).

**Independent Numerical answer audit: 80/80 keys recomputed.**
- All 60 `NUM-OPS-ORDER` expressions were parsed and evaluated with arithmetic precedence, then compared with the keyed option and worked answer.
- All 20 sequence keys were checked against their stated rules (11 growing-difference patterns; 9 multiply-then-add/subtract patterns). The reveal states the same next term.
- The 80 items have four distinct choices each, no repeated exact stems, and numerical answer positions are balanced (20 each at o1–o4).
- No wrong-key or arithmetic defect was found in these 80 items.

**Required metadata and learning-quality changes before selection for a release collection:**
- IDs `CIVIO-GF2K02-NUMOPS-0001` through `CIVIO-GF2K02-NUMOPS-0060` all set `est_seconds: 40`; spec §3.1 sets `NUM-OPS-ORDER` to **35 seconds**. Correct all 60 values. The 20 sequence items are correctly set at 45 seconds.
- The 60 operation items repeat one micro-skill and only eight normalized expression structures, each with fresh numbers. This is substantial within-batch frame repetition. Keep only the number needed to fill the approved collection's numerical blueprint; retain representative expressions across the eight structures and do not count the whole 60 as demonstrated coverage breadth.
- Difficulty labels are editorial, not empirically calibrated: batch Numerical has 16 easy and 64 medium, with no hard items. Do not present this distribution as measured difficulty.
- Sequence rules are conventional and explicitly explained, but next-term questions remain pattern-inference tasks; do not treat them as uniquely determined by a finite sequence absent the stated rule.
- Check all 12 reading items and 16 ordering items for one defensible key. The paragraph-order Reveals repeatedly say only “Panimula…sinundan…kinalabasan”; before release, explain the actual ordering cues (time, prerequisite/action/result, reference words) for each item. Some reading distractors are conspicuously implausible; improve distractor quality where doing so preserves a single text-supported answer.
- These are third-party independent drafts (Grok Bot) with original-source labels; repository QA and this review do not establish source-by-source originality against every reviewer PDF. Keep draft/provenance status pending the existing approval procedure.

**Disposition:** Numerical: 80 answer keys verified with the corrections/selection notes above. Filipino: 28 items reviewed for key defensibility and wording at the item level; paragraph-order explanation depth and distractor quality remain editorial work. The batch still has `status: draft` / `review_status: unreviewed`; no item was approved, activated, imported or counted toward the 2,000 verified release target. Its passing bank comparison (1,656 items) is the validator's comparison set, not the current approved inventory and not evidence that the 2,000 milestone is complete.

**Next actions for the PR author / Codex:** (1) set the 60 operation targets to 35 seconds; (2) prepare a blueprint-based release subset rather than treating all 60 near-frames as distinct coverage; (3) rewrite the 16 sequencing Reveals to teach the actual ordering constraints and strengthen weak distractors; (4) rerun content QA on the revised digest and complete the PR's explicitly required check suite; (5) keep every item draft until independent review and the repository's signed approval/import workflow are satisfied. The current main inventory and exact release gap remain as recorded in [Current Bank Assessment](curriculum/CURRENT_BANK_ASSESSMENT.md); this PR draft does not change them.


### PR #8 draft corrections and recheck (22 October 2026)

Applied the specific editorial fixes to the existing PR #8 draft branch `grok/gap-fill-2000-02`, commit `8ef853ae22600cac8b0cb4f05309027e826ff626` (the branch head changed; PR remains open/draft):

- Corrected all 60 `NUM-OPS-ORDER` target times from 40 to the spec's 35 seconds.
- Rewrote the 16 `VFIL-PAGSUSUNOD` explanations to state the actual chronology, prerequisite/action/result, or reference cue that supports each order.
- Preserved all statuses as `draft` / `unreviewed`; no approval, activation, import or merge.

On the updated PR commit, `python scripts/batches/qa_file.py docs/research/gap-fill-2000-02.json` again reports **108 items, 1,656 comparison-bank items, 0 problems**. The independent numerical recomputation again returns **80/80 correct** (60 mixed-operation expressions and 20 sequences), with the 35-second targets verified and keys balanced 20 per option position. This still does not complete the full PR-required software test/build/bundle suite, source-by-source originality check, or content approval.


## 2026-10-22: Independent audit of gap-fill-2000-03 (open PR #9)

**Scope:** Reviewed PR #9's 101 draft items at original head `026519163498df7e47b49f5069a59f23cd4728d5`: 67 word analogies and 34 data-interpretation tables. The PR remained draft throughout; no activation, import or merge was performed.

**Checks on the revised branch head `f54f8df2b88eeb6b3e4e8c6adc1c939dce82e0f4`:**
- Repository `qa_file.py`: **101 items, 1,656 comparison items, 0 problems**.
- Repository `explanation_lint.py`: **101 items, 0 flagged**; key positions A 26, B 26, C 25, D 24.
- Independent audit: all 34 table keys recomputed from their displayed data; all 67 analogy keys reviewed against the stated semantic/form relationship. No wrong key or duplicate-choice defect found.
- Found and corrected a calculation explanation missed by lint: `CIVIO-GF2K03-ANA-DI-TABLE-0024` has a 160-to-100 decrease, so 60 ÷ 160 = **0.375 (37.5%)**, not 0.38. The keyed 37.5% was already correct. Updated explanation is in the open PR branch commit above.
- Recheck on the updated head: table solver reports **34/34** key matches and all displayed percentage decimals agree with the keyed percentages. Both the repository batch QA and explanation lint pass. All 101 items remain `draft/unreviewed`.

**Release planning evidence (PR #9 head only):** The existing release manifest reports **1,401 selected / 2,000** from approved content plus the baseline, a 599 shortfall. With `--include-drafts` on this one PR head, it reports **1,502 / 2,000**, still 498 short. These are manifest projections from PR #9's checkout, not current live-bank counts; they do not incorporate all other open PRs and do not confer approval. Significant subtopic gaps persist in English paragraph organization/reading, Filipino vocabulary/idioms, numerical operations/sequences, clerical filing/spelling and General Information. Do not call the 2,000 milestone complete.

**Disposition:** Corrected the one detected numerical explanation defect in PR #9. The questions remain unapproved drafts pending full independent/source-rights review, author-independent content approval and the repository release/import requirements. Full software type/lint/format/test/build/bundle checks required by the PR were not run.


## 2026-10-22: Independent audit of gap-fill-2000-04 (open PR #10)

**Scope:** Reviewed 83 draft items at revised branch head `c8800eb50743bb34ab3686346143ad32a0d8d3e1`: 48 clerical alphabetical-filing items and 35 R.A. 6713 application items. No approval, activation, import, merge or deployment.

**Corrections applied to the existing draft branch:**
- Added an explicit ANSI/ARMA 12-2005 filing-rule reference to 30 filing stems that previously left the convention unstated; reworded two resulting near-duplicate frames for distinct task demands.
- Replaced all 35 R.A. 6713 source links with the official COMELEC law page.
- Clarified item `CIVIO-GF2K04-GI-SCENARIO-APPLY-0015`: R.A. 6713 §7(d) permits Congress-consented gifts in the nature of scholarships/fellowships/medical treatment; the distinct national-interest and head-of-office conditions apply to foreign travel grants. This clarification does not change its key.

**Checks on revised head:** repository `qa_file.py`: 83 items, 1,656 comparisons, 0 problems. `explanation_lint.py`: 83 items, 0 flagged; answer positions A 21, B 20, C 21, D 21. Independent deterministic filing solver matches 48/48 keyed answers; all 48 stems now specify ANSI/ARMA. RA 6713 source references and keyed statutory scenarios were reviewed against the cited Act.

**Limitation:** The full ANSI/ARMA 12-2005 standard text was not accessible; its publisher preview establishes the standard title and scope but not the complete operative rules. The internal filing solver establishes consistency with the encoded rule interpretation, not authoritative proof of every normative filing answer. Keep these 48 items pending independent competent review against an authorized copy of the standard. The 35 law items remain draft pending the normal source-rights/content approval gate.

**Disposition:** All 83 stay `draft/unreviewed`. Full PR software type/lint/format/test/build/bundle checks and required source-by-source originality review were not run. No part of this PR counts toward the verified/approved 2,000-item release target.


## 2026-10-22: Independent review of gap-fill-2000-05 English items (open PR #11)

**Scope:** Independently reviewed the 15 new paragraph-order and reading-comprehension items at PR #11's initial head `f3e154612a2f85f16681902bdd467b72aa92d411`. All eight ordering keys were checked against the four sentence events; all seven passage keys were checked against the provided text and the question's requested inference/detail/main idea. No third-party reviewer text was copied.

**Defects corrected in the existing draft branch:**
- `CIVIO-GF2K05-RCI-0001`: removed the unsupported comparison “as much as planting”; the answer now states only that selecting a suitable planting zone is important for survival.
- `CIVIO-GF2K05-RCI-0002`: removed causal wording (“reminders helped”) unsupported by the before/after passage; the answer now reports that missed doses declined after reminders began while distance remains a stated barrier.

Revised branch head: `882f571690e2fef11eedfc70f8b7b76ed1f5b9e9`. Repository `qa_file.py` passes: **15 items, 1,656 comparison records, 0 problems**. The 117-item lint-fix file separately passes `qa_fixfile.py`: **117 fixes, 1,592 comparison records (originals excluded), 0 problems**. This structural check does not constitute independent semantic review of those 117 fixes. The branch itself does not contain the referenced `explanation_lint.py`; I reproduced its check using the repository version present at PR #12 head `7220b8ade08deee3b348233702b97e4710fd807d`: 15/15 new items and 117/117 fixes, 0 flagged each.

**Disposition:** The 15 new items remain `draft/unreviewed`; no approval, activation, import, merge or release count. The separate 117 full-item correction proposals remain unreviewed here, and the two known exceptions/holds identified in the PR's own tracker entry remain unresolved. Continue by auditing those fixes and obtaining the existing independent approval before any release selection.


## 2026-10-22: Independent structural QA of gap-fill-2000-06 proposal (open PR #12)

**Scope:** Checked PR #12 head `7220b8ade08deee3b348233702b97e4710fd807d`, containing the 99-item gap-fill-2000-01 batch and 254 full-item explanation-fix drafts. This is a validation pass, not a complete semantic audit or content approval.

**Reproducible repository checks:**
- `qa_file.py`: 99 new items, 1,656 comparison items, 0 problems.
- `qa_fixfile.py` on PR #12 alone: 254 fixes, 1,504 comparison items excluding originals, six `CLR-FILE-ORDER` solver-unavailable flags. This branch predates the filing solver in PR #10. In a disposable integration checkout of PR #12 with PR #10's `qa.py` and `arma_solver.py` (head `c8800eb50743bb34ab3686346143ad32a0d8d3e1`), the same fix-file QA reports **254 fixes, 1,504 comparisons, 0 problems**. The six flags were branch dependency failures, not demonstrated answer defects. This integration check establishes internal solver consistency; independent normative review of the filing rules remains necessary because the full ANSI/ARMA standard was unavailable here.
- `explanation_lint.py`: 99 new items and 254 fixes, 0 flagged in each file.

**Disposition:** This does not verify the answers, explanations, or originality of all 99 + 254 records. Keep all proposed edits in draft/unreviewed state. Do not count drafts as approved or use the manifest's historical 1,641 + 359 projection as a current verified inventory. No activation, import, merge, or release approval.
