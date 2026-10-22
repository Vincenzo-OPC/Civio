# Next-agent execution plan

> **Issue #18 status (22 Oct 2026): DONE on main (dfa8fd7, a44bc0e + follow-up).** All owner-key AI goes through `App\Services\Ai\OwnerAiSpendLock`. It is closed by default and opens only when `CIVIO_OWNER_FUNDED_AI` is exactly `true`, and never in production; credentials alone do nothing. The only path to an AI host is `AiGatewayService`, which checks the lock first in every network method. The architecture test `tests/Unit/Architecture/AiEgressTest.php` fails if app code names an AI host or uses an HTTP client elsewhere (Turnstile is the only allowed non-AI exception) or reads AI keys with `env()`. **New AI code must go through the gateway and keep these tests green. Do not open the lock without GT's explicit approval.**

> **Latest Astra decision gate (21 Oct 2026):** Read [timing, telemetry and educational AI evaluation brief](DEXTER_TIMING_AND_EVALS_2026-10-21.md). GT's optional elapsed/pacing bar, eventual concept-level pace and multi-turn tutor evals are proposals for research, not blanket feature approval. Require Astra-reviewed ADR, rigorous correctness-first / speed-second evaluation, user privacy, realistic exam timing and Lite budget; proceed in small tested slices **only after existing F1/F2/F6, importer, readiness integrity and Review Mistakes gates**. Existing explicit no-spend/no-deploy/no-bank-activation rules remain in effect.


> **GT adaptive learning directive (21 Oct 2026):** After verifying the existing 20 Oct security / bank approval / fabricated-readiness gates and completing the first eligible Review Mistakes slice, execute [Dexter adaptive tutor master plan](DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md) in independently tested steps. Read [tutor policy](DEXTER_TUTOR_POLICY_2026-10-21.md), [AI access and monetization](DEXTER_AI_ACCESS_AND_BUSINESS_2026-10-21.md), [100%-practice CSE research](CSE_PERFECT_SCORE_RESEARCH_2026-10-21.md). User wants Subprofessional first and math/spelling emphasis; prioritize independent unseen mastery, not assisted success or invented pass odds. Upgrade Ask AI policy without answer leaks; follow persistent mistake events, FSRS, concept model, then optional in-app Dexter. **No billing activation, OAuth partner activation, production spend, deployment, live DB mutation, or question-bank changes have been approved.**

> Execution refresh, 20 October 2026: follow GT's current order: F1/F2/F6 security, importer review gate, fabricated-readiness removal, Review Mistakes, mock composition, mock repetition. Earlier learning/visual roadmaps below are historical context. Security implementation and verification checkpoints are at the end of this file. No bank approval, live study mutation, or deployment is authorized.


This is the only roadmap to follow. [CIVIO_CURRENT_STATE_HANDOFF.md](CIVIO_CURRENT_STATE_HANDOFF.md) is the current-state note. Specialized docs stay where they are. If this file and the code disagree, the code and tests win.

## Engineering slice, 22 October 2026

Pre-deployment check, same day: [DEPLOYMENT_READINESS_2026-10-21.md](DEPLOYMENT_READINESS_2026-10-21.md). The sandbox still cannot unpack image layers. The manual `image smoke` workflow passed on GitHub as [run 39631539498](https://github.com/Vincenzo-OPC/Civio/actions/runs/39631539498). That verifies the image only. Smart Review stays implemented, not production verified. No deploy.

Astra's 21 October research is on `main` as `3c1fd91` and `b51c311`. It is research only. The ten numerical drafts stay unapproved and inactive.

Review Mistakes now exists for signed-in drills and Study Mocks. A wrong server-graded answer creates one `review_items` row. Reveal or Expound marks the answer assisted, so a later correct answer does not clear it. A Strict Mock writes nothing. The list is `/reviews/mistakes`. It does not include the key. FSRS is still not wired.

Analytics no longer shows a Top 50% rank when fewer than six attempts exist or the average is zero. A subject missing from an attempt is null in the breakdown, not a zero. The dashboard still has a heuristic pass index in `DeterministicAnalysisService`. That formula was not replaced.

Bank signature tests need the PHP sodium extension. This environment does not have it, so those tests were not treated as a regression. No question was imported or activated. No deploy.

Help on Review Mistakes follows the served drill batch, or the open Study Mock when no drill batch exists. A second drill in the same browser does not inherit the first explanation. A later overlapping drill also does not erase the first drill's explanation. The practice percentage is the stored correct-item count, not a weighted category formula.

Smart Review is wired for signed-in online practice. The production image keeps Node for `ts-fsrs` and removes npm. A failed reminder is not shown as saved. It is not deployed. See [FEATURE_CATALOG.md](FEATURE_CATALOG.md). FSRS parameters are not trained. The next learning slice is Astra's curriculum work, not another scheduler.

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
- Smart Review for signed-in online practice: [FsrsScheduler.php](../app/Services/Exam/FsrsScheduler.php). The production image keeps Node and drops npm. Not deployed. Not offline. See [FEATURE_CATALOG.md](FEATURE_CATALOG.md).
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
| 1. CI | [tests.yml](../.github/workflows/tests.yml) runs Pest, build, types, JS tests, and size. [lint.yml](../.github/workflows/lint.yml) is read-only and uses `npm ci`. | Done 17 October 2026. Backlog formatted (`fb71fb5`). lint.yml generates Wayfinder routes, then runs `composer lint:check`, `npm run format:check`, and `npm run lint:check`. The Node 22 size failure is fixed (`6b48b73`); all JS is 1,035,527 of 1,040,000 B, so about 4 kB of headroom remains. | Trim lazy chunks before adding JS. Do not raise the budget silently. |
| 2. Performance | Lite Mode already turns on for Save-Data and slow-2g, 2g, or 3g. A manual on or off beats that. CSS is 28.58 kB brotli of 33 kB. | There is no separate Enhanced tier. Confirm a connection change cannot rebuild an exam in progress. | Read [LITE_MODE_PLAN.md](LITE_MODE_PLAN.md) and [lite-mode.ts](../resources/js/lib/lite-mode.ts). Do not add a second mode system. |
| 3. Exam setup | Study Mode and Exam Mode copy no longer mentions Dexter. PDF export now has an authorized keyed payload and a fail-closed answer-key page. | PDF integrity fix complete; no new mode changes. | [setup-exam-view.tsx](../resources/js/pages/user/exams/components/setup-exam-view.tsx). |
| 4. Visual polish | Time dials, the 80% mark, and solid buttons exist. | Hover copy on the homepage sample is a `title`, not the exam tooltip. | Do not add Motion. Reuse CSS. |
| 5. Exam workspace | The live exam is the source of truth. Slice 1 (answer icons + words, timer pill/hairline ring, untimed hides the clock) is on branch `grok/exam-workspace-timer-answers`. | No rendered screenshot yet: capture desktop/mobile, light/dark/Lite before merging. Next slices: question typography and breadcrumb, then mobile nav, then scorecard. | Compare [exam-screen-preview.tsx](../resources/js/components/domain/exam-screen-preview.tsx) with the live exam when you change a control. |
| 6. Teaching | Reveal checks perimeter, PEMDAS, sequences, filing, mixture, grammar, mean, median, percent, interest, and factors against the key. | Many items still show only the stored explanation. | Add one solver in [RevealTutor.php](../app/Services/Exam/Reveal/RevealTutor.php) with a Pest test. Never publish a lesson that disagrees with the key. |
| 7. FSRS | Signed-in online Smart Review. Server runs ts-fsrs. Due list is Review Mistakes. | No offline sync. No trained parameters. Resolved is not mastered. | [FEATURE_CATALOG.md](FEATURE_CATALOG.md) and [ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md). |
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

## CSE 2027 dates page (17 October 2026)

`/cse-2027-dates` is live in the app (not deployed). Its rows live in `app/Support/CseExamDates.php`. Re-read the CSC Examination Advisories page and update `LAST_CHECKED` on every check. When the CSC publishes the detailed announcement for the 14 March 2027 sitting, replace the unconfirmed row with its date and link. Never take a date from a reviewer, news site or social media. `tests/Feature/Public/CseDatesTest.php` enforces official CSC sources, last-checked dates, and no confirmed row without a date. PRC and scholarship pages wait for GT.

## Next learning slice

Build [REVIEW_MISTAKES_BRIEF.md](REVIEW_MISTAKES_BRIEF.md). All JS is 1,037,038 of 1,040,000 B after the dates page.

## Review queue continuation — 18 October 2026

GT's current handoff requires feature-branch PRs and owner review: no pushes to main, merges, force-pushes, or deployments. Sixteen draft PRs were opened in the supplied order. The first branch, `grok/fix-welcome-format` at `cf00b8a`, passed every required check plus Pint: 328 PHP tests and 94 JS tests. Total JS measured 1,037,085 of 1,040,000 B on Node 22. Real desktop/phone light/dark welcome screenshots and check details are in [the review evidence](review/2026-10-18/README.md). Other PRs remain draft with validation and screenshots pending; the drills-preview decision and editorial approvals remain with GT/Chief of Staff. This is not exam-workspace or Lite-mode browser verification.
