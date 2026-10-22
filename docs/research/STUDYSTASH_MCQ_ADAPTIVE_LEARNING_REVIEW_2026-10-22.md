# StudyStash research -> Civio adaptive MCQ learning (22 October 2026)

**Status:** GT-approved PRODUCT DIRECTION / competitive research brief, **NOT implementation evidence**. Owner: GT. Primary actors: Astra (architecture review), Grok Bot (research and independent QA), Codex/Grok Build (engineering only when separately started). Related: [Dexter master plan](../DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md), [tutor policy](../DEXTER_TUTOR_POLICY_2026-10-21.md), [feature catalog](../FEATURE_CATALOG.md), [current execution plan](../CIVIO_NEXT_AGENT_EXECUTION_PLAN.md), [issue #17](https://github.com/Vincenzo-OPC/Civio/issues/17).

## User decision, October 22: MCQ-FIRST, NOT STUDYSTASH CLONE

GT reviewed Instagram [@studystash_app](https://www.instagram.com/studystash_app/) and StudyStash and directed Civio to **stay focused on multiple-choice question (MCQ) practice**. Do **not** expand the roadmap into flashcards, podcasts, matching games, drag-and-drop question types or standalone gamified exercises. Those StudyStash features are not requirements. Preserve existing small diagrams, checked worked solutions, hints, and optional accessibility support **inside the MCQ learning flow**; a diagram used to explain a fraction is not a new exam format.

Civio is an original, source-reviewed Philippine Civil Service Exam reviewer (Subprofessional first for GT, Professional supported), **not affiliated with CSC**. Prioritize mastering *new* MCQs through understanding, delayed recall, and honest exam simulation rather than copying StudyStash's aesthetics or importing its materials.

## What is actually verified about the competitor

- StudyStash describes an instructor-material-grounded adaptive system with AI StudyChat, personalized study support, practice tests, flashcards, and instructor/learner insights: https://studystash.com/en-us
- Its October 2, 2026 announcement says StudyStash was acquired by Kortext: https://studystash.com/en-gb/about/news/studystash-joins-kortext
- The company's Birmingham pilot percentages are self-reported for performance/confidence; they **do not** establish an independently measured causal gain for Civio, CSE readiness, or AI effectiveness. Do not reuse marketing claims as scientific performance evidence.
- No access to StudyStash's source code, model, private LMS, user data, or internal adaptation logic is claimed. Treat its marketed approaches as **product inspiration**, not reverse-engineered algorithms.

## Civio status (read latest source before repeating)

From [FEATURE_CATALOG.md](../FEATURE_CATALOG.md), checked October 22, 2026:
- Already implemented: MCQ drills, Study Mode, Strict Mock/Exam Mode, checked explanations for applicable items, server grading and exam history; Review Mistakes marked verified.
- Smart Review/FSRS has server review cards/events and due items implemented **online**, **not yet production verified/deployed**; offline reconciliation remains unbuilt. Do not start a duplicate FSRS subsystem.
- Existing smart weakness practice is **partial**, not concept-level mastery. Dexter is currently a key-check/explanation helper, **not** an interactive personal tutor. Performance breakdowns are historical, not an established pass predictor.
- Question-bank audit reported 2,100 mechanically checked unique candidates, 1,377 GT-approved and 723 still pending review on October 22. **Candidate count does not mean active or fully approved.** Do not approve/import/activate them based on this brief; use current bank ledger for exact figures.

## Adopt: a single MCQ learning loop

1. **DIAGNOSE:** show an approved, unseen or scheduled MCQ without the key. Record track, concept, question family, novelty, independent/assisted answer, difficulty if reviewed, and server-graded result. Avoid question-key payload leakage. Ask learner confidence only if useful and optional.
2. **EXPLAIN:** for Study Mode, show canonical checked rationale, why the right choice fits and why each wrong distractor fails, plus concise concept-specific methods. An optional Socratic Dexter offers one hint at a time and asks how the learner reasoned; no unsupported confident diagnosis. Strict Mock stays sealed until authorized submit.
3. **TRANSFER:** choose a *different approved MCQ* testing the same concept/prerequisite with altered framing, not an exact-repeat clone or AI draft silently promoted to the bank. Record truly independent outcome separately from hinted/revealed performance.
4. **REMEMBER:** feed valid server-owned practice events into the existing versioned FSRS queue. Assisted correct responses cannot prove recall. Due items may reuse the same MCQ for retrieval, but that result is not independent *new-item* transfer evidence.
5. **ADAPT:** select the next MCQ using documented rules that balance weak prerequisites, due reviews, novelty/family separation, exam blueprint coverage, accessibility, difficulty and user choice. Explain *why this question* with a server-grounded reason. Keep clean held-out mock pools unaffected.
6. **MEASURE:** show observed independent accuracy, sample size, unseen-item performance, overdue reviews, and improvement over time. Assess delayed retention and fresh held-out mocks. Do not invent mastery percentages, pass odds, fake AI diagnoses, official CSC time targets or performance claims based on raw speed.

All question interactions stay MCQ. At most, small **optional explanatory visuals** can live *within* Reveal/Teach. Avoid new frontend dependencies and rich animated interactions on low-end phones.

## Priority and non-goals

**P0:** preserve exam/security integrity, signed bank approval gate, clean 2,100 candidate audit, existing Study/Strict protections, user-data isolation and real score wording. **P1:** verify and harden existing Review Mistakes + online FSRS, including operational scheduler failure states; do not duplicate completed slices. **P2:** build distractor/concept mapping and a transparent selector for fresh MCQs plus prerequisite-specific explanation quality (begin Subprofessional fractions, percentage, word problems, spelling and filing). **P3:** optional Dexter interactions anchored in checked rationales and fresh approved MCQs, external AI handoff first, bounded/consented in-app AI only after evaluations. **P4:** offline FSRS reconciliation and descriptive dashboard improvements as tested slices.

**Explicitly OUT OF SCOPE:** flashcard generator, podcast mode, image-identification game, matching, drag-and-drop question format, leaderboard/XP redesign, microtransactions, automatic AI question approval, magic 100% readiness meters, StudyStash branding or visual copying, new subscriptions, unapproved paid API calls, or deployment.

## Grok Bot: bounded research/QA handoff (not engineering authorization)

Grok Bot is the independent research/quality agent, not an automatic recipient of this file. On its **next user-launched session**, read AGENTS.md, this brief, docs/FEATURE_CATALOG.md and Issue #17, then:

1. Verify publicly accessible StudyStash feature descriptions and gather date/URL/source provenance for any extra adaptive-MCQ evidence. Separate vendor marketing from product behavior; note inaccessible pages and uncertainties. Do not pretend to have interacted with a login-only UI.
2. Audit Civio's actual current quiz-selection, distractor explanations, concept metadata, current FSRS, Review Mistakes, and dashboard to identify precise **missing** behavior; differentiate implemented/partial/planned and cite code/test paths, without proposing duplicate services.
3. Produce one short evidence-backed competitor-to-Civio gap matrix, 3-5 ranked MCQ-only candidate improvements, expected educational value, smallest safe first slice, and how to test novelty, question-key secrecy, independent vs assisted learning, source truthfulness, accessibility and slow Android/Lite.
4. Commit findings as a **new dated research dossier** in docs/research/sentinel/ or a linked research memo, with a conventional docs commit ending **[skip netlify]**; link it in Issue #17. Do not edit question bank, grant approvals, change code, run paid tools, deploy, or touch GT's protected MSI/Hermes services.

**Astra/architect:** review the resulting proposal against Dexter timing/evals brief and learner-model plan; document an ADR rejecting unnecessary formats before permitting implementation. **Codex:** after remaining gates and explicit user-start, implement the *first eligible MCQ-only safe slice* with tests and verified bundle limits, updating feature catalog, change log and issue as appropriate. Never treat a GitHub doc/issue as an instruction that an always-on external bot has already received.

## Acceptance criteria for eventual code

- Learner can go wrong MCQ -> accurate method/choice explanations -> *different approved* MCQ -> record independently answered performance -> due review, without a separate study format.
- Strict Mock answer/grade and key protection unchanged, server-only grading, no cross-user histories, no repeat-submission evidence inflation, assisted-correct separated from independent, and no leakage to Ask AI.
- An unaided answer on a fresh item is measured separately from exact-item review; selector gives an honest explainable reason and does not train on mock-held-out families.
- Page fits 360px and low-end Android/Lite without heavyweight charts, hover-only controls or newly expanded JS size budgets; zero-paid-AI path works.
- Educational claims need predeclared measurement on unseen answers and delayed recall, not an attractive dashboard, faster guessing or aggregate quiz count.

This brief is a scope correction **inside** the existing Civio/Dexter roadmap; it does not supersede current bank/security gates or claim a feature has shipped.
