# Adaptive learning

The reader-facing map of the engines, including the class names, is
[`ENGINES.md`](ENGINES.md). This file is the shorter status note.

Phase 0 looked at the current exam, not a new app.

What already teaches without an AI call:

- `RevealTutor` recomputes rectangle perimeter, order of operations, and a few number patterns. A lesson is published only when it matches the stored key. A mismatch is a conflict, and the stored explanation is kept.
- The explanation panel already hid empty sections.
- Guest study bias and follow-up items already exist. They are not a full mastery model.

What this pass changed (Phase 1 slice):

- The study button is **Show Explanation**. The panel heading is **Understand the Answer**.
- Extra parts keep their own names: Step-by-Step, Exam Tip, Common Mistake, Explain Simpler, Try Another, Diagram.
- Terminal-digit filing is taught by groups, with a three-group diagram, only when the key is the last group.
- A two-solution mixture is taught from the amount of substance, not by averaging the percentages, and only when that result is the stored answer.
- Alphabetical filing is taught by sorting the written names. The lesson appears only when the stored answer is the name or sequence in that place.
- Three grammar errors are taught only when the stored answer is the sentence that contains them: "between you and I," "me and him" as a subject, "each ... need," and "the set ... were." Other grammar items keep their stored explanation.
- A next-number list is taught when it has one rule: a constant gap, a constant multiplier, or consecutive squares. A list that does not fit those rules keeps its stored explanation.
- A mean, a median, a percent change, simple interest, and a greatest common factor are taught only when the recomputed value is the stored answer.

Not done, and not claimed:

- A concept library shared across questions.
- A diagnostic that changes the next item for every skill.
- Pass probabilities.
- Offline spaced review.

FSRS, updated 22 October 2026:

Signed-in drills and Study Mocks now persist a review card and an append-only review event. The server runs the existing `ts-fsrs` 5.4.2 package (`scripts/fsrs-apply.mjs`). The browser does not choose the due date. Policy `civio-fsrs-policy-1`: a wrong answer is Again, an independent correct answer is Good, and an assisted correct answer does not move the date. Speed never selects Hard or Easy. Due reviews are listed at `/reviews/mistakes`. A Strict Mock writes nothing. The client wrapper in `resources/js/lib/review/fsrs.ts` remains for unit tests and is not what grades a learner.

The 16 October 2026 trace, which found no card table, is historical. Offline packs still do not sync review cards.
