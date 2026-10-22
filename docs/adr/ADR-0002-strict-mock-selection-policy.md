# ADR-0002 (DRAFT): Separate adaptive and representative selection without a third mode

- Status: **Accepted by GT (owner) 2026-10-22; Astra review not performed.** Option A implemented.
- Date: 2026-10-22 (Asia/Manila)
- Issue: #21
- Evidence: `app/Services/Exam/MockPoolSelector.php`, `app/Services/Exam/MockSessionService.php`, `tests/Unit/Exam/MockPoolSelectorTest.php`, `tests/Unit/EngineHardeningTest.php`.

## Context

`MockSessionService::startUnlocked` passes the same `bias` (server `seenIds`/`wrongIds` + client `wrong_ids`, client `weakSubcategories`/`weakCategories`) to `MockPoolSelector::select` for **both** Study and Strict. So a Strict Mock:

- fills up to `WRONG_PRIORITY = 0.5` of each block with previously-wrong items;
- gives weak subcategories a larger quota share inside their subject;
- shuffles with `HARD_BIAS = 0.6` using a text heuristic (`estimateDifficulty`), not measured difficulty;
- accepts client-supplied weak lists, so a learner can steer their own Strict composition.

Subject counts still match the blueprint (EngineHardeningTest). But within-subject composition is personalised, so a Strict score is not comparable across learners or over time. That undermines the "readiness" number. `MockPoolSelectorTest` "previously wrong items are favoured" asserts the bias without saying which mode it applies to.

The per-subject counts (45/52/45/8 and 45/47/45/8) are the **Civio blueprint**. Docblocks say "official blueprint". CSC publishes the subject coverage and time limits, not per-subcategory quotas. Wording should say "Civio blueprint" and never "official CSC weights".

## Options

A. **Policy object, two existing modes.** Add a `SelectionPolicy` value (`adaptive` | `representative`) derived from the mode on the server: Study gives adaptive, Strict gives representative. Representative ignores `wrongIds`, weak lists and the hard bias, and uses uniform sampling within subcategory quotas. It keeps the no-repeat-within-mock and clone/copy/offline exclusions, and prefers unseen items with a seen fallback. The client cannot choose the policy.
B. **A + exposure control.** In representative mode, prefer items with the lowest server-side exposure count for that learner (least-recently-seen). This reduces memorised repeats across mocks without targeting weakness.
C. **A + fixed forms.** Pre-assemble N parallel Strict forms per track from approved items (balanced FIL/EN, subcategory, difficulty once measured), and rotate them. These are the most comparable, but thin pools (Subpro Clerical/Filipino) may not support many forms.

## Migration risks

- Learners used to Strict "drilling weak spots" will see easier-feeling mocks, and score history will shift. Mark scores before and after the change in analytics (`selection_policy` on the attempt).
- Thin pools: representative sampling plus unseen preference makes short mocks more likely sooner. Keep the existing "shorter mock, clear notice" behaviour; never pad.
- Old client builds still send `wrong_ids`. The server must ignore it for Strict, not reject it.

## Acceptance tests

- With identical seed and bank, a Strict mock for a learner with 300 wrong ids and weak lists equals the Strict mock for a fresh learner, except for unseen-preference ordering under option B.
- Strict ignores client `wrong_ids`, `weakSubcategories` and `weakCategories` (request with and without gives the same item set).
- Study keeps the current favouring behaviour (existing test is re-scoped to Study).
- FIL/EN split and subcategory quotas hold for both policies, for both tracks.
- Over 1,000 seeded Strict draws, each eligible item's selection frequency within its subcategory is within ±3σ of uniform (option A).
- `exam_attempts.selection_policy` (or equivalent) records the policy used.
- No answer key, reveal, or `distractor_codes` appears in any Strict payload before submit (existing lock test extended).

## Decision (GT, 2026-10-22)

Option A, implemented:

- `App\Enums\SelectionPolicy::forMode()`: Study → `adaptive`, Strict → `representative`. Server-derived; the client cannot choose it.
- Representative ignores wrong history, weak subjects/subcategories, client `bias`, **and exposure (seen/unseen) history**. GT asked for an explicit choice: Strict does **not** prefer unseen items, so the form depends only on bank + seed. The difficulty heuristic is off; picks are uniform random within the Civio blueprint quotas.
- Kept: subject totals (150 Pro / 145 Subpro), FIL/EN split, uniqueness, clone/copy/offline-key exclusions, no padding, server scoring, server deadlines (11,400 s / 9,600 s), key protection.
- `selection_policy` and `selection_policy_version` (`MockPoolSelector::POLICY_VERSION`) are stored on `exam_sessions` and `exam_attempts`. Older rows stay null (= legacy shared pick). `LearningInsightsService` reports `strictMockPolicies` {representative, legacy} so analytics keep them apart.
- Wording: "Civio blueprint" for our weights.

### Claims (kept separate)

1. **Not weakness-targeted**: claimed and tested (same bank + seed with or without wrong/weak/client data gives the same form; chi-square uniformity within a subcategory, df 99, α 0.001, with a power check).
2. **Follows the Civio blueprint**: claimed and tested on both tracks.
3. **Scores comparable across forms / equal difficulty**: **not claimed.** That needs measured item difficulty and calibration.

Options B (exposure control) and C (fixed forms) remain open follow-ups.
