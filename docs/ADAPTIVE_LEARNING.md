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
- Persistent mastery, spaced review, and a diagnostic that changes the next item for every skill.
- Pass probabilities.

FSRS, traced on 16 October 2026 against `main`:

The scheduler in `resources/js/lib/review/fsrs.ts` can create a card and compute the next due date. `tests/Js/fsrs.test.ts` covers that function. Nothing else imports `initCard`, `scheduleAfterAnswer`, or `previewRatings`.

| Link | Status |
| --- | --- |
| A learner finishes a question | The exam and drills save an attempt. They do not call the scheduler. |
| A persistent review record | No review-card table. The card state is not stored. |
| A computed next-review date | Computed only inside the unused wrapper. |
| A due-review queue | Not built. The study calendar is a task list, not FSRS. |
| The next drill the learner opens | Chosen by topic, weakness, or a saved set. Not by due cards. |
| Offline review and sync | Offline packs sync answers. They do not sync FSRS cards. |

The smallest next slice is one table for card state, one write when a drill item is answered, and one due list. That is a separate change, with its own tests. It is not part of the exam typography pass.

Those stay later. The scoring, mock timer, and strict-mode lock (no explanation until submit) are unchanged.
