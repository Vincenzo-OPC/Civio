# Next-agent execution plan

This is the only roadmap to follow. [CIVIO_CURRENT_STATE_HANDOFF.md](CIVIO_CURRENT_STATE_HANDOFF.md) is the current-state note. Specialized docs stay where they are. If this file and the code disagree, the code and tests win.

Session start SHA: `3c18ec0258ec855795654afc85a93fa435684d55`. The setup-copy commit is `d8d1714`. Confirm the tip with `git rev-parse origin/main` after the docs commit that records it.

## Startup

1. Read [AGENTS.md](../AGENTS.md), this file, and [CIVIO_CURRENT_STATE_HANDOFF.md](CIVIO_CURRENT_STATE_HANDOFF.md).
2. `git fetch origin main` and confirm the working tree. Leave `app/Providers/AppServiceProvider.php` uncommitted if it only sets a local asset root.
3. Do one phase slice. Do not start the book, FSRS, and a visual rewrite in the same change.
4. Run the checks for the files you touched. Do not claim a check you did not run.
5. Commit, push without force, and update this file plus [CHANGES_SINCE_BASELINE.md](CHANGES_SINCE_BASELINE.md).

## What already works

- Study Mode and Exam Mode, server-picked mocks, withheld keys, server scoring, Strict Mock lock. [live-exam-view.tsx](../resources/js/pages/user/exams/components/live-exam-view.tsx), [StrictMockLock.php](../app/Services/Exam/StrictMockLock.php).
- Show Explanation / Hide Explanation, checked Reveal, Copy Question, Ask. [answer-reveal.tsx](../resources/js/pages/user/exams/components/session/answer-reveal.tsx), [RevealTutor.php](../app/Services/Exam/Reveal/RevealTutor.php).
- Dexter is a backend key check at [DexterEvaluationService.php](../app/Services/Exam/DexterEvaluationService.php). It is not a chat tutor. Do not describe it as one.
- Flag, Question List, Notes, timer, pause where allowed, guest study, Lite Mode, offline drill packs.
- FSRS math only: [fsrs.ts](../resources/js/lib/review/fsrs.ts). Not wired. See [ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md).
- Exam booklet PDF for admin and `can_download_pdf` accounts. Libraries stay out of the main bundle. [global-pdf-exporter.tsx](../resources/js/components/shared/global-pdf-exporter.tsx).

## Do not restore

Auto-Next, a permanent sidebar, the word Palette in the interface, a second Hide control, in-bank Try Another, long BIR or CSC blocks in the exam, glass blur on dark cards, a previous product name, unverified readiness scores.

## Design that stays

Light violet `#5B35F5`. Logo green `#B3F52D`. Dark paper `#000000`. Solid study buttons in [app.css](../resources/css/app.css) (`.civio-action`). Question List closed by default. Title Case for headings and actions. Sentence case for descriptions. Reduced motion is respected. No new animation package.

Approved homepage lines, if you touch that screen: "PHILIPPINE CIVIL SERVICE EXAM", "Choose Your Exam." No subtitle. Professional: 150 questions, 3 h 10 m. Subprofessional: 145 questions, 2 h 40 m.

## PDF answer-key fix completed (17 October 2026)

The dedicated `POST /exams/export-pdf` route calls `checkPdfExportLimit` before returning keys and shares the existing daily throttle. It uses server-selected items in stored option order, accepts no question/session selector, and refuses export while the requesting learner has any active Strict Mock (including guest sessions retained after login). Its response is private/no-store. The response token only deduplicates client rendering; it grants no server access.

Normal `POST /exams/sessions` remains keyless. The booklet omits the whole key page unless every item has an integer key inside its actual options. The permission-gated button now says "Download PDF & Answer Key". PDF code remains lazy.

Evidence: `tests/Feature/User/PdfAnswerKeyTest.php` covers stored A/B/C/D keys and printed option order, keyless sessions, guests, permission denial, arbitrary selectors, Strict Mock locks, expired locks, invalid database keys, and throttling. `tests/Js/pdf-answer-key.test.ts` covers missing/invalid keys and renderer wiring. Verified on 17 October 2026 from a fresh clone: `php artisan test` 323 passed (7,478 assertions), `npm run test:js` 94 passed, and `types:check`, `lint:check`, `build` and `size` passed (exam chunk 10.22 kB of 11 kB; all JS 1,035,732 B of 1,040,000 B). The PDF libraries (`jspdf`, `html2canvas`) build as separate lazy chunks, not into the exam chunk.

## Later phases

Do them in order. One slice each.

| Phase | Now | Missing | Start here |
| --- | --- | --- | --- |
| 1. CI | [tests.yml](../.github/workflows/tests.yml) runs Pest, build, types, JS tests, and size. [lint.yml](../.github/workflows/lint.yml) is read-only and uses `npm ci`. | Formatting backlog cleared on 17 October 2026: `npm run format:check` and `composer lint:check` pass. CI still runs the fixing commands. | Change lint.yml from `composer lint`, `npm run format`, and `npm run lint` to `composer lint:check`, `npm run format:check`, and `npm run lint:check`. |
| 2. Performance | Lite Mode already turns on for Save-Data and slow-2g, 2g, or 3g. A manual on or off beats that. CSS is 28.58 kB brotli of 33 kB. | There is no separate Enhanced tier. Confirm a connection change cannot rebuild an exam in progress. | Read [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md) and [lite-mode.ts](../resources/js/lib/lite-mode.ts). Do not add a second mode system. |
| 3. Exam setup | Study Mode and Exam Mode copy no longer mentions Dexter. PDF export now has an authorized keyed payload and a fail-closed answer-key page. | PDF integrity fix complete; no new mode changes. | [setup-exam-view.tsx](../resources/js/pages/user/exams/components/setup-exam-view.tsx). |
| 4. Visual polish | Time dials, the 80% mark, and solid buttons exist. | Hover copy on the homepage sample is a `title`, not the exam tooltip. | Do not add Motion. Reuse CSS. |
| 5. Exam workspace | The live exam is the source of truth. | No rendered screenshot was captured in the last session. | Compare [exam-screen-preview.tsx](../resources/js/components/domain/exam-screen-preview.tsx) with the live exam when you change a control. |
| 6. Teaching | Reveal checks perimeter, PEMDAS, sequences, filing, mixture, grammar, mean, median, percent, interest, and factors against the key. | Many items still show only the stored explanation. | Add one solver in [RevealTutor.php](../app/Services/Exam/Reveal/RevealTutor.php) with a Pest test. Never publish a lesson that disagrees with the key. |
| 7. FSRS | Wrapper and unit tests only. | No table, no write on answer, no due queue, no offline sync. | PDF prerequisite complete. Establish durable server-graded review events before scheduling; see the delivery recommendation. |
| 8. Dashboard | History, drills, and the calendar exist. | Meters must come from stored data. No fake readiness. | [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) section 0.2 is the brief, not a claim that it exists. |
| 9. Book architecture | The exam booklet generator exists. The Complete Reviewer does not. | Separate content from print. Do not import the typesetter into the exam bundle. | Research Vivliostyle, Paged.js, or Typst. Pick one. |
| 10. Sample chapter | Not started. | One verified chapter: terminal-digit filing, from the definition through worked items. | Write the lesson before the layout. |
| 11. Full book | Not started. | Editions, print size, and QA. Do not claim the book exists. | Only after the sample chapter is accepted. |

## Invariants

- No answer keys in the live exam payload.
- Copy Question must not call `/exams/reveal`.
- The client score is ignored.
- Do not commit `.env`, databases, or the local asset-root override.
- Do not force-push.
- Do not touch protected MSI containers or Hermes.

## Delivery recommendation

See [LEARNING_DELIVERY_RECOMMENDATION.md](LEARNING_DELIVERY_RECOMMENDATION.md) for the evidence-based Astra assessment. The highest-value next learning slice is a persistent, owner-scoped return-to-mistakes queue from server-graded drills, with assisted answers distinguished from independent recall. FSRS scheduling follows reliable review-event persistence. No mastery/readiness model, Complete Reviewer, or sample chapter is claimed.
