# Next-agent execution plan
> Execution refresh, 20 October 2026: follow GT's current order: F1/F2/F6 security, importer review gate, fabricated-readiness removal, Review Mistakes, mock composition, mock repetition. Earlier learning/visual roadmaps below are historical context. Security implementation and verification checkpoints are at the end of this file. No bank approval, live study mutation, or deployment is authorized.


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
| 1. CI | [tests.yml](../.github/workflows/tests.yml) runs Pest, build, types, JS tests, and size. [lint.yml](../.github/workflows/lint.yml) is read-only and uses `npm ci`. | Done 17 October 2026. Backlog formatted (`fb71fb5`). lint.yml generates Wayfinder routes, then runs `composer lint:check`, `npm run format:check`, and `npm run lint:check`. The Node 22 size failure is fixed (`6b48b73`); all JS is 1,035,527 of 1,040,000 B, so about 4 kB of headroom remains. | Trim lazy chunks before adding JS. Do not raise the budget silently. |
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

## CSE 2027 dates page (17 October 2026)

`/cse-2027-dates` is live in the app (not deployed). Its rows live in `app/Support/CseExamDates.php`. Re-read the CSC Examination Advisories page and update `LAST_CHECKED` on every check. When the CSC publishes the detailed announcement for the 14 March 2027 sitting, replace the unconfirmed row with its date and link. Never take a date from a reviewer, news site or social media. `tests/Feature/Public/CseDatesTest.php` enforces official CSC sources, last-checked dates, and no confirmed row without a date. PRC and scholarship pages wait for GT.

## Next learning slice

Build [REVIEW_MISTAKES_BRIEF.md](REVIEW_MISTAKES_BRIEF.md). All JS is 1,037,038 of 1,040,000 B after the dates page.

## Security execution checkpoint - 20 October 2026

Verified MSI main was clean at efc0d81 and fast-forwarded it to fetched origin/main f2766db. GitHub PRs 1-16 were all OPEN and unmerged. No live service, study database, protected stack, question approval, or deployment was changed.

Implemented F1/F6 answer-access slice: sessionless online drills/retakes require a browser- and principal-scoped served batch (20 recent batches, 300 items each, 24-hour expiry); arbitrary IDs cannot turn submission into a key endpoint. Active status and actual option bounds are checked again before grading. Session-backed mocks grade their entire served set, including blank items, and submissions re-read the session under a database row lock. Client track labels cannot turn drills into mocks. Strict locks cover other submissions and historical question feedback. Reveal/Expound reject inactive items. Reused PR #2's bank-key withholding while preserving an author's own draft response. Cached pool members are revalidated for current active status. Drill browsing is paged at 100; exam candidates and saved-set question responses are bounded at 300; saved-set summaries exclude inactive items. Bank-access limits apply in testing/local environments too, with distinct account/IP identity namespaces.

F2 remains PARTIAL: complete-set scoring and stale-model duplicate protection are implemented; authoritative deadline enforcement, answer autosave, late-final grading from saved answers, and absolute UI recovery clocks are still pending. Do not present Strict Mock timing as protected until that work ships.

Next: finish F2 before the importer review gate, readiness removal, Review Mistakes, composition and repetition work. The 496-item reparameterized file was not imported or approved. No current live-bank count was obtained (live database access is out of scope). Browser screenshots have not been captured.
## Strict deadline checkpoint - 20 October 2026

This supersedes the earlier PARTIAL F2 checkpoint. New Strict sessions persist started_at and deadline_at. Legacy sessions keep the deadline implied by original created_at and track. The authenticated/guest owner can save original-option answer patches with an optimistic save_version; stale writes, unserved IDs, inactive items, invalid options, expiry and submission all fail closed. Final grading uses the complete served set; at or after the exclusive deadline it ignores final-request answers and uses only saved server answers, leaving other items blank. The ten-minute grace protects visibility only and grants no answer-write time.

Strict UI selections save serially, shuffled options map back to stored indices, and recovery fetches the server deadline and saved choices. Remaining time follows the absolute deadline rather than interval ticks or saved timeLeft. A failed save stops further answer changes until recovery and explains that late submission uses saved answers only. Study pause/untimed behavior and offline drills remain separate.

Strict starts are serialized per learner/browser and a second protected Strict session is refused. Guest sessions also carry a server-only hash of their browser session identity, and protected guest session IDs survive the recent-session cap and login. This closes the ownership-list eviction bypass. Starts/submissions now share the always-on bank-access limiter; answer saves have a separate 180/minute limiter.

Verification so far: full PHP suite 368 tests / 7,824 assertions; 96 JS tests and TypeScript passed. Final lint/format/build/size results are recorded below when complete. SQLite regressions cover stale models and revisions; a real concurrent PostgreSQL load test has not been run. No rendered browser screenshots or live migration/deployment are claimed.

Shipped-to-source scope: F1/F2/F6 engineering. Still pending: fail-closed reparameterization importer and independent review gate; removal of fabricated readiness; Review Mistakes; fact/theme/passage composition; item exposure balancing. Do not approve or import the 496-item set. Editorial bank quality is not established by these security fixes. Next bounded slice is the importer review gate. Hosting remains GT's decision. See PAPER_PRACTICE_ASSESSMENT.md for the paper-booklet assessment; no paper flow or Complete Reviewer was built.
Final security verification (20 October 2026): php artisan test passed 369 tests / 7,829 assertions; npm run types:check, npm run test:js (98 tests), npm run lint:check (no warnings), npm run format:check, composer lint:check, npm run build and npm run size all passed in the isolated test checkout. Exam JS is 10,944 / 11,000 bytes; aggregate JS is 1,038,071 / 1,040,000 bytes (Brotli). Budgets were not changed. A pre-existing homepage formatting issue was isolated in 43f9922; the first answer-access security commit is a390683. No rendered browser or real concurrent PostgreSQL load test is claimed. The new migration has only run against test SQLite, not the live study database. No question-bank source or approval status changed.

## Bank import engineering checkpoint - 20 October 2026

Canonical main was clean and synchronized at 06f3d23 before this slice. Both console importers now fail closed on malformed/colliding content and require separately signed GT authorization for active writes. Replacements require unambiguous baseline-only matches plus reviewed original fingerprints. The shared ledger preserves stable revision identities, prevents content overwrites, detects drift, and supports signed promotion of unchanged tracked drafts. Signed record/report/signature/signer digests are retained. Dry run performs equivalent locked validation. All-or-nothing writes and deferred observer cache invalidation are covered by regression tests.

See [BANK_IMPORT_APPROVAL.md](BANK_IMPORT_APPROVAL.md) for the exact approval contract, operational prerequisites and limitations. No real approving key is configured or generated. No bank content/status, live database, deployment or collection changed. The 496-item file remains unapproved and was not imported. A separate reviewed revision workflow for changed legacy content and complete collection versioning remain future work. Verified in the isolated PHP 8.4 / Node 22 runtime: php artisan test 407 passed / 3,960 assertions; 98 JS tests; types, ESLint, Prettier, Pint, build and size passed. Aggregate JS remains 1,038,071 / 1,040,000 bytes and exam JS 10,944 / 11,000 bytes. Five inventory regressions pass separately. The old 496-row assertion loop was replaced with synthetic behavior/security tests; assertion totals are not comparable to the earlier manifest loop. No browser screenshots or concurrent PostgreSQL test are claimed.
