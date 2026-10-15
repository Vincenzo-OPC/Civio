# Civio engines

This is the map of the study machinery that does **not** need a generative
model. Class names below are the ones in the repo. A learner never has to
see them.

Civio is not the Civil Service Commission. A practice score is not an exam
result.

## Words used in the code

| Word | What it means here |
|---|---|
| Engine | A piece of server code that decides something from rules and stored data, not from a chat model. |
| Solver | One rule inside the explanation engine. It either recognizes an item or it leaves the item alone. |
| Stored key | The correct option saved on the question. The browser does not receive it until Show Explanation or until the mock is submitted. |
| Checked lesson | A solver recomputed the answer. The lesson is published only when that result equals the stored key. |
| Conflict | The solver recognized the pattern, but the stored key does not match the recomputed result. The stored explanation is kept. Dexter can say the stored answer may be wrong. |
| Stored explanation | The sentence already saved on the question. Used when no solver owns the item. |
| Progressive disclosure | The first screen is short. Step-by-Step, Exam Tip, and the rest appear only if that part exists, and only after a tap. |
| Deterministic | The same item always produces the same lesson. No model call, no randomness. |
| Handoff | Copy Question and Ask. They send the item to a clipboard or another site. They do not grade it. |
| Strict Mock | Timed rehearsal. Show Explanation, Dexter, Copy Question, and Ask stay hidden until submit. |

## Explanation engine

Entry point: `App\Services\Exam\Reveal\RevealTutor`.

The study button is **Show Explanation**. The panel heading is
**Understand the Answer**. The response is `POST /exams/reveal`.

Order of work:

1. Each solver is asked, in a fixed order, whether it recognizes the stem.
2. The first solver that both recognizes the item and matches the stored key wins.
3. If a solver recognizes the item and the key does not match, that is a conflict. The stored explanation is shown instead. No shortcut or diagram is invented for that item.
4. If no solver recognizes the item, the stored explanation is split into a lead sentence and later sentences. Empty sections are not rendered.
5. A Taglish “Explain Simpler” line is attached only on an English item. A Filipino item is not given a second language it did not ask for.
6. A follow-up item, when one exists, is chosen from the bank. It is not generated.

The panel may then offer, only when the payload has that part:

- Step-by-Step
- Exam Tip
- Common Mistake
- Diagram
- Explain Simpler
- Try Another

### Solvers

| Solver | Publishes a lesson when |
|---|---|
| `RectanglePerimeterSolver` | A rectangle perimeter recomputes to the key. Area (`length × width`) is named as the usual miss. |
| `TerminalDigitFilingSolver` | Terminal-digit filing, and the key is the last digit group. |
| `AlphabeticalFilingSolver` | The key is the name, or the sequence, that sorts into the place the question asks for. |
| `FibonacciSequenceSolver` | Each shown term is the sum of the two before it, and the next term is the key. |
| `NumberSequenceSolver` | One other rule fits: a constant gap, a constant multiplier, or consecutive squares. A list with no single rule is left alone. |
| `MixtureConcentrationSolver` | Two solutions, and the weighted concentration is the key. An unweighted average is named only when the volumes differ. |
| `GrammarRuleSolver` | The key itself is one checked error: “between you and I”, “Me and him” as the subject, “Each … need”, or “The set … were”. Any other pronoun item keeps its stored explanation. It is not marked a conflict. |
| `OrderOfOperationsSolver` | The expression evaluates to the key. Multiply and divide before add and subtract. |
| `CheckedQuantitySolver` | Mean, median, percent change from a start value, simple interest, or a greatest common factor, and the recomputed value is the key. |
| `CheckedPatternSolver` | Percent of a number, a square root, a fraction of a whole, speed from distance and time, a percent reduction, or a least common multiple, and the recomputed value is the key. |

Audit, without rewriting any item:

```bash
php artisan civio:audit-explanations
```

Tests: `tests/Unit/Exam/RevealTutorTest.php` and `tests/Feature/User/RevealTutorTest.php`.

## What this engine does not do

These are not built. They are not described as if they were.

- A concept library shared across questions.
- A mastery score, a spaced-review queue, or a study plan that changes for every skill.
- A pass probability.
- A generated question. Try Another opens a bank item.

## Dexter

`App\Services\Dexter\DexterEvaluationService` is a separate checker. It looks for a few calculation conflicts and can warn that the stored key may be wrong. It is not the explanation engine, and it is not a chat model. In a Strict Mock, Dexter is hidden until submit.

## Ask and Copy Question

These are a handoff, not a tutor.

- **Copy Question** writes the stem, the choices, and — only after Show Explanation or on review — the result. The key is not copied just because the browser already has it. See `resources/js/lib/ai-handoff.ts`.
- **Ask** follows the assistant chosen in Settings → Preferences: ChatGPT, Gemini, Copilot, Grok, or Ask AI. ChatGPT and Gemini can open with the question in the box when the text is short enough. Copilot and Grok open, and the question is copied, because those sites do not fill the box safely. Ask AI only copies.
- The choice is stored in the browser under `civio_ask_assistant`. No Civio API key is required.

The older product note is `docs/EXTERNAL_AI_HANDOFF.md`. Where it still says “Copy for AI”, the shipped label is **Copy Question**.

## Related files

- UI: `resources/js/pages/user/exams/components/session/answer-reveal.tsx`
- Phase notes and the list of what is still unfinished: `docs/ADAPTIVE_LEARNING.md`
- Change log since the baseline: `docs/CHANGES_SINCE_BASELINE.md`
