# Next learning delivery recommendation

Repository assessment: 17 October 2026, starting from `2f113403ec0eb81a17891a9461971a2e711d34fc`. The supplied Astra handoff is product research context, not a specification or proof of shipped features.

## Evidence and status

| Capability | Verified code evidence | Status and limits |
| --- | --- | --- |
| Server selection and grading | `MockSessionService`, `MockPoolSelector`, `SubmitExamAttemptAction`, `ExamGradingService` | Implemented. Preserve these paths rather than rebuilding them. |
| Protected attempts | `StrictMockLock` and `ExamSession` | Implemented for active Strict Mocks; any new learning endpoint must reuse the lock. |
| Checked teaching | `Exam/Reveal/RevealTutor.php` and its solvers | Implemented for recognized patterns only. A computed lesson must agree with the stored key; coverage is not universal. |
| Dexter | `Services/Dexter/DexterEvaluationService.php` | Backend key checking. Not a conversational tutor. The handoff's `Services/Exam/DexterEvaluationService.php` reference is stale. |
| Weakness-driven practice | `lib/guest-study-bias.ts`, `MockPoolSelector`, drill flows | Partial adaptive foundation. Not a durable competency or misconception model. |
| Spaced review | `lib/review/fsrs.ts`, `tests/Js/fsrs.test.ts` | Scheduler and unit tests only. Search of application imports and migrations finds no persistent review cards, ordinary-answer integration, or due queue. |
| Dashboard and calendar | `pages/user/dashboard`, `pages/user/calendar`, `DeterministicAnalysisService` | Existing history, analysis, and scheduled tasks. These do not establish a completed learner model or validated readiness prediction. |
| Reviewer books | `printable-exam.tsx` | Exam booklet only. The Civio Complete Reviewer and a completed terminal-digit filing sample chapter are not present. |
| Study Studio, six subject engines, psychometric prediction | Astra handoff | Research proposals. No implementation or effectiveness claim follows from the handoff. |
| Dates, market pricing, provider economics, library suitability | Astra handoff | Unverified for production. No new exam dates, prices, providers, or dependencies are adopted in this slice. |

## Highest-value next learning slice: a durable return-to-mistakes queue

Start with one signed-in, online drill flow: save a server-graded mistake, show a “Review Mistakes” list, and let the learner answer again before opening the existing checked explanation. This closes a useful persistence gap without requiring a new taxonomy, AI provider, or a claim of mastery. Keep guests, offline drills, and Strict Mocks on their existing paths.

Implementation boundary:

1. Add a per-user/question review record with the source attempt, authoritative grading result, timestamps, and pending/resolved state. Use a unique source-attempt/question key for idempotency. Record whether help was used; an assisted correct response must not establish independent recall.
2. Write from the existing server-graded drill submission transaction, not from browser scores or arbitrary question IDs. Do not change mock scoring or publish new questions.
3. Add an owner-scoped pending list and one small Lite-compatible entry point. Reuse drill rendering and answer-key withholding. Exclude locked items, drafts, and unavailable questions; enforce the Strict Mock lock again on submission and explanation access.
4. Resolve only after a later independently answered, server-graded review. Repeated submissions must not inflate evidence. Label this as practice history, not mastery or readiness.

Acceptance: owner isolation, duplicate-submission safety, persistence across login sessions, server-side grading, assisted/unassisted distinction, Strict Mock protection, empty states, and mobile/Lite usability. Measure delayed repeat error rates; separately evaluate improvement on unseen items before claiming transfer. Repeating a known question alone cannot establish skill mastery.

FSRS follows once reliable review events exist: retain the installed scheduler, version its parameters, persist card state and review logs, and decide how the Laravel backend will validate scheduling without trusting browser-supplied intervals. Do not map speed alone to “Easy.” Offline reconciliation and due-date ordering require a separate tested slice. A full learner model, broad dashboard redesign, or six new services would exceed this boundary.

## Research basis and remaining uncertainty

The [upstream ts-fsrs documentation](https://github.com/open-spaced-repetition/ts-fsrs/blob/main/packages/fsrs/README.md) describes card scheduling and review-log outputs; it does not provide Civio's persistence or authoritative grading integration. The [retrieval-practice classroom research summary and database](https://www.retrievalpractice.org/strategies/2019/10/28/database-of-retrieval-practice-research) supports testing retrieval practice with feedback. These sources were checked on 17 October 2026. They support a bounded experiment, not a claim that Civio already improves exam outcomes or that one scheduling algorithm is best for this question bank.

No new learning feature is implemented by this recommendation. No deployment or real-user learning validation was performed.
