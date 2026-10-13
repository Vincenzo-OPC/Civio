# Civio audit tracker (single source of progress)

The rules are in spec §7 and §10. Never auto-approve or deploy. Batch 001-011 approval stays as Chief of Staff recorded it.

| Round | Date | Items / files | Pass | Fix | Fail | Report |
|---|---|---|---|---|---|---|
| 01 | 2026-10-13 | ChatGPT supplements 001: 150 (VFIL 80, GI 30, CLR 40) | 0 release-ready (140 content-pass) | 140 | 10 | audit/round-01.md |
| 01 fixes | 2026-10-13 | All 150 supplement items fixed (still draft); gap-fill-001 23 | gap-fill: 20 CoS PASS + 3 fixed → approved | 150 fixed | 0 open | audit/round-01-fixes.md |
| 02 | 2026-10-13 | Batches 001-011, Subprofessional domains: 759 (CLR 151, VEN 203, GI 102, NUM 303) | 759 key-correct | ~27 proposed (CoS) + 58 metadata applied | 0 | audit/round-02.md |
| 02 gap | 2026-10-13 | gap-fill-002: 14 new drafts (VEN error 5, NUM frac/dec 6, CLR business filing 3) | pending review | – | – | audit/round-02-review-request.md |

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
