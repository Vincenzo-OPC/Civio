# Dexter 2 research audit

- Date: 2026-10-22 (Asia/Manila). Main at audit start: `ae24920`.
- Scope: docs and offline research only. No production code, no bank status changes, no model calls, no keys, no deploys.
- Fixtures (all reproducible offline, no packages):
  - `docs/research/dexter2/mastery_simulation.py` → `mastery_simulation_results.json`
  - `docs/research/dexter2/bank_metadata_audit.py` → `bank_metadata_audit.json`
- Draft ADRs: `docs/adr/ADR-0001-dexter-mastery-evidence-policy.md`, `ADR-0002-strict-mock-selection-policy.md`, `ADR-0003-dexter-rescue-loop.md`. All are **Proposed**, none accepted.

## 1. Executive summary

1. **Strict Mock is personalised, so it is biased as an assessment.** Strict uses the same wrong-first (≤ 50% per block), weak-subcategory, and hard-biased selection as Study. It also accepts client-supplied weak lists. Subject totals still match the Civio blueprint, but Strict scores are not comparable across learners or attempts.
2. **BKT is not yet trustworthy as a learner-facing "mastery" claim.** The parameters are fixed. Blanks count as wrong, repeats count as fresh evidence, and order comes from ids. On non-BKT synthetic data, fixed BKT issued false "≥ 0.85" estimates 29–37% of the time, against 9–11% for Elo. It is fine as an internal ranking signal for "what to practise next".
3. **About 25% of the approved bank is Rescue-ready today: 344 of 1,377 items.** Every approved item has a resolvable key, `why_wrong` text for each wrong option, distractor codes, a source and a passed review. But only 371 use codes in the Dexter taxonomy, and only 402 fall in a skill-graph archetype. The most common code, `NUM-PARTIAL` (332 uses), is too generic to diagnose anything.
4. **Civio already has most of the Rescue loop's parts.** These are RevealTutor, MisconceptionDiagnoser, SkillGraph, Fresh Same Skill, Review Mistakes with FSRS, Today's Focus and LearningInsightsService. What's missing is the orchestration and honest fallbacks, not new engines.
5. **The kill switch is closed by default and closed in production by code.** CI on `ae24920` is green: tests, linter and e2e.

## 2. Implemented vs missing

| Feature | Status | Evidence |
|---|---|---|
| Owner-funded AI kill switch | Implemented | `OwnerAiSpendLock::enabled()` returns false unless the raw env value is exactly `"true"`, and always false in production; tests in `tests/Feature/Ai/OwnerAiSpendLockTest.php`, `tests/Unit/Architecture/AiEgressTest.php` |
| Misconception codes on questions | Implemented (schema + diagnoser); data not imported | migration `2026_10_22_170000`, `MisconceptionDiagnoser`, codes still live only in bank source JSON |
| Skill graph | Implemented, 14 skills | `config/dexter_skill_graph.php` |
| BKT mastery + next focus | Unfinished integration | `SkillMasteryEstimator`, `NextSkillRecommender`, `nextFocus` in LearningInsightsService; evidence-stream defects (§4) |
| RevealTutor / Expound | Implemented | `app/Services/Exam/Reveal/RevealTutor.php`; Strict-locked until submit (ExamSessionTest) |
| Fresh Same Skill, Review Mistakes, FSRS | Implemented | `ExamService`, `ReviewMistakeRecorder`, `FsrsScheduler`, `drills/mistakes.tsx` |
| Strict Mock lock + server deadline | Implemented | `StrictMockLock`, `MockSessionService` |
| Strict representative selection | Missing | §5 |
| Rescue orchestration | Documentation only | Issue #23, ADR-0003 |
| Item difficulty (measured) | Missing | `estimateDifficulty` is a text heuristic |
| Calibration reporting | Missing | none |
| Generative Dexter tutor | Experimental, disabled | lock closed; ₱0 policy |

## 3. Open-source survey (verified 2026-10-22 via GitHub API `/repos/{r}` license field and repo READMEs)

| Project | What it does / how | Civio has? | Borrow | License / paid deps |
|---|---|---|---|---|
| OATutor (github.com/CAHLR/OATutor) | React ITS; content as JSON "problems → steps → hints"; BKT per skill in-browser | Partly (reveal, no step hints) | Step/hint *structure* for multi-step word problems; skill tag per step | MIT; content is CC BY, so don't copy questions |
| pyBKT (github.com/CAHLR/pyBKT) | Python BKT fitting by EM, with forgets/guess/slip per skill and per-item guess/slip | No (fixed params) | Offline fitting per archetype once data exists (ADR-0001 D) | MIT; Python/offline only, no runtime |
| Khan Perseus (github.com/Khan/perseus) | React renderer for widget-based exercises (numeric input, expressions, graphs) | No | Ideas: accessible numeric input, hint reveal pacing | MIT code; Khan content not licensed for reuse; heavy bundle, so reject as a dependency |
| h5p-multi-choice (github.com/h5p/h5p-multi-choice) | Accessible MCQ with per-option feedback | Yes (equivalent) | Per-option "chosen feedback" pattern = our `why_wrong` | MIT (README); H5P runtime is not wanted |
| ts-fsrs (github.com/open-spaced-repetition/ts-fsrs) | FSRS scheduler in TypeScript | Yes (PHP `FsrsScheduler`) | Parameter-optimizer approach later | MIT |
| shadcn/ui (github.com/shadcn-ui/ui) | Copy-in Radix + Tailwind components | Yes (stack) | RadioGroup/Collapsible patterns already compatible | MIT |
| GOV.UK Design System (github.com/alphagov/govuk-frontend) | Accessibility-tested patterns (error summary, radios, "details") | No | Error-summary and progressive "details" patterns, in Civio styling | MIT code; GOV.UK brand, crown and font excluded, so don't imitate the look |
| Storybook (github.com/storybookjs/storybook) | Component workshop | No | Not now: a new devDependency/framework (rule: none) | MIT |
| 21st.dev (github.com/serafimcloud/21st) | Community component registry | No | Inspiration only | Site repo MIT; each component's licence is set by its author, so check per item; reject by default |
| Mobbin (mobbin.com) | Paid screenshot library of commercial apps | No | Reference only; no copying designs | Proprietary, subscription; reject |
| catsim (github.com/douglasrizzo/catsim) | Python CAT: IRT item selection, stopping rules, exposure control | No | Exposure control idea for Strict (ADR-0002 B) | BSD-3-Clause |
| mirt (github.com/philchalmers/mirt) | R IRT model fitting | No | Offline difficulty estimation only, never shipped | GPL (≥ 3) per DESCRIPTION 1.48.2, so it must stay outside the codebase |
| Elo for learning (Pelánek 2016, doi:10.1016/j.compedu.2016.03.017) | Learner rating and item difficulty updated per answer | No | Population item difficulty (ADR-0001 B); simulation shows best calibration of the three | Algorithm, no licence issue |
| CTAT / TutorShop (github.com/CMUCTAT/CTAT) | Example-tracing / model-tracing tutors | No | Step-level error feedback concept | NOASSERTION per API; treat as unlicensed for reuse |
| ASSISTments (assistments.org) | Hosted homework platform with "skill builders" (N correct in a row) | Similar (Fresh Same Skill) | Skill-builder completion rule as a simple, explainable alternative | Proprietary service; idea only |
| Oppia (github.com/oppia/oppia) | Explorations with misconception-tagged answer groups | Partly (distractor codes) | Answer-group → misconception → targeted feedback, which matches Rescue | Apache-2.0 |
| OpenStax (github.com/openstax/openstax-cms) | Open textbooks | No | Content not needed (CSC scope differs) | Code AGPL-3.0; books CC BY; reject |

Complexity and mobile impact: everything recommended is a pattern or an offline Python script. No runtime package is added and nothing changes the bundle.

## 4. Issue #20: BKT audit

Code read: `SkillMasteryEstimator` (pInit .2, learn .1, slip .1, guess .25, MIN_ANSWERS 5), `LearningInsightsService` skill events.

| Check | Finding |
|---|---|
| Unanswered | `$chosen === null` is fed as wrong. A blank is not evidence of a misconception, and timeouts in Strict inflate weakness |
| Repeats | The same question id answered again counts as new evidence; Review Mistakes loops can inflate mastery |
| Assisted | Excluded after the Expound `continue`. Correct; keep it |
| Guess/slip | Guess .25 matches 4 options, but guessing is item-dependent (strong distractors < .25, weak > .25) |
| Fixed params | One set for all 14 skills; spelling and percent-change behave differently |
| Difficulty | None; a hard item failed counts the same as an easy one |
| Ordering | By attempt id; exam answers have no `answered_at` column (only `offline_practice_results` has one) |
| Small samples | MIN_ANSWERS 5 counts answers, not distinct items |
| Archetype coverage | Graph covers 14 skills; 402/1,377 approved items fall in them |
| Calibration | Never measured |

Simulation (3 seeds × 300 synthetic learners × 40 answers; see the script for the generators):

| generator | model | Brier | log loss | ECE | false-ready |
|---|---|---|---|---|---|
| bkt_hetero | bkt_fixed | 0.139 | 0.441 | 0.019 | 0.007 |
| | rolling10 | 0.153 | 0.478 | 0.078 | 0.001 |
| | elo | 0.156 | 0.483 | 0.043 | 0.008 |
| irt_drift | bkt_fixed | 0.227 | 0.668 | 0.131 | 0.339 |
| | rolling10 | 0.213 | 0.615 | 0.059 | 0.117 |
| | elo | 0.199 | 0.583 | 0.055 | 0.088 |
| repeats | bkt_fixed | 0.202 | 0.608 | 0.119 | 0.290 |
| | rolling10 | 0.195 | 0.574 | 0.073 | 0.108 |
| | elo | 0.181 | 0.541 | 0.055 | 0.091 |
| skips | bkt_fixed (blank ignored) | 0.238 | 0.692 | 0.139 | 0.372 |
| | bkt_skip_wrong (current) | 0.235 | 0.676 | 0.127 | 0.319 |
| | rolling10 | 0.223 | 0.637 | 0.067 | 0.122 |
| | elo | 0.209 | 0.605 | 0.058 | 0.108 |

Reading: each model wins on data shaped like itself. Synthetic results can't choose a winner, and the ADR doesn't. The one robust lesson: fixed-parameter BKT is over-confident whenever reality isn't BKT. The small gain from "blank = wrong" comes from offsetting that over-confidence, not from correctness. See ADR-0001.

## 5. Issue #21: Strict Mock findings

- `MockSessionService::startUnlocked` builds a single `bias` (server seen/wrong ids + client `wrong_ids`, client weak subcategories/categories) and passes it to `MockPoolSelector::select` regardless of mode.
- The selector fills ≤ `WRONG_PRIORITY` 0.5 of each block with wrong items, then unseen, then seen-correct. Weak subcategories get bigger quota shares. `HARD_BIAS` 0.6 orders by a text heuristic.
- Tests: `MockPoolSelectorTest` "previously wrong items are favoured" asserts the bias for everyone. `EngineHardeningTest` proves subject totals hold. **No test says Strict ignores the bias.**
- Blueprint: 150 Pro (45 Verbal split EN/FIL, 52 Analytical, 45 Numerical, 8 GI) and 145 Subpro (Clerical 47 instead of Analytical). Time limits are 11,400 s and 9,600 s. Docblocks call this "official blueprint". The per-subject/subcategory quotas are Civio's. Call them the **Civio blueprint**, never official CSC weights.
- Thin pools: Subpro Filipino and Clerical pools are the first to produce short mocks once unseen preference is added. The existing "never pad, show notice" rule must stay.
- The fix keeps two modes and adds a server-derived selection policy (ADR-0002 A). Exposure control (B) and fixed forms (C) are follow-ups.

## 6. Issue #22: bank metadata coverage (fresh count, `bank_metadata_audit.json`)

Source: the flat 2,100 manifest (approved 1,377 / draft 685 / reviewed 38) and the bank JSON each row names. All 2,100 source records were found.

| Approved items (n = 1,377) | Count |
|---|---|
| Resolvable 4-option answer key | 1,377 |
| `why_wrong` for every wrong option | 1,377 |
| Distractor code for every wrong option | 1,377 |
| …all codes in the Dexter taxonomy (25 codes) | 371 |
| Archetype in the skill graph (14 skills) | 402 |
| Source field present | 1,377 |
| `review_status: passed` | 1,377 |
| Subpro-eligible | 934 |
| **Rescue-ready** (key + why_wrong + taxonomy codes + graph archetype) | **344** |

Subpro priority archetypes (approved / rescue-ready / rough distinct stem families):

| Archetype | Approved | Ready | Families |
|---|---|---|---|
| NUM-WP-PCT-CHANGE | 37 | 37 | 20 |
| NUM-WP-RATIO | 29 | 29 | 29 |
| NUM-WP-RATE | 27 | 27 | 27 |
| NUM-WP-ALGEBRA | 16 | 16 | 15 |
| NUM-FRAC-DEC | 19 | 19 | 10 |
| NUM-OPS-ORDER | 30 | 30 | 6 (template-heavy) |
| NUM-PCT-BASIC | 0 | 0 | 0 |
| CLR-SPELL-WRONG | 57 | 57 | 57 |
| CLR-SPELL-RIGHT | 36 | 36 | 36 |
| CLR-FILE-POSITION | 58 | 0 | 58 |

Filing items carry the parent code `CLR-FILE-ORDER`, which is not in the taxonomy. All 58 carry `distractor_subreason` with sub-codes (CLR-LETTER-ORDER, CLR-FIRSTNAME-FIRST, CLR-PREFIX-SPLIT, CLR-TITLE-COUNTED). A mapping proposal, not an edit, makes them ready.

Caveats: the counts say metadata *exists*, not that it is *right*. "Families" is a masked-stem heuristic. NUM-OPS-ORDER's 6 families means fresh follow-ups will feel repetitive.

**Pilot proposal (editorial, no approvals or rewrites by agents):** 60 items. That is 20 each from NUM-WP-PCT-CHANGE, NUM-WP-RATIO and CLR-SPELL-WRONG, chosen across distinct stem families. A human reviewer checks per item that the code matches the wrong option's real error and that `why_wrong` names that error, scoring agree / disagree / unclear. Pilot passes at ≥ 90% agree. Separately, editors decide whether to adopt the filing sub-codes and to split `NUM-PARTIAL`.

## 7. Issue #23: Rescue design

See ADR-0003. Summary:

- Loop: wrong answer → server-side diagnosis → checked `why_wrong` + taxonomy fix → optional prerequisite → different approved item of the same skill → independent answer → FSRS review → evidence update.
- Security: 423 with no body details while Strict is active. `distractor_codes` stay hidden. No generative calls.
- Smallest prototype: Study mode, three pilot archetypes, no prerequisite step.

## 8. UI (React/Tailwind/Radix; no new packages)

- **Choices:** Radix RadioGroup with a full-row label, ≥ 44 px targets and a visible focus ring. Feedback appears in an `aria-live="polite"` region after submit. Never use colour alone: pair lime (correct) and violet/neutral (wrong) with icon and text.
- **Progressive explanation:** Radix Collapsible in three tiers: (1) "Why your answer is wrong" (`why_wrong`), (2) "The idea" (taxonomy fix), (3) "Try a fresh one". Only tier 1 is open by default. This follows the GOV.UK "details" pattern in Civio styling.
- **Error feedback:** name the error ("You divided by the new value"), not the learner. Never claim a diagnosis when the code is missing.
- **Visual math:** CSS-only fraction and percentage bars (div widths) with text equivalents. No chart library.
- **Knowledge map:** a list grouped by graph prerequisite, with an "estimate" badge and the counts behind it ("6 fresh answers"). No graph-drawing library.
- **Modes:** Study Mode shows Rescue; Exam Mode never shows it. Lite Mode gets text-only tiers, no transitions, and respects `prefers-reduced-motion`. The Rescue panel must be lazy-loaded so the 11 kB Exam chunk budget holds.

## 9. Licensing summary

Allowed as idea/pattern sources: MIT, BSD-3 or Apache-2.0 code (OATutor, pyBKT, Perseus, h5p-multi-choice, ts-fsrs, shadcn/ui, govuk-frontend, Storybook, catsim, Oppia). Offline only, never in the repo: mirt (GPL ≥ 3). Rejected: OpenStax code (AGPL-3.0), CTAT (no clear licence), Mobbin (proprietary), and 21st.dev components without a per-item licence. No paid dependency in any recommendation. No questions, designs or brand assets copied.

## 10. Recommended decisions (for Astra)

1. ADR-0002 A: Strict uses a representative policy that ignores weakness bias and client weak lists.
2. ADR-0001 A: fix the evidence stream (blanks, repeats, timestamps) before any learner-facing "mastery" wording.
3. Approve the 60-item editorial pilot and decide on the filing sub-code mapping and the `NUM-PARTIAL` split.
4. ADR-0003 prototype scope (three archetypes, Study only).
5. Rename "official blueprint" to "Civio blueprint" in code comments and UI.

## 11. Risks and rejected alternatives

- Risks: Strict score shift after the policy change. Thin Subpro pools. Editors' time for the pilot. Over-trusting the synthetic results.
- Rejected:
  - a third "Assessment" mode (the user asked for none, and it confuses users)
  - Perseus or H5P as runtime dependencies (bundle, scope)
  - Storybook now (new framework)
  - IRT/CAT in production (too little data)
  - generative explanations (₱0 rule, lock closed)
  - Mobbin and 21st.dev copying (IP)

## 12. Prioritised work items

| # | Item | Acceptance test |
|---|---|---|
| 1 | Strict representative policy (ADR-0002 A) | Strict item set unchanged by wrong ids / weak lists; Study bias test re-scoped; quotas hold |
| 2 | Mastery evidence fixes (ADR-0001 A) | Blank doesn't move mastery; repeats count once per 7 days; timestamp ordering |
| 3 | `answered_at` on exam answers (if 2 needs it) | Migration + backfill-null test |
| 4 | Editorial pilot (60 items) | Reviewer sheet with ≥ 90% agree |
| 5 | Rescue v0 (ADR-0003) | 423 under Strict; fallback copy; fresh item rules; FSRS scheduled |
| 6 | Calibration report script (offline) | Reliability bins from anonymised attempts |

## 13. CI and kill-switch verification (2026-10-22, ~17:05 Asia/Manila)

- GitHub Actions on `ae24920` (main): `tests` success, `linter` success, `e2e` success (runs created 2026-10-22 17:04 Asia/Manila). There are no workflows literally named "ci" or "quality"; the repo's workflows are `tests.yml`, `lint.yml`, `e2e.yml` and `image-smoke.yml`.
- Kill switch: `config/ai.php` reads `CIVIO_OWNER_FUNDED_AI` through `OwnerAiSpendLock::parseFlag` (true only for the exact string `"true"`). `.env.example` leaves it unset. `OwnerAiSpendLock::enabled()` returns false in the `production` environment regardless of the flag. I can't read the production environment's variables from here, so "closed in production" is verified in code, not on the live host.

## 14. Sources

- Repos and licences: GitHub REST `/repos/{owner}/{repo}` license.spdx_id, fetched 2026-10-22, for the 14 repos above (21st.dev under serafimcloud/21st). h5p-multi-choice licence from its README. mirt from DESCRIPTION (Version 1.48.2, GPL (≥ 3)).
- Pelánek, R. (2016). Applications of the Elo rating system in adaptive educational systems. Computers & Education 98.
- Corbett & Anderson (1995). Knowledge tracing. UMUAI 4.
- GOV.UK Design System patterns: https://design-system.service.gov.uk/ (accessed 2026-10-22).
