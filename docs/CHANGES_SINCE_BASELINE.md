# Changes since baseline

The living record of how Civio differs from the baseline (commit `d3f0368`, tag
`baseline`) and the upstream code it was built from. Update it in the same commit
as any change that makes Civio behave differently from the baseline (see "How to
keep this current" below).

## Baseline

| | |
| --- | --- |
| Upstream repo | local fetch-only remote `upstream-baseline`, default branch `main` |
| Upstream tip checked | `7b9f6bbb638938f7ab8f75688bc3976ed1ce4c7c`, 25 Sep 2026 00:09 PHT, "fix(analytics): safely handle missing keys in ai analysis orchestrator" (checked 7 Oct 2026) |
| Where Civio forked | `e91c26d` (21 Sep 2026, "feat(ui): extract reusable AiModelSelect component…"). Civio's git history contains upstream history up to this commit. |
| Civio baseline | `d3f0368` (5 Oct 2026), tag `baseline`: upstream `e91c26d` plus GT's desktop study patches (`718763a` → `d3f0368`) |
| Civio versions | `v0.1.0-phase0` (`647e484`), `v0.1.5-phase0.5` (Phase 0.5 + Copy for AI + clone removal) |

**Upstream changes not in Civio:** none as of `7b9f6bb`. That last upstream
commit was **pulled in** on 7 Oct 2026 with `git cherry-pick -x` (see "Upstream
fixes pulled in" below).

**Diff size, upstream tip → Civio** (at `ba8c622`, before this doc and the changelog
tooling): 182 files, +20,040 / −10,936 lines. 84 added, 90 modified, 8 deleted.
Biggest areas by file count: `scripts/` (bank seeds), `app/`, `resources/js/pages/user/exams/`.

To see it yourself:

```bash
git remote add upstream-baseline <upstream repo URL>   # local only, ask GT for the URL
git remote set-url --push upstream-baseline DISABLED_read_only
git config remote.upstream-baseline.tagOpt --no-tags
git fetch upstream-baseline
git diff --stat upstream-baseline/main HEAD
git log --oneline upstream-baseline/main..HEAD     # Civio + desktop commits
git log --oneline HEAD..upstream-baseline/main     # upstream commits Civio lacks
```

## Summary by area

Commits are on `Vincenzo-OPC/Civio` `main`. "Desktop" means it arrived through
`d3f0368` from GT's MSI tree (see the desktop section).

### Security and scoring

| What changed | Why | Commits |
| --- | --- | --- |
| Scores are recomputed on the server from the bank (`ExamGradingService`); client `cat_scores` are ignored. | The baseline trusted the browser's score, so results could be forged. | `d19afda` |
| Live exam JSON no longer carries `correct_option` or `explanation` (`ExamQuestionResource` `$includeAnswerKey`). Keys come back only from `/exams/reveal` or after submit. | Answer keys were readable in page props during a mock. | `d19afda` |
| Answers are stored by question ID and original option index (`originalOptionIndices`); legacy position-keyed attempts still read. | Option shuffle made position keys and Reveal ("sirit") mark the wrong choice. | `d19afda` |
| Open `/clear-cache-temp-route` removed; browser migrate/rollback only with `CIVIO_ALLOW_BROWSER_MIGRATIONS` outside production. | Anyone could clear cache or run migrations from a URL. | `761a3bd` |
| User custom drill questions are saved as `draft`, not straight into the shared active pool. | Users could inject items into everyone's mocks. | `761a3bd` |
| Deleting a user nulls `questions.created_by` instead of cascading. | Deleting an account deleted bank questions. | `761a3bd` |

### Exam UX

| What changed | Why | Commits |
| --- | --- | --- |
| Demographic (EDQ) block dropped from mocks; Professional 150 / Subprofessional 145 scored items; Skip button for old sessions. | Mocks should start on scored items. | Desktop `224c42e` |
| Harder-biased, crypto-backed shuffle of the pool (`shuffleHardBiased`, `fisherYatesShuffle`). | Fresh mocks felt repetitive and easy. | Desktop `17073bb` |
| Mock pools use unique items only: no "(variant N)" clones, no exact copies, no cross-category padding. A short bank gives a shorter mock with a toast showing the real count. Pool logic now lives in pure `utils/mock-pool.ts`. | Clones inflated familiarity, not coverage. Replaces the desktop variant fill (`f807222`). | `ba88fa5` |
| Lite L1, server-picked mocks: `POST /exams/sessions` picks the mock on the server (`App\Services\Exam\MockPoolSelector`, a pure PHP port of the old client rules: unique items, blueprint quotas, weak-topic bias, no clones, no padding) and sends only those 150 / 145 items, keys still withheld. The picked IDs are stored in `exam_sessions`; submit is checked against them (only served items, one submit per session, owner only). `/exams` no longer ships the whole bank: only scorecard/retake items or a drill's subset. Client whole-bank pooling (`buildMockScoredPool`, `use-exam-pool-builder.ts`) removed. | The whole bank (~550 items) was downloaded on every exam page; server-side picking also stops mock-pool tampering. | `c825fe9` |
| Two clocks: "Exam left" countdown (3:10:00 / 2:40:00, amber ≤ 10 min, red ≤ 2 min, auto-submit at 0) and "This item" (amber 45–75 s, red > 75 s). Pure helpers in `lib/exam-clock.ts` with tests. | Pacing practice for the real exam. | Desktop `d3f0368`, `518ee08` |
| Reveal and Expound endpoints (`POST /exams/reveal`, `/exams/expound`); Reveal maps the original key index back to the shuffled option. | Learn after answering; fix wrong-choice Reveal. | Desktop `d3f0368`, `d19afda` |
| Home shows Start Pro · Start Sub Pro · Practice Drills; no "Try Mock Test" button or picker. | Fewer taps to start. | Desktop, guarded by `76f0542` |
| Content shield (blur/copy/print blocking) off when `CIVIO_CONTENT_SHIELD=false`, then reduced to a safe stub API (`use-content-shield.ts`). | It blocked study use, and its early return broke React's rules of hooks. | Desktop `095ef1b`, `acedd26` |
| Inline scripts in `app.blade.php` are plain JavaScript again. The desktop copy override had TypeScript casts (`as HTMLElement`, `as KeyboardEvent`), so browsers threw a SyntaxError and skipped the whole block, including the pre-paint system dark-mode check. Dark-mode detection now has its own `<script>`; the copy override runs as intended on exam pages and localhost but only intercepts copy, cut, contextmenu and selectstart (the old version would also have swallowed every keydown/keyup, breaking dialogs, forms and React key handlers). Pest checks the rendered scripts with `node --check` and runs the dark-mode logic. | Dark pages flashed light before the app loaded, and the copy override never ran. | `51c429b` |
| Mojibake punctuation fixed on the scorecard and submit dialog. | Garbled characters from a bad encoding pass. | `4f4eb21` |

### Study and tutor

| What changed | Why | Commits |
| --- | --- | --- |
| Guests study without limits (`CIVIO_GUEST_UNLIMITED`, `config/civio.php`, `AllowGuestStudy`); dashboard, drills, history and analytics readable as a guest; no Register wall after a free attempt; Subprofessional no longer bounces to an old attempt. | GT studies logged out; the one-attempt wall blocked practice. | Desktop `095ef1b`, `d3f0368`; tests `ce41c82` |
| Tutor loop: scorecard strengths/weaknesses → weak-area drill → next pool leans to misses (`lib/guest-study-bias.ts`). Now recorded from **server** grading and drills lean to weak subtopics. | Turn mistakes into the next session's practice. | Desktop `d3f0368`, `a4df9f8` |
| Dexter evaluation service (`app/Services/Dexter/DexterEvaluationService.php`): a basic rule check of an item against its stored key (answer-key conflict, ambiguity, confidence). | First piece of the Dexter tutor. | Desktop `d3f0368` |
| `TutorProvider` contract with `NullTutorProvider` default (Prism installed, no live tutor yet). | Seam for an AI tutor without vendor lock-in. | `9fe51a4` |
| FSRS spaced-repetition wrapper (`lib/review/fsrs.ts`, ts-fsrs), not wired to UI yet. | Groundwork for review scheduling. | `9fe51a4` |

### AI handoff

| What changed | Why | Commits |
| --- | --- | --- |
| "Copy for AI" button beside Reveal and in review; clean, semantic export formatter (`lib/ai-handoff.ts`) with tests. The key is included only when the item was revealed or the attempt is in review. | Let users paste an item into their own AI assistant without leaking live keys. | `3ab87d2`, `3ba17ab`; spec `29caf02`, `d62b7bc`, `1d4c96d` |

### Bank and seeds

| What changed | Why | Commits |
| --- | --- | --- |
| Local practice seeds and ~495 original CSE-style practice items (`scripts/seed_unique_cse_batch_2026-09-30.sql`, `…2026-10-03.sql`, `seed_cse_pack_200_2026-10-03.sql`) plus generators. Not official CSC items. | The baseline shipped no practice bank for local use. | Desktop `718763a`, `f807222`, `d3f0368` |
| Seed scripts moved to `scripts/seeds/` with a README. | Root was cluttered. | `e21d94c` |
| `??` lost math symbols: root cause (PowerShell 5.1 pipe), `client_encoding` in seed SQL, `scripts/import-sql-utf8.ps1`, and `php artisan civio:repair-bank-encoding`. | Stems showed `??` instead of × ÷ ₱ etc. | `22fc855` |
| `questions.source_group` (nullable, indexed; `App\Enums\QuestionSourceGroup`): existing rows tagged `baseline`, except post-baseline drafts (`civio`); questions created by the app default to `civio`; PHP seed scripts set `baseline`; `php artisan civio:tag-source-groups [--dry-run]` tags raw SQL seed rows. Never sent to the browser. Spec v0.1 Section 10 decisions recorded; re-parameterize workflow documented (`docs/QUESTION_SOURCE_GROUPS.md`). No question text changed. | Keep baseline items grouped for later re-parameterizing; new authored items stay drafts until approved. | `ac27f5a` |
| Seeder saves one copy per item; `php artisan civio:remove-variant-clones` deletes or archives old "(variant N)" clones; Postgres SQL for desktop DBs. | Clone filler questions removed (GT approved). | `d8406d8`, `4bce08e` |

### Branding

| What changed | Why | Commits |
| --- | --- | --- |
| Rebrand to **Civio** (Title Case) in UI, manifest, Blade SEO, README, Docker/env defaults, legal seeder; `civio_logo*.png`; one-time migration of legacy localStorage keys to `civio_*`. Not-official-CSC disclaimer kept; tutor stays Dexter. | Civio is GT's product. | `5fe2d40`, `6277c17` |
| Neutral Civio mark (violet tile, lime "C" and dot) replaces the inherited sun-and-shield art everywhere: `public/favicon.svg` and `images/civio-mark.svg` (under 300 bytes), PWA icons, maskable icons, apple-touch icon, `favicon.ico`, print/PDF logo. Old logo files deleted. Footer "Made with ♥ by …" author credit and link removed; footer split into small typed components. Legacy storage migration moved to `lib/legacy-storage.ts` and now also carries cookie consent, the drills tab and the in-tab back/exam-origin keys (sessionStorage), with JS tests. | One Civio identity; returning users keep their progress and choices. | `08b4640` |

### Performance and PWA

| What changed | Why | Commits |
| --- | --- | --- |
| Inertia pages lazy-loaded (no eager `import.meta.glob`), so routes split into chunks. | The main bundle was ~3 MB eager. | `6277c17` |
| Hand-written `public/sw.js` replaced by vite-plugin-pwa `injectManifest` (`resources/js/sw.ts`): exams, auth, dashboard and other sensitive routes are NetworkOnly; prompt-to-update. | Old SW risked caching exam payloads. | `9fe51a4`, `647e484` |
| Lite L0: PDF export (jspdf, html2canvas-pro) and the printable booklet load only when exporting/printing; realtime (Echo + Pusher) loads on demand via `lib/realtime.ts`; hero served as AVIF/WebP with PNG fallback; 3.5 KB logo mark for header and favicon; unused Instrument Sans web fonts and their 6 preloads removed; PWA precache trimmed to the app shell + critical routes, other hashed chunks cached on first use. | First-load JS was 436–496 KB gzip on every page; now 213–284 KB. Lighthouse mobile landing 70 → 85, exam 61 → 77. | `5ea1cd5` |
| Lite L1, Lite mode: auto-on for Save-Data or slow-2g/2g/3g, manual Auto/On/Off in Settings → Appearance plus a "Lite" switch on the dashboard and exam headers (`lib/lite-mode.ts`, `useLiteMode()`, `civio_lite` cookie, `html.lite` class). Lite turns off animations, transitions, blur and shadows, uses system fonts, skips the landing hero, shows analytics as text tables (recharts never loads), skips realtime, and skips the PWA precache unless the user opts into offline. Exams and drills get a text-first screen (question, choices, Reveal / Copy for AI / Next, palette behind "View all", large tap targets). With the cookie the server drops the realtime config, strips chart-only analytics fields, and defers the AI analysis on dashboard, analytics and exam pages. | Usable on cheap phones and prepaid 3G/2G data. | `c825fe9` |
| Sentry Laravel installed but inactive unless `SENTRY_LARAVEL_DSN` is set. | Opt-in error reporting. | `9fe51a4` |
| Lite L2, offline drill packs: `questions.offline_eligible` plus `php artisan civio:mark-offline-eligible [--dry-run]` (per category up to unique items minus 1.5x the largest mock quota; never demographics, clones or exact copies; deterministic, never unmarks). Offline items and their exact copies are excluded from strict mocks. Guest-friendly, always-throttled endpoints: `GET /offline/packs` (manifest), `GET /offline/packs/{category}` (40 per page, keys and explanations, ETag/304), `POST /offline/attempts` (server re-grades into `offline_practice_results`, rejects non-offline items without grading them and tampered keys, idempotent per `client_id`). Drills hub "Download for offline" panel (size in KB, version, Update pack, Remove, Online/Offline badge); `/offline` runner reuses the Lite drill screen with local Reveal and Copy for AI, queues answers in IndexedDB (`idb-keyval`) and syncs on open, after a drill and when back online; weak-topic stats update only from server verdicts. | Practise on cheap phones with no data, without leaking strict-mock keys. | `09c62da` |
| Service worker now served by Laravel at `/sw.js` with scope `/` (`ServiceWorkerController`, `Service-Worker-Allowed: /`, `no-cache`); precache URLs are absolute `/build/…`; old `/build/` registrations are removed on load. Before this the worker registered at `/build/sw.js` with scope `/build/` and controlled no page, so page and asset caching never ran. `/offline` has its own NetworkFirst cache. | Needed for any offline use; the page and asset caching planned in L0 now actually applies. | `09c62da` |

### Upstream fixes pulled in

| Upstream commit | What | Civio commit |
| --- | --- | --- |
| `7b9f6bb` (25 Sep 2026) | `AiAnalysisOrchestrator::resolveAnalysis` treats a non-array `analysis_json` as `[]` and defaults missing `subject_breakdowns`, `critical_weaknesses`, `top_strengths` (`[]`) and `readiness_index` (`0`) when merging fresh drill results. Applied cleanly; Pest coverage added in `tests/Feature/Services/AiAnalysisOrchestratorTest.php`. | `c6a173f` (message ends "cherry picked from commit 7b9f6bb…") |

### Docs, tests and agent setup

| What changed | Why | Commits |
| --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `ENTIRE.md`, `.entire/`; Entire hooks for Codex (`.codex/hooks.json`) and Claude Code (`.claude/settings.json`) plus committed git hooks in `.githooks/` (the earlier `.cursor/hooks.json` was dropped); docs for architecture, deploy, libraries, audit plan, build brief, question design spec, AI study system, AI product standard, external AI handoff, desktop patches. | Repeatable agent work and decisions on record. | `d66d2aa`, `5fe2d40`, `9fe51a4`, `e4e3d4c`…`1d4c96d`, `9ab859c`, `9f3891c`, `9bf7508` |
| Pest coverage for server scoring, Unicode round-trip, bank repair, clone removal, tutor stub; JS tests (`npm run test:js`) for clocks, study bias, home launchers, AI handoff, FSRS, mock pools, Lite mode. Pest for the server mock selector, mock sessions and Lite prop trimming. tsc/eslint green. | The baseline had no tests for these paths. | `d19afda`, `22fc855`, `4bce08e`, `ed5aa64`, `acedd26`, others above |
| `CHANGELOG.md` via git-cliff (`npm run changelog`), bundle budgets via size-limit (`npm run size`), `docs/LITE_MODE_PLAN.md`. | Track releases and page weight. | this doc's commit series |
| This file renamed to `docs/CHANGES_SINCE_BASELINE.md` ("Changes since baseline"); tag `baseline` added on `d3f0368` (the older baseline tag is left as is); the local read-only remote is now `upstream-baseline`. | One neutral name for the baseline everywhere. | `bc8d3dd` |

### Removed

| What | Why | Commits |
| --- | --- | --- |
| AdSense script, `public/ads.txt`, Search Console verify file. | No ads in Civio. | `e21d94c` |
| GCash / Maya / Buy Me a Coffee QR images and donation links in the support widget. | The baseline's donation channels don't belong in Civio. | `e21d94c` |
| Desktop debug junk: `_pw/` Playwright bundles, `_restore/` patch copies, debug PNG/HTML, `_php-shim`, `public/clear-exam.html` and `resume-exam.html`, `.bak-demo` files, pnpm lockfiles. | Not source code. | `e21d94c`, `ba8c622` |
| Hand-written `public/sw.js`. | Replaced by the generated SW. | `647e484` |
| Old fork notes, the archived README, the local patch log (folded into `docs/DESKTOP_PATCHES_TO_PORT.md`) and the pre-Phase-0 audit doc. README rewritten for Civio only; agent skills, build brief, backend guide, seed READMEs, SQL header comments and generator comments say Civio or baseline. The placeholder explanation in `seed_real_practice.php` no longer names another app or says to replace the items. | No other app names in the repo; the files stay in git history. | `a0019af` |

## Desktop-only patches that came in through `d3f0368`

These were made on GT's MSI desktop tree (Docker app :8080 / db :5433; paths and
container names in `docs/DESKTOP_PATCHES_TO_PORT.md`) between 21 Sep and 5 Oct 2026,
then pushed as the Civio baseline. Sources: `git log e91c26d..d3f0368`, the MSI note
`Local-Study-Patches.md`, and `docs/DESKTOP_PATCHES_TO_PORT.md` (the older fork notes
and patch log were folded in there and removed; they remain in git history).

| Commit | Date (PHT) | Patch | Status in Civio now |
| --- | --- | --- | --- |
| `718763a` | 21 Sep | Docker 8080/5433 compose + env, guest/shield fixes, exam persistence/hydration fixes, practice seed scripts | Kept; seeds moved to `scripts/seeds/` |
| `224c42e` | 23 Sep | Demographics optional on mocks, totals 150/145, Skip button | Kept |
| `17073bb` | 23 Sep | Harder-biased pool + crypto shuffle | Kept (now in `utils/mock-pool.ts` + `exam-utils.ts`) |
| `f807222` | 30 Sep | Fill mocks to 150 with "(variant N)" clones; first unique bank batch | Variant fill **removed** (`ba88fa5`); bank batch kept |
| `095ef1b` | 30 Sep | Unlimited guests, Subprofessional unblock, no Register wall, shield toggle | Kept |
| `d3f0368` | 5 Oct | Exam clocks, Reveal/Expound + shuffle-safe Reveal, scorecard strengths/weaknesses, guest study bias, guest-readable pages, Dexter evaluation service, more bank batches and repair SQL, plus debug junk | Kept and hardened in Phase 0/0.5; junk removed |

Container-only and data-only changes on the MSI are **not** in git and are not
reproduced by Civio: `replace_first_20.sql` applied to IDs 457–476 in the desktop DB,
the Docker autostart task, the desktop start shortcut, and any files
`docker cp`'d into the running container. The MSI DB still needs
`civio:repair-bank-encoding` and `civio:remove-variant-clones` (or the SQL in
`docs/DESKTOP_PATCHES_TO_PORT.md`).

## How to keep this current

1. Any commit or PR that makes Civio behave differently from the baseline updates this
   file in the same change: add or edit the row in the right area with what, why
   and the commit (use the short SHA after merging, or "this PR").
2. Before a release tag: `git fetch upstream-baseline`, then
   `git log --oneline HEAD..upstream-baseline/main` to list new upstream commits.
   Note each one under "Upstream changes not in Civio" or cherry-pick it.
3. Bump the "Upstream tip checked" row with the SHA and date you compared against.
4. Regenerate the changelog with `npm run changelog` (add `-- --tag vX.Y.Z` when
   cutting a release), then tag with an annotated tag and `git push origin <tag>`.
5. Never push to `upstream-baseline`; it is a local, read-only remote.
