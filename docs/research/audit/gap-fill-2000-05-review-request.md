# gap-fill-2000-05: English Verbal drafts and EV lint fixes, review request for Chief of Staff

Grok Bot, 2026-10-18. Everything here is draft/unreviewed. No bank item has been edited and no status has changed.

## Part A: new drafts (15). File `docs/research/gap-fill-2000-05.json`

| Subtopic | Archetypes | Drafts | Need | Buffer |
|---|---|---|---|---|
| Paragraph organization | VEN-PARA-ORDER | 8 | 6 | +2 |
| Reading comprehension | VEN-RC-DETAIL 2, INFER 2, MAIN 2, VOCAB 1 | 7 | 5 | +2 |

- **Paragraph order items:** four sentences labelled P–S and shown shuffled (never already in order). There are three distractors, each with its own code:
  - PO-OPENER-MISPLACED: the outcome is placed first
  - LOG-ORDER-SWAP: the middle two sentences are swapped
  - PO-TRANSITION-IGNORED: the outcome is placed before the last step
- **Reading comprehension items:**
  - Original public-service passages.
  - Wrong options coded RC-OPPOSITE, RC-NOT-IN-TEXT, and RC-EXTREME, RC-TOO-NARROW or RC-TOO-BROAD.
  - The vocabulary item uses VRB-ANTONYM-TRAP and VRB-SYNONYM-TRAP.
- **Legacy flag:** the items carry `_legacy: true`, the same as gap-fill-005, because there is no solver for passage items. Each why_correct names the supporting sentence.
- **QA:** `qa_file.py` 0 problems; `explanation_lint.py` 0 flagged; positions 4/4/4/3.

## Part B: lint fixes (117). File `docs/research/audit/fixes/gap-fill-2000-05-lintfix.json`

- **What they are:** full-item proposals with id `<orig>-LINTFIX` and `fix_of: <orig>`, covering every English Verbal Release Collection pick that failed `explanation_lint.py`. Accepting a fix means replacing the original's reveal/options with the fix.
- **Coverage by subtopic:**

| Subtopic | Fixes |
|---|---|
| Sentence structure (priority) | 27 |
| Error recognition | 11 |
| Paragraph organization | 36 |
| Reading comprehension | 43 |

- **Changes:**
  - Every why_correct now opens with `Answer: "<key>"` followed by a specific reason.
  - Boilerplate removed: "Therefore, the correct option is ... The other choices fail because the other choices ...", and the generic first sentence on the gap-fill-005 structure items.
  - The "Local practice item for Docker study" placeholders and the too-short agreement explanations are rewritten by hand.
  - The 41 baseline items are completed to full spec: terms, shortcut, a spec code and why for every wrong option.
  - **Long-key giveaways (22 items):** the wrong options are rewritten to similar length, keeping the same error. One rewrite was checked so it does not create a second correct answer: in BASELINE-0114 the old "...before the manager arrived" would also be complex, so it now reads "...on Monday and left the office at noon".
  - **Clarified stems:** BASELINE-0023, 0114, 0117 and 0453 were false near-duplicates of other short baseline stems and have been reworded. GAP2-VEN-ERROR-0002 was a duplicate of -0005 and has also been reworded.
- **QA:**
  - `scripts/batches/audit/qa_fixfile.py` (new): the same checks as qa_file, except a fix is not compared with its own original. Result: 0 problems.
  - `explanation_lint.py`: 0 flagged; positions A 42, B 33, C 23, D 19.
  - Solvers still recompute the 7 agreement items. The hand-written verbal and baseline fixes are marked `_legacy`, like gap-fill-005.

## Needs a CoS decision (not fixed here)

1. `CIVIO-BASELINE-0466` is a Filipino-language item filed under English Verbal. Move it to verbal_fil or drop it from the EV pick.
2. `CIVIO-GAP1-VEN-RC-0014..0017` (approved) share a passage shorter than the 400-character sibling floor, so the approved set already fails qa_file. Lengthen the passage or keep one question.
3. Several baseline paragraph/RC items are definition-style questions with weak distractors (e.g. 0025, 0122, 0123, 0124). They are now lint-clean and full-spec, but CSC-style replacements would be stronger. Recommend replacing them over time.
4. On the drill-shuffle correction: drills do shuffle choices, and the key leak in drills-hub payloads is fixed on `grok/drill-choice-shuffle`. The earlier contrary notes are marked superseded.

Accept, revise or reject each ID.
