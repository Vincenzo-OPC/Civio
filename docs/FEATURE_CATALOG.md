# Civio feature catalog

Canonical inventory of what the application actually does. A roadmap line is not an implementation. When a user-facing feature changes status, update this file in the same commit. Do not copy this table into other documents. Point here.

Checked against the routes, controllers, and tests on 22 October 2026. Statuses:

- **VERIFIED IMPLEMENTED** — behavior tested in this session.
- **IMPLEMENTED, NOT END-TO-END VERIFIED** — code and older tests exist. This session did not re-walk the screen.
- **PARTIAL** — a real slice exists and a claimed part does not.
- **PLANNED** — described, not built.
- **EXPERIMENTAL** — present, not a product promise.
- **DISABLED** — kept from doing the thing it used to imply.
- **BLOCKED** — cannot finish without a decision or a missing dependency.
- **IMPLEMENTED, NOT PRODUCTION VERIFIED** — behavior is tested. The production image has not been built and the feature is not deployed.

Public wording lives in [WEBSITE_FEATURE_COPY.md](WEBSITE_FEATURE_COPY.md).

## Practice

| Feature | Purpose | Who | Level | Where | Code | Tests | Status | Limits | Access | Promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Professional mock | 150 scored items, 3 h 10 m | Examinee | Professional | `/exams` | `ExamSessionController`, `MockPoolSelector` | Exam session tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Server picks items. Keys stay withheld until the rules allow them. | Free study | Yes, as practice |
| Subprofessional mock | 145 scored items, 2 h 40 m | Examinee | Subprofessional | `/exams` | same | same | IMPLEMENTED, NOT END-TO-END VERIFIED | Same protections | Free study | Yes. Founder-first level |
| Study Mode | Pace yourself and open explanations | Examinee | Both | `/exams` | `ExamMode`, live exam | Exam session tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Not a chat tutor | Free | Yes |
| Exam Mode / Strict Mock | Timed mock. No explanation until submit | Examinee | Both | `/exams` | `StrictMockLock` | `ExamDeadlineTest`, `ExamSessionTest` | IMPLEMENTED, NOT END-TO-END VERIFIED | Open Strict Mock locks those items | Free | Yes |
| Practice drills | Topic practice | Examinee | Both | `/drills`, `/exams?drill=true` | `DrillController`, `ExamService` | Drill and exam tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Guests can study when guest study is on | Free | Yes |
| Saved drill sets | Keep a personal set | Signed-in learner | Both | `/drills/saved-sets` | `SavedDrillSetController` | Saved-set tests if present | IMPLEMENTED, NOT END-TO-END VERIFIED | Owner scoped | Account | Yes, as saved sets |
| Smart weakness drill | Another drill biased to weak topics | Signed-in learner | Both | `/drills/smart-weakness` | `DrillController` | Not re-run here | PARTIAL | Not a mastery model | Account | No. Do not call it an adaptive tutor |

## Learn

| Feature | Purpose | Who | Level | Where | Code | Tests | Status | Limits | Access | Promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Explanations | Show the stored explanation and a checked lesson when the rule matches the key | Examinee | Both | Reveal on the exam | `RevealTutor`, `ExpoundService` | `RevealTutorTest`, expound unit tests | IMPLEMENTED, NOT END-TO-END VERIFIED | A mismatch keeps the stored explanation. Not every item has a solver | Free | Yes, as explanations |
| Dexter | Check the stored key. It is not a conversation | Internal | Both | `DexterEvaluationService` | that service | Dexter tests | PARTIAL | Do not describe Dexter as a chat tutor | Not a learner product | No |
| Copy Question | Copy the visible question for an outside assistant | Examinee | Both | Exam actions | `copy-for-ai-button.tsx` | Copy tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Does not call Reveal. Does not grade | Free | Yes, as Copy Question |
| Ask | Open the assistant chosen in Settings | Examinee | Both | Exam actions and Settings | Ask buttons, settings | Settings tests if present | IMPLEMENTED, NOT END-TO-END VERIFIED | No Civio API call. No answer key is added by the button | Free | Yes, as Ask |
| Review Mistakes | Remember a wrong practice answer and let the learner retry without the key | Signed-in learner | Both | `/reviews/mistakes` | `ReviewMistakeRecorder` | `ReviewMistakeTest` | VERIFIED IMPLEMENTED | Strict Mock writes nothing. An explanation blocks that drill from clearing the mistake. Resolved is not mastered | Account | Yes |
| Smart Review | Remind the learner to practice a missed question again before they forget it | Signed-in learner | Both | `/reviews/mistakes` | `FsrsScheduler`, `scripts/fsrs-apply.mjs`, `review_cards`, `review_events` | `ReviewMistakeTest` | IMPLEMENTED, NOT PRODUCTION VERIFIED | Online only. Needs Node and `ts-fsrs` beside PHP. A failed reminder stays unfinished, including after repeated failures, and is not Review Complete. Assisted answers and Strict Mocks do not move a due date. Due Today is paged at 20. A manual image smoke passed on GitHub. The app is not deployed and is not operationally verified | Account | No. Not production verified |

## Improve

| Feature | Purpose | Who | Level | Where | Code | Tests | Status | Limits | Access | Promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Saved exam sessions | Resume a server-picked mock and its answers | Examinee | Both | `/exams/sessions`, `/exams/sessions/progress` | `ExamSession`, `ExamProgressController` | Exam session and deadline tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Strict progress is server-owned | Free | Yes, as saved progress |
| Exam history | See finished attempts and delete your own | Signed-in learner | Both | `/history` | `ExamHistoryController` | History tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Does not rewrite old rows into a new formula | Account | Yes |
| Scorecards | Show the server grade after submit | Examinee | Both | Exam scorecard | `ExamScorecardResource` | Scoring tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Practice score, not a CSC rating | Free | Yes |
| Subject breakdown | Counts by subject | Examinee | Both | Scorecard and analytics | formatters, analytics components | `PracticeScoreTest` | IMPLEMENTED, NOT END-TO-END VERIFIED | Unpracticed is not zero | Free | Yes, as counts |
| Performance analytics | Practice averages and subject counts | Signed-in learner | Both | `/analytics`, `/dashboard` | `AnalyticsService`, `DeterministicAnalysisService` | Analytics tests | PARTIAL | The stored `pass_probability` field is the mock-item percentage, not a pass forecast. Labels say so. Do not promote a ranking or a pass chance | Account | Only as practice history |
| Study plan | A calendar of study tasks | Signed-in learner | Both | `/study-schedules` | `StudyScheduleController` | Schedule tests | IMPLEMENTED, NOT END-TO-END VERIFIED | A task list. Not the Smart Review queue | Account | Yes, as a study plan |
| Study suggestions | Suggested tasks and templates | Signed-in learner | Both | `/study-suggestions` | `StudySuggestionController` | Not re-run here | PARTIAL | Not a personalized mastery plan | Account | No |

## Study anywhere

| Feature | Purpose | Who | Level | Where | Code | Tests | Status | Limits | Access | Promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lite Mode | Smaller exam UI on Save-Data or a slow connection | Examinee | Both | Cookie `civio_lite`, `useLiteMode` | `lib/lite-mode.ts` | Lite tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Manual choice beats the automatic one | Free | Yes |
| Offline drills | Download a topic, answer offline, sync for a server grade | Examinee | Both | `/offline` | `OfflinePackController`, `OfflinePracticeController` | Offline tests | IMPLEMENTED, NOT END-TO-END VERIFIED | Offline items never enter a full mock. Smart Review does not sync offline | Free | Yes, for drills only |
| Accessibility | Keyboard help, focus rings, reduced motion | Examinee | Both | Exam and homepage | live exam, CSS | Not a dedicated audit this session | PARTIAL | Not a certified accessibility conformance claim | Free | No certification claim |

## Account and reference

| Feature | Purpose | Who | Level | Where | Code | Tests | Status | Limits | Access | Promote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Login and account | Register, sign in, passkeys, terms | Learner | Both | Fortify and auth routes | Fortify, `AuthController` | Auth tests | IMPLEMENTED, NOT END-TO-END VERIFIED | OAuth routes exist. Do not activate a paid provider | Account | Yes |
| Civil Service information | Public dates and a reviewer guide | Examinee | Both | `/cse-2027-dates`, `/guide` | `PublicController` | Not re-run here | IMPLEMENTED, NOT END-TO-END VERIFIED | Not a CSC announcement | Free | Yes, as Civio's own notes |
| PDF booklet | Download a booklet and, when allowed, an answer key | Authorized account | Both | `POST /exams/export-pdf` | `PdfExamExportService` | `PdfAnswerKeyTest`, `PdfExportTest` | IMPLEMENTED, NOT END-TO-END VERIFIED | The exam screen receives `can_download_pdf`. Permission, daily throttle, and an open Strict Mock still apply. An isolated browser made a 4-page JPEG PDF from fixtures. Not checked in a production image | Restricted | Only for accounts that can download |
| Support form | Send a message | Public | Both | `/support` | `SupportController` | Not re-run here | IMPLEMENTED, NOT END-TO-END VERIFIED | Not a tutoring service | Free | Yes, as contact |

## Administration

Admin question, user, syllabus, announcement, feedback, exam-date, and learn screens exist under `/admin`. They are for operators. The question-generate route queues `GenerateQuestionsJob`. That is **EXPERIMENTAL**, can depend on a configured model, and is not a learner feature. Do not promote it. Bank approval and activation are not authorized by this catalog.

## Not built

| Feature | Status | Note |
| --- | --- | --- |
| In-app generative tutor | PLANNED | Optional later. Explanations work without it |
| Concept mastery model | PLANNED | Astra's research. Not this scheduler |
| Personalized FSRS weights | PLANNED | Policy stays `civio-fsrs-policy-1` until there is evidence |
| Offline Smart Review | PLANNED | Would need a tested sync that cannot overwrite a newer server history |
| Pass probability | DISABLED as a claim | Do not revive it as a forecast |
| Payments | PLANNED / not authorized | No paywall in this work |
