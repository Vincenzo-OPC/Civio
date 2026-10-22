# Codex handoff plan

> **Superseding GT addition, 21 Oct 2026:** Read [Dexter timing and AI evaluations](DEXTER_TIMING_AND_EVALS_2026-10-21.md) alongside the master Dexter plan. Research and design optional question pacing/interactive bar, separate accuracy from speed and item familiarity, and use human-calibrated hybrid AI tutoring evals. **Astra reviews the architecture and can veto/improve proposals**; Codex must prepare ADR and perform only first eligible tested change after security gates. Existing earlier copy-paste prompts are superseded. No deployment, billing, unauthorized question access or live-service mutation.


> **New GT directive, 21 October 2026:** Mandatory Codex startup reading: [Dexter adaptive tutor master plan](DEXTER_ADAPTIVE_TUTOR_MASTER_PLAN_2026-10-21.md), [tutor policy](DEXTER_TUTOR_POLICY_2026-10-21.md), [AI funding/access](DEXTER_AI_ACCESS_AND_BUSINESS_2026-10-21.md), and [near-perfect CSE research](CSE_PERFECT_SCORE_RESEARCH_2026-10-21.md). GT wants 100% on independent unseen practice (especially Numerical and spelling), a durable learner model, proactive Socratic Dexter, and inference costs funded by opt-in user accounts where legitimately supported. **These are plans, not shipped features or permission to incur costs.** Maintain the latest security -> import -> analytics credibility -> Review Mistakes ordering in [next-agent execution plan](CIVIO_NEXT_AGENT_EXECUTION_PLAN.md), and implement the first safe slice only after current tip verification. ChatGPT SIWC plan access cannot be resold or gated behind a Civio payment. Existing phases remain valid.


> **Long-range AI research (2026-10-08):** `docs/AI_SELF_IMPROVEMENT.md` defines a future opt-in, independently benchmarked Civio testbed for THE-MACHINE's evolutionary agents. It does not change the current ranked product phases, security rules, or authorization gates.

Read this first. It says what Civio is, what has been built (with commits), what
must never break, what is still open, and what to build next, in order.

Updated 7 Oct 2026. `main` is the source of truth; if this file and the code
disagree, the code and tests win, then `AGENTS.md`.

## 0. Learning Features (next)

> **Pending Astra handoff (17 Oct 2026):** read [ASTRA_PENDING_HANDOFF.md](ASTRA_PENDING_HANDOFF.md) first. It puts the Sentinel security and exam-integrity findings (F1, F2, F6, then F3) ahead of this section, and gives each learning feature an honest status. The 2,000-question milestone proposal is in [research/MILESTONE_2000_PLAN.md](research/MILESTONE_2000_PLAN.md).

Added 13 Oct 2026 for Grok Build or Codex. This is a brief only; none of it is built yet.
Stack: Laravel 13 / Inertia / React 19 / TS / Tailwind 4 / Pest (+ Vitest for TS).
Every meter and message must come from real stored data, never decoration.
Write one small commit per item, and keep CI green.

Start with [REVIEW_MISTAKES_BRIEF.md](REVIEW_MISTAKES_BRIEF.md) (17 Oct 2026). FSRS waits for its stored review events.

### 0.1 Visible FSRS spaced review (`ts-fsrs`, already a dependency)
- **Next-review card** after each answer: "Next review in 3 days because you answered fast and correct."
  - AC: the interval and the reason come from the ts-fsrs scheduler and the stored review log (rating from correct + response time).
  - Tests: unit tests for rating mapping and interval text; Pest feature test that an answer persists a card state.
- **Review calendar**: due Today / This week / Later.
  - AC: counts equal the number of due cards in the DB; works in Lite mode.
  - Tests: Pest test with fixed clock and seeded cards checks the bucket counts.
- **"Why this question?"** on every item, e.g. "missed ratio 2 days ago", "due for review", "new topic".
  - AC: the reason is chosen by the selector and sent with the item, never invented.
  - Tests: selector unit test for each reason type.

### 0.2 Dashboard meters (game feel, plain labels, calm, not arcade)
- **Memory**: mean FSRS retrievability over the cards the learner has seen. It falls as cards come due and refills on review. Test with a time-travel clock.
- **Focus**: today's goal budget (minutes/items) left; suggests a break when low. Test the threshold.
- **Progress**: XP and level from correct recall of due/new cards and passed Strict Mocks only. Re-answering the same item or practice mode gives no XP (anti-farming). Test that repeats give 0 XP.
- **Topic Map**: mastery per archetype (FSRS stability + accuracy), lighting up by level. Test the aggregation.
- **Readiness**: predicted score per subject from Strict Mock results only, hidden until there is enough data. Test that drills don't change it.
- **Streak** with one freeze day that is used automatically. Test with day-boundary cases in Asia/Manila.
- AC: each meter has a server source and a test; no meter shows on fake data; it meets the a11y contrast rules and plain-language labels.

### 0.3 Learning methods
- Retrieval-first quizzes: answer before seeing any hint or explanation.
- Interleaving that mixes subjects in real exam proportions (Prof/Subprof blueprint). Test the mix ratios.
- Dexter gives a hint before the answer (one hint step, the key stays withheld). Test that the hint never leaks `answer_option_id`.
- The Reveal names the learner's specific error from the chosen option's distractor code (spec §codes). Test the mapping for each code family.
- Post-session insight line from repeated error codes, e.g. "you keep mixing affect/effect". Test with a threshold of ≥2 same-code misses.

### 0.4 Constraints (must not break)
- Lite mode and cheap phones: keep the `size-limit` budgets (`docs/LITE_MODE_PLAN.md`). No heavy chart libs.
- Works offline with the L2 packs: FSRS state queues locally and syncs later.
- The Strict Mock lock is unchanged: no hints, Reveal, or meters during a Strict Mock.
- "Civio" in Title Case; never imply CSC affiliation.
- Normal pushes only, never force-push; CI green.

### 0.5 Other open items
- **Deploy:** Hosting undecided pending GT. Cloud Run and Koyeb/Neon/Netlify are historical alternatives; no deployment or spending is authorized.
- **Bank:** import the 1,000-item bank into production with `php artisan civio:import-batch` (batches 002–011, `--status=active` after QA) at deploy.
- **Old desktop app:** Item 1530 is untouched; GT skipped it.

## 1. Read in this order

1. This file.
2. `AGENTS.md`: locked rules (product, MSI, push, bank). `CLAUDE.md` repeats them.
3. `docs/CHANGES_SINCE_BASELINE.md`: every difference from the baseline, with commits.
4. `docs/CODE_STANDARD.md`: how to write code here, plus the modernization backlog.
5. `docs/LITE_MODE_PLAN.md`: performance budgets, Lite mode, offline packs.
6. `docs/CSE-Question-Design-Spec.md` before touching any question content.

## 2. What Civio is

Civio is a Philippine Civil Service Exam (CSE) reviewer: full mock exams
(Professional 150 items, Subprofessional 145), topic drills, a tutor named Dexter,
study analytics and schedules. It works for guests and on cheap phones (Lite mode,
offline drill packs). It is not official CSC software and never says it is.

- Brand: **Civio**, Title Case. Lowercase `civio` only in identifiers, URLs and env.
- Tutor: **Dexter**.
- The product is Civio everywhere; no other app names in code, UI, docs or seeds.

## 3. Stack, run, test, push

Laravel 13, PHP 8.4, Inertia 3, React 19, TypeScript (strict), Vite, Tailwind 4,
shadcn/Radix, Pest 4, Pint, Postgres (SQLite in-memory for tests). Commands are in
`AGENTS.md` ("How to run / test / lint / build").

Before every push, all of these must pass:

```bash
php artisan test
npm run types:check
npm run lint:check
npm run test:js
npm run build && npm run size
vendor/bin/pint --test <touched PHP files>
npx prettier --check <touched resources/ files>
```

Push rules: normal `git push origin main` only. Never force-push, never
`--no-verify`, no branches. `git pull --rebase origin main` first.

## 4. What has been built (by phase, with commits)

Baseline: `d3f0368` (tag `baseline`), the desktop study tree imported as Civio's
starting point. Tags: `v0.1.0-phase0`, `v0.1.5-phase0.5`.

### Phase 0: fixes first

| What                                                                                                | Commits                         |
| --------------------------------------------------------------------------------------------------- | ------------------------------- |
| Agent setup, Phase 0 docs                                                                           | `d66d2aa`                       |
| Server-side grading, keys withheld until reveal/submit, answers keyed by question ID + option index | `d19afda`                       |
| Dangerous routes locked, user custom questions are drafts, `nullOnDelete`                           | `761a3bd`                       |
| Ads, donation links and debug junk removed                                                          | `e21d94c`, `ba8c622`            |
| Rebrand to Civio across UI, meta and docs                                                           | `5fe2d40`                       |
| Lazy Inertia pages (code split)                                                                     | `6277c17`                       |
| Libraries: vite-plugin-pwa, ts-fsrs, Prism tutor stub, Sentry opt-in; old hand-written SW removed   | `9fe51a4`, `647e484`            |
| CI green (tsc, eslint, Pest aligned with guest unlimited)                                           | `acedd26`, `ce41c82`, `ed5aa64` |

### Phase 0.5: desktop ports and bank hygiene

| What                                                                                                           | Commits                                    |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Exam and item clocks with urgency colours                                                                      | `518ee08`                                  |
| Tutor loop: weak topics from server grading, drills lean weak                                                  | `a4df9f8`                                  |
| Desktop home launchers guarded (no redundant Mock button)                                                      | `76f0542`                                  |
| Encoding repair: mojibake punctuation, `??` lost math symbols (`civio:repair-bank-encoding`)                   | `4f4eb21`, `22fc855`                       |
| Variant clones removed: one copy per item in seeds, `civio:remove-variant-clones`, mocks use unique items only | `d8406d8`, `4bce08e`, `ba88fa5`, `9bf7508` |
| Upstream fix pulled in (AI analysis orchestrator missing keys)                                                 | `c6a173f`                                  |
| Phase 0.5 docs                                                                                                 | `9ab859c`                                  |

### Copy for AI

| What                                                           | Commits                                               |
| -------------------------------------------------------------- | ----------------------------------------------------- |
| Specs (AI study system, 2026 AI standard, external AI handoff) | `e4e3d4c`, `4cffde5`, `29caf02`, `d62b7bc`, `1d4c96d` |
| Formatter with tests, button beside Reveal and in review       | `3ab87d2`, `3ba17ab`, `9f3891c`                       |

### Tracking

| What                                                        | Commits                         |
| ----------------------------------------------------------- | ------------------------------- |
| git-cliff changelog and size-limit budgets                  | `9dcdf3b`, `82aedb6`, `e1e48c4` |
| Baseline diff log (now `docs/CHANGES_SINCE_BASELINE.md`)    | `f28f717`, `bc8d3dd`            |
| Entire: Codex and Claude Code hooks, committed `.githooks/` | `3fe931b`                       |
| Tags `baseline`, `v0.1.0-phase0`, `v0.1.5-phase0.5`         | (annotated tags)                |

### Lite mode

| What                                                                                                                                      | Commits   |
| ----------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| Plan                                                                                                                                      | `db775f7` |
| L0: on-demand PDF and realtime, light images, no unused fonts, slim precache                                                              | `5ea1cd5` |
| L1: server-picked mocks (`POST /exams/sessions`, `MockPoolSelector`), Lite mode flag, text-first exam/drill screens, server prop trimming | `c825fe9` |
| L2: offline drill packs, worker served at `/sw.js`                                                                                        | `09c62da` |

### De-baseline rename, brand, source groups

| What                                                                                                         | Commits   |
| ------------------------------------------------------------------------------------------------------------ | --------- |
| Cursor not used; Codex, Grok Build and Grok Bot are                                                          | `912d318` |
| Diff log renamed, "baseline" wording everywhere, remote `upstream-baseline`                                  | `bc8d3dd` |
| Neutral Civio mark (violet `#6D28D9`, lime `#A3E635`), no footer author credit, legacy storage keys migrated | `08b4640` |
| Civio-only README and docs; desktop patch log folded into `docs/DESKTOP_PATCHES_TO_PORT.md`                  | `a0019af` |
| `questions.source_group` (`baseline` / `civio`), `civio:tag-source-groups`                                   | `ac27f5a` |
| Code standard and modernization backlog                                                                      | `fa431e0` |

### Dark mode fix

`51c429b`: the inline scripts in `app.blade.php` contained TypeScript (`as`
casts), so the browser threw a syntax error and system dark mode never applied
before paint. Now plain JS, with a Pest test that runs `node --check` on every
inline script.

## 5. Security invariants (never break these)

1. **The server grades.** Scores come from server keys; client `cat_scores` are
   never trusted.
2. **Keys stay on the server** in live exams. `correct_option` and `explanation`
   are sent only after Reveal (drills) or submit. Answers are keyed by question ID
   plus original option index; `originalOptionIndices` maps the shuffle.
3. **The server picks mocks.** `POST /exams/sessions` chooses unique items by
   blueprint quotas and stores their IDs in `exam_sessions`.
4. **Submit checks.** A mock session can be submitted once, only for the items it
   served.
5. **Offline packs only carry `offline_eligible` items, and strict mocks never use
   them** (nor exact copies under another ID). The sync endpoint re-grades with
   server keys, rejects tampered keys, and refuses to grade non-offline items
   (so it cannot be used to check mock answers).
6. No provider keys in `VITE_*` or any client bundle. No secrets in commits.
7. Never touch GT's MSI machine, its Docker containers, or Hermes (`:8642`).

## 6. Known gaps

- [ ] Formatting leftovers: Pint and Prettier still flag older files (backlog row 1
      in `docs/CODE_STANDARD.md`). Fix in separate `style:` commits.
- [x] Exam Simulation modes shipped (2026-10-13): `exam_sessions.mode` and
      `exam_attempts.mode` are `study` or `strict`. While a learner (or a guest
      browser session) has an open Strict session, `/exams/reveal` and
      `/exams/expound` answer 423 for its items (`App\Services\Exam\StrictMockLock`).
      Submit lifts the lock; an abandoned session stops locking after its time
      limit + 10 min. The Strict UI hides Reveal, Dexter and Copy for AI, and the
      timer is forced on (optional in Study). Labels read "Exam Simulation";
      route names are unchanged. Real mock sizes: 150 items in 3h10m (Professional,
      ~76 s/item), 145 items in 2h40m (Subprofessional, ~66 s/item).
- [ ] Lite L0 Item 6: nginx/deploy cache headers are not set up (needs deploy
      config).
- [ ] The MSI desktop app is still at the baseline. Ports and the clone cleanup SQL
      are listed in `docs/DESKTOP_PATCHES_TO_PORT.md`.
- [ ] Offline results are stored server-side (`offline_practice_results`) but only
      feed the on-device weak-topic list; they are not yet in server analytics or
      history.
- [ ] Now that the worker controls pages, NetworkFirst page caching applies to
      public pages and `/offline`; cached HTML carries the shared Inertia props
      (including the signed-in user's name/email) on that device.

## 7. Open decisions for GT

1. ~~Hide Reveal during strict mocks?~~ Decided: Study Mock / Strict Mock split (shipped).
2. ~~Remove the Mock Exams links?~~ Decided: keep them, renamed "Exam Simulation".
3. Keep the Lite switch in the exam header on phones, or move it to Settings only?
4. L0 Item 6: who owns nginx/deploy cache config, and when?
5. Copy override on exam pages: only copy, cut, right-click and text selection are
   intercepted (keyboard blocking was dropped because it broke dialogs and forms).
   Keep it that way?
6. Keep the legacy storage-key migration permanently, or remove it after a few
   months?

## 8. Question design decisions (spec v0.1 Section 10, approved 7 Oct 2026)

1. **GI term-match stems are allowed:** a plain-English description, the article or
   section in `source`, sibling terms as distractors. The no-teaching rule still
   applies to the other subtests.
2. **Practice mixes are Civio's own choices**, recalibrated with data:
    - Numerical: operations 30 / sequences 20 / word problems 50
    - Verbal English: word meaning 15 / completion 20 / error recognition 20 /
      structure 10 / paragraph organization 15 / reading 20
    - Verbal Filipino: synonym 25 / antonym 20 / idiom 15 / grammar 15 / reading 15 /
      paragraph order 10
    - Analytical: analogy 30 / symbolic logic 20 / assumptions and conclusions 25 /
      data interpretation 25
    - Clerical: filing 55 / spelling 45
    - GI: Constitution 40 / RA 6713 35 / peace and human rights 15 / environment 10
3. **Filing Rules v2 (CoS ruling 2026-10-13, spec v0.1.3 section 10.2):** ARMA
   International Simplified Filing Standard Rules 1-8 (unit order and letter by
   letter; minor words and symbols with a leading "The" last; punctuation ignored;
   initials and abbreviations; titles and suffixes last; prefixes joined; digits
   before letters; organizations as written). v1 was dropped because CSC publishes
   no filing rules. Every filing Reveal must say the rule is the standard office
   rule (ARMA), not CSC-published, and cite its rule number.
4. **First release is text only.** Text tables are fine. Figures wait for an image
   pipeline with alt text and a text fallback.
5. **Review flow:** CSE authors; Chief of Staff reviews (Codex as alternate); GT
   approves item by item, then spot-checks 1 in 5. First batch of 10: 3 Numerical,
   3 Verbal, 2 GI, 1 Analytical, 1 Clerical spelling.
6. **New items** get `source_group = civio` and status `draft` until approved.

Also recorded in `docs/CSE-Question-Design-Spec.md` and
`docs/AI_STUDY_AND_SPELLING_SYSTEM.md`.

## 9. What to build next (in this order)

Each task: tick it only when the acceptance line is true and checks pass.

### 9.1 Modernization backlog (`docs/CODE_STANDARD.md`)

- [ ] Row 1, formatting leftovers. **Done when** `vendor/bin/pint --test` and
      `npm run format:check` pass on the whole repo.
- [ ] Row 2, exam grading core to readonly DTOs. **Done when** existing scoring
      tests pass unchanged and each scoring rule has a unit test.
- [ ] Row 3, exam client state as a pure reducer. **Done when** JS tests cover
      start, answer, reveal, resume and submit.
- [ ] Row 4, split exam screens. **Done when** each file is under ~300 lines and
      Lite and normal screens look the same.
- [ ] Rows 5–12 in order. **Done when** each row's acceptance column is met.

### 9.2 Phase 1 foundation (`docs/CIVIO_CODEX_BUILD_BRIEF.md`)

- [ ] Shell, design tokens and mobile nav. **Done when** usable at 360 px width.
- [ ] PWA: versioned worker, update prompt, no stale bank. **Done when** a deploy
      bumps the precache and exam JSON is never cached.
- [ ] `learning_events` (append-only). **Done when** core exam and drill flows write
      `session_started`, `answer_submitted`, `explanation_opened`, `mock_exam_completed`.
- [ ] Taxonomy (Exam → Domain → Competency → Concept → Micro-skill → Archetype →
      Question). **Done when** tables exist and old drills/mocks still work.
- [ ] Learner state derived on the server. **Done when** mastery and review dues are
      computed without client scores.
- [ ] Question metadata (provenance, difficulty, time, distractor notes, status
      workflow). **Done when** new items can move draft → reviewed → approved.
- [ ] Civio Today dashboard. **Done when** it shows readiness, today's training, due
      reviews and focus concepts (heuristics are fine).

### 9.3 Dexter AI layer

- [ ] `TutorProvider` methods: explain, hint, classify mistake, summarize session,
      draft question, moderate. **Done when** the stub works with zero keys, real
      providers are server-only, and AI-off degrades cleanly.
- [ ] Ask Dexter from Reveal and review. **Done when** answers never reveal a key
      before Reveal/submit.

### 9.4 FSRS review

Build [Review Mistakes](REVIEW_MISTAKES_BRIEF.md) first: it stores the server-graded review events FSRS will need.


- [ ] Review queue on `ts-fsrs` (`resources/js/lib/review/fsrs.ts`) with server
      storage. **Done when** missed items come back on schedule and dues show on the
      dashboard.

### 9.5 Re-parameterize workflow (`docs/QUESTION_SOURCE_GROUPS.md`)

- [ ] Tooling to create a `civio` draft from a `baseline` item: keep the item's
      soul, vary the names, numbers and phrasing. **Done when** drafts go through the
      review flow in section 8 and nothing goes live without GT approval.

### 9.6 Master Product Context 2026 UX plan

- [ ] Write the UX plan from GT's Master Product Context 2026 (Obsidian vault)
      **before any redesign code**. **Done when** GT approves the plan.

### 9.7 Speed targets

- [ ] LCP under 2.5 s on Lighthouse mobile (slow 4G, 4x CPU, mid-tier phone) for
      landing and the first exam screen. Today: landing 3.5 s, exam 4.5 s.
- [ ] Time to Interactive under 5 s on the same profile.
- [ ] JS budgets (brotli, `.size-limit.json`): main entry ≤ 48 kB (today 47),
      vendor ≤ 122 kB (119), exam chunk ≤ 10 kB (9.5), all JS ≤ 1.04 MB (1.03).
      Tighten each budget when a phase lowers the number.

## Frontend redesign

See `docs/DESIGN_IMPLEMENTATION_BRIEF.md` (mockup: `docs/design/focused-learning-canvas-mockup.png`). Deliver the section 17 analysis first, then implement in small verified commits; no question bank edits; no deploy.

## 10. Rules (short version)

- Normal pushes to `main`; never force-push; never `--no-verify`; no branches.
- Behaviour change → update `docs/CHANGES_SINCE_BASELINE.md` in the same commit.
- Formatting fixes in separate `style:` commits.
- No bank rewrites, new items or question-text edits without GT approval.
- Title Case **Civio**; never imply official CSC.
- Regenerate `CHANGELOG.md` with `npm run changelog`; never hand-edit it.
- Entire runs on GT's MSI clone `C:\Users\GT\Desktop\Claude\Civio`. Activate it
  there with `git config core.hooksPath .githooks`, then check with
  `entire status` (see `ENTIRE.md`).
