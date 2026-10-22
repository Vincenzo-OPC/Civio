# gap-fill-2000-06: lint fixes for the non-English Release Collection picks, review request for Chief of Staff

Grok Bot, 2026-10-18. Everything here is draft/unreviewed. No bank item has been edited and no status has changed.

## What this is

File `docs/research/audit/fixes/gap-fill-2000-06-lintfix.json`, 254 items:

- **247 lint fixes.** These are full-item proposals with id `<orig>-LINTFIX` and `fix_of: <orig>`. They cover every Filipino Verbal, Analytical, Clerical and General Information Release Collection pick that fails `explanation_lint.py`. Accepting a fix means replacing the original's stem, options and reveal with the fix.
- **7 passage-set companions.** See "Filipino passage sets" below.

Built by `scripts/batches/gapfill/lintfix_2000_06.py`, with data in `lintfix_2000_06_data.py`:

```
python3 scripts/batches/gapfill/lintfix_2000_06.py docs/research/release/release-collection-manifest.json
```

The manifest comes from `release_manifest.py` on the integration bank.

| Subject | Subtopic | Fixes |
|---|---|---|
| Filipino Verbal (39 + 7 companions) | reading | 16 (+7) |
| | synonym/antonym | 10 |
| | grammar | 9 |
| | idiom | 4 |
| Analytical (96) | data interpretation | 58 |
| | symbolic logic (letter series) | 24 |
| | word analogy | 12 |
| | assumptions and conclusions | 2 |
| Clerical (58) | spelling | 34 |
| | filing | 24 |
| General Information (54) | constitution | 22 |
| | peace and human rights | 18 |
| | environment | 8 |
| | R.A. 6713 | 6 |
| **Total** | | **247 + 7 = 254** |

Lint flags fixed: PLACEHOLDER 128, LONG-KEY 69, KEY-NOT-STATED 58, GI-NO-SECTION 13, BOILERPLATE 3. One item can have several flags.

## What changed

- **Answer line.** Every why_correct opens with `Answer: "<key>".` and then gives the specific reason. Filipino items explain in Filipino.
- **Explanations generated and checked by code where a rule exists:**
  - **Letter series (24):** the generator recomputes both letter jumps, asserts the key, and writes each wrong option's actual error (for example `its first letter (Q) is P + 1, but the first letters move by +4`). The original why_wrong lines for several series were factually wrong, such as "moves by 2" when the jump was 4.
  - **Data interpretation tables (58):** the generator re-reads the table, asserts the key, and names each distractor's slip: total instead of one month, wrong column, average, two-month sum, wrong month.
  - **Numeric and date filing:** the generator re-sorts the list, asserts the key, and states the full sorted order.
- **Explanations written by hand:**
  - Analogies, assumptions, Filipino items, GI, and the 34 spelling items. Each spelling item gives the correct spelling and names the error in each wrong spelling.
  - The 37 baseline items are completed to full spec: terms, shortcut, a spec code and a reason for every wrong option.
- **Long-key giveaways (69 items, 70 option sets).** Wrong options were rewritten to a length similar to the key, and they keep the same error. In a few legacy and Filipino items the key was shortened instead (WIKAIN-0012, VFIL-0055, PAGBASA-040077, PAGBASA-040078, BASELINE-0135, 0139, 0141, 0248). I checked every rewrite for a second correct answer. Notes:
  - In BASELINE-0056, the new distractors Art. XIII and Art. XI do not contain the sovereignty clause, which is Art. II, Sec. 1.
  - In GI-060051 and GI-060055, the replacement distractors are other R.A. 6713 Sec. 4(A) norms, and each why_wrong cites that norm's letter: (c) justness, (f) nationalism.
  - In GI-000505, "Six" became "Twelve" because the count is eight.
- **GI citations.** All 54 GI fixes cite a section or article, and `source_url` points to the LawPhil text. Every quoted law span (61) was checked by code against the LawPhil texts of the 1987 Constitution and R.A. 6713, 11313, 9003, 8749, 9745 and 9851, using normalized substring matching. All 61 were found; 0 are missing.
- **Fix bookkeeping.** Each fix is status `draft`, review_status `unreviewed`, source_group `civio`, and has notes ending "Pending CoS". Reviewer fields are removed from the copies.

## Stems changed (QA near-duplicate or solver format)

- **Filipino passage sets.** The five 4-question sets VFIL-0055–0074 had passages under the 400-character sibling floor, so each sibling was flagged as a near-duplicate of the others. That includes the approved originals. One neutral sentence was appended to each passage, and it does not change any key:
  - Battery box: "Hinikayat din ang mga residente…"
  - Munisipyo: "May nakapaskil na karatula…"
  - Reading corner: "Inaasahan ng mga guro…"
  - Talaan: "Inilalagay rin sa talaan ang petsa…"
  - Kooperatiba: "Itinatala rin nila sa isang kuwaderno…"
- **Companions.** Seven siblings in those sets were already lint-clean: 0057, 0063, 0064, 0066, 0067, 0068 and 0072. They are included as companions with the same lengthened passage and unchanged explanations, so that a set never holds two versions of one passage. Accept or reject each set as a whole.
- **Filipino grammar stems:** VFIL-0047, 0048, 0049 and 0053 were near-duplicates of each other or of baseline stems. They are now item-specific, for example "…tungkol sa palarong ipinagpaliban dahil sa ulan?"
- **Letter series re-based:** 000251 (+1), 000363 (−2), 000647 (+4) and 000747 (−1) repeated a bank series shifted by one step. Every letter in the stem and options was moved by the same amount, so the rule and the errors stay the same. The key is recomputed.
- **Numeric and date filing:** CLR-20261013-0009..0020 had template stems that were near-duplicates of each other. Each now names its record type, for example "Which dated signed meeting minutes sheet…". They are marked `_legacy` because the repo has no solver for CLR-NUMERIC or CLR-CHRONOLOGICAL; the generator asserts each key instead.
- **Analogy:** ANALOGY-FORM-000954 now reads `Which pair is linked the same way as "frown : displeasure"?`
- **ANALOGY-PART-WHOLE-000009** is marked `_legacy`. The repo analogy table maps PAGE : BOOK to "brick : wall", which is a different generated variant, so the solver cannot check this item.
- **Clerical:**
  - CLR-FILE-POSITION-000895: the names were made distinct (Rosalinda B. Dizon, Andres D. Villanueva, Imelda N. Manalastas).
  - GAP3-CLR-FILE-ORDER-0016 and 0020: the stems now say "which **business** name". arma_solver uses business indexing only when the stem says "business" or "organization". The approved original 0020 fails the solver on integration for this reason.
- **GI:** WHO-HOLDS-POWER-000905 is now "Which institution does the 1987 Constitution vest with the legislative power?" and 001011 is now "Under the 1987 Constitution, where does judicial power reside?" Both were near-duplicates of the executive-power stem. Each carries `_fact`, the gi_facts index of the original stem, so the fact check still matches after acceptance.

## QA (run on `integration/2000`, full merged bank)

- `python3 scripts/batches/audit/explanation_lint.py docs/research/audit/fixes/gap-fill-2000-06-lintfix.json` reports 254 items, **0 flagged**. Key positions are A 83, B 63, C 54, D 54; the originals' positions are unchanged.
- `python3 scripts/batches/audit/qa_fixfile.py docs/research/audit/fixes/gap-fill-2000-06-lintfix.json` reports 254 fixes against 1,811 bank items, with originals excluded, and **0 problems**. This covers schema, codes, solvers for series, tables, analogies and ARMA, near-duplicates, baseline hits and spelling.
- A code check confirmed that no why_wrong or why_correct still contains the old text of an option that was replaced.
- `_legacy`: 62 fixes, which are the hand-checked formats that have no solver. The other analytical and clerical fixes are recomputed by the repo solvers.
- `qa_fixfile.py` is copied from `grok/gap-fill-2000-05` so this branch can run it.

## Needs a CoS decision (not fixed here)

1. **Passage-set floor.** The approved originals in VFIL-0055–0074 fail the sibling floor today. Accepting the five lengthened sets, including the companions, fixes this.
2. **R.A. 6713 citation.** GI-TERM-MATCH-000302 cited "Sec. 2" for the short title. On LawPhil the title is **Sec. 1**, and the fix corrects it.
3. **GI-TERM-MATCH-000509:** the wrong options now share the key's "until otherwise provided by law" qualifier, so the qualifier no longer gives the answer away. Confirm the wording.
4. **Duplicate baseline facts:** BASELINE-0039/0165, 0040/0166 and 0163/0172 test the same fact. Keep one of each pair in the Release Collection.
5. **"Pilotist"** (BASELINE-0031) is not an English word. It is replaced by "Sculptor" in the fix.
6. **arma_solver and the word "business":** the approved GAP3-0020 fails the solver as written. Accept the reworded stem, or change the solver rule.
7. **Re-based series and record-type stems:** these change the visible stem of approved items. Confirm this is acceptable as a fix rather than as a new item.

Accept, revise or reject each ID.
