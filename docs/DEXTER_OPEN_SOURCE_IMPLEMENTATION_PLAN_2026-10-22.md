# Civio / Dexter: open-source-informed execution plan (22 October 2026)

**Status:** Product/engineering proposal for GT + Astra review. **No feature implementation, live DB mutation, paid inference, deployment, or bank approval is authorized by this document.** This is a scoped companion to the **canonical execution order** in [CIVIO_NEXT_AGENT_EXECUTION_PLAN.md](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md), not a second competing master roadmap. [Issue #17](https://github.com/Vincenzo-OPC/Civio/issues/17) remains Dexter's parent; the tracking issue is [Epic #19](https://github.com/Vincenzo-OPC/Civio/issues/19) with scoped [BKT #20](https://github.com/Vincenzo-OPC/Civio/issues/20), [Strict selection #21](https://github.com/Vincenzo-OPC/Civio/issues/21), [metadata pilot #22](https://github.com/Vincenzo-OPC/Civio/issues/22), and [Rescue #23](https://github.com/Vincenzo-OPC/Civio/issues/23).

## North star, product scope, and red lines

Civio is an independent Philippine CSE reviewer, not CSC software. Subprofessional foundations first (fractions, percentages, ratios, word problems, spelling, filing), but support both exam levels. The goal is independent success on **new, different, difficult** approved multiple-choice questions with trustworthy delayed recall and sensible timing, not a promised real CSE score. **MCQ only**, no flashcards, minigames, podcasts, matching, or new exam modes. Keep existing **Study Mode** and **Exam Mode / Strict Mock** only.

**Owner-funded generative inference: ₱0.** The existing `OwnerAiSpendLock` is default closed and production closed; no new model keys, paid trials, provider activation, OAuth/SIWC launch or live API tests. Offline fixtures and local deterministic code only. External user-controlled Ask/Copy may remain, respecting key lock. Follow [binding policy](DEXTER_ZERO_COST_ACTIVATION_GATE_2026-10-22.md). **No deploy, production activation, MSI/Hermes access, edits to live learner history, or changes to GT-approved bank statuses without explicit GT instruction.** Existing security, signed import/approval, anti-leak, offline and performance gates always take precedence.

## Verified repository starting state and discovered gaps

Checked on main around commits `12cda0d`, `f8717ae`, `6163412`, `1a4412d`; re-fetch main before work because Grok Bot and other agents are concurrently committing. See [FEATURE_CATALOG.md](FEATURE_CATALOG.md) for canonical implementation status.

**Already in code:**
- Laravel 13 + React/TypeScript/Inertia; Study and Strict mocks; server-grading/key secrecy; `MockPoolSelector`; Review Mistakes; fresh same-skill items; Today's Focus; server-owned online FSRS; checked `RevealTutor` solvers; external Ask/Copy; Lite and offline drill packs.
- New deterministic `SkillMasteryEstimator` (BKT-v1), `NextSkillRecommender`, versioned `SkillGraph`, `MisconceptionDiagnoser`, `questions.archetype` and hidden `distractor_codes`. **Schema/engines are not the same as approved metadata populated, validated learner UI or a full intelligent tutor.**
- Owner-key AI call lock and zero-outbound-network tests. 22 Oct main has been moving quickly; check the newest complete GitHub Actions runs before claiming green.
- Browser E2E Strict Mock tests exist and now have a GitHub workflow; initial workflow run failed on job configuration and a follow-up changed the runner temp DB path. **Confirm actual Chromium E2E completion**, not merely PHP/JS CI or an isolated browser run.

**Specific code problems or questions requiring tests:**
1. `LearningInsightsService::forUser` increments independent counters even when the answer is `null`; `isCorrect` becomes false. Are omissions meant as performance misses, or should BKT *skip* them? Distinguish scoring accuracy from learning evidence.
2. Same/repeated questions can each update BKT, yet repetition and recalled answer position may not prove transferable skill. Order is oldest attempt id and within each attempt question order, not necessarily actual response chronology. Assisted-event capture, hint timing, abandoned attempts, question withdrawal, track, attempts over the 50-run cap, and 4-choice guessing assumption require audit.
3. `SkillMasteryEstimator` uses **fixed** `P_INIT=.2, P_LEARN=.1, P_SLIP=.1, P_GUESS=.25`, `MIN_ANSWERS=5` and `WEAK_BELOW=.6`. Treat these as provisional model assumptions, **not calibrated mastery percentages** or an official pass probability.
4. `SkillGraph::skillFor` returns null without a matching archetype. The bank review process currently has many unapproved items and proposed metadata; measure approved, active, eligible item coverage before promising personalized practice.
5. `MockSessionService` passes seen/wrong learner history into `MockPoolSelector` for both Study and Strict. A **diagnostic/benchmark Strict Mock should not prefer previous mistakes or weak topics**. Keep security/time/blueprint rules. Check current selector behavior before any edit; don't accidentally alter an existing released exam contract.
6. The question pool uses subcategory-name balancing and author/heuristic difficulty. Test whether it actually samples the intended CSE topic mix, language proportions, item novelty and level constraints, instead of assuming CSC published Civio's chosen quotas.
7. `MisconceptionDiagnoser` is a key-dependent *possible mistake* classifier; ensure item-option index mapping and no exposure of code, right answer, key or clue before authorized post-grading Reveal.
8. Legacy documentation describes some features as missing after they've been implemented; use **actual code/tests + FEATURE_CATALOG** to update stale status, not a rewrite of working systems.

## Delivery gates, in dependency order

### Gate 0 — Stabilize and pin a known-good test baseline (P0, immediate)

**Owner:** Codex engineering; Grok Bot independent CI read; Astra review gate; GT retains deployment approval.

- Rebase on current main and confirm green `tests`, `linter`, `size`, plus Playwright Chromium **E2E** from a *throwaway guarded SQLite DB* (never MSI database or protected ports). The [first passing Chromium CI run after the repair](https://github.com/Vincenzo-OPC/Civio/actions/runs/39751013201) completed successfully on commit `1a4412d` (later commits must be checked independently). The 22 Oct E2E workflow was initially invalid because `runner.temp` was used in job `env`; commit `1a4412d` changed setup. Treat subsequent CI status as the evidence, not the presence of `e2e.yml`.
- Keep strict mock offline/reload, multi-tab, server deadline, double-submit, withdrawn-item no-key, guest/owner and keyless UI tests. Add checks if new selector routes touch these flows. Stop if CI is red; **don't raise bundle limits to suppress failures**.
- Preserve `OwnerAiSpendLock`, zero AI egress architecture test, default OFF and no secrets. Confirm open Issue #18 is genuinely satisfied before closing, but do not reimplement it.
- **Acceptance:** latest source commit has all required checks green (or clearly marked as blocked with reproducible logs); no real HTTP to model providers; test DB guard aborts for protected ports. Document SHA/run URLs and measured main/vendor/exam/CSS sizes.

### Gate 1 — Trustworthy learning events and BKT audit (P0 learning validity)

**Owner:** Astra pedagogical ADR and evidence definitions; Codex isolated tests/implementation; Grok Bot audit fixtures.

- Define an explicit attempt event taxonomy: independently correct, independently wrong, unanswered/skipped, assisted correct/wrong, timed-out/withdrawn/not scored, repeated exposed question, truly unseen item, confirmed guess (if explicitly captured). Separate **exam scoring** from **learning update**.
- Verify server-owned answer state and actual help exposure; avoid assuming `null` is incorrect in mastery; avoid counting withdrawn items; measure repeated-item overconfidence; tests with out-of-order answers, missing data, stale cached result, mobile recovery and 3-vs-4 choice items. Preserve old records; don't silently backfill or rewrite live history.
- Keep BKT-v1 behind truthful wording and/or internal-only until tested. Compare with **simple rolling independent accuracy**, optionally an offline Elo-style baseline and a research-reference pyBKT fixture; split train/test **chronologically and by non-overlapping question family**. Compare probability calibration (Brier score/log loss where applicable), unseen prediction, minimum sample and explanation stability. An external Python library is a local research benchmark only, **not a new production runtime**.
- Decide model version, confidence/insufficient-evidence states, forgetting strategy vs FSRS role, and whether per-skill BKT is justified given sparse item tags. Include approval, rollback and feature-off rules.
- **Acceptance:** regression fixtures cover omissions/assistance/repeats/leaks/old records; the estimate never appears as official pass odds or an absolute mastered badge; held-out prediction vs baseline is measured; no paid call or bulk import.

### Gate 2 — Clean assessment blueprint, distinct from teaching (P0 assessment validity)

**Owner:** Astra curriculum/assessment ADR; Codex selector implementation; bank reviewer verifies blueprint source.

- For **Strict Mock**: preserve established 150/145 counts and total timer, question/answer secrecy, no offline-key items, no active withdrawn questions, de-duplication, approved/active track constraints. Selection should obey a **versioned, source-labeled Civio practice blueprint**, with representative CSC-listed areas and Filipino/English topic coverage, and sample **fresh unseen** eligible items where possible. No weak-topic/past-wrong boost for Strict; no personalized difficulty boost that invalidates between-attempt comparisons. The specific quota is Civio policy, *not* claimed CSC weighting.
- For **Study Mode and targeted drills**: keep existing personalized weak-topic and fresh practice behavior, with a distinct selector policy rather than confusing it with Strict. Prefer limited recent exposure and explanation status, not answers sourced from the client.
- Handle pool exhaustion transparently: if no eligible independent fresh sample exists, show a notice and avoid falsely calling it an unseen calibrated assessment. No padding with clones or secretly using unapproved questions.
- Tests: controlled seeded pool with language, topic, level, withdrawn, offline, repeat and empty-category cases; blueprint quotas and no-client-cheating; same mock rules after resume/refresh; stable cross-subject counts; reproducible random seed in tests.
- **Acceptance:** Strict distributions cannot depend on one learner's wrong/weak history; Study/Practice still personalized; security suite and bundle limits pass. No live bank mutation.

### Gate 3 — Content/metadata validation and human sign-off (P1, parallel *research* with gates 1–2; activation afterward)

**Owner:** Grok Bot / question-bank worker research and candidate tagging; independent human editorial review and **GT content approval**; Codex importer/QA tests, not approvals.

- Recount latest signed 2,100-item manifest at execution time. Oct 22 snapshot was 1,377 GT-approved, 723 nonapproved (later drafts/review states may move); mechanical validity **does not mean** human-approved learner content. Never bulk activate/approve or bypass signed importer.
- Measure by **approved-and-eligible** item: `archetype` coverage, `distractor_reasoning` availability, verified right key, explanation/why_wrong quality, language, multi-choice count, licensing/source rights, family/near-clone, exposed/offline status. Create a coverage matrix with unknown explicitly shown.
- Pilot a *small, human-reviewed* Subprofessional set across percent/fractions/ratio/word problems, spelling and filing. Convert source option IDs into **stored option indexes** and strip key-implying fields from the client payload; `MisconceptionDiagnoser::problems()` runs as an importer gate. Handle duplicate/missing/malformed metadata by **no diagnosis**, not guesses.
- Revision of previously approved items requires reviewer-approved -R1 workflow; metadata changes count as content and require appropriate sign-off. Existing QA packets and separate answer sheets remain source of truth.
- **Acceptance:** reviewed pilot items have correct keys and distractors, complete provenance and approvals; zero pre-reveal metadata leaks; no automatic changes to active bank; a coverage report honestly says how much personalized Dexter can address.

### Gate 4 — First complete, zero-LLM *Dexter Rescue* loop (P1, after 1–3)

**Owner:** Astra teaching/UX sign-off; Codex code; Grok Bot adversarial question QA.

In **existing Study Mode only** and after a server-authorized answer/reveal:
1. Show **one** plausible error tied to the **chosen wrong option**, phrased as `You may have ...`, with `Not enough evidence` on untagged items; never infer a student's ability/personality from a single click.
2. Offer brief **method-first** checked explanation: asked → givens → procedure → worked computation / rule → check → why chosen option fails; collapsible `Explain Simpler` or existing progressive sections only, no instant text generation. Allow optional deterministic diagram (Gate 6).
3. Serve a **different, approved, keyless, unexposed MCQ** of that archetype or the missing prerequisite with server-side track/skill matching, distinct stems/families when available. If none, show honest empty state; never synthesize an exam item or bypass review.
4. Mark all help correctly. Only *independent*, unassisted transfer attempts influence learning estimates, while an already-exposed/fresh distinction is retained. FSRS schedules according to **current** policy (do not make user success fake).
5. Explain the evidence-based next step in human language, and let students return to normal practice; no added quiz mode or new paid tutor.

- **Acceptance:** test wrong option -> correct plausible method, then new item -> independent answer -> appropriate review due status; Strict Mock prohibits pre-submit hints/metadata/reveal and never triggers Rescue until authorized post-submission review; works with an untagged question; guest state does not leak cross-account; renders on 360px Lite without heavy libraries.

### Gate 5 — One integrated daily adaptive practice route (P2, after Rescue)

**Owner:** Astra selection policy; Codex wiring; Grok Bot evaluation.

- Reuse **Today's Focus**, **Review Mistakes**, existing **FSRS**, **Fresh Same Skill** and existing exam/practice mechanisms. **Do not create a new mode, scheduler, reminder system, or duplicate database of learner profiles.**
- Choose a small MCQ session from due review → weak prerequisite verification → fresh approved transfer → appropriate mixed exposure/blueprint balance. Distinguish item objective `recall`, `transfer`, `diagnosis`, `assessment` without labeling an ordinary practice item as official.
- Make `Why this question?` available when evidence actually exists; cold start defaults to balanced fundamentals and says so. No hidden boosts based on guesses or assisted success.
- Defer **offline FSRS sync** until conflict resolution is specified and separately tested. Offline packs must never contaminate sealed mock inventory. User-controlled daily goals, no gamified pressure.
- **Acceptance:** deterministic replay for a given snapshot, no contradictory duplicate queues, guardrails for scarce pools, role/track/privacy tests, no increase to exam bundle or new external infrastructure.

### Gate 6 — Make the existing UI a focused teaching experience (P2, progressive enhancement)

**Owner:** Astra UX review + GT visual sign-off; Codex targeted components, not total rewrite.

- Preserve design tokens violet `#5B35F5`, lime `#B3F52D`, light paper/black, solid buttons, no blur/glass slop. Current React/Tailwind/Radix/shadcn-style stack stays. **No new animation or quiz framework by default.**
- **Question canvas:** one dominant stem, four legible radio/answer choices, clear selected-vs-correct state, strong keyboard/touch/focus semantics, responsive reading width, reduced motion; reuse `answer-option.tsx`, `answer-reveal.tsx` and existing timing UI. No flashcards, gamified distraction or answer-guessing animation.
- **Visual math**: lightweight SVG/CSS fraction bars, percent grids, number lines, ratio tables, equations; source values from verified server-side lesson methods. Validate geometry/value alignment; do not introduce new model-generated SVG or unsafe HTML.
- **Dashboard/analytics:** one unambiguous `Continue Studying` / `Today's Focus` CTA, `Why next` within the existing UI, evidence sample size; only show real practice data, optional comparison with own earlier new-item performance; never fabricate forecasts, achievements, rankings or official ratings. Reuse existing cards rather than making a second dashboard.
- Test 360px and Samsung/slow-Android conditions, Lite, keyboard-only, focus order, screen reader labels, long Tagalog/English passages, high text zoom, dark/light, reduced motion, offline failure. Keep E2E screenshots and screenshot diff for reviewed representative **fixture** screens.
- **Performance:** check `npm run size` per change; 11kB brotli exam chunk budget remains hard. Prefer lazy components, CSS/SVG and no unnecessary cross-site scripts or fonts.
- **Acceptance:** accessible error+correct+unavailable states, no key leak, no adverse mock timer event, browser E2E, within current budgets.

### Gate 7 — Independent educational evaluation and release criteria (P2/P3)

**Owner:** Astra research/measurement design; Grok Bot independent adjudication; Codex offline harness; GT release decision.

- Pre-register metrics/decision rules rather than claim Dexter works because it looks clever: unseen comparable MCQ correct rate, transfer immediately and after ≥24 hours, weak-skill recovery, confidence/calibration, skipped and repeated exposures, time *conditional on accuracy*, performance by language/track and device.
- Human-reviewed gold fixtures (correct key, option traps, explanation clarity, prerequisite map); controlled offline learner simulations; longitudinal split by time and question family; compare baseline ordinary practice vs new Rescue/selection. Track sample-size uncertainty; flag data sparsity, not fake `mastery 98%`.
- Test on synthetic records and consented real study histories only. Don't publish personally identifying data or exam keys in external research services. Store versioned policy IDs and reasons for reproduction.
- Release gradually *only when separately approved*: internal fixtures → human reviewer demonstration → small opted-in pilot after branch/host readiness, with rollback; zero extra GT AI cost. No timing promises, production deployment or automatic instrumentation purchase.
- **Acceptance:** signed human editorial sign-off, regression suite+E2E+budget green, zero owner-key HTTP, validated outcomes on withheld non-duplicated MCQs, accessibility and data/privacy review. If no evidence of improvement, retain simpler baseline.

### Gate 8 — Optional generative provider research (BLOCKED, not in implementation critical path)

Sign in with ChatGPT for an approved commercial hosted partner (not yet accepted) and OpenRouter user-funded OAuth remain potential external user-funded inference options. **Neither is an activated feature or a prerequisite for Gates 0–7.** Gemini, Cloudflare, Groq shared free developer quotas are not a scalable unlimited public free service. No billing/sign-in/provider work unless GT explicitly authorizes a separate architecture + privacy + commercial terms review.

## Open-source research ledger: **inspect patterns, don't clone platforms**

| Reference | Verified source / role | Civio action | Import policy |
| --- | --- | --- | --- |
| [OATutor](https://github.com/CAHLR/OATutor) | React adaptive tutoring, scaffolding and BKT; optional Firebase | Read source for skill mapping, scaffold progression, deterministic next-problem loop | **Architecture inspiration first**. Repository includes CC BY 4.0 teaching content with per-file attribution; **do not copy OATutor textbook problems, hints or branded UI** into Civio's bank. Verify license of any exact code before adaptation |
| [pyBKT](https://github.com/CAHLR/pyBKT) | Python reference BKT modeling and variants | Reproduce **offline** fixtures to audit Civio BKT priors/calibration | No Python production dependency, no server inference, verify file license if copying source |
| [Khan Perseus](https://github.com/Khan/perseus) | MIT question renderer/editor; broad widget architecture | Study schema/authoring preview and accessibility patterns | **Do not import full monorepo/widgets** into 11kB exam route; keep server grading |
| [H5P Multi Choice](https://github.com/h5p/h5p-multi-choice) | MIT multiple-choice engine | Study per-option feedback and accessibility | Borrow behavior, not a new content format/runtime |
| [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs) | Already part of Civio's server-owned scheduler | Keep it; verify policy, failures, scheduling semantics and version | No duplicate scheduler or automatic personal FSRS parameter training |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | MIT customizable React components | Refine **existing** components and semantics | No new UI framework |
| [GOV.UK Design System](https://design-system.service.gov.uk/components/) | Public-service accessibility and forms guidance | Readability/keyboard/touch/feedback patterns | Refer to patterns, not GOV.UK branding |
| [Storybook](https://github.com/storybookjs/storybook), [Mobbin](https://mobbin.com), [21st.dev](https://21st.dev) | Isolated component previews / visual flows / components | Design reference for focused mobile learning and fixture previews | Mobbin: visual inspiration, **not source code**; check exact licenses/assets for any 21st.dev component. Storybook optional dev-only after E2E works, not required |

Source checks made 22 Oct 2026 using the primary project repository pages; recheck license and version **per exact asset** before reuse. Under no circumstances import external review questions into GT's approved bank without rights + original rewriting + human review.

## Decisions Astra must make *before Gates 1–2 are implemented*

1. **ADR BKT:** What is a scored omission vs an observed learning event? How are repeats, assisted answers, item family, and real chronology handled? Which baseline is sufficient to justify BKT? Conservative sample threshold/uncertainty?
2. **ADR assessment:** Should Strict sample independently from a fixed Civio versioned, CSC-scope-grounded blueprint with no weakness/past-wrong targeting? How will scarce bank pools/exposures be disclosed?
3. **ADR content/Rescue:** What constitutes reliable per-option misconception evidence? How can we prove the key/index is never client-exposed? What minimum approved metadata coverage is enough for a pilot?
4. **ADR daily policy:** How do existing FSRS and next-focus interact without double scheduling or overexposing the same questions?
5. **ADR design:** Confirm focused explanation components and smallest safe SVG lessons; reject heavyweight page/animation packages.

Document each ADR with: alternatives, decision, impact on existing code, risks, reversed/rejected options, metrics, gate, author/reviewer, and explicit GT approval points. If Astra is unavailable, **audit/test only and record the open decision; don't use Grok research as automatic approval**.

## Work allocation and handoff policy

- **GT (product owner):** approve or reject architecture changes, visual language, content sign-offs, spending and deployment. Never infer a general GitHub research instruction means paid features may be enabled.
- **Astra (architect/reviewer):** independently validate BKT/blueprint/scaffold decisions, design evaluation and review gates. Architecture approval is **not** bank/production approval.
- **Codex (engineering):** one small phase slice per session, run local + GitHub checks, do not duplicate existing systems; update FEATURE_CATALOG and existing canonical handoff with evidence.
- **Grok Bot (independent research/QA):** inspect open-source source and licenses, build benchmark fixtures and item QA proposals; no automatic approval of bank data, no paid AI, no unreviewed deployment. Grok has previously committed feature code directly; for this plan, **keep unreviewed new features out of main until Astra ADR, with reversible small changes under repo's existing branch rules**.
- **Bank/editorial reviewers:** source, key, distractor, copyright, language and approval QA; preserve signed import separation.

Each engineering slice's final note includes: base/head SHA, source/test files, why needed, behavior before/after, security and no-cost invariants, command/test/CI URLs, size numbers, reviewer decision and rollback path. **Do not promise background work or imply a GitHub document automatically launches an agent.**

## Immediate next three actionable tickets

1. **Green browser E2E and validate its isolated database path**, plus keep all existing tests/size green; identify the actual failing step from workflow logs before touching code.
2. **Evidence correctness of BKT and Strict selection**, as separate ADRs and tests, not a broad refactor.
3. **Count approved metadata and ship only a GT-reviewed small diagnosis/Rescue pilot** after previous gates. Other future gates follow, no provider dependence.

## Stop / defer list

No LLM chat at this stage, no SIWC/OAuth build, no free-tier owner proxy, no new quiz formats, no duplicate FSRS implementation, no social leaderboard, no fabricated pass prediction, no arbitrary raising bundle caps, no full replatform to Perseus/H5P/OATutor, no automatic bank content activation, no direct testing on MSI/protected DB, no deployment, and no copying proprietary UI assets. 
