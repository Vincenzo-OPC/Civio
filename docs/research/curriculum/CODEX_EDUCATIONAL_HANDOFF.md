# Educational and product research handoff

21 October 2026. Inspected main: `dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1`. Research only. No new feature, migration, account policy, deployment, payment, paid inference or protected-database operation is authorized by this document. Preserve the security and Review Mistakes order in the existing next-agent plan. This is a set of findings for small implementation decisions, not a replacement roadmap.

## What is established

The [bank assessment](CURRENT_BANK_ASSESSMENT.md) and [Vera reconciliation](VERA_45_QUESTION_AUDIT.md) contain the numerical evidence. The 2,000 milestone remains incomplete. 497 existing answer keys were independently checked; full editorial certification of all accessible content was not completed. Ten original foundations items remain unreviewed drafts, with a full-QA parser blocker. No release approval or activation occurred.

Product conclusions below come from source inspection and the isolated test/build checkpoint, not a deployed-site audit or observed learner study. No supplied Facebook performance screenshot is attached to this session; its actual three attempts, ratings and visual details cannot be assessed. No personal CSC ratings have been invented or entered.

## Existing feature inventory

Status describes the inspected implementation, not production availability. “Partial” identifies a concrete missing capability. Useful advanced features are candidates for testing and organization, not automatic deletion.

| Feature | Status and evidence | Placement and recommended action |
|---|---|---|
| Exam choice, Study Mock, Strict Mock, drills | Implemented; server `MockPoolSelector`, session actions and exam page | Core. Keep the choose-exam to practice journey; distinguish formative help from strict evaluation. |
| Authoritative submission | Implemented; `SubmitExamAttemptAction`, `ExamGradingService`; row/cache locks, server-owned pool, saved-answer expiry handling | Core integrity. Preserve; resolve score presentation disagreement below. |
| Saved exam sessions | Implemented; `ExamSession`, saved answers/version/owner-session hash; resume hook | Core. Test expiry, multi-tab saves and identity transitions before altering persistence. |
| Saved drill sets | Implemented separately from completed attempts | Useful secondary. Explain saved selection versus resumable session versus historical result. |
| Scorecards | Implemented; `scorecard-view.tsx`; explanations and category review | Core, but weighted score and “Passing Mark” language require correction planning. |
| History | Implemented; `ExamAttemptService`, history page, owner-filtered query | Core. Reuse it. Guest history and in-memory pagination need work. |
| Subject performance and graphs | Implemented; `AnalyticsService`, lazy `AnalyticsCharts`, existing Recharts `score-history-chart.tsx` | Useful secondary. Reuse graph; make comparison scope and sample counts explicit. |
| Readiness/percentile/pass prediction | Implemented calculations, educationally unsupported | Candidate for removal or replacement of claims, subject to founder decision; do not treat as validated measurements. |
| Targeted wrong-question practice | Existing wrong-ID selection and subject links | Core route for remediation. Historical key changes and ownership must be resolved. |
| Review Mistakes and spaced repetition | Partial: FSRS wrapper exists; durable cards/due-review UI remains in `REVIEW_MISTAKES_BRIEF.md` | Core educational priority in existing roadmap; do not create a competing queue. |
| Offline drills | Implemented packs, runner, queued sync, server re-grading, `OfflinePracticeResult` | Core low-bandwidth capability. Keys in offline packs remain excluded from secure mocks. |
| Response timing | Partial: server elapsed attempt time; client item timing is cumulative and not authoritative first-attempt evidence | Advanced learning signal. Label provenance and help/exposure status before interpretation. |
| First-exposure independent mastery | Partial: seen IDs derived from completed attempts, not every reveal/offline/abandoned exposure | Advanced, high educational value. Cannot currently certify “unseen” from this signal alone. |
| Study Hub and Study Plan | Existing routes and surfaces | Useful secondary. Link from weak-skill actions rather than add more first-screen choices. |
| Optional tutor/AI handoff | Existing external handoff and default `NullTutorProvider`; deterministic analysis also uses AI-related names | Experimental/park paid inference. Static explanations and truthful recommendations come first. |
| Actual CSC ratings journal | Not found in models/migrations inspected | Future optional capability; separate provenance from mock scores. No implementation authorized. |

No entire feature is declared broken solely because it is advanced. Concrete defects are scoring disagreement, fallback invented metrics, and incomplete history/exposure semantics. Full end-to-end usability testing remains outstanding.

## Performance report: confirmed problem and minimal approach

### Scoring disagreement

`ExamGradingService` derives raw percentage correct from the server-owned denominator, including skipped questions. `ExamAttemptFormatter::calculateWeightedPercentage` instead uses Verbal 30%, Numerical 30%, Analytical or Clerical 35%, GI 5%, normalizing present categories. `ExamAttemptResource`, history and analytics use this formatter. The scorecard also calls a client `calculateWeightedPercentage(results)` and marks 80 as “Passing Mark.”

Reproduced without a database: a Subprofessional result with Numerical 45/45, Verbal 0/45, Clerical 0/47 and GI 0/8 is **45/145 = 31.03448% raw**, but **30.00% weighted**. This is an implementation inconsistency, not evidence of a CSC formula. Preserve correct/total integers and format a common raw percentage at display boundaries; the existing server integer rounding alone is too coarse for two-decimal history displays.

The [official 2026 CSC announcement](https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_03_Conduct%20of%2009%20Aug%202026%20CSE-PPT_orig%20signed.pdf), sections F/G, establishes different level scopes and a general passing rating of 80.00. It does not publish the 30/30/35/5 formula or establish raw percentage equivalence to an official general rating. No official level-specific weighting formula was verified. Use “Civio mock percentage correct”; do not label 80% raw as an official pass. Recheck the announcement for the founder's selected sitting.

### Unsupported comparisons

- `AnalyticsService::calculatePercentileRank` returns **50** when system attempts are five or fewer, or the learner average is zero. Otherwise it compares against all system attempts, mixing users, levels, drills and repeat exposures. The CSE card renders a Top-percent claim. Neither fallback nor unbalanced attempt pool is a valid percentile norm.
- `DeterministicAnalysisService::calculatePassPrediction` scales mock average and adds/subtracts trend bonuses before capping the result. The estimated range is also heuristic. No calibration against actual CSC outcomes was found. Do not present these as pass probability or predictive confidence.
- Readiness caps tied to syllabus completion and subject thresholds are internal heuristics, not validated readiness. “x/5” completion can conflict with the four broad domains relevant to one level.
- `use-analytics-state.ts` contains demo fallback statistics (including an 84 average and 12 attempts). Some charts have a Sample Data overlay, but empty-account behavior needs a complete audit. Empty real histories should state “No completed attempts”; any demonstration must be explicitly isolated.
- Attempt breakdowns use zero for some absent subjects. Missing evidence must be null/not assessed, not an earned zero. History statistics computed before list filters can describe a different population than the visible attempts.

### Small report contract, extending existing history

| Requirement | Reuse | Necessary change and acceptance evidence |
|---|---|---|
| Persist every completed mock | `ExamSession` to `ExamAttempt`, authoritative submission action | Preserve idempotence, withdrawal/expiry behavior and server counts. Two concurrent submits create one result. Full mocks with skipped items retain the full denominator. Do not silently reinterpret incomplete drills as full mocks. |
| Overall, subjects, level, completion and time | Existing attempt metadata, category counts, duration and history rows | One server-derived raw-score contract across submission/resource/scorecard/history/analytics. Subject count and denominator visible. Show mode, actual item count and duration provenance. |
| Improvement graph | Existing lazy Recharts history graph and Lite tables | Filter level and comparable mode; plot dated attempts with counts. Percentage-point changes, not “percent improvement.” Avoid smooth interpolation implying unobserved scores. Missing subjects remain missing. |
| Actual CSC ratings | Separate future data model or explicitly isolated typed record after schema review | Self-reported, owner-private, exam date/level/source label. Optional general and subject ratings preserved exactly; never back-calculate raw correct counts or blend with mocks. Input range/precision follows verified CSC format. |
| Unseen versus repeated | Existing seen-ID helpers and response history | Add version/family-aware exposure evidence only after approval. Include reveals, study, offline and earlier abandoned sessions. Old unknown exposure stays unknown. Strict fresh sets exclude contaminated families. |
| Declining subject review | Existing subject/wrong-question links and forthcoming Review Mistakes | Show comparable observed subject changes with sample counts. Require repeated evidence for recommendations; a single decline is not a diagnosis. Route into existing targeted practice. |
| No invented prediction | Existing analytics/card components | Remove or withhold unsupported percentile/readiness/probability outputs; do not replace with another arbitrary score. Show descriptive accuracy, coverage and retention evidence. |
| Guest history and account privacy | Guest session ownership, pending guest claim, authenticated owner scopes | Current single `pending_guest_attempt_id` is replaced each time; login claims only that pending result. Design a bounded server-owned guest attempt list, then explicit claim/retention policy. Never attach arbitrary IDs. |
| Lite and offline | Existing text table, lazy chart boundary, offline result table | No chart dependency on exam route. Offline practice remains distinct from secure mocks; authoritative sync must not convert exposed-key practice into independent evidence. |
| Minimal implementation | Existing history and analytics components | No second dashboard. Actual-rating entry is a later optional slice; scoring correctness and Review Mistakes precede it. |

### Privacy and historical integrity

Authenticated history queries are owner-scoped; guest scorecard lookup checks the pending guest ID. These are controls to preserve, not evidence of a proven server leak. Shared-browser risk needs tests: `active_exam_session_v1`, `civio_guest_study_bias_v1` and the IndexedDB offline `queue` are not visibly account-namespaced. Verify logout, A-to-B login, claim, reload and offline reconnection. Scope or clear data according to owner/provenance; never discard unsynced work silently or claim another user's history.

`seenQuestionIdsByTrack` covers completed attempts, and `wrongQuestionIdsByTrack` can re-evaluate using current question keys. Future historical records need a server grading/version fingerprint and stable scored outcomes so a later approved correction does not silently change history. Do not rewrite historical results without an explicit correction policy and audit trail. Elapsed server time is authoritative within current session semantics; client per-item time and offline timestamps are observational, not tamper-proof measures.

## Navigation and lightweight interaction review

Keep the Focused Learning Canvas, warm off-white `#FAFAF7`, ink `#101426`, violet `#5B35F5`, and restrained existing lime `#B3F52D`. Preserve approved capitalization and microcopy. Tailwind 4, React 19, Radix/shadcn and existing CSS are sufficient.

`pages/public/welcome.tsx` still renders `ExamScreenPreview`, `ExamFormat` and MODES links. The existing `HOMEPAGE_CHOOSE_EXAM_2026.md` already proposes simplifying these. Dashboard start links, public header and sidebar also repeat ways to reach practice/history/analytics. This is a roadmap reconciliation issue, not a reason to implement another home page. Audit PRs 13-16 before touching the same surfaces.

Recommended primary journey: choose exam, start practice, answer, review, target weak skills, see history. Keep Study Hub, saved sets, offline downloads and deeper analytics accessible as secondary destinations. Test labels for “saved session,” “saved drill” and “history”; avoid three labels that appear to describe one action. Do not delete advanced features before the founder pilot.

Reuse existing button states and toasts. Improvements worth testing are immediate selected-answer feedback, stable-width save feedback, an inline error with retry, accessible disclosure of detailed explanations, and restrained progress updates. Use semantic buttons/links for clickable category tiles, visible keyboard focus, and text equivalents for charts. No success indication before a server success response. Do not announce an entire chart on every answer. Avoid animation of layout dimensions that shifts answer choices.

Existing CSS already has approximately 120 ms transitions and reduced-motion rules. `.civio-action` is 36 px high in one shared style while navigation is at least 44 px. Audit actual spacing and touch interactions; a 36 px target is not automatically a WCAG 2.2 AA failure (24 px minimum has exceptions). Prefer the project's larger mobile touch target where feasible, without blanket restyling. Keyboard operation and reduced motion need browser verification, not a claim based solely on CSS.

## Selective open-source references

Read-only repository snapshots were inspected; no library was installed in Civio and no component was copied into the application.

| Reference | Snapshot and activity | License/dependencies/accessibility | Verdict |
|---|---|---|---|
| [motion-primitives](https://github.com/ibelick/motion-primitives) | `120f64f6ca60348e251f929e9c81f11ccbe45eda`; last commit 28 Sep 2026 | MIT in `LICENCE.md`; inspected project uses React 18, Motion 11, Next 15, Tailwind 4. Accordion has a native button/aria-expanded, but no explicit reduced-motion branch or aria-controls in that sample. | Study restrained disclosure only. Existing Radix accordion is a better fit; do not add Motion for it. |
| [animate-ui](https://github.com/imskyleen/animate-ui) | `e6cea6b5ae5a4985d3bf3cc0ebea173555eafd72`; last commit 19 Oct 2026 | MIT **with Commons Clause**, not unrestricted MIT. React peer 19, Motion 14; optional underlying UI adapters. Inspected Base UI progress uses reduced-motion configuration and semantic primitive. | Reference behavior, not a new dependency. Check restrictions before reuse or redistribution; commercial app inclusion is distinct from selling the component library. |
| [velora-ui](https://github.com/ColorlibHQ/velora-ui) | `a07bcc129b45eeed3fc070357a6a74b876d96159`; last commit 30 Sep 2026 | MIT. Project uses Next 16, React 19.3, Motion 13; inspected stateful button itself uses React, cn and CSS, native semantics, pending guard, status announcement, reduced-motion class. | Most relevant small pattern: focus-preserving pending/success feedback with stable width. Adapt to existing button only if a real gap survives testing; preserve license notices if copied. |

Measured isolated minified/Brotli lower bounds: motion accordion 1,927/738 bytes; animate progress 7,162/2,525; Velora stateful button 3,094/1,149. React/Motion/UI package dependencies are excluded. These are **not** incremental Civio bundle costs, nor license/accessibility certification. Full pinned measurements are in [design-source-measurements.json](data/design-source-measurements.json). React version compatibility still requires a real integration build if future adoption is approved. Repository activity alone does not prove long-term maintenance.

## Performance constraints and testing plan

The isolated production build passed existing limits: entry 45.42/48 kB, vendor 119.21/122 kB, CSS 28.67/33 kB, exam chunk 10.94/11 kB, all JavaScript chunks **1,038,071/1,040,000 bytes Brotli**. Total remaining headroom is **1,929 bytes**; all-chunks size is not first-load transfer size. The exam chunk also has little room. Do not raise budgets to fit decoration. Remove unnecessary code or use existing CSS before adding dependencies.

Existing analytics chart lazy-loading and Lite tables should remain. Offline packs and service-worker behavior must retain answer-key separation and predictable sync. History currently fetches all user attempts and then paginates in memory; move pagination/aggregation into bounded queries in an approved performance slice when the growth case is tested.

No physical low-end phone or throttled browser was tested in this research. Proposed matrix: a representative 3-4 GB Android device, slow mobile network, cold and warm cache, Lite on/off, offline reconnect, long history, keyboard and reduced motion. The S23 Ultra is an additional device, not the baseline. Use laboratory CPU/network throttling to locate problems, then validate on physical hardware. Measure route transfer, requests, LCP, INP, CLS and memory before/after. [Core Web Vitals](https://web.dev/articles/vitals) good thresholds are LCP <=2.5 s, INP <=200 ms, CLS <=0.1 at the 75th percentile; lab results are not field percentiles. [W3C target sizing](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) and [motion guidance](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) support the interaction checks.

## Free, advanced and founder testing proposals

| Access proposal | Educationally appropriate content | Boundary |
|---|---|---|
| Free | Correct questions, verified grading, essential worked explanations, basic mocks/history, mobile access and Lite | Keep guest-unlimited and current free behavior. No inferior answer keys, misleading scores or withheld safety fixes. |
| Future advanced | Longitudinal diagnostic detail, curated challenge forms, planning convenience, expanded export/history and carefully qualified comparisons | Potential value is interpretation and saved effort. Requires demonstrated utility, adequate samples and founder approval; no pricing or billing decision here. |
| Founder private pilot | All approved testing tools, full private history, diagnostic and retention views, early feature flags where existing permissions support them | No public personal data, privileged answers during evaluation, artificial scores or contaminated holdouts. No new private application or flags implemented. |

Start founder testing with the [diagnostic and mathematics protocol](SUBPRO_MASTERY_AND_FORECAST.md). Select fresh independently reviewed forms, keep teaching and evaluation families separate, and record accuracy, method, help, time, retention and usability friction. Use a private existing account. Confirm privacy and ownership before collecting expanded learning history. Conduct a baseline, two weeks of focused study with weekly mixed fresh checks, and a delayed assessment; adjust duration to the founder's availability. This is a proposed pilot, not observed improvement. Keep a simple error diary distinguishing setup, computation, reading, convention and uncertainty. Ask the founder to find a saved session, review a mistake, resume offline practice and compare two comparable mocks without coaching. Fix failures before cosmetic additions or monetization.

## Prioritized, independently testable work packages

These are reviewable recommendations. Coordinate with the existing security roadmap and open PRs; do not treat this research directive as authorization to implement features.

| Priority | Confirmed problem and exact target | Proposed slice | Acceptance criteria |
|---|---|---|---|
| P0 existing gate | Security, owner checks, server scoring and signed bank approvals | Finish/confirm existing security tasks first | Existing ownership/key-withholding/expiry/idempotence and signature tests pass. No protected DB access. |
| P1 content integrity | Baseline #462 duplicate choices; numerical `CIVIO-NUM-WP-ALGEBRA-000025`; 83 flags in `main-audit.json` | Resolve stable identities and exclusions; independent editorial corrections in batches | Every flag has disposition, source/version, reviewer and decision; #462 cannot enter release unchanged. No silent historical/runtime ID conflation. |
| P1 scoring truth | Formatter/client weighted formula versus server raw counts | One raw-score contract in formatter/resource/scorecard/history/analytics; descriptive labels | 45/145 fixture displays 31.03% throughout; skipped items count; no division by zero; Pro/Sub and partial drills separated; no asserted CSC weights. |
| P1 truthful analytics | 50th-percentile fallback, pass prediction, demo/empty mixing | Withhold unsupported claims; null for missing evidence; match filter scope | Empty account shows no invented results; filters govern graph/stat denominator; no pass probability or unsupported readiness badge. |
| P1 existing Review Mistakes | Scheduler not yet a durable review workflow | Follow `REVIEW_MISTAKES_BRIEF.md`, reuse targeted links | Owner-isolated cards/queue; correct attempt/version linkage; helpful static explanations; Lite works. Do not create a second scheduler. |
| P2 bank reconciliation | 1,478 file labels, 550 baseline rows, 406 unmerged candidate IDs, unresolved versions | Reconcile manifests and signed approvals from authorized export, review PR conflicts | Exact eligible unique count with explicit exclusions; never derive runtime inventory from old docs. Maintain current 2,000 target proposal. |
| P2 QA extensibility | Ten new foundation structures fail/error under generator-specific QA | Separate structural validation from supported mathematical verifier contracts; unsupported must remain blocked | All ten independently reviewed; no parser crashes or hidden legacy bypass; false keys/equivalent options rejected; author check is not independent approval. |
| P2 coverage | Numerical foundations and transfer; analytical labels; Filipino depth | Map eligible items to 44-node blueprint, review existing drafts before writing more | All 45 Vera IDs retain disposition; prerequisite and unfamiliar-form floors; no count inflation or number-swapped filler. |
| P2 evidence and privacy | Incomplete exposure and single pending guest result | Small owner-safe guest history and version/exposure slices after Review Mistakes | Multi-mock guest history survives permitted flow; A/B account switch isolated; unknown old exposure stays unknown; revealed/offline items excluded from fresh evaluation. |
| P3 history refinement | Existing graphs need comparable scopes and honest trends | Extend existing graph/table and subject review links | Comparable level/mode/time labels, denominators, missing-data behavior, stable history and Lite parity; no second dashboard. |
| P3 polish | Existing approved homepage simplification and competing controls | Reconcile PRs 13-16 with current design brief, then small CSS/semantic fixes | No new motion dependency; keyboard/touch/reduced motion verified; existing size budgets hold. Founder can complete primary journey unaided. |
| Later optional | Manual official ratings, premium policy | Separate reviewed proposals after pilot | Self-reported official data isolated; no mock-to-CSC conversion; explicit approval before access/billing changes. |

## Validation, publication and decisions

407 Pest tests (3,960 assertions), 98 JavaScript tests, TypeScript, ESLint, build and size checks passed at the audit checkpoint. JS used the equivalent direct Node/tsx test runner because the npm wrapper could not create an IPC socket here. These tests validate existing code, not unimplemented recommendations, content approval, device performance or learning efficacy. No application source changes were made.

Decisions still required: independent reviewer and authorized signed-approval route for content; access to an approved non-sensitive inventory export if exact runtime reconciliation is desired; founder's exam sitting and study availability; future actual-rating retention and guest claim policy; eventual tiers only after testing. None is a reason to postpone the completed audit findings.

Publication is separately blocked: a normal GitHub push failed because this environment has no Git authentication. `AGENTS.md` requires normal `git push origin main` only, so the connected GitHub API was not used to bypass it. Research is locally committed and a recovery package is prepared; do not call it published until a remote commit is confirmed. An authenticated normal push or an explicit workflow exception is needed. No force push, merge, deployment, protected DB modification or content activation occurred.
