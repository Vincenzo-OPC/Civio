# Adaptive learning

Phase 0 looked at the current exam, not a new app.

What already teaches without an AI call:

- `RevealTutor` recomputes rectangle perimeter, order of operations, and a few number patterns. A lesson is published only when it matches the stored key. A mismatch is a conflict, and the stored explanation is kept.
- The explanation panel already hid empty sections.
- Guest study bias and follow-up items already exist. They are not a full mastery model.

What this pass changed (Phase 1 slice):

- The study button is **Show Explanation**. The panel heading is **Understand the Answer**.
- Extra parts keep their own names: Step-by-Step, Exam Tip, Common Mistake, Explain Simpler, Try Another, Diagram.
- Terminal-digit filing is taught by groups, with a three-group diagram, only when the key is the last group.
- A Fibonacci-type sequence is taught only when every shown term is the sum of the two before it and the next term is the key. An ordinary sequence is not labeled Fibonacci.

Not done, and not claimed:

- A concept library shared across questions.
- Persistent mastery, spaced review, and a diagnostic that changes the next item for every skill.
- Mixture, grammar, and the rest of the visual set.
- Pass probabilities.

Those stay later. The scoring, mock timer, and strict-mode lock (no explanation until submit) are unchanged.
