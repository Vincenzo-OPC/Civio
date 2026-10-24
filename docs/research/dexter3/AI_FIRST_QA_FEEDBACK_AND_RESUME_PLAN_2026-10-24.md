# Dexter 3.0: AI-first quality assurance, learner feedback and efficient Work resumption

**Research date:** 2026-10-24 (Asia/Manila)  
**Observed `main`:** `4fe22cde49cb4d14e768283a53f4e58e23267388`; recheck HEAD and open issues before implementation.  
**Status:** Research + design proposal only. No automatic bank signoff, content activation, owner-funded AI, runtime changes or deployment.  
**Related:** [Dexter roadmap #19](https://github.com/Vincenzo-OPC/Civio/issues/19), [content pipeline](BULK_EXECUTION.md), [bulk summary](bulk-summary.json), [tutor policy](../../DEXTER_TUTOR_POLICY_2026-10-21.md), [Issue #28](https://github.com/Vincenzo-OPC/Civio/issues/28), [Ask #29](https://github.com/Vincenzo-OPC/Civio/issues/29). This supplements `docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md` and `AGENTS.md`, not a new overarching roadmap.

## Decision and limitation

No dedicated human review staff is available. Prefer an **AI-assisted, risk-tiered, deterministic-first editorial process** and **real learner issue reporting** instead of inventing human review decisions. Keep these concepts separate:
1. **Canonical bank approval/import:** Still governed by `docs/BANK_IMPORT_APPROVAL.md`; GT signature and current author/reviewer separation cannot be silently waived. AI audit is not a human review or a signed approval.
2. **Optional tutoring sidecar quality:** Draft -> structural checks -> deterministic mathematical/source checks -> independent-context AI critique -> validated-for-defined-scope -> opt-in pilot *only if an explicit activation policy is approved*. No universal truth label, no direct activation.
3. **Runtime learner safety:** If a tutorial is uncertain, unsupported, stale or reported with verified contradictory evidence, **fall back to the existing checked Reveal**; do not change canonical exam grading, invent mastery, or let anyone access locked Strict answers.

Evidence for caution: Pardos/Bhandari's 2024 PLOS ONE controlled help study reported 32% of raw model-generated hints failing quality checks before self-consistency mitigation (https://doi.org/10.1371/journal.pone.0304013). Reddig et al. (2025) found 35% of model-generated tutor hints were too general, incorrect or disclosed an answer (https://doi.org/10.1007/s40593-025-00505-6). These are different research contexts, **not measured defect rates for Civio**, and demonstrate why a report button alone cannot be a certification gate.

## Critical new finding: report infrastructure already exists

Inspected current GitHub code:
- `resources/js/components/domain/report-issue-modal.tsx`: **existing "Report an Issue"** for Question and LearnModule; categories include incorrect answer, confusing explanation, AI hallucination, typo, layout and other.
- `app/Models/Feedback.php`, `app/Services/FeedbackService.php`, `app/Repositories/FeedbackRepository.php`, `database/migrations/2026_06_05_120000_create_feedbacks_table.php`: existing `feedbacks` rows with reporter, polymorphic item reference, reason/details/status.
- `resources/js/pages/admin/feedbacks/index.tsx`: existing Flagged Content Hub with pending/resolved/dismissed and item report counts.
- `app/Http/Requests/Admin/Feedback/StoreFeedbackRequest.php`: rejects multiple pending reports from same user/target; checks reason length, but currently accepts client-supplied integer ID and free-form `flaggable_type` without an explicit allowed morph list or existence/served-content authorization in that request.
- `FeedbackService::updateFeedbackStatus()` and repository `updateStatusForTarget()`: resolving **one** report updates **all pending reports on its question/target** to that status. This is too coarse for independently tracking a bad tutoring step vs a bad key vs a typo. Preserve existing behavior until a tested migration changes semantics.

**Recommendation: evolve this existing feedback workflow; do not add another feedback platform.** Audit the actual route/auth middleware and policy before any assertion about guest access. Current submit DTO assumes an authenticated `user()->id`.

### Minimal Study Mode learner interaction

Keep the existing report control. Under the optional Guide Me section, add a lightweight post-help question (not mandatory after every turn):
- "Did that explanation help?" **Yes** / **Still confused**.
- Secondary "Report a problem" (existing modal) categories: **Wrong answer**, **Explanation seems wrong**, **Unclear hint**, **This step gave away the answer**, **Tutoring path didn't fit my thinking**, **Wrong subject/outdated fact**, **Display/accessibility issue**. Maintain familiar global categories elsewhere.
- One optional text note: "What did you expect?" No screenshot required.
- Do not publicly display report counts, expose other reporters, collect full chats by default, or show diagnosis keys during active Strict.

A report should be **linked to the immutable tutoring artifact** (question stable ID, canonical/source hash, recipe ID + version/hash, exact current node/response ID, reason, safe server-owned graded attempt reference, assist/reveal state, client locale, timestamp). Question text/answer keys need not be copied into the feedback row; keep code/key/hidden branch server-only. Consent and retention rules for user notes, IP signals, and learner traces. Plan migrations as extensions of the existing model and admin dashboard.

### Triage / quarantine policy

- `untriaged` -> `automated_check_in_progress` -> `verified_defect` | `not_reproduced` | `needs_evidence` | `content_revision_pending` | `fixed_and_rechecked`. Existing feedback status names may be adapted through scoped fields or a separate investigation record rather than overloading question-level pending/resolved.
- Aggregate independent reports by **(artifact version, question ID, issue category)**, deduplicate reporters, throttle, and prioritize severity and verified contradictions rather than raw votes. A crowd cannot vote a correct answer into being wrong.
- Deterministic source/hash/key mismatch, arithmetic contradiction, key leakage or security violation can **auto-disable only the affected optional tutor sidecar / node** under a separately authorized runtime policy, reverting to checked Reveal; log change and offer rollback. Do not automatically edit/correct/withdraw a canonical approved question or alter signed bank manifests.
- Mere confusion or one learner flag -> investigation queue or extra diagnostic testing, not automatic question withdrawal. High-severity answer/key complaints trigger reproducible checks and surface to operator.
- Consider a simple admin triage report: affected questions, code/version, severity, distinct reporters, reproduction evidence, suspected family-wide impact, reviewer type (AI vs owner), decision and fix hash.
- Guard against spam/brigading, untrusted free-form prompt injection, arbitrary morph types and other-user attempt references, duplicate writes, strict answer leakage, false success toasts on redirect and unfounded auto-closure of all pending same-question reports.
- Existing `flaggable_type` MUST be whitelisted via an allowed morph type, resolved to actual authorized content; never trust raw client class names in a new tutor report. Anonymous/guest reporting requires a separate rate-limited scoped design if supported; do not silently bypass auth.

## New repository/tool research (verified 2026-10-24)

| Project | Evidence and role | Decision |
| --- | --- | --- |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | GitHub license MIT; local/CI prompt comparisons, JSON/assertion tests and optional rubric judge (https://github.com/promptfoo/promptfoo/blob/main/site/docs/configuration/expected-outputs/index.md). | **Best first OPTIONAL offline evaluation framework** after golden fixtures exist; no package in learner app and no paid provider by default. Existing Python validators remain primary. |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | Apache-2.0; Python multi-turn learner simulations with `ConversationalGolden` (https://github.com/confident-ai/deepeval/blob/main/docs/content/docs/evaluation-end-to-end-multi-turn.mdx). | Research/eval harness candidate for multi-turn pedagogical simulations; heavy and model-based metrics can incur cost; don't require it to run Civio. |
| [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | MIT; rigorous task/agent evals, turn limits, cost budgets, checkpoints. | Reference for reproducibility, trace disclosure, capped eval budgets; **not** a Civio runtime dependency. |
| [dubzzz/fast-check](https://github.com/dubzzz/fast-check) | MIT; property-based/state-machine testing in TypeScript (https://github.com/dubzzz/fast-check/blob/main/examples/README.md). | Optional **dev-only** tests for tutor state machine, shuffling and reveal locks. Native JS/Pest deterministic fixtures may suffice at first. |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | Property-based Python test library. GitHub's license field was NOASSERTION; inspect `LICENSE.txt` before copying code. | Research-time arithmetic/metamorphic fuzzing; prefer existing `fractions.Fraction` first; optional offline dependency. |
| [comet-ml/opik](https://github.com/comet-ml/opik) | Apache-2.0; large self-hosted tracing/evaluation platform. | **Defer**. Existing feedback admin + compact JSON reports are lighter, cheaper and fit repo. |
| Existing [OATutor](https://github.com/CAHLR/OATutor), [ai-tutor](https://github.com/NavyashreeNS/ai-tutor), [Oppia](https://github.com/oppia/oppia), [pyBKT](https://github.com/CAHLR/pyBKT) | Step hints, misconception hypothesis/abstention, branching, offline skill model fitting; licenses documented in `reference-evidence.json`. | Reuse *ideas*, not full apps or model-derived mastery penalties. |

**Selection:** do **not** install all these libraries. Start with 100% offline zero-network Python/Pest/JS tests and golden conversations. If the manual test suite becomes unwieldy, evaluate promptfoo **offline** on saved model outputs with deterministic assertions. Add DeepEval only if true conversation simulation needs it. Avoid paid judges in CI or production. GPL/AGPL and unclear lesson/data licenses need extra scrutiny.

## Offline quality gate and golden conversation tests

A robust test requires multiple **independent kinds of evidence**, not several prompts asking one model "is this good?".

1. **Exact verification (where applicable):** fraction/rational maths, multiple solution approaches, only one keyed option, base/units/inverse forward checks, known policy/primary-source evidence, source hash, option-index translation, approval label.
2. **Graph validation:** finite, acyclic, bounded guided paths; every wrong/unknown route reaches an appropriate hint/fallback; branch never assumes reason from final MCQ choice alone; no answer leaking before authorization.
3. **Pedagogical golden interactions** (different synthetic personas per lesson and method): understands math but misreads "original"; misreads final target; correct answer by guessing; mistakes percent numeral for pesos; misuses second discount base; correct intermediate but stops early; confuses after-markup inverse; uncertain/other reasoning; requests Reveal/stop; after-help performance incorrectly treated as independent. Add simple clerical ambiguity and Taglish comprehension tests.
4. **Metamorphic/property tests:** correct original→markup→reverse recovers original; changed percentage base not silently reused; units conserved; shuffling choices changes display IDs but not stored meaning; fresh-family assessment cannot select same stem-family; stale artifact hash fails closed; unknown taxonomy abstains; Strict always 423 and no key payload; assistance events never raise independent mastery.
5. **Separate fresh-context AI critic:** for a *sample* of representative clean cases + **all semantic exceptions and high-risk cases**. Give explicit rubric, original item and source evidence; ask it to produce counterexamples/alternatives rather than "approve". Store model label/date/context disclosure/critic output with source hashes. Disagreement -> exception queue, not majority-vote truth. Different model/reasoning effort where accessible, but do not claim different agents are independent humans.
6. **No human proxy fiction:** content may be described as "deterministically checked for X", "AI cross-checked for Y", "learner-trialled for Z". Do not mark as "human approved" or claim comprehensive educational validation.

For General Information/legal current facts, automated source retrieval and effective dates are mandatory before any trust claim; an AI summary without official source proof remains excluded from high-confidence release. For spelling, dictionaries are screening tools not complete language-variety policy (see existing `yield`/`yeld` issue).

## Efficient Work usage: resume, do not restart

**The October 23 snapshot is farther along than the pilot:**
- All **2,100** manifest records are in `bulk-state.json.gz`; **73** queue groups from 70 archetype labels. NOT 73 semantic families.
- 1,377 `approved`, 685 `draft`, 38 `reviewed` labels; **0** optional tutor runtime approvals.
- Existing deterministic answer screens audited **400 numerical source records**, including approved/draft/reviewed; **133** clerical spelling records lexically screened. No independent editorial approval follows from these screens.
- **257 approved numerical-source tutoring drafts** are covered by the original 40 + 217 incremental drafts. Some are shallow/repetitive scaffolds and no full-target transfer is validated.
- Bulk summary: **2,013** family drafts needing binding review, **362** records across 11 semantic-split groups, **1,565** with unrecognized taxonomy-code mappings, **15** price drafts with a separate AI review, **0** approved sidecars.

**Next Work session startup contract:**
1. Read `AGENTS.md`, `docs/research/dexter3/BULK_EXECUTION.md`, `bulk-summary.json`, this memo, and current issues. Inspect HEAD and artifact digests, don't load all 2,100 full stems in the prompt.
2. Run `python3 docs/research/dexter3/bulk_pipeline.py --write` and `python3 docs/research/dexter3/validate_bulk.py` **from a correctly installed local checkout, if available**; if Work only has GitHub access, inspect the committed artifacts and don't claim running commands. Read the existing resume state and process only `needs_` queue entries; never reset `bulk-state.json.gz` or overwrite `pilot-v0.1`/`price15` review snapshots.
3. **First finish high-return semantic splits** in the 11 mixed groups (362 records), based on solution operation/unknown/stage, not category name alone; include count of distinct methods and exception examples. This is more valuable than rewriting 2,100 prompts.
4. Next prioritize **approved** bank items by risk: wrong-unit/wrong-base/code mismatch, unsupported prereq, source ambiguity, duplicate stem families, no approved transfer, frequently exposed or later user-reported. Treat 723 nonapproved separately as editorial research, never runtime candidates.
5. **Batch one genuine method family at a time** (roughly 25–100 source bindings/checks per durable checkpoint depending on complexity), with deterministic verifier across the full batch. Author one versioned recipe per truly shared method; bind stable IDs and hashes; preserve exact source/option identity. Avoid the pattern of tiny 3–5-item microcommits and repeated full-manifest model reading.
6. For straightforward checked templates, use user's Work Luna/Medium configuration **if available** for draft writing. Use higher reasoning effort or a separate model/context ONLY for exceptions, contradictory results, new methods, spelling ambiguity and source-law cases. No claim that a ChatGPT plan can fund a Civio runtime API. Work usage remains finite and the user must explicitly start a future Work session.
7. Record structured exceptions with `reason_code`, severity, stable IDs, source/recipe digests, failing assertion, evidence URL or numerical counterexample, decision, recheck target; derive one sortable `review-queue.json` rather than many prose reports.
8. **Checkpoint meaningful work**: append/update a machine-readable per-batch ledger, concise human-readable summary, validation receipts and Git commit. Commit after each cohesive method batch, not individual items, and retain a resumable cursor so usage exhaustion loses at most the current uncommitted batch. Recheck HEAD to avoid concurrent workers overwriting each other.
9. Before usage ends, final checkpoint should state processed audited vs enriched vs AI-reviewed vs runtime eligible **separately**, remaining counts by queue reason, issue blockers and exact next cursor. Do not claim "the 2,100 are done" because the queue has entries.
10. Suggested quality metrics (targets **proposals**, not measured): 100% source/hash integrity for each released binding; 100% exact-key verification for deterministically supported math; zero known path key leaks; zero unreviewed canonical question approvals; count missed/false tutor diagnoses on held-out golden scenarios; report unknown cause rather than guess; no silently auto-released unverified high-risk content.

### Next Work session: short copyable starter

> Continue Civio Dexter 3.0 from the current GitHub HEAD, not from original 4934bc2. Read AGENTS.md, docs/research/dexter3/BULK_EXECUTION.md, bulk-summary.json, this AI_FIRST_QA_FEEDBACK_AND_RESUME_PLAN_2026-10-24.md and existing backlog. Preserve all 2,100 ledger entries, 400 numerical audits, 133 spelling screens, original 60 pilot, price v0.3 patch and 257 approved numerical-source tutoring drafts; do not regenerate them. First classify and split 11 mixed work groups (362 items) using actual solution method and sought quantity. Process method families in resumable 25–100 binding/check groups with exact validators, exception queue, draft tutoring flow, and separate fresh-context AI critique for ambiguous/high-risk cases. Never fill human-review decisions, sign bank approvals, activate runtime tutor, incur Civio model charges, deploy, or alter canonically approved questions. Give concise per-batch commits, progress totals and a strict next cursor. After semantic splits, improve evidence-based misconception mappings and extend non-numerical coverage without assuming a report button can validate content.

## Codex work order (NOT yet authorized by this research document)

P0. Solve Issue #28 durable answer saving, then #29 external Ask Socratic prompt and no-key regressions.  
P1. Audit/harden existing `ReportIssueModal` + feedback validation/triage: controlled morph types, served item/account authorization, safe issue context/version references, duplicate/abuse controls, no untrusted URLs or key leak; preserve existing feedback reports with compatible migration.  
P1. Add light Guide Me report/Still Confused UI only when an authorized Study-only pilot exists; do not automatically ask a rating on each turn.  
P2. Implement optional tutor-sidecar fail-closed checks and rollback/quarantine separate from canonical bank status. Security gate first: server-owned graded attempt, state transitions and 423 Strict lock.  
P3. Evaluate real held-out independent transfer vs ordinary Reveal with consent and sufficient sample sizes before broad rollout.

## Safety and performance

- Owner-funded inference spend remains **₱0**. No production LLM inference key, no live model judge in CI or user-facing path by default.
- No standalone survey platform, second tutoring engine, new assessment format, heavyweight frontend visualization, third-party SaaS, full history export or model-generated unreviewed canonical answer. Keep low-data 360px/Lite and existing JS size budgets.
- Keep clear user-facing wording "Reported", "Under Review", "Updated" only when verified; an issue report is not itself proof of error, and "No reports" is not proof of correctness.
- Respect user privacy, history ownership, minimal telemetry and retention; avoid full chat transcripts unless specifically opted in. Provenance must survive source edits and cache invalidation.

**No production behavior was changed in this research checkpoint.**
