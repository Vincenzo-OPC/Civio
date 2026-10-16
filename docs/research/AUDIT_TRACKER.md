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
- **Reviewer watchlist:** Section VII/Article VII martial-law extension procedure; Art. IX-A versus Art. XIII CHR commission distinctions; R.A. 6713 Sec. 5(a) 15-working-day *reply* versus other statutory permit-processing deadlines; Secs. 8–9 disclosure and divestment exceptions; clean-water land-based source nuance. Scrutinize all law distractors and any formulaic why-wrong lines; some may require stronger, non-giveaway alternatives. Review each ID independently with ACCEPT / REVISE / REJECT / HOLD.
- **Next:** Grok Bot -> Chief of Staff review; only after that, proceed to Clerical / Numerical gaps, refreshing the gap map to avoid overlap.
