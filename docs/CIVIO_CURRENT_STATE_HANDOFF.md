# Civio current state handoff

The executable plan is [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md). This file is the current-state note only.

Audit time: 16 October 2026, Philippine Time. Session start SHA `3c18ec0258ec855795654afc85a93fa435684d55`. Confirm the tip after the setup-copy commit.

## 1. Repository

| Item | Value |
| --- | --- |
| Repository | [Vincenzo-OPC/Civio](https://github.com/Vincenzo-OPC/Civio) |
| Branch | `main` only. No other local or remote branches. |
| Remote | `origin` tracks `origin/main` |
| Synchronization | Local `main` matched `origin/main` at `3c18ec0258ec855795654afc85a93fa435684d55` before the exam-setup copy commit. Confirm both SHAs after that push. |

Do not commit `app/Providers/AppServiceProvider.php` while it contains the local preview `assetRoot` override. That change is sandbox-only. It is not product code.

No `.env`, credentials, or databases are part of this handoff.

## 2. Stack

Laravel, Inertia, React, TypeScript, Vite, Tailwind CSS v4. Motion is mostly CSS. Framer Motion is not the exam-workspace foundation. PostgreSQL is the MSI study database; tests use isolated SQLite. Reveal grading and the answer key stay on the server.

Read [ARCHITECTURE.md](ARCHITECTURE.md), [CODE_STANDARD.md](CODE_STANDARD.md), [LIBRARIES.md](LIBRARIES.md), and [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md).

## 3. Routes that matter

Defined in [routes/web.php](../routes/web.php).

| Route | Role |
| --- | --- |
| `GET /` | Homepage and exam selection |
| `GET /exams` | Study Mock, Strict Mock, drills, review |
| `POST /exams/sessions` | Server picks the mock items. The page does not receive the whole bank. |
| `POST /exams/reveal` | Returns the key, Dexter's check, and the structured tutor payload |
| `POST /exams/expound` | Longer stored explanation |
| `POST /exams/attempts` | Score submission |
| `GET /drills` | Practice by topic |
| `GET /learn` | Lessons |
| `GET /offline` | Offline drill runner |

## 4. Exam workspace

The live exam is [resources/js/pages/user/exams/components/live-exam-view.tsx](../resources/js/pages/user/exams/components/live-exam-view.tsx), mounted from [resources/js/pages/user/exams/index.tsx](../resources/js/pages/user/exams/index.tsx). State is [resources/js/pages/user/exams/hooks/use-exam-state.ts](../resources/js/pages/user/exams/hooks/use-exam-state.ts).

Lite mode replaces the body with [resources/js/pages/user/exams/components/lite-exam-body.tsx](../resources/js/pages/user/exams/components/lite-exam-body.tsx). Same handlers. Less chrome.

The homepage sample is [resources/js/components/domain/exam-screen-preview.tsx](../resources/js/components/domain/exam-screen-preview.tsx). It is not a bank item and it is not scored.

Study controls use `.civio-action` and `.civio-action-primary` in [resources/css/app.css](../resources/css/app.css). Previous and Next use `.civio-nav`. They only apply inside `.civio-session`.

## 5. What is implemented

Verified in code, not from old screenshots.

| Area | Status | Where |
| --- | --- | --- |
| Homepage, Professional and Subprofessional selection | Implemented | `resources/js/pages/public/welcome.tsx` |
| Study Mock and Strict Mock | Implemented | `resources/js/pages/user/exams/utils/exam-mode.ts` |
| Practice drills | Implemented | `resources/js/pages/user/drills/` |
| Server-picked mock, keys withheld | Implemented | `app/Services/Exam/MockSessionService.php`, `app/Http/Resources/ExamQuestionResource.php` |
| Answer selection, Previous, Next, Submit | Implemented | `live-exam-view.tsx` |
| Show Explanation / Hide Explanation as one toggle | Implemented | `live-exam-view.tsx`, `session/answer-reveal.tsx` |
| Structured Reveal: concept, steps, shortcut, mistakes, diagram | Implemented | `app/Services/Exam/Reveal/RevealTutor.php` |
| Dexter answer-key check | Implemented | `app/Services/Exam/DexterEvaluationService.php` |
| Copy Question | Implemented | `resources/js/pages/user/exams/components/copy-for-ai-button.tsx` |
| Ask ChatGPT, Gemini, Copilot, Grok, or AI | Implemented | `ask-assistant-button.tsx`, `resources/js/lib/ai-handoff.ts` |
| Similar Item | Implemented as an assistant handoff, not an in-exam item | `answer-reveal.tsx` |
| Flag | Implemented. Marks the item for return. | `use-exam-state.ts` |
| Question list | Implemented. Closed by default. The user-facing name is Question List, not Palette. | `question-palette-panel.tsx` |
| Notes, keyboard help, focus mode | Implemented behind Tools | `live-exam-view.tsx` |
| Timer and a written pace line | Implemented for timed exams | `use-exam-timer.ts` |
| Pause | Implemented when the mode allows it | `live-exam-view.tsx` |
| Scorecard and review | Implemented | `scorecard-view.tsx`, `review-exam-view.tsx` |
| Strict Mock lock on Reveal | Implemented | `app/Services/Exam/StrictMockLock.php` |
| FSRS scheduler code | Present | `resources/js/lib/review/fsrs.ts` |
| Offline drill packs | Implemented | `resources/js/lib/offline/`, `GET /offline` |
| Lite mode | Implemented | `resources/js/lib/lite-mode.ts`, [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md) |

## 6. Removed or rejected

These were taken out on purpose. Do not bring them back.

| Item | Why |
| --- | --- |
| Auto-Next | It skipped ahead after an answer. |
| Try Another as an in-exam jump | It left the mock and could open an item with no choices. The bank is not organized well enough to pick a truly similar item. |
| The word Palette | User-facing copy says Question List. Internal file names still say palette. |
| A separate Hide control under the explanation | Hide Explanation is the same button that opened it. |
| Long BIR and CSC disclaimer blocks on the exam chrome | Removed earlier. Do not restore that copy into the workspace. |
| Glass blur and purple wash on dark cards | Dark mode is solid black. The accent is logo green `#B3F52D`. |
| Any previous product name in source, storage keys, or docs | Do not reintroduce it. |

## 7. Design tokens

Exam surface, `.civio-session` in `resources/css/app.css`:

| Token | Light | Dark |
| --- | --- | --- |
| `--civio-violet` | `#5B35F5` | `#8B74FF` |
| `--civio-lime` | `#B3F52D` | `#B3F52D` |
| `--civio-ink` | `#101426` | `#F4F4F5` |
| `--civio-paper` | `#FAFAF7` | `#000000` |
| `--civio-surface` | `#F4F5F2` | `#141414` |
| `--civio-line` | `#E3E5EA` | `#2A2A2A` |

Study buttons, as of this handoff:

- Secondary, including Report, Copy Question, and Ask: solid `#E4E6EB`, 8px radius, 36px tall. Dark fill `#3A3B3C`.
- Primary, Show Explanation and Next: `#1D1D1F` in light mode. Logo green with black text in dark mode.
- Hover darkens the fill. Press scales to 0.98 unless the user prefers reduced motion.

Hover tips on Flag, the question list, and cross-out exist. Their wording has not been refined. The product owner asked to review that copy later for length and tone. Do not treat the current tooltip sentences as final.

## 8. Constraints

- Do not ship the answer key in the live exam payload. Reveal is `POST /exams/reveal`.
- Copy Question must not call Reveal. It copies only what the learner can already see. See [EXTERNAL_AI_HANDOFF.md](EXTERNAL_AI_HANDOFF.md).
- Strict Mock cannot reveal during the attempt.
- Lite mode has a bundle budget. Read [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md) before adding a library.
- Do not force-push. Do not commit `.env`, databases, or the local `assetRoot` hack.

## 9. Known limits

- Similar Item opens the learner's assistant in a new tab. Civio does not generate or insert that question.
- The question bank is not tagged well enough for a reliable in-exam "similar item."
- FSRS code exists in `resources/js/lib/review/fsrs.ts` and is covered by `tests/Js/fsrs.test.ts`. No exam, drill, or offline path imports it. There is no review-card table, no due queue, and no next-drill selection from a due date. See [ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md).
- This audit did not capture new screenshots of the solid buttons. Confirm them in the running Study Mock.
- Dedicated authorized POST /exams/export-pdf is implemented; ordinary POST /exams/sessions remains keyless. The prior keyless-export warning is superseded by the PDF integrity fix.
- Preserve a local asset-root override if one appears. None was present in the verified clean MSI checkout at this session's start.

## 10. What to read next

- [CHANGES_SINCE_BASELINE.md](CHANGES_SINCE_BASELINE.md)
- [ENGINES.md](ENGINES.md)
- [ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md)
- [CSE-Question-Design-Spec.md](CSE-Question-Design-Spec.md)
- [DESIGN_RESEARCH_AND_ANTI_AI_SLOP.md](DESIGN_RESEARCH_AND_ANTI_AI_SLOP.md)
- [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md)

## 11. Suggested review order

1. Study Mock buttons: Report, Show Explanation, Copy Question, Ask. Confirm they look like buttons in light and dark.
2. Reveal payload and Dexter. Confirm explanations are checked, not invented.
3. Whether FSRS is wired into the drills the learner actually opens.
4. Hover-tip copy. Make it shorter. Do not add a new tooltip system until that copy is decided.
5. Homepage sample versus the real exam. The sample must not drift from the real controls.

## Execution refresh - 20 October 2026

The earlier repository/stack table is historical. MSI main was clean at efc0d81, then fast-forwarded to fetched f2766db; security commits follow that tip. PRs 1-16 were still OPEN and unmerged when checked. Deployment is unverified and no deployment was performed. Current service boundaries and hosting uncertainty are in DEPLOY.md. The current execution checkpoint is in CIVIO_NEXT_AGENT_EXECUTION_PLAN.md.
