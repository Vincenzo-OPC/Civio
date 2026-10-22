# ADR-0001 (DRAFT): Dexter mastery evidence policy

- Status: **Proposed, awaiting Astra.** Not accepted. No code changes until accepted.
- Date: 2026-10-22 (Asia/Manila)
- Issue: #20
- Evidence: `docs/research/dexter2/mastery_simulation.py` and `mastery_simulation_results.json` (synthetic, offline, seeds 11/23/37); `docs/research/DEXTER_2_RESEARCH_AUDIT_2026-10-22.md` §4.

## Context

`SkillMasteryEstimator` (`bkt-v1`) runs fixed BKT parameters (pInit .2, learn .1, slip .1, guess .25, min 5 answers) over events built in `LearningInsightsService`. Known defects in the current event stream:

1. A blank (`$chosen === null`) is fed as a wrong answer.
2. Repeats of the same question (Review Mistakes, re-taken mocks) count as fresh evidence.
3. Order is by attempt id, not answer time; out-of-order offline sync is possible.
4. One parameter set for every archetype, regardless of difficulty or four-option guess rate.
5. No per-item difficulty. No calibration check against real outcomes.

Assisted answers are already excluded (after the Expound `continue`). Keep that.

## What the synthetic run shows (not a verdict)

| generator | best Brier | BKT fixed false-"ready" rate* |
|---|---|---|
| true BKT, varied learners | BKT (home ground) | 0.7% |
| logistic ability + difficulty, slow growth | Elo | 34% |
| same + 30% repeats | Elo | 29% |
| same + 15% blanks | Elo | 37% (32% when blanks fed as wrong) |

*share of estimates ≥ 0.85 where the true P(correct) < 0.70.

Feeding blanks as wrong scored slightly better only because it offsets BKT over-confidence on this generator. It is not evidence that a blank means "doesn't know".

Synthetic data cannot pick a model. It shows BKT with fixed parameters is fragile when data are not BKT-shaped. Elo and rolling accuracy are only better calibrated here.

## Options

A. **Keep BKT, fix the evidence stream.** Exclude blanks from mastery (track them as a separate "unanswered" signal). Count only the first answer per item per 7 days. Order by `answered_at` with an id tiebreak. Keep MIN_ANSWERS ≥ 5 *distinct* items. Low cost and no schema change if `answered_at` exists; otherwise add it.
B. **A + per-item difficulty via population Elo.** Store `elo_difficulty` per question, updated offline nightly from independent first attempts only. Use it to weight evidence or to replace BKT in `NextSkillRecommender`. Medium cost; needs a column and a job.
C. **Rolling independent accuracy with a confidence band (Wilson).** The simplest to explain to learners ("7 of your last 10 fresh fractions questions"). It ignores difficulty.
D. **Fit BKT per archetype with pyBKT (MIT) offline.** Only after ≥ 200 learners × 10 independent answers per archetype exist. pyBKT runs offline in Python; nothing ships at runtime.

## Decision

None yet. Recommended next step for any option: A's evidence-stream fixes, because every option needs them.

## Acceptance tests (any option)

- A blank never changes the mastery probability. It increments `unanswered` only.
- Answering the same question id 5× correct within 7 days moves mastery no more than once.
- Events with shuffled ids but real timestamps give the same estimate as sorted events.
- An Expound-assisted answer never changes mastery (existing test kept).
- Fewer than 5 distinct independent items gives `status: insufficient`, never "mastered".
- An offline calibration report (reliability bins) can be produced from anonymised production attempts before any wording like "ready" is shown.

## Risks

Option B adds a writable column on `questions`. The bank owner must agree, and it must never be editable by editors. Learner-facing wording must stay "estimate" until calibration exists.
