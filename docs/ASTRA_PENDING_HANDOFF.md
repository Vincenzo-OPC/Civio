# Pending handoff for Codex Astra

- Written 17 October 2026 (Asia/Manila) by Grok Bot for GT. Repo state read: `main` at `2313fbd`.
- **This is research and product context, not an engineering spec.** Astra keeps its own technical judgment on architecture, order inside a phase, libraries and tests. Where this file and the code disagree, the code and tests win, then [AGENTS.md](../AGENTS.md). Where it and a linked doc disagree, the linked doc wins: this file is a map.
- The only roadmap is [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md), with the learning-feature brief in [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §0. This file does not replace or reorder either of them, except that it puts the security findings first, as the [Sentinel dossier](research/sentinel/DOSSIER_2026-10-17.md) asks.

> **About GT's ChatGPT prompt for Astra.** GT wrote a long, comprehensive ChatGPT prompt for Astra and hasn't pasted it yet. **That prompt is not in this repo, and Grok Bot has never seen it.** This file does not reproduce it, verbatim or otherwise. It collects what the repo can verify. §7 lists what may be missing. When GT pastes the prompt, read it next to this file. Where the prompt adds requirements, the prompt carries GT's intent. Where it claims something is built, check the code.

## 0. How to use this doc

1. Read [AGENTS.md](../AGENTS.md), [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) (§5 security invariants) and [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md).
2. Read §1 here and the dossier's F1, F2 and F6. Those fixes come before any learning feature.
3. For each feature in §3, follow the links. Each status here was checked against code at `2313fbd`, not against older docs.
4. Do one slice per change, keep CI green, and update `CHANGES_SINCE_BASELINE.md` and the execution plan as those docs require.

**Status legend**

| Label | Meaning |
|---|---|
| **SHIPPED** | In `main`, wired into the app and covered by tests. Not deployed: nothing of Civio is on the public internet. |
| **PARTIAL** | Some of it exists in code. The rest is missing, as stated. |
| **BRIEF** | A build brief exists in `docs/`. No code. |
| **PROPOSAL** | Described in research or product docs, with no build brief and no code. |
| **NOT STARTED** | Named in the roadmap, with nothing built and no brief. |
| *GT idea, not yet specified in repo* | GT has raised it, but no repo doc defines it. Ask GT before building. |

## 1. IMMEDIATE PRIORITY: security and exam integrity

These are integrity defects in shipped code. The dossier ranks them "before any public deploy" and before any Strict-based meter. They were re-checked by reading code at `2313fbd` and are still present. The probes were not re-run for this file. Detail and evidence: [DOSSIER_2026-10-17.md](research/sentinel/DOSSIER_2026-10-17.md) §2.

**F1. Answer keys leak through `POST /exams/attempts` (Critical).**
- The public route accepts any `question_ids` when `exam_session_id` is omitted. `ExamGradingService::grade` then returns `correct_option` and `explanation` for every ID.
- The controller never consults `StrictMockLock`. So keys come back for items locked in an open Strict Mock, and for drafts.
- Fake attempts are also stored, and they feed the analytics behind F3.
- The `StrictMockLock` docblock claims a wider lock than the code enforces (Reveal, Expound and PDF export only).
- Dossier direction: free-form attempts accept only active items, never return keys for locked items, and probably require a server session for anything that counts as a mock. Add a regression test.

**F2. The server doesn't enforce Strict Mock time or completeness (High).**
1. **No server deadline.** A Strict submit long after the limit is accepted. The lock expires at limit + 10 min, so a learner can Reveal everything and then submit for 100% as `mode=strict`. `exam_sessions` has no `expires_at`.
2. **Subset submit.** `SubmitExamAttemptAction` only checks that the submitted IDs were served. Submitting 2 of 9 served items scores 2/2 = 100%.
3. **The clock lives on the phone.** `use-exam-timer.ts` counts `setInterval` ticks. Resume restores the saved `timeLeft` without subtracting the time that passed, so closing the tab freezes the clock. Chrome also throttles hidden-tab timers to about once a minute, so the Strict clock runs slow on phones.
- Dossier direction: store `expires_at`, compute remaining time as `expires_at − now`, reject or flag late Strict submits, and require the full served set, with unsent items counted as blank.

**F6. Drafts are exposed through Reveal and Expound, and the bank can be scraped (Medium).**
- `revealAnswer` and `expoundAnswer` validate only `exists:questions,id`, with no `status=active` check (`ExamController.php:163` and `:213`). A draft's key and explanation come back with 200.
- `global-views` allows 120 requests per minute per IP, so the whole bank can be downloaded from one IP in about 16 minutes.
- The Strict lock is per account or browser session, so a second browser gets around it.
- Dossier direction: active items only. Consider per-route limits and requiring an item to have been served by a session or a drill before Reveal.

**Probes.** The four throwaway Pest probes are in dossier [Appendix A](research/sentinel/DOSSIER_2026-10-17.md#appendix-a-integrity-probe-throwaway-run-in-an-isolated-clone-never-commit):
- P1: keys returned through `/exams/attempts` during an open Strict Mock.
- P2: a subset submit scores 100%.
- P3: a late submit after the keys unlock.
- P4: a draft key through Reveal.

Each passes today, which means the bug is present. Run them in a scratch clone and never commit them as written. When you fix a finding, flip its expectation so it becomes a committed regression test. The nightly Civio Security Review routine runs these probes against new commits that touch exam code, and it reports to GT. It never edits anything.

The security invariants in [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §5 still apply. These findings are places where the code falls short of them.

## 2. Readiness analytics: the fake predictor card (F3, High, honesty)

- **Status: SHIPPED but not real.** The dashboard card [`ai-readiness-bento-card.tsx`](../resources/js/pages/user/dashboard/components/ai-readiness-bento-card.tsx) is titled "AI Readiness Predictor" and shows a pass percentage.
- The number is `round(mockAvg × 0.9)`, with +5 when "improving" and −8 when "declining" (`DeterministicAnalysisService.php`, around line 509). It is not AI, not calibrated and not a probability.
- "Mock" there means any attempt whose **client-sent** `metadata.track` isn't "Drill". That includes Study mode with Reveal, F2 subset submits and F1 free-form attempts.
- It conflicts with [ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md) ("Not done, and not claimed: pass probabilities"), [ENGINES.md](ENGINES.md), the execution plan's "Do not restore … unverified readiness scores" and [DESIGN_IMPLEMENTATION_BRIEF.md](DESIGN_IMPLEMENTATION_BRIEF.md) §15.
- Dossier direction (needs GT's agreement on wording): drop "AI" and "Predictor" and show a fact, e.g. "Latest full Strict Mock: 74% (80 needed)". Count only server-session Strict attempts, which depends on F1 and F2. The real Readiness meter in CODEX_HANDOFF_PLAN §0.2 ("from Strict Mock results only, hidden until there is enough data") stays a BRIEF until the integrity fixes land.

## 3. Learning features: honest status

| Feature | Status | What exists, and where to read |
|---|---|---|
| **Review Mistakes** | **BRIEF** | [REVIEW_MISTAKES_BRIEF.md](REVIEW_MISTAKES_BRIEF.md), from [LEARNING_DELIVERY_RECOMMENDATION.md](LEARNING_DELIVERY_RECOMMENDATION.md). The next learning slice in the execution plan. No table and no UI. The dossier (F8) suggests adding classical item analysis (percent correct, distractor pick rate, point-biserial) to this slice. |
| **Duplicate-fact rule (`fact_id`)** | **PARTIAL** (column + import on branch `grok/fact-id-theme`; mock rule not built) | [FACT_ID_MOCK_RULE_BRIEF.md](FACT_ID_MOCK_RULE_BRIEF.md), see Status. There are 8 recall/applied pairs plus the 10 gap-fill-004 IDs. The `MockPoolSelector` rule is still for Astra. A mock may serve one item per `fact_id`. |
| **Theme cap (`theme`)** | **PARTIAL** (column + import on branch `grok/fact-id-theme`; cap not built) | Same brief, addendum 1. At most 2 items per theme per mock. One theme is tagged on 8 items today. |
| **Passage sets (`passage_id`)** | **BRIEF** | Same brief, addendum 2, and spec v0.1.9 §10.8. Siblings are tagged only in `notes` for now. gap-fill-005 has 7 passage sets, active on the MSI. |
| **Adaptive difficulty** | **PARTIAL** (heuristic only) | `MockPoolSelector`: a harder-biased shuffle (`estimateDifficulty`, `HARD_BIAS`, no DB column), weak-topic bias, wrong items first. Browser-side guest bias is in `lib/guest-study-bias.ts`. No calibrated difficulty and no learner model. Item `difficulty` labels are author-assigned and mostly `medium`. The dossier (F8) advises deferring IRT and BKT until there are real responses. Taxonomy and learner state are BRIEF in [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §9.2. |
| **Six subject-specific learning engines** | **PROPOSAL** (no spec in repo) | [LEARNING_DELIVERY_RECOMMENDATION.md](LEARNING_DELIVERY_RECOMMENDATION.md) records them as "research proposals" from an earlier Astra handoff whose text is not in the repo. It warns that "six new services would exceed this boundary". What does exist: [ENGINES.md](ENGINES.md) documents the deterministic Reveal solvers (about 10 patterns), and [2026_AI_PRODUCT_STANDARD.md](2026_AI_PRODUCT_STANDARD.md) §3 describes six *product* engines: Simulation, Mastery, Tutor, Study Studio, Source Library and Focus Toolkit. Those are not subject engines. A per-subject engine design is *GT idea, not yet specified in repo*. |
| **FSRS spaced review** | **PARTIAL** (scheduler math only) / **BRIEF** | `resources/js/lib/review/fsrs.ts` and `tests/Js/fsrs.test.ts`. Nothing imports them. No card table, no write on answer, no due queue, no offline sync ([ADAPTIVE_LEARNING.md](ADAPTIVE_LEARNING.md)). Brief: CODEX_HANDOFF_PLAN §0.1 and §9.4. It waits on Review Mistakes' stored events. The dossier (F8) suggests storing the review log on the server and clamping client-computed due dates. |
| **Dexter** | **PARTIAL** | `Services/Dexter/DexterEvaluationService.php` checks answers against the key. It is **not a chat tutor**, and the execution plan says never to describe it as one. `TutorProvider` / `NullTutorProvider` (Prism) is a stub. Hint-before-answer, classify mistake and session summary are BRIEF (CODEX_HANDOFF_PLAN §0.3 and §9.3). |
| **Study Studio** | **PROPOSAL** | [2026_AI_PRODUCT_STANDARD.md](2026_AI_PRODUCT_STANDARD.md) §3D, §6A and roadmap P2; [AI_STUDY_AND_SPELLING_SYSTEM.md](AI_STUDY_AND_SPELLING_SYSTEM.md). No code. |
| **Dashboard meters** | **PARTIAL** / **BRIEF** | Shipped: history, streak, daily goal and exam countdown (`resources/js/pages/user/dashboard/components/`). Brief only: Memory, Focus, XP/level, Topic Map, Readiness and a streak freeze (CODEX_HANDOFF_PLAN §0.2). Every meter needs a server source and a test. The readiness card is F3 (§2 above). |
| **Exam Day Hub** | *GT idea, not yet specified in repo* | Related pieces that do exist: the dashboard countdown (`exam-countdown.tsx`), the sourced [CSE 2027 dates page](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md#cse-2027-dates-page-17-october-2026) (`app/Support/CseExamDates.php`, SHIPPED) and a "Day 60: Exam Day Preparation" study-plan template. The 22 Nov 2026 reset exam for NCR and parts of Region IV and CAR (fallback 24 Jan 2027) is dossier F4, with a decision pending from GT. |
| **Application tracker** | *GT idea, not yet specified in repo* | The dossier (F5) says to **hold** any requirements checklist until CSC posts the March 2027 announcement. As of 17 Oct 2026 it is not posted. The August 2026 ID rule ("expires within CY 2026") must not be copied forward. Cite csc.gov.ph only, never cse.ph (dossier §1 lists its date errors). |
| **Premium AI** | **PROPOSAL** (paid tier: *GT idea, not yet specified in repo*) | Provider routing (no-AI, cheap, strong and frontier tiers) and a "Sign in with ChatGPT" readiness are in [2026_AI_PRODUCT_STANDARD.md](2026_AI_PRODUCT_STANDARD.md) §11 to §13. In code there is only the Prism stub, Copy for AI, and the Ask ChatGPT and Ask Gemini handoffs ([EXTERNAL_AI_HANDOFF.md](EXTERNAL_AI_HANDOFF.md)). No billing, no plan gating apart from the admin-set `can_download_pdf` flag, and no paid provider calls. Competitor prices are in dossier F10. Pricing is GT's decision. AGENTS.md: provider keys are never in `VITE_*`. |
| **Design direction** | **PARTIAL** | [DESIGN_IMPLEMENTATION_BRIEF.md](DESIGN_IMPLEMENTATION_BRIEF.md) (mockup `docs/design/focused-learning-canvas-mockup.png`, §17 deliverables) and [design/HOMEPAGE_CHOOSE_EXAM_2026.md](design/HOMEPAGE_CHOOSE_EXAM_2026.md). Shipped: the exam-screen redesign (violet selection, lime only after Reveal, Study pause; `9b65704`), solid study buttons and the wordmark. Most of the full brief, such as the four destinations and the replacement for the Question Palette, is still brief only. The execution plan's "Design that stays" and "Do not restore" lists are binding. |
| **Complete Reviewer book** | **NOT STARTED** | Execution plan phases 9 to 11. Only the exam booklet PDF exists. |
| **"Why this question?" and interleaving** | **BRIEF** | CODEX_HANDOFF_PLAN §0.1 and §0.3. |

## 4. Content

- **Milestone (GT, 17 Oct 2026):** exactly **2,000 approved questions**, a clean hundred per subject. 3,000 stays the long-term goal. The proposed split, the Release Collection idea and a Codex implementation brief are in [research/MILESTONE_2000_PLAN.md](research/MILESTONE_2000_PLAN.md). **It is a PROPOSAL until GT approves it.** Its recommendation: Verbal 600 (English 300 + Filipino 300), Numerical 400, Analytical 400, Clerical 300, GI 300.
- **Live bank:** the MSI local DB had 1,978 active items on 17 Oct 2026 (Analytical 365, Clerical 262, GI 347, Numerical 400, Verbal 604; 501 of them baseline). Nothing is in production.
- **New finding for Astra:** mock composition follows subcategory labels rather than CSC subtopics. On today's data, 6 Numerical and about 16 Clerical items land in almost every unbiased mock, and about 6 of every 8 GI items come from 30 single-item labels. See plan §3.5. It needs a selector change (per-subtopic quotas) plus a label clean-up that GT approves.
- **Pipeline:**
  1. ChatGPT drafts batches from [research/CHATGPT_NEXT_PROMPT.md](research/CHATGPT_NEXT_PROMPT.md).
  2. Grok Bot audits with `scripts/batches/qa.py` and by hand, then writes review packets.
  3. **Chief of Staff** (a Grok agent that holds GT's delegation for Civio approvals) rules item by item.
  4. Approved items are imported with `civio:import-batch`.
  5. Progress is logged in [research/AUDIT_TRACKER.md](research/AUDIT_TRACKER.md).

  The full process is in [HANDOFF_ANY_AI.md](HANDOFF_ANY_AI.md) §3, with the spec at [CSE-Question-Design-Spec.md](CSE-Question-Design-Spec.md) (v0.1.9). **Astra does not author or approve bank items.** AGENTS.md "Question bank rule" applies: no new stems without approval, and no filler clones.

## 5. Current shipped state (verified in code, 17 Oct 2026)

- **Exam engine:** server-picked full mocks (150 Professional in 3 h 10 m, 145 Subprofessional in 2 h 40 m; `MockPoolSelector`, `MockSessionService`), server grading, keys withheld in the session payload, unique items only, no padding.
- **Study and Strict modes:** `exam_sessions.mode` / `exam_attempts.mode`. Strict hides Reveal, Dexter and Copy for AI, and `StrictMockLock` returns 423 on Reveal, Expound and PDF export (gaps: §1).
- **Reveal tutor plus shortcuts:** `RevealTutor` publishes a lesson only when its solver matches the stored key. Show/Hide Explanation and Expound. Numerical items show "Shortcut:" before "Method:" (spec §10.6). See [ENGINES.md](ENGINES.md).
- **Copy for AI** with Ask ChatGPT and Ask Gemini ([EXTERNAL_AI_HANDOFF.md](EXTERNAL_AI_HANDOFF.md)).
- **PDF export with answer key:** `POST /exams/export-pdf`, permission-gated and throttled, refused during an active Strict Mock (`698ba7c`, `PdfAnswerKeyTest`).
- **Lite Mode and offline drill packs** with a server re-grade ([LITE_MODE_PLAN.md](LITE_MODE_PLAN.md)).
- **PWA:** vite-plugin-pwa, an update prompt, NetworkOnly for `/exams`.
- **CSE 2027 dates page:** `/cse-2027-dates`, CSC sources only (`e3055c5`, `CseDatesTest`).
- **CI:** [tests.yml](../.github/workflows/tests.yml) (Pest, build, types, JS tests, size) and [lint.yml](../.github/workflows/lint.yml), which is check-only.
- **Bundle:** all JS is 1,037,038 of 1,040,000 B brotli, so there's **about 3 kB of headroom**. The exam chunk is 10.22 of 11 kB. Trim lazy chunks before adding JS. Never raise a budget silently.
- **Not shipped and not claimed:** see §3. Offline results are stored but don't appear in history (CODEX_HANDOFF_PLAN §6).

## 6. Guardrails

- **No deploy and no spend.** Nothing is deployed. Hosting is GT's call ([DEPLOY.md](DEPLOY.md)). Add `[skip netlify]` to docs-only and bank-only commits.
- **Protected machines.** Never touch GT's MSI Docker study containers or Hermes (`:8642`) (AGENTS.md, CODEX_HANDOFF_PLAN §5.7).Grok Bot imports approved items into the local Civio DB only after a backup.
- **Git.** Normal pushes to `main` only. `git pull --rebase` first, because several agents push. Never force-push and never use `--no-verify`. Conventional Commits. No secrets.
- **No invented stats.** No pass rates, mastery or readiness without stored data and a test (DESIGN_IMPLEMENTATION_BRIEF §15). The unverified "14.41% pass rate" post in dossier §3 must not appear in product copy.
- **UI constraints** are in AGENTS.md and the execution plan:
  - Title Case **Civio**, and never imply CSC affiliation.
  - Light violet `#5B35F5` and logo green `#B3F52D`.
  - No new animation package.
  - Usable at 360 px, Lite-compatible.
  - The "Do not restore" list holds: Auto-Next, permanent sidebar, the word Palette, and so on.
- **Never claim an unbuilt feature.** In docs, UI copy and commit messages alike, use the status labels above.

## 7. Missing context and open questions for GT

**Possibly missing from this file:**
1. GT's comprehensive ChatGPT prompt for Astra. Not in the repo, and not seen by Grok Bot. Anything it adds beyond §1 to §6 is missing here.
2. The earlier "Astra handoff" that [LEARNING_DELIVERY_RECOMMENDATION.md](LEARNING_DELIVERY_RECOMMENDATION.md) assessed (from `2f11340`). Only Astra's assessment of it is in the repo, not its text. The six subject engines and the psychometric prediction came from it.
3. GT's Master Product Context 2026, which [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §9.6 places in GT's Obsidian vault. A 5 Oct 2026 "Civio Master Product Context for Grok Bot" exists outside the repo, on Grok Bot's box. It isn't committed, so Astra can't read it unless GT adds it.
4. Any definition of Exam Day Hub, the application tracker, a premium tier or the six subject engines.

**Open questions:**
1. Approve the 2,000 split and the Release Collection approach ([MILESTONE_2000_PLAN.md](research/MILESTONE_2000_PLAN.md) §9)?
2. F3 wording: rename the readiness card to a factual "Latest full Strict Mock" line now, or hide it until F1 and F2 are fixed?
3. F4: show the 22 Nov 2026 reset exam (fallback 24 Jan 2027) as a date option in Civio?
4. Deploy target: [DEPLOY.md](DEPLOY.md) says Cloud Run + Neon + Cloudflare, but [CODEX_HANDOFF_PLAN.md](CODEX_HANDOFF_PLAN.md) §0.5 says Koyeb + Neon + a Netlify landing. Which one is current?
5. The MSI port note in AGENTS.Which containers count as protected?
6. Who owns `qa.py` changes (dossier F9: the audit agent, not Astra)?

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

## Bank evidence inventory checkpoint - 20 October 2026

Importer boundary shipped in 93633ef. Added a read-only Git-object inventory, five Python regressions, pinned source lock for main 06f3d23 and open PRs #3-12, and a mechanical review/report using the existing PR #12 explanation linter. Inventory covers 143 artifacts / 4,276 file occurrences (not live items), with 294 identity groups needing version reconciliation. Existing qa_all.py --no-fixes passed on 1,000 main batch occurrences, but GI official-text verification was skipped because no source cache was present. No editorial approval or status changed; AUDIT_TRACKER was intentionally left unchanged.

See [bank review queue](research/bank/REVIEW_QUEUE_2026-10-20.md) for source hashes, exact reproduction commands, #462/B3 HOLD/source gaps, PR #12 passage-companion decisions, and the distinction between projection and release approval. Reconciliation/independent content review, sanitized runtime evidence, GT's final exact-content approvals and the provisional 2,000 split remain pending. No collection activation or authored bank content was produced. Next bounded bank slice: independently reconcile the #462 evidence and B3 HOLD/source gaps into a digest-bound decision packet for GT; do not apply fixes or retirements from stale snapshot IDs.
