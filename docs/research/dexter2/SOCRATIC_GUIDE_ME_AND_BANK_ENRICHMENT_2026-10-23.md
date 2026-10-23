# Dexter: Socratic Guide Me, question-bank enrichment and external Ask handoff

**Date:** 2026-10-23 (Asia/Manila)  
**Status:** Owner-requested research and execution handoff. **Not an implemented feature or approval to activate anything.**  
**Repository baseline checked:** `main` at `7dd6f21e4bdd3d7b591d53d1d343ea575b4bbe66` (2026-10-23 12:22 PHT). Recheck main before execution.  
**Parents:** [Dexter #17](https://github.com/Vincenzo-OPC/Civio/issues/17), [Dexter roadmap #19](https://github.com/Vincenzo-OPC/Civio/issues/19), [metadata review #22](https://github.com/Vincenzo-OPC/Civio/issues/22), [Rescue #23](https://github.com/Vincenzo-OPC/Civio/issues/23). **Priority blocker:** [answer persistence #28](https://github.com/Vincenzo-OPC/Civio/issues/28).  
**Canonical execution order:** `docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md`; this memo supplements it and does not create a competing roadmap.

## Owner's observed learning failure

Given: "A store marks up an item's price by 25%, then gives a 20% discount. The **original price** is ₱640." The learner correctly knows 25% of 640 = 160, but initially interprets ₱640 as the price **after** the markup. This is an interpretation/base-identification error, not proof of a percentage arithmetic deficit.

- Forward problem: original ₱640 → ×1.25 = ₱800 → ×0.80 = **₱640**.
- Reverse *different* problem: ₱640 **after** 25% markup → ÷1.25 = **₱512**, **not** ₱640 minus 25% of ₱640.
- Good tutoring asks first: "**Does ₱640 describe the original price, or an already marked-up price?**" It branches on the response and asks one short next question. Showing only `640 × 1.25 × 0.80` misses the learner's actual reasoning gap.
- A wrong MCQ choice alone may not prove the misconception. Confirm by one diagnostic response; abstain where unsupported.

**Product direction:** in existing **Study Mode**, add an optional **Guide Me** interaction *alongside* Show Explanation/Reveal and Expound, not as another exam mode and not as a replacement for full explanations. Keep MCQs as Civio's sole assessment format. A short, multiple-choice diagnostic inside an explanation is scaffolding, not a new graded exam type. Direct Reveal remains available when authorized. Strict Mock remains sealed until authorized submission.

## Verified existing foundation and gaps

Source: current code, `docs/ENGINES.md`, `docs/FEATURE_CATALOG.md`, 2026-10-22 audit, and `docs/research/dexter2/INTELLIGENCE_REVIEW_2026-10-23.md`.

| Capability | Found in repository | Do not conflate with |
| --- | --- | --- |
| Checked explanations | `app/Services/Exam/Reveal/RevealTutor.php` and existing solvers; progressive concept/steps/shortcuts | An interactive conversation or proof every explanation is correct |
| Misconception taxonomy | `config/dexter_misconceptions.php`; `MisconceptionDiagnoser.php` | Human-validated coverage of every distractor |
| Prerequisite graph | `SkillGraph`, `config/dexter_skill_graph.php`; 14 coarse nodes in audit | Fully granular math concepts |
| Rescue proof-of-concept | `RescueService.php`, `config/dexter_rescue.php`; disabled; `validated_question_ids=[]` | A shipped Guide Me interface |
| Memory and review | First-answer evidence, internal BKT ranking, Review Mistakes and FSRS scheduling | Calibrated mastery, production verification, or pass prediction |
| External AI handoff | `resources/js/lib/ai-handoff.ts`; `ask-assistant-button.tsx` | Stateful tutoring; currently short generic hint/explain suffixes |

**Critical gates inherited, not waived:**

1. #28 has reproduced a failed dynamic-import recovery path where selected answers were locally retained but did not reach the server until reload. Correct this before new interactive question UI.
2. The 2026-10-23 intelligence review identifies mismatched "independent accuracy" denominators, truncated first-exposure windows, and a generic false `0.85` validator confidence. Fix these before using progress/misconception claims as learner-facing intelligence.
3. The Rescue endpoint must authorize **server-recorded, graded Study attempts**, rather than trust a caller-supplied question/choice. Preserve 423 on an active Strict session; do not expose answer-derived codes, methods or keys before authorized Reveal.
4. Fresh transfer must be a different **approved, independently unexposed stem family**, not only a different question ID or identical wording with new numbers; report if there is no eligible item.

## Existing open-source research, assessed for borrowing patterns

| Repo | Relevant pattern | Recommendation / limits |
| --- | --- | --- |
| [CAHLR/OATutor](https://github.com/CAHLR/OATutor) | Authored problem → steps → hints, skill-linked guidance | **Primary learning-step pattern.** MIT code, do not copy its CC BY lesson content; do not import its Firebase stack. |
| [NavyashreeNS/ai-tutor](https://github.com/NavyashreeNS/ai-tutor) | Socratic turn loop, dependency graph, misconception hypothesis with abstention | **Primary dialogue/orchestration reference.** Small proof of concept, MIT. Do not copy uncalibrated BKT confidence/penalty logic blindly. |
| [oppia/oppia](https://github.com/oppia/oppia) | Branching learner responses and specific misconception feedback | **Primary branching-authoring reference.** Apache-2.0, full framework too heavy for Civio. |
| [Galliard7/OpenMath](https://github.com/Galliard7/OpenMath) | Offline/precomputed math instruction and separated runtime tutoring | **Workflow reference only.** License not established in this audit: don't copy code/content until reviewed. |
| [CAHLR/pyBKT](https://github.com/CAHLR/pyBKT) | Offline skill-specific fitting | Later evaluation option, not a new runtime dependency; require evidence sufficient to fit/calibrate. |

**Decision:** borrow patterns and author Civio-specific deterministic metadata. Do not copy a complete foreign app, its questions, its UI brand, or its model training assumptions.

## Bank-enrichment policy: audit 2,100, never re-generate 2,100 by default

A reproducible 2026-10-22 manifest audit recorded **2,100 candidate records**: 1,377 marked approved, 685 draft, 38 reviewed (723 not approved). Among the 1,377 approved, 344 had structurally Rescue-ready key, rationale, taxonomy code and graph archetype. This **does not** establish that 344 diagnoses passed independent human validation, that 2,100 are active, or that the current production DB has these counts.

The existing [60-item metadata pilot](pilot/README.md) has 20 each of `NUM-WP-PCT-CHANGE`, `NUM-WP-RATIO`, `CLR-SPELL-WRONG`, totaling 180 wrong-option reviewer rows; no human decisions were recorded at audit. The first pilot should reuse this packet rather than silently claiming it has been reviewed.

**Three enrichment levels:**

1. **Concept recipes (once per concept):** interpretation cue, underlying meaning, prerequisite, checked method, optional visual, graduated hint ladder, reverse/contrast case, fast exam method. Pilot: percent base, markup/discount, reverse percent, fraction meaning/equivalence, ratio setup, algebra word translation. Do not claim a new prerequisite exists when there are no approved questions to assess it: `NUM-PCT-BASIC` had zero approved graph-tagged items in the audit.
2. **Distractor/misconception bindings (per answer choice where evidence supports it):** reuse `why_wrong`, `distractor_reasoning`, approved key and stable option IDs. Normalize to stored index before any client shuffling. Classify only known, reviewed errors; absence means "cause unknown."
3. **Question-specific prompts (only where necessary):** an authored initial diagnostic, one-step replies/hints, and a **separate approved** fresh transfer family. Avoid giant per-question conversations for template families where a reusable concept recipe suffices.

**Recommended versioned sidecar, separate from signed canonical bank** (illustrative schema, not permission to import):

```json
{
  "schema_version": "dexter-guide-v0.1",
  "question_id": "existing-stable-id",
  "source_question_hash": "recompute-on-source-change",
  "concept_id": "NUM-WP-PCT-CHANGE",
  "prerequisite_concept_ids": ["NUM-PCT-BASIC"],
  "recipe_id": "percentage-forward-vs-reverse",
  "initial_diagnostic": {
    "stem": "Does ₱640 mean the original price or the price after markup?",
    "options": ["Original price", "Already marked-up price", "Not sure"],
    "branches": {
      "0": "Correct; 25% has not yet been added.",
      "1": "Read original price: the 25% increase has not happened yet.",
      "2": "Original price names the starting value before any markup."
    }
  },
  "hint_ids": ["identify-starting-base", "fraction-or-decimal-method"],
  "candidate_misconception_codes": ["REVIEWED_CODE_ONLY"],
  "transfer_question_id": null,
  "validation": {"automated": "pending", "human": "pending"},
  "status": "draft"
}
```

Separate authoring metadata from learner response/session data and canonical keys. No client receives `branches` containing locked solutions or tutor validation data before the authorized stage. Authoring may use stable option IDs; UI and server must distinguish display indices from stored indices.

## ChatGPT Work versus Codex

- **ChatGPT Work (user-launched, Luna/other available configuration):** inventory and deduplicate candidate metadata; produce reusable concept recipes and draft per-item diagnostic bindings; run checkable mathematical/source validations; emit versioned sidecars and issue-linked review packets. Work output is **draft**, not automatically accepted. No repeated bulk pass if hash/recipe/field unchanged. Chunk and checkpoint data by stable IDs.
- **Independent reviewer, with a different pass and human adjudication:** verify correctness, especially law/GI, option indexing and pedagogy, before signing/approving bank changes. A model cannot mark its own drafts as human-reviewed or sign owner approvals.
- **Codex, after #28 and existing gated work:** implement the minimal Laravel state machine, authorization, React UI and tests; reuse `RevealTutor`, `RescueService`, `ExposureHistory`, `SkillGraph`, `MisconceptionDiagnoser`, and existing FSRS. No new heavy packages, parallel intelligence engines, unapproved learner modes, in-app model bill, deploy or question activation.

### Work instruction, first bounded deliverable

"Read AGENTS.md, this memo, the Dexter audit and the existing pilot. Reconcile current question counts. Audit the 60-item packet and source records, prioritizing interpretation versus arithmetic misconceptions. Produce a **draft-only**, versioned concept recipe and metadata-enrichment packet with stable IDs, old/new field comparisons, reason codes, math-checked explanations, distinct-stem transfer candidates, an exception queue and an independently reviewable evidence sheet. Do not approve, sign, rewrite or import canonical bank data. Do not deploy or call owner-funded Civio AI APIs. Report exact coverage and missing prerequisites. Only after independent validation should we consider batched enrichment of remaining **eligible** items."

## Ask ChatGPT: quickest safe product improvement, after #28 readiness check

The current handoff in `resources/js/lib/ai-handoff.ts` sends:
- Pre-Reveal: "Do not reveal the correct answer yet. Give me one useful hint and help me reason it out."
- Post-Reveal: "Please explain this simply, tell me what to remember for the CSE, and give me one similar question."

Replace **closing text only** in a scoped, tested engineering slice, keeping the existing structured question/attempt fields and `canIncludeAnswer` safety gate. Never pass hidden keys, full history, personal information, grader internals or misconception metadata before authorization. Any opt-in learner notes are clearly optional. Do not claim an external assistant enforces answer secrecy merely because a prompt requests it; Civio itself must not disclose keys. A remote model may independently solve the public question.

**Suggested pre-Reveal handoff** (request one interaction, no answer):

> Act as a patient Philippine CSE tutor. Don't give the final answer. First check if I understood what the given values and wording mean: which value is original, before/after, total, remaining, or unknown? Ask **one** diagnostic question at a time and wait. If my reasoning reveals an error, name the specific *possible* misunderstanding, confirm it rather than guessing, and offer one small hint. Prefer clear natural English or Taglish. Do not invent my prior learning history or an official CSC rule.

**Suggested post-Reveal handoff** (authorized key/explanation may be included):

> Act as a conversational Philippine CSE tutor, not an answer dispenser. Use the checked Civio explanation as reference and flag any apparent inconsistency instead of silently accepting it. First ask how I interpreted the question; ask **one question and wait**. Distinguish reading/word-problem setup, wrong percentage base, incorrect operation, and arithmetic slips. Explain the actual misconception only when supported; use brief progressive hints and a short worked method when needed. Then give a **new, differently framed** practice question for me to answer unaided; do not count a hinted success as mastery. Suggest the exam shortcut only after I understand the underlying method. Natural English/Taglish, no long lecture.

**Implementation files:** `resources/js/lib/ai-handoff.ts`; `resources/js/pages/user/exams/components/ask-assistant-button.tsx`; `tests/Js/ai-handoff.test.ts`; `docs/EXTERNAL_AI_HANDOFF.md`. Keep `?q=` safe URL length behavior: full prompt in clipboard for long payload, never silently drop tutoring constraints or source metadata. Preserve click-to-copy fallback. Existing external Ask is disabled within active Strict Mock; verify direct requests and resume edge cases.

**Additional optional improvement:** an opt-in learner note in Study/Review ("I thought ₱640 already included the markup") is more useful diagnostic context than blindly sending complete study history. Treat user text as untrusted content, not instruction override.

## Proposed Guide Me backend contract and state machine

`INTERPRET → DIAGNOSE (if evidence) → HINT_1 → HINT_2 → EXPLAIN (only when allowed) → FRESH_TRANSFER → REVIEW_SCHEDULED`; optional Skip/Reveal exits. Follow existing `docs/DEXTER_TUTOR_POLICY_2026-10-21.md` and the parent Rescue issue. This is an **authorized per-attempt server state machine**, not a generic client-directed solution endpoint.

Acceptance checks:
- Active Strict cannot access any hint/diagnosis/key/reveal, by route, prefetched payload, resume, offline pack or export.
- Request binds to authenticated/guest-owned **served and graded** attempt; cannot choose arbitrary question/choice to obtain answers.
- Display shuffle is correctly translated to stored option IDs; no codes applied to correct answer.
- Missing/ambiguous/unvalidated metadata falls back to normal checked Reveal rather than invented diagnosis.
- One-step branch responds differently to at least two plausible learner interpretations.
- Authentic independent unseen family is scored separately from assisted, repeated or revealed answers; BKT/analytics do not inflate from hints/blank/repeats.
- Empty prerequisite or fresh question pools produce truthful fallback.
- Numeric checks include `640×1.25×0.80=640` and reverse `640÷1.25=512`, plus unit and rounding edge cases.
- 360px and Lite/low-end tests, keyboard focus/accessible announcements, existing exam chunk and total size budgets, error/reconnect behavior, idempotency and no paid network calls.
- Pilot content is adjudicated by distinct human reviewers; existing 180 rows cannot be auto-approved by the content-generating agent.

## Decision gates and priority

1. **P0:** resolve #28 and revalidate safe answer persistence; do not let Guide Me accept unsaved answers.
2. **P1, narrow isolated improvement:** Ask ChatGPT tutor handoff copy/tests, without exposing new key paths. This may be delivered earlier than the full Rescue UI once the relevant safety checks pass.
3. **P1 editorial:** Work inventories bank, reuses 60-item pilot; produce reviewed math/reading misconception recipe exemplars. Preserve 2,100 target/statuses and signed approval process.
4. **P2:** correct independent-learning evidence and false validator confidence; secure Rescue attempt authorization.
5. **P2:** pilot one Guide Me percentage interpretation/reverse path on reviewed, approved items in Study only, behind existing gate; owner approves activation separately.
6. **P3:** evaluate independent unseen transfer and delayed recall against plain Reveal baseline; scale across eligible approved bank only on demonstrated improvement and adequate source coverage.

**Nothing in this memo is proof the first-party Socratic tutor has been coded, tested or deployed.** No runtime code, approved bank status, user history, AI spend flags or deploy settings are changed by this documentation-only commit.
