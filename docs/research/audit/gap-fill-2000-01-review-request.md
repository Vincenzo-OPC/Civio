# gap-fill-2000-01: Filipino Verbal (99 drafts), review request for Chief of Staff

Grok Bot, 2026-10-18. File `docs/research/gap-fill-2000-01.json`, generator `scripts/batches/gapfill/gap_fill_2000_01.py`. Every item is draft/unreviewed. Nothing is imported.

- **Why:** the 2,000 plan needs FIL 300. The pool had 188 approved items plus 1 baseline item. Per-subtopic quotas: synonym 75, antonym 60, idiom 45, grammar 45, reading 45, paragraph order 30.
- **Contents:** antonyms 41 (fills 60 with a 1-item buffer), synonyms 34 (fills 75 with an 8-item buffer), idioms 24 (fills 45 with a 2-item buffer).
- **Standards:**
  - Every target word and idiom is new to the bank (checked against all verbal_fil stems and options).
  - Each stem gives a sentence context.
  - Each item has three distinct distractor types:
    - antonyms: synonym trap, same field, weaker degree
    - synonyms: antonym trap, same field, other trait
    - idioms: literal reading, opposite meaning, other trait
  - KWF spelling, with no nakaka- and no kanya.
  - Lengths are balanced (no long-key giveaway) and positions are balanced 25/25/25/24.
- **QA:** `qa_file.py` 0 problems; `explanation_lint.py` 0 flagged; `qa_fil.py` GREEN.
- **Reviewer focus:**
  - Idiom forms: "PANTAY NA ANG PAA" (also said "pantay na ang mga paa"); "MAHABA ANG BUNTOT" (spoiled and hard to command).
  - Synonyms where a same-field distractor is close: SAKUNA/bagyo, LIPON/kawan, BUKAS/"handang tumanggap".
  - Antonym weak-degree options that could be argued as partial antonyms (e.g. MAINIT/"maligamgam").
  - Accept, revise or reject each ID.
- **Not covered here:** FIL reading (10 short) and paragraph order (14 short) need passage work and come in gap-fill-2000-02.
