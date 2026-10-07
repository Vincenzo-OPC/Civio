# Civio Codex Build Brief

**Copy this entire file into Codex as one prompt.**

---

## For GT (plain language)

1. Civio is your Philippine Civil Service Exam study app (tutor: Dexter). Not official CSC.
2. Codex builds from the MSI desktop tree, which replaced GitHub `main` as the baseline `d3f0368` (done; tag `baseline`).
3. First: fix cheating/scoring bugs, remove dangerous routes, rebrand to Civio, green the linters.
4. Then: port the MSI-only UX (timers, tutor loop, remove Mock button), then lay the adaptive-learning foundation.
5. Keep the MSI local study app on `localhost:8080` working; never touch Hermes on port 8642.

---

## Hard decisions (do not reopen)

- **Brand:** `Civio` (Title Case). Lowercase only in identifiers (`civio`, `civio.ph`, env prefixes). Tutor name: **Dexter**. Disclaimer: not official CSC.
- **Starting tree:** GitHub `main` will be replaced by the MSI desktop tree. **Begin only from that tree.** If `main` has not been replaced yet, **STOP** and say so — do not commit on the old audited snapshot (`1302608`).
- **Protect local study:** The desktop study app on the MSI (Docker, `localhost:8080`) stays the stable study app. Do not break it. **Never touch Hermes on port 8642.**
- **Hosting (free-first):** Keep Laravel. Target: Google Cloud Run (scale to zero, instance cap, budget alert) + Neon free Postgres + Cloudflare (DNS/CDN, Turnstile, analytics, optional AI gateway).
- **AI:** Optional. Server-side provider abstraction (Gemini, OpenAI, Grok/xAI, Claude, local/stub). **Never** expose API keys client-side (`VITE_` secrets forbidden).

**Repo:** `Vincenzo-OPC/Civio`. **Audit map:** historical only, in git history (`912d318:docs/CIVIO_AUDIT_AND_PLAN.md`); current state is `docs/CODEX_HANDOFF_PLAN.md`. **Desktop patch list:** `/workspace/civio-audit-report/DESKTOP_PATCHES_TO_PORT.md` (also copy into `docs/DESKTOP_PATCHES_TO_PORT.md`).

---

## Gate 0 — Confirm starting tree

Before any commit:

1. Confirm GitHub `main` is the MSI desktop tree (not only `1302608` audit snapshot).
2. If not replaced → **STOP**. Report: "Desktop tree has not replaced main yet. Waiting."
3. If replaced → proceed Phase 0 → desktop ports → Phase 1 → question bank → checklists.

Work in small logical commits. Normal pushes only. **Never force-push** after the initial desktop replacement.

---

# PHASE 0 — Fixes first (do these before new features)

Do in roughly this order. Exact paths are relative to the repo root.

## P0.1 Server-side scoring (Critical)

**Stop trusting the client score.**

- `app/Actions/Exam/SubmitExamAttemptAction.php` — recompute score and `cat_scores` from the question bank + submitted answers. Ignore client-supplied scores for persistence.
- `app/Http/Requests/User/Exam/StoreExamAttemptRequest.php` — stop accepting authoritative client `cat_scores`; validate answer payload shape only.
- Add Pest tests: forged 100% POST must not store a perfect score.

## P0.2 Withhold answers until after submission (Critical)

- `app/Http/Resources/ExamQuestionResource.php` — for live exam play, **do not** send `correct_option` or `explanation`. Expose them only on review/scorecard after the attempt is submitted and server-graded.
- Update frontend exam hooks that currently expect keys in pool props (`use-exam-pool-builder.ts`, submission/hydration hooks) accordingly.

## P0.3 Fix shuffle / review bug (Critical)

Store answers keyed by **question ID** and **option ID** (or original option index), **not** live shuffled position.

Touch:

- `resources/js/pages/user/exams/hooks/use-exam-hydration.ts`
- `resources/js/pages/user/exams/hooks/use-exam-pool-builder.ts` (`shuffleOptionsForQuestion`)
- `resources/js/pages/user/exams/hooks/use-exam-submission.ts`
- `resources/js/pages/user/exams/hooks/use-exam-persistence.ts` (if present)
- `app/Services/ExamAttemptFormatter.php`
- `app/Services/DeterministicAnalysisService.php`

Acceptance: after option shuffle, Reveal / wrong-list / scorecard match the actual chosen option. Add regression tests (frontend unit and/or Pest feature).

## P0.4 Remove open clear-cache route

- `routes/web.php` — delete `GET /clear-cache-temp-route` (approx lines 71–76).

## P0.5 Lock or remove browser migration buttons

- `app/Http/Controllers/Admin/SystemController.php` — remove or hard-disable `runMigrations` / `rollbackMigrations`.
- `routes/web.php` — remove `run-migrations` / `rollback-migrations` admin routes (or gate to CLI-only ops; no browser artisan migrate).

## P0.6 User custom questions must not go live in shared bank

- `app/DTOs/Drill/StoreCustomQuestionData.php` — default `status` to `draft` / private ownership, **not** `'active'`.
- `app/Services/DrillService.php` (`createCustomQuestion`) — do not bust global active-pool cache into guest/shared bank for user-authored items.
- Ensure only admin/moderation can promote to shared `active`.

## P0.7 Stop deleting a user's questions on user delete

- Migration: `database/migrations/2026_05_24_025354_create_questions_table.php` has `created_by` → `cascadeOnDelete()`.
- Add a new migration: change `questions.created_by` to `nullOnDelete()` (or `restrict`), and set `created_by` nullable if needed. Preserve bank content when a user account is deleted.

## P0.8 Replace or remove AdSense / ads.txt / donation links

- `resources/views/app.blade.php` — remove AdSense script (`ca-pub-2027977096641438`) unless GT provides a Civio publisher id.
- `public/ads.txt` — replace with GT's publisher line or delete.
- `resources/js/components/shared/support-widget.tsx` — remove BuyMeACoffee / legacy GCash/Maya/BMC QR links unless GT supplies replacements.
- `public/googleca999b3ae7424c1b.html` — delete (old Search Console verify).
- Keep product functional without monetization scripts.

## P0.9 Fix toolchains (CI must go green)

Fix until these pass:

- `npm run types:check` — fix Announcement `last_checked_at` drift in `resources/js/pages/admin/announcements/index.tsx`
- `npm run lint:check` — fix rules-of-hooks in `resources/js/hooks/use-content-shield.ts` (and related)
- `npm run format:check` / Prettier
- `vendor/bin/pint --test` — fix `seed_sample_questions.php`, `seed_topup_questions.php`
- `php artisan test` — keep Pest green (205+ tests)
- `npm run build` — must succeed

Address `composer audit` / `npm audit` **high** advisories with safe upgrades. Pick **npm** as canonical; drop unused `pnpm-lock.yaml` / `pnpm-workspace.yaml` unless actively used.

## P0.10 Code-split the ~3 MB bundle

- `resources/js/app.tsx` — stop `import.meta.glob(..., { eager: true })`; lazy-load Inertia pages.
- Split exam/admin heavy routes so initial JS is not ~3 MB eager.

## P0.11 Rebrand to Civio

Replace leftover old-brand and all-caps CIVIO strings (done; see `docs/CHANGES_SINCE_BASELINE.md`). Priority list:

| Area | Paths |
| --- | --- |
| Manifest / PWA | `public/manifest.json` → name `"Civio"`; `public/sw.js` precache Civio assets |
| Blade / favicon | `resources/views/app.blade.php`, `public/favicon.svg` |
| Logos | `public/images/*`, `resources/js/components/layout/app-logo-icon.tsx`, scorecard/printable watermarks |
| PDF / print | `resources/js/pages/user/exams/components/printable-exam.tsx`, `scorecard-view.tsx` |
| robots | `public/robots.txt` → `https://civio.ph/sitemap.xml` |
| localStorage keys | migrate legacy keys → `civio_*` with one-time read of old keys (`lib/legacy-storage.ts`) |
| Docker / seeds | `docker-compose.yml`, `env.docker.example`, `seed_sample_questions.php` (`admin@civio.local`) |
| Tests / composer | `tests/Unit/AiGatewayServiceTest.php`, `composer.json` name → `civio/app` (or similar) |
| Dockerfile | `APP_NAME` → `"Civio"` |
| Sidebar / copy | Title Case Civio; tutor **Dexter**; not-official-CSC disclaimer |

## P0.12 Docs

- Rewrite `README.md` for Civio (setup, Docker, guest mode, disclaimer).
- Refresh `.env.example` / `env.docker.example` with Civio prefixes and hosting notes (Cloud Run + Neon + Cloudflare).
- Add short `docs/SETUP.md` and `docs/DEPLOY.md` (Cloud Run scale-to-zero, max instances, budget alert, Neon, Cloudflare Turnstile).
- Copy desktop patch tracker into `docs/DESKTOP_PATCHES_TO_PORT.md`.

### Phase 0 acceptance

- [ ] Server grades attempts; forged client score rejected
- [ ] Live exam JSON has no `correct_option` / `explanation`
- [ ] Shuffle → Reveal / analytics correct (ID-keyed answers)
- [ ] `/clear-cache-temp-route` gone
- [ ] No browser migrate/rollback
- [ ] Custom user questions default draft/private
- [ ] Deleting a user does not wipe their authored questions from the bank
- [ ] No legacy AdSense/donation accounts
- [ ] tsc, eslint, prettier, pint, pest, build all green
- [ ] Bundle code-split (no 3 MB eager app chunk)
- [ ] UI/docs say **Civio** / **Dexter**; not official CSC
- [ ] README + `.env.example` + setup/deploy docs present

---

# PHASE 0.5 — Port desktop-only patches

Source of truth: MSI tree + `docs/DESKTOP_PATCHES_TO_PORT.md`. Do not mark PORTED until cherry-picked from MSI and covered by tests.

| Patch | Action |
| --- | --- |
| Mock button removed | Remove/rename sidebar **"Mock Exams"** entry in `resources/js/components/layout/app-sidebar.tsx` (and related guide copy) per MSI UX |
| Tutor loop with study bias | Port Dexter/tutor study-bias loop from MSI |
| Exam countdown | Session timers already aim for Pro **3h10m / 150** (`11400s`) and Sub **2h40m / 145** (`9600s`) in `resources/js/pages/user/exams/utils/exam-utils.ts` — re-verify vs MSI |
| Per-item clock + urgency | Port per-question clock with **green / amber / red** urgency colors from MSI (not on audited GitHub) |
| Guest unlimited | Re-verify `config/civio.php` / `CIVIO_GUEST_UNLIMITED` vs MSI |
| Demographics omitted | Re-verify `includeDemographics = false` in pool builder |
| Incomplete-class / cache | Re-verify `QuestionRepository::getActivePool` vs any MSI extras |
| Sirit / Reveal after shuffle | Closed by P0.3 — still verify on MSI data |
| `'??'` lost math operators | Flag + fix in bank pass (Phase bank); preserve `÷ × − ₱` through import/render/Dexter `plain()` |

### Desktop-port acceptance

- [ ] No unwanted Mock Exams CTA (per MSI)
- [ ] Tutor loop + study bias works without keys (stub) and with provider when configured
- [ ] Countdown matches Pro 3h10m/150 and Sub 2h40m/145
- [ ] Per-item clock shows green→amber→red urgency
- [ ] Guest unlimited + demographics behavior matches MSI
- [ ] Each item marked PORTED in `docs/DESKTOP_PATCHES_TO_PORT.md` with a test

---

# PHASE 1 — Foundation (after Phase 0 + desktop ports)

## P1.1 Product shell + design tokens

- Civio shell: layout, typography, color tokens (Tailwind 4 / shadcn), dark mode.
- Consistent Civio logo, Dexter presence, not-CSC footer disclaimer.

## P1.2 Responsive mobile nav

- Working mobile nav (hamburger / sheet); usable exam + drills on narrow viewports.
- Verify with mobile viewport (Chrome device mode or real device).

## P1.3 PWA

- `public/manifest.json` — Civio name, icons, theme.
- Icons under `public/icons/` (Civio art).
- Safe service worker: **versioned cache**, update prompt, **no stale questions** (never cache exam JSON/answer keys as immutable forever; bump cache on deploy).
- Network-first HTML; skip auth routes; precache only Civio assets.

## P1.4 Learning event table

Append-only `learning_events` (`user_id` nullable, `session_id`, `type`, `payload` jsonb, `created_at`).

Event types (minimum):

`session_started`, `session_ended`, `question_presented` (alias `item_shown`), `answer_submitted`, `answer_changed`, `item_flagged`, `explanation_opened`, `confidence_recorded`, `hint_requested`, `tutor_message_sent`, `mock_exam_started`, `mock_exam_completed`, `review_started`, `schedule_task_done`, `module_completed`.

Attempts remain authoritative for scores (server-graded). Events feed mastery — not a full event-sourcing rewrite.

## P1.5 Knowledge taxonomy

Hierarchy:

`Exam (Professional | Subprofessional) → Domain → Competency → Concept → Micro-skill → Archetype → Question`

- Backward-compatible migrations: keep existing `categories` / `subcategories` / `questions` working while new tables (or columns) map onto them.
- Do not break current drills/mocks while migrating.

## P1.6 Learner state

- **Raw:** learning events + attempt rows.
- **Derived:** mastery by competency/concept, review due dates, readiness proxy, seen/wrong sets.
- Store snapshots in `learner_states` (or evolve existing analysis tables), recomputed server-side — never from client `cat_scores`.

## P1.7 Question metadata

Extend questions with (migrate carefully):

- provenance (author, source, import_batch)
- difficulty, estimated time
- distractor reasoning
- status workflow: `curated | generated | reviewed | approved | deprecated` (map from today's `active|draft` over time)

## P1.8 AI provider interface stubs

Server-only interface, e.g. `TutorProvider`:

`explain_answer`, `generate_hint`, `classify_mistake`, `summarize_session`, `generate_question_draft`, `moderate_text`

Implementations: Stub (default), Gemini, OpenAI, Grok/xAI, Claude, local/Workers AI. Route via existing gateway patterns. Keys only in server env. Features degrade cleanly when AI is off.

## P1.9 Civio Today dashboard foundation

Dashboard cards (auth + sensible guest empty states):

- Readiness snapshot
- Today's training
- Due reviews
- Focus concepts

Wire to learner state + schedules; no fake client scores.

### Phase 1 acceptance

- [ ] Shell + tokens + mobile nav usable on phone viewport
- [ ] PWA installable; SW versioned; no stale question bank cached forever
- [ ] `learning_events` writing for core exam/drill flows
- [ ] Taxonomy tables/migrations exist; old exams/drills still work
- [ ] Learner state derived server-side; review dues computable
- [ ] Question metadata fields present; status workflow usable for new items
- [ ] AI stubs compile; stub works with zero keys; no client secrets
- [ ] Civio Today shows readiness / today / dues / focus (even if early heuristics)

---

# PHASE BANK — Question bank export / import

1. Export **all** existing questions (baseline pool + GT-added items, told apart by `questions.source_group`) to a portable JSON with **stable IDs**, stem, options, correct key, explanation, category/subcategory (and new taxonomy IDs when ready), status, provenance.
2. Import into the new taxonomy without losing items.
3. **Known bug flag:** some explanations show `'??'` where math operators (`÷ × −`) were lost — detect, fix, and add a content QA check so re-import does not reintroduce mangling.
4. Preserve Unicode currency/operators through seed, API, Dexter `plain()`, and React render.

### Bank acceptance

- [ ] Round-trip export → import preserves count and stable IDs
- [ ] No unexplained `'??'` operator loss in sampled math items
- [ ] Import attaches items into taxonomy without breaking active pool

---

# Workflow rules (always)

1. **Small logical commits** (one concern per commit).
2. Before each push: `pint` / `prettier` as needed, `npm run types:check`, `npm run lint:check`, `npm run build`, `php artisan test`.
3. **Normal pushes only.** Never force-push after the initial desktop→`main` replacement.
4. Verify **mobile viewport** and **persistence** (exam resume / localStorage migration) after UI changes.
5. **No secrets in builds** — spot-check built assets; never put provider keys in `VITE_*`.
6. **Guest mode** works without mandatory login (`CIVIO_GUEST_UNLIMITED` deliberate).
7. Do not break MSI `localhost:8080` study Docker; never touch Hermes `:8642`.
8. Prefer fixing in place over large rewrites; keep Laravel.

---

# Suggested commit sequence

1. chore: confirm desktop tree base / docs pointer  
2. security: server-side grading + withhold exam keys  
3. fix: ID-keyed answers + shuffle/review regression tests  
4. security: remove clear-cache + browser migrations  
5. fix: custom questions draft + nullOnDelete for created_by  
6. chore: remove legacy ads/donations  
7. chore: green tsc/eslint/prettier/pint + audit highs  
8. perf: lazy Inertia pages / code-split  
9. chore: rebrand to Civio + docs  
10. feat: port MSI mock-button / tutor-loop / per-item clock  
11. feat: learning_events + learner_states foundation  
12. feat: knowledge taxonomy migrations (compat)  
13. feat: question metadata + AI provider stubs  
14. feat: Civio Today dashboard foundation  
15. chore: question bank JSON export/import + `??` QA  

---

# Out of scope for this brief

- Capacitor / native apps  
- Rewriting off Laravel to a static SPA  
- Touching Hermes (port 8642)  
- Force-pushing history after desktop lands  
- Reopening brand or hosting stack decisions  

---

*End of brief. Execute Gate 0 first; then Phase 0 → 0.5 → 1 → Bank. Report blockers instead of inventing new product decisions.*
