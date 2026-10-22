# gap-fill-2000-03: Analytical (101 drafts), review request for Chief of Staff

Grok Bot, 2026-10-18. File `docs/research/gap-fill-2000-03.json`. Generator `scripts/batches/gapfill/gap_fill_2000_03.py`, with its content in `gf03_analogies.py` and `gf03_di.py`. Every item is `draft` / `unreviewed`, and nothing is imported.

## Why

The Release Collection quota (`release_manifest.QUOTA`) for Analytical is word analogy 120 and data interpretation 100. Before this batch, the pool held 59 analogy items (30 Civio + 29 baseline) and 69 data interpretation items (41 + 28), so analogy was **61 short** and data interpretation **31 short**. This batch adds 67 analogy and 34 table items, which is the gap plus a buffer of about 10% (6 and 3 items).

`release_manifest.py --include-drafts`, run with the converted baseline export, now gives Analytical exactly **400**:

| Subtopic | Quota | Pool |
|---|---:|---:|
| Word analogy | 120 | 126 |
| Symbolic logic | 80 | 108 |
| Assumptions and conclusions | 100 | 129 |
| Data interpretation | 100 | 103 |

## Contents

**Word analogy (67).** All five spec relation types (§3.4) are covered:

| Type | Items | Note |
|---|---:|---|
| Degree | 17 | The bank had only 3 |
| Synonym/antonym | 14 | 7 synonym, 7 antonym |
| Part/whole and member/group | 12 | |
| Function | 12 | Tool : use, worker : tool, maker : product, container : contents, document : what it allows |
| Word form | 12 | Real grammatical forms: irregular and Latin/Greek plurals, past tense, past participle, pronoun case, possessive pronoun, comparative, noun forms, abbreviation, female form |

- **Frames:** four stem frames (A1–A4), and each relation type uses at least 3 of them.
- **Distractors:** each wrong choice has its own spec code (`ANA-REVERSED`, `ANA-SAME-TOPIC`, `ANA-OTHER-RELATION`, `ANA-ONE-LINK`, `ANA-SOUND`) and a Reveal line that names that pair's real link.
- **No reversed distractor on symmetric links:** synonym/antonym items use `ANA-SOUND` (real confusables such as council/counsel or stationary/stationery) instead. A reversed synonym or antonym pair would still be a correct answer.
- **Fresh content:** no stem pair, key pair or distractor pair repeats an analytical stem or option already in the bank. One stem ("sentence : paragraph") hit the baseline pair check, so I replaced it with "room : house".
- **Difficulty:** easy 20, medium 33, hard 14.

**Data interpretation (34), all `ANA-DI-TABLE` as text tables.** `ANA-DI-CHART` stays out until the image pipeline exists (spec §3.4).

- **Why:** the bank's 41 Civio table items test only "table total" and "table diff". This batch adds the other skills CSC expects:

| Skill | Items |
|---|---:|
| Average (row or column) | 6 |
| Difference (rows, columns or row totals) | 6 |
| Percent share (of a row total, a column total, or the grand total) | 5 |
| Percent increase or decrease | 4 |
| Compare rows (highest total, largest increase, largest percent increase, fewest) | 4 |
| Ratio in lowest terms | 3 |
| Totals (column, row or grand) | 6 |

- **Scale traps:** 6 tables are "in thousands of pesos". 4 of them ask for an amount in pesos and carry a `DI-SCALE` trap. In the other 2, the scale is a decoy, because the answer is a percent.
- **Format:** each stem is a title line, a pipe table (`Head | Col | Col`, one line per row), a blank line, then the question.
- **Figures:** all invented, for unnamed offices. No real LGU, agency or statistic is described.
- **Difficulty:** easy 10, medium 15, hard 9.

**Positions and lengths:**

| Check | Result |
|---|---|
| Answer positions, whole file (A/B/C/D) | 26 / 26 / 25 / 24 |
| Answer positions, analogy (A/B/C/D) | 17 / 17 / 17 / 16 |
| Answer positions, tables (A/B/C/D) | 9 / 9 / 8 / 8 |
| Analogy key is the longest choice | 16 of 67 (24%) |
| Table key is the longest choice | 4 of 34 |

## QA (all run on this branch)

- `qa_file.py docs/research/gap-fill-2000-03.json`: **0 problems** (compared against 1,656 bank items, including the baseline and the near-duplicate check at 0.65).
- `audit/explanation_lint.py --strict`: **0 flagged**, no POSITION warning.
- **Keys recomputed by code:**
  - Analogies are checked through a registry that `qa.solve_ana` now reads, alongside `analytical.ANALOGIES`.
  - Tables are checked by a new independent solver, `scripts/batches/di_grid.py`. It parses the table and the question from the stem text only.
  - The generator asserts that the solver result equals the key for all 34 tables, and that all 4 options are distinct.
- `qa_all.py`: GREEN after the `qa.py` change.

**Code change to review:** `scripts/batches/qa.py`. `solve_ana` sends pipe-table stems to `di_grid.solve` and adds the gap-fill analogy registry. Older items take the same paths as before. `explanation_lint.py` and `release_manifest.py` are carried over unchanged from `grok/gap-fill-2000-01`.

## Reviewer focus (please rule)

1. **Code reuse in tables.** `CIVIO-GF2K03-ANA-DI-TABLE-0020` (fewest absences) and `-0030` (largest percent increase) code the "picked the wrong end" distractor as `LOG-ORDER-REVERSED`. The spec has no DI code for most-vs-fewest. Approve the reuse, or add a code such as `DI-WRONG-END`.
2. **Close degree pairs (hard tier):**
   - respect : reverence → fondness : adoration
   - skirmish : war → squabble : feud (a feud is longer as well as bigger)
   - frugal : miserly → confident : arrogant (a trait and its excess)
   - glance : stare → sip : gulp
3. **Word-form items:**
   - "Department : Dept." → "Avenue : Ave." (abbreviation style)
   - "we : ours" → "they : theirs" (possessive pronoun, not determiner)
   - "go : went" has "swim : swum" as the participle trap
   - "write : written" has "take : took" as the simple-past trap
4. **Table rendering.** The app shows stems as text, so the table appears as pipe-separated lines. This is readable, but a real table renderer for `ANA-DI-TABLE` stems would be better (app work, Astra).
5. **Accept, revise or reject each ID.** Six analogy items and three table items are buffer.

## Not in this batch

- Charts (`ANA-DI-CHART`), which wait for the image pipeline.
- "Which statement is supported by the table?" items (`DI-NOT-SUPPORTED` as the key idea). These need a hand-written solver.
- "Cannot be determined" keys.
- `AUDIT_TRACKER.md` is not edited here, to avoid merge conflicts with gap-fill-2000-01, 02 and 04.
