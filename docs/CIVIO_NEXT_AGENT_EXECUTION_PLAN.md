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

## Next task: stop the booklet from printing a fake answer key

The setup screen no longer says the PDF includes an answer key. The renderer still does.

[printable-exam.tsx](../resources/js/pages/user/exams/components/printable-exam.tsx) builds a key from `correct_option`. [handlePrintExam](../resources/js/pages/user/exams/hooks/use-exam-state.ts) loads questions with [startMockSession](../resources/js/pages/user/exams/utils/mock-session.ts), and [MockSessionService.php](../app/Services/Exam/MockSessionService.php) withholds keys. Missing `correct_option` becomes `0`, so the printed key can be all A.

Do this:

1. Omit the answer-key pages unless the payload includes real keys.
2. Add a server export that returns keys only after `checkPdfExportLimit` succeeds for that user. Do not put keys in `POST /exams/sessions`.
3. Keep the button hidden unless `auth.user.role === 'admin'` or `can_download_pdf`.
4. Label it "Download PDF & Answer Key" only after a test proves the letters match the stored keys.
5. Do not load the PDF libraries into the exam bundle.

Tests: a feature test that a normal session payload has no `correct_option`, and that the authorized export's letters match the database. Run `php artisan test`, `npm run types:check`, `npm run test:js`, `npm run build`, `npm run size`.

## Later phases

Do them in order. One slice each.

| Phase | Now | Missing | Start here |
| --- | --- | --- | --- |
| 1. CI | [tests.yml](../.github/workflows/tests.yml) runs Pest, build, types, JS tests, and size. [lint.yml](../.github/workflows/lint.yml) is read-only and uses `npm ci`. | Formatting is not enforced. `npm run format:check` fails on 81 existing files. `composer lint:check` fails on 5 PHP files. Switching CI to those commands would turn `main` red. | Format those files in one commit, then change lint.yml from `composer lint`, `npm run format`, and `npm run lint` to `composer lint:check`, `npm run format:check`, and `npm run lint:check`. |
| 2. Performance | Lite Mode already turns on for Save-Data and slow-2g, 2g, or 3g. A manual on or off beats that. CSS is 28.58 kB brotli of 33 kB. | There is no separate Enhanced tier. Confirm a connection change cannot rebuild an exam in progress. | Read [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md) and [lite-mode.ts](../resources/js/lib/lite-mode.ts). Do not add a second mode system. |
| 3. Exam setup | Study Mode and Exam Mode copy no longer mentions Dexter. The "Mode" legend is screen-reader only. The PDF sentence is gone. | The false printed key, above. | [setup-exam-view.tsx](../resources/js/pages/user/exams/components/setup-exam-view.tsx). |
| 4. Visual polish | Time dials, the 80% mark, and solid buttons exist. | Hover copy on the homepage sample is a `title`, not the exam tooltip. | Do not add Motion. Reuse CSS. |
| 5. Exam workspace | The live exam is the source of truth. | No rendered screenshot was captured in the last session. | Compare [exam-screen-preview.tsx](../resources/js/components/domain/exam-screen-preview.tsx) with the live exam when you change a control. |
| 6. Teaching | Reveal checks perimeter, PEMDAS, sequences, filing, mixture, grammar, mean, median, percent, interest, and factors against the key. | Many items still show only the stored explanation. | Add one solver in [RevealTutor.php](../app/Services/Exam/Reveal/RevealTutor.php) with a Pest test. Never publish a lesson that disagrees with the key. |
| 7. FSRS | Wrapper and unit tests only. | No table, no write on answer, no due queue, no offline sync. | Do not start until the PDF key bug is fixed. Schema, then one drill write, then a due list. |
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
