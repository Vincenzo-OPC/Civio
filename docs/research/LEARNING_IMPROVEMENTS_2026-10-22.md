# Learning improvements audit (2026-10-22)

The passer insights from the GT directive are anecdotal, not official. Core goal: answer **unfamiliar** questions accurately under time.

## Audit: what already exists
| Insight / requirement | Existing Civio feature | Status |
|---|---|---|
| Guided vs independent attempts; never mastery from one assisted correct | `ReviewMistakeRecorder` + `FsrsRatingPolicy`: help (explanation shown) is tracked per served batch; assisted results don't move FSRS cards (tests in ReviewMistakeTest) | ✅ exists |
| Revisit wrong answers | Review Mistakes list, due reviews (FSRS), retry same item | ✅ same item only. **Added fresh-question revisit** (below) |
| Extra practice on weaknesses | Mock selector biases about 50% toward wrong items and weak categories/subcategories | ✅. **Fixed:** the weak top-up wiped GI (ce4f988) and ignored key-trap rules (23e855f) |
| Accuracy + time tracking | Analytics `pacingTrend` (sec/question, accuracy per run), per-item `questionTimes` | ✅ per run; ⚠ no per-subject time yet |
| Timed after competence | Study (untimed option) vs Strict modes | ⚠ manual choice; no competence gate or suggestion |
| Daily one-subject focus, then mixed set | Study-plan templates (calendar) | ⚠ templates exist; no "today's focus" launcher |
| Beginner lessons first / method explanations | Learn modules; explanation audit command | ⚠ explanation quality varies; the method-first format (asked/givens/method/check/distractors) is not enforced |
| Speed ≠ understanding | Scorecard shows score and pace separately | ⚠ subject mastery chart mixes Study (assisted) and Strict runs |

## Implemented today (pushed, tests run)
- **a0b36c4:** "Practice New Questions on These Skills" on Review Mistakes. The server picks up to 20 active, never-served items from the subcategories of the learner's pending mistakes (no client IDs, keys withheld, drafts excluded). Tests: `FreshSameSkillTest` (2).
- **ce4f988:** the weak-subject boost now swaps proportionally from the largest subjects (GI keeps its share). Test in `EngineHardeningTest`.
- **23e855f:** the weak top-up obeys key-trap and repeat rules; grading counts each ID once.
- **4806240:** timer warnings fire even when a background tab skips the exact second. Tests: `tests/Js/timer-warning.test.ts` (4).

## Roadmap (next slices, smallest first)
1. **Mastery chart honesty:** compute subject mastery from Strict and independent results only; show Study/assisted runs as "practice".
2. **Today's focus launcher:** one subject per weekday (rotating, weakest first), a 15-item focused drill, then a 10-item mixed set. Server-picked, reusing `drillCandidates`.
3. **Competence nudge:** suggest timed mode once a subject reaches ≥80% independent accuracy across at least 30 items. Show it as a suggestion, never as "proficient".
4. **Per-subject pace:** average seconds per item per subject from `questionTimes`, next to accuracy.
5. **Method-first explanation template:** extend `AuditExplanationsCommand` to flag explanations missing method, check and distractor reasoning (this needs the bank owner to do the repair).
6. **Exam-day guide page** linking to csc.gov.ph.

## Blockers / notes
- Explanation repairs touch the bank, which another worker owns.
- No paid APIs were used. Lite mode and bundle budgets were respected (exam chunk 10.8 / 11 kB br).
