# Civio Audit and Plan

**Repo audited:** `Vincenzo-OPC/Civio` @ `main` (`1302608`, 2026-09-23)  
**Audit date:** 2026-10-05 (Asia/Manila)  
**Scope:** read-only audit of GitHub `main`. No commits, no branches, no push.  
**Build base going forward:** GT will replace GitHub `main` with the newer MSI desktop Docker tree later. Phase 0 / product work should start from that desktop tree once it is pushed — not from current GitHub `main`. Treat this report as a map of what exists on GitHub today and what must be preserved or fixed when merging.

Brand spelling: product name is **Civio** (Title Case). Use lowercase `civio` / `civio.ph` only for package names, URLs, env prefixes, and identifiers. Avoid all-caps **CIVIO** in UI, metadata, README, and docs (current tree still uses all-caps in many places).

---

## Plain-language summary (non-engineer)

1. Civio is a Philippine Civil Service Exam study app (mocks, drills, lessons, calendar, analytics) with a tutor named Dexter; it is not official CSC software.
2. GitHub `main` already has early Civio renaming and guest unlimited practice, but the MSI desktop app still has newer unpushed patches (timers, tutor loop, more bugfixes).
3. On this box, PHP tests all passed (205), Vite build succeeded, but TypeScript check, ESLint, Prettier, and Pint failed — CI linter is already red on `main`.
4. Scoring is calculated in the browser and trusted by the server — anyone can POST a fake 100% score; answers are also stored against shuffled option indexes, so review and “wrong list” can lie after option shuffle.
5. The whole active question bank (with answers and explanations) is shipped to the browser on exam load — fine for a private study tool, bad if the bank is treated as secret.
6. A public “clear cache” URL and admin “run / rollback migrations” buttons are dangerous if this ever faces the internet with a leaked admin account.
7. Lots of Hiraya / Kenth leftover branding remains (logos, PDF watermarks, localStorage keys, Docker DB user `hiraya`, robots sitemap).
8. Keep Laravel for now on a free/cheap PHP host + Neon Postgres; pure static hosting cannot run this app without a large rewrite.
9. AI (Dexter, question generators) must stay optional and server-keyed; stub mode already works with no API keys.
10. Do not build on current GitHub `main`; wait for the MSI desktop tree to become the new `main`, then run Phase 0 cleanup there.

---

## 1. Executive Summary

`Vincenzo-OPC/Civio` is a Laravel 13 + Inertia/React/TypeScript (Vite) CSE reviewer historically forked from `codebykenth/hiraya-review`. GitHub `main` (216 commits; last push 2026-09-23) already includes partial Civio branding, Dexter explain, guest unlimited practice, demographics-off mocks, unique-stem sampling, and a moderated recalled-question queue. The MSI desktop Docker study app still sits ahead of GitHub with unpushed UX/timer/tutor patches and a larger (≈919) low-quality bank — **migration risk**.

Verified on this box (PHP 8.4.26, Node 20.19.2): `composer install` OK; `npm ci` OK; `npm run build` OK (~3.0 MB eager JS bundle); `php artisan test` / Pest **205 passed**; `tsc --noEmit` **failed** (2 errors); `eslint` **failed** (23 errors, incl. rules-of-hooks); Prettier **failed** (20 files); Pint **failed** (seed scripts). Composer audit: 34 advisories / 10 packages. npm audit: 5 issues (3 high). No committed `.env` secrets found. No `LICENSE` file; README_ARCHIVE still says proprietary.

**Health score: 5.5 / 10.** Architecture is mature for a study SPA, but client-trusted scoring, full answer leak in exam props, leftover Hiraya brand, and red lint/CI make it not production-ready as-is.

**Recommendation:** Keep Laravel. Run the existing Docker image on **Google Cloud Run** (request-based billing, scale to zero, max-instances cap, budget alert) + **Neon Free Postgres** + **Cloudflare** in front (DNS/CDN, Turnstile, Web Analytics, AI Gateway / Workers AI). Pay when traffic exceeds Cloud Run monthly free allowances or Neon's DB stops scaling to zero. Do **not** rewrite to static SPA yet.

---

## 2. Current Architecture

```
Browser (Inertia/React 19 + Vite)
  ├─ resources/js/pages/user/exams/*  (client mock builder, shuffle, timer, score)
  ├─ resources/js/pages/user/{dashboard,drills,learn,history,analytics,calendar}
  ├─ resources/js/pages/admin/*       (questions, learn, users, system, …)
  └─ public/sw.js + manifest.json     (PWA shell; network-first HTML)

Laravel 13 (PHP 8.3+/8.4)
  ├─ routes/web.php                   (public + auth.or.fail + admin)
  ├─ Controllers → Services → Repositories → Eloquent Models
  ├─ Actions (SubmitExamAttemptAction), DTOs, FormRequests, Policies
  ├─ Jobs (GenerateQuestions, GenerateLearnModule, GenerateUserAnalysis)
  ├─ Dexter ExplainQuestionService (stub | gemini/groq/openai/xai)
  └─ AiGatewayService (Cloudflare Workers AI / Gemini / Groq)

Postgres (prod intent) / SQLite (phpunit)
  questions, exam_attempts, categories/subcategories, learn_modules,
  study_schedules, saved_drill_sets, feedbacks, announcements, …
```

**Data flow (exam):**  
`QuestionRepository::getActivePool()` → `ExamService::getExamSessionData()` → `ExamQuestionResource` (includes `correct_option` + `explanation`) → Inertia `user/exams/index` → `useExamPoolBuilder` (track mix + option shuffle) → `useExamSubmission` (client grades) → `POST /exams/attempts` → `SubmitExamAttemptAction` (stores client `answers` + `cat_scores` verbatim) → scorecard / history / `DeterministicAnalysisService`.

Docker: `Dockerfile` (serversideup/php:8.4-fpm-nginx) + `docker-compose.yml` (app `:8080`, Postgres `:5433`). CI: `.github/workflows/tests.yml`, `lint.yml`.

---

## 3. Repository Health Score /10

| Area | Score | Notes |
| --- | --- | --- |
| Architecture / layering | 7.5 | Clear Controllers/Services/Repos/DTOs/Policies |
| Tests | 7.0 | 205 Pest tests green on sqlite memory |
| Frontend quality | 4.5 | Eager 3 MB bundle; hooks lint fail; tsc fail |
| Security | 3.5 | Client scoring; answer leak; clear-cache route; admin migrate |
| Branding readiness | 4.0 | Partial Civio; many Hiraya leftovers |
| Ops / free hosting fit | 5.5 | Docker present; PHP required; env examples OK |
| Docs | 6.0 | README strong; archive claims proprietary; no LICENSE file |
| **Overall** | **5.5** | Usable study fork; not ship-as-is |

---

## 4. Existing Stack

| Layer | Verified |
| --- | --- |
| PHP | Laravel 13.7, Fortify, Socialite, Wayfinder, Chisel, Passkeys, Pest 4, Pint |
| JS | React 19, Inertia 3, Vite 8, Tailwind 4, shadcn/Radix, Recharts, DOMPurify, jspdf, html2canvas |
| Auth | Email/password + Google/Facebook OAuth + 2FA + passkeys |
| DB | Postgres preferred (`DB_CONNECTION=pgsql`); tests force sqlite `:memory:` |
| Queue/Cache/Session | database drivers in `.env.example` |
| Realtime | Pusher (optional) |
| AI | Gemini / Groq / Cloudflare Workers AI gateway; Dexter stub default |
| PWA | `public/manifest.json`, `public/sw.js`, icons under `public/icons/` |
| Ads / monetization | AdSense loader in `resources/views/app.blade.php`; `public/ads.txt`; GCash/Maya/BMC in support widget |

---

## 5. Keep

- Layered PHP: Actions, DTOs, FormRequests, Policies, Repositories (`app/Repositories/*`).
- Exam UX core: pool builder track ratios (Pro Analytical / Sub Clerical), timers at official lengths (`EXAM_CONSTANTS` in `resources/js/pages/user/exams/utils/exam-utils.ts`).
- Guest unlimited flag (`config/civio.php`, `AllowFreeAttempt`).
- Dexter stub path (`app/Services/Dexter/ExplainQuestionService.php`) — AI optional.
- Deterministic analytics (`app/Services/DeterministicAnalysisService.php`) without paid AI.
- Syllabus seeder scope (`database/seeders/DatabaseSeeder.php`).
- Recalled-question moderation queue + NoHtml/NoProfanity rules.
- Pest feature coverage under `tests/Feature/{User,Admin,Auth,Public,…}`.
- Docker + `env.docker.example` for MSI local study.
- PWA shell concepts (but rebrand assets).
- Official-scope honesty already in README (“not affiliated with CSC”).

---

## 6. Remove / Replace

- Unauthenticated `GET /clear-cache-temp-route` (`routes/web.php:71-76`).
- Admin UI ability to `migrate` / `migrate:rollback` from the web (`SystemController`).
- Legacy Hiraya assets and strings (see §10); replace logos with Civio art.
- `composer.json` name still `laravel/react-starter-kit` — rename when packaging.
- Duplicate lockfiles: `pnpm-lock.yaml` + `package-lock.json` (pick npm; drop pnpm unless used).
- Eager `import.meta.glob(..., { eager: true })` in `resources/js/app.tsx:108` — move to lazy page loading.
- Client-authoritative `cat_scores` acceptance — replace with server grading (§7).
- Shipping `correct_option` + `explanation` in live exam props — withhold until review (§7).
- Seed scripts that create `admin@hiraya.local` / `password` (`seed_sample_questions.php`) from any production path.
- AdSense script until Civio owns the publisher account and policy review (currently still original pub id).
- `TransactionMiddleware` wrapping every mutating web request (fragile with queued jobs / nested transactions) — keep only where intentional.

---

## 7. Critical Bugs

| # | Bug | Evidence | Severity |
| --- | --- | --- | --- |
| B1 | **Client-trusted scoring.** Server stores `cat_scores` / answers from the client without recomputing from bank keys. Forged guest POST produced `attempt_id` with score 100 on this box. | `StoreExamAttemptRequest.php`; `SubmitExamAttemptAction.php`; verified via local sqlite POST `/exams/attempts` | **Critical** |
| B2 | **Option shuffle vs stored answer index.** `shuffleOptionsForQuestion` remaps `correct_option` (`use-exam-pool-builder.ts:12-35`) but persistence stores answers by live index; scorecard hydration reloads **unshuffled** bank questions (`use-exam-hydration.ts:96-99`) and compares `chosen === q.correct_option` (`:129`). Matches reported “Reveal marks wrong after shuffle”. | same files | **Critical** |
| B3 | **Wrong-question analytics key mismatch.** `ExamAttemptFormatter` indexes answers by list position; `DeterministicAnalysisService` uses `$answers[$qId]` (`:325`). Conflicting interpretations corrupt weakness lists. | `ExamAttemptFormatter.php` ~230; `DeterministicAnalysisService.php` ~325 | **High** |
| B4 | **Full answer key in exam payload.** `ExamQuestionResource` sends `correct_option` + `explanation` for every active item (`ExamQuestionResource.php:44-45`). With ~919 MSI items this is a large cheat channel. | ExamQuestionResource; confirmed 55 items × `correct_option` in local Inertia props | **High** |
| B5 | **Custom drills publish as `active`.** `StoreCustomQuestionData::toAttributes` sets `'status' => 'active'` and clears `questions.active` cache — any logged-in user can inject into the global pool. | `StoreCustomQuestionData.php:50`; `DrillService::createCustomQuestion` | **High** |
| B6 | **`'??'` / lost math operators in explanations.** Seed bank uses Unicode `÷ × − ₱` (`seed_real_practice.php`); Dexter `plain()` uses `strip_tags` + whitespace collapse only — encoding/transport or SVG/HTML path can still mangle operators (open MSI bug; root cause may be import/AI path, not verified end-to-end here). | seed_real_practice.php; ExplainQuestionService::plain | **High** (open) |
| B7 | **Announcement TS drift.** `last_checked_at` required in one Announcement type but missing when constructing modal state. | `tsc` errors in `resources/js/pages/admin/announcements/index.tsx:142` | **Medium** (blocks types:check) |
| B8 | **Content-shield hooks after early return.** `use-content-shield.ts` violates rules-of-hooks (17 eslint errors). | eslint log | **Medium** |
| B9 | **Pool builder file has excessive blank lines** around demographics block (style / maintainability). | `use-exam-pool-builder.ts` ~320+ | **Low** |

Official CSE timing/counts on GitHub main are already aligned for scored items (Pro 150 / 11400s; Sub 145 / 9600s; demographics omitted). Pass mark 80 used in history stats. Calculator policy is product/copy only — not enforced in code (N/A).

---

## 8. Security Problems

| Finding | File:line | Severity |
| --- | --- | --- |
| Unauthenticated cache wipe | `routes/web.php:71-76` (`clear-cache-temp-route`) | **Critical** |
| Client-trusted exam score / answers | `SubmitExamAttemptAction.php`; `StoreExamAttemptRequest.php:48` | **Critical** |
| Answer key + explanations in live exam JSON | `ExamQuestionResource.php:44-45` | **High** |
| Guest/user can spam `POST /exams/explain` (no auth; throttled only in production) | `routes/web.php:64-66`; rate limiters disabled when not production (`AppServiceProvider.php:71-96`) | **High** (cost/abuse) |
| Any verified user can publish questions straight into the global active bank (custom drill questions saved as `active`, rendered to all users incl. guests; SVG/HTML only regex-sanitized) | `routes/web.php:109`; `app/DTOs/Drill/StoreCustomQuestionData.php:50`; `DrillService::createCustomQuestion` | **High** |
| Root seed script creates `admin@hiraya.local` / `password` user if DB empty | `seed_sample_questions.php:15-19` | **Medium** (local tool; must never run in prod) |
| Deleting a user cascades to every question they authored; deleting a category cascades to subcategories → questions → users' drill attempts | `create_questions_table.php:16,23`; `create_exam_attempts_table.php:17` | **High** (data loss) |
| Public `POST /community/recalled-questions` (validated, moderated — OK intent; still abuse surface) | `routes/web.php:81-83` | **Medium** |
| Admin migrate / rollback from browser | `SystemController.php:36-58`; routes `run-migrations` / `rollback-migrations` | **High** (needs admin; catastrophic if account compromised) |
| AuthOrFail / admin failures return **404** (obscurity, not authz) | `AuthOrFail.php`; `EnsureUserIsAdmin.php` | **Low** (intentional UX) |
| Social login can link by email without proving ownership of existing password account | `AuthController.php:71+` | **Medium** |
| `User` fillable includes `role` | `User.php` Fillable list | **Medium** (mitigated if only validated fields used — Profile uses validated(); watch mass assignment) |
| `env()` outside config in request path | `HandleInertiaRequests.php:65` (`PUSHER_HOST`); `routes/web.php:46`; `SupportService.php`; `NoProfanity.php:108` | **Low/Medium** (breaks config:cache assumptions) |
| SVG sanitizer is regex-based, not a full SVG cleaner | `resources/js/lib/sanitize-svg.ts` | **Medium** (admin/AI SVG content) |
| Pagination labels via `dangerouslySetInnerHTML` | `admin/attempts/index.tsx:229` | **Low** (Laravel pagination HTML) |
| Global AdSense script with original publisher id | `app.blade.php:23`; `ads.txt` | **Medium** (account/ownership / policy) |
| Docker DB password `hiraya_local_dev` in compose (local only) | `docker-compose.yml:10-11` | **Info** (local) |
| No committed APP_KEY / API secrets found | `.gitignore` has `.env`; only `.env.example` in history | **OK** |
| Secrets in Vite build | Spot-check of `public/build/assets/app-*.js` — no API keys; false positives on CSS `mask-*` | **OK** |
| CORS | `bootstrap/app.php` appends `'cors'` on **api** group; app is mostly `web` session — not verified as misconfigured API CORS | **Not fully verified** |
| File uploads | No `UploadedFile` / `storeAs` usage found in `app/` | **OK / N/A** |
| Attempt ID enumeration | Guest scorecard gated by session `pending_guest_attempt_id` (`ExamAttemptService::getScorecardAttempt`); auth users scoped by `user_id` | **Mostly OK**; guest session fixation still possible if session stolen |

---

## 9. Technical Debt

### Critical
- Server-side grading + withhold keys until review.
- Normalize answer schema (always `{question_id: chosen_original_index}` or store shuffle map).

### High
- Split Inertia page graph (stop eager glob); code-split exam/admin.
- Fix rules-of-hooks in content shield; fix Announcement types.
- Custom questions → `draft` + ownership, never global `active`.
- Remove clear-cache route; gate system artisan behind CLI / very locked ops role.
- Dependency upgrades for composer/npm audit findings (guzzle, commonmark, dompurify, …).
- Dual package locks (`pnpm-lock.yaml` vs npm).

### Medium
- `TransactionMiddleware` on all writes.
- `selectRaw` date activity in DashboardService (driver-specific).
- `cascadeOnDelete` on `questions.created_by` / subcategory — deleting a user/category can wipe bank.
- Learn module `completed_by_user_ids` JSON array (not relational).
- Rate limiters no-op outside production — staging abuse.
- README/CI still assume all-caps CIVIO / old lint autofix habits.

### Low
- Seed script style (Pint failures).
- Extra blank lines in pool builder.
- Hard-coded track ids `selectedExamId === 1|2` in submission hook.
- `.agents/` skill pack referencing “Premium Hiraya Pattern”.

---

## 10. Legacy Branding Inventory

| Location | Legacy | Action |
| --- | --- | --- |
| `public/images/hiraya_logo.png`, `hiraya_logo_cropped.png` | filenames + art | Replace with Civio logos; keep files only if license requires archival |
| `resources/views/app.blade.php:36` | favicon → hiraya_logo_cropped | Civio icon |
| `public/favicon.svg` | embeds hiraya image | Replace |
| `public/sw.js:8-9` | precaches hiraya images | Civio assets; cache name already `civio-v1` |
| `public/manifest.json` | name/short_name `"CIVIO"` | → `"Civio"` |
| `public/robots.txt:4` | `https://hirayareview.com/sitemap.xml` | → `https://civio.ph/sitemap.xml` |
| `resources/js/components/layout/app-logo-icon.tsx:9` | hiraya image | Civio |
| `resources/js/pages/user/exams/components/printable-exam.tsx` | watermarks `HIRAYA REVIEW`, logo paths | Civio watermarks |
| `resources/js/pages/user/exams/components/scorecard-view.tsx:796` | hiraya logo | Civio |
| localStorage / events | `hiraya_cookie_consent`, `hiraya_drills_active_tab`, `hiraya_previous_location`, `hiraya:export-pdf` | migrate keys with one-time read of old keys |
| `docker-compose.yml` / `env.docker.example` | user/password/volume `hiraya*` | rename to `civio_*` (local only) |
| `seed_sample_questions.php:17` | `admin@hiraya.local` | `admin@civio.local` |
| `tests/Unit/AiGatewayServiceTest.php` | gateway id `hiraya-gateway` | `civio-gateway` |
| `README.md:279` | “Built by Kenth / codebykenth” | Keep as **required attribution** until license clarified; do not erase credit |
| `site-footer.tsx` | link `kenthalexisosila.dev`, name | Keep attribution or move to Credits/About |
| `support-widget.tsx` | BMC `buymeacoffee.com/kenthalexisosila`; `public/images/gcash-qr.png`, `maya-qr.png`, `bmc-qr.png` (donation QR codes, very likely the original author's personal accounts — not verified) | Remove or replace with Civio-owned accounts; donations currently would not reach GT |
| `resources/views/app.blade.php:23`, `public/ads.txt` | AdSense publisher `ca-pub-2027977096641438` / `pub-2027977096641438` (original owner's) | Remove until Civio has its own AdSense account; ad revenue currently goes to that publisher |
| `public/googleca999b3ae7424c1b.html` | Google Search Console verification file of previous owner | Delete; verify civio.ph with GT's own account |
| `.agents/skills/unique-ui-designer/SKILL.md` | “Premium Hiraya Pattern” | Civio |
| `composer.json` | `laravel/react-starter-kit` | `civio/app` or similar |
| Dockerfile `ENV APP_NAME` | `"Civil Service Exam Reviewer"` | `"Civio"` |
| App strings / phpunit `APP_NAME=CIVIO` | all-caps | Title Case **Civio** in UI; env may stay token |

### License / legal notices that must stay

- **No `LICENSE` file** in `Vincenzo-OPC/Civio` (GitHub `licenseInfo: null`).
- `README_ARCHIVE.md` §License: “This project is proprietary software. All rights reserved.”
- Upstream `codebykenth/hiraya-review` also has **null** license on GitHub.
- **Not verified:** written assignment / permission for the Vincenzo-OPC fork beyond existing public clone. Until clarified, **retain author attribution** (Kenth Alexis Osila / codebykenth) in About/Credits and do not strip copyright-looking notices in PDFs without legal review.
- Laravel / MIT dependencies keep their upstream notices via Composer/npm license metadata — do not vendor-strip.

Product brand going forward: **Civio** (Civil Service Intelligence OS), domain **civio.ph**, tutor **Dexter**, disclaimer **not official CSC**.

---

## 11. Database / Data Model

Core tables (from migrations):  
`users` (+ 2FA, OAuth, pdf flags, terms, is_active), `categories`, `subcategories`, `questions` (stem, options jsonb, correct_option, explanation, status active|draft, created_by), `exam_attempts` (nullable user_id, question_ids, answers, cat_scores), `track_configs`, `learn_modules` (+ completed_by_user_ids json), `study_schedules`, `exam_dates`, `user_ai_analyses`, `role_permissions`, `feedbacks`, `announcements` (+ last_checked_at), `legal_contents`, `saved_drill_sets` / `saved_drill_items`, `recalled_questions`, passkeys, cache/jobs/sessions.

**Gaps vs proposed knowledge model (§21):** no Domain/Competency/Concept/Micro-skill/Archetype tables; no provenance or curated/generated/reviewed/approved/deprecated workflow beyond `active|draft` + recalled queue; attempt events are not an event log — only aggregate attempt rows.

---

## 12. Existing Learning Logic

- **Mocks:** client builds Pro/Sub pools with category quotas (~45 Verbal, 52 Analytical or 47 Clerical, 45 Numerical, 8 GI); prefers unique stems; 30% wrong-priority resampling; option shuffle.
- **Drills:** category/subcategory/language filters; saved sets; smart weakness route; custom questions (unsafe active — §7).
- **Learn:** published modules by slug; completion toggle for auth users.
- **Calendar / study plan:** schedules, templates, suggestions (`StudyPlanAnalyzer`, `StudyPlanTemplateService`).
- **Analytics:** history KPIs, charts, deterministic readiness; optional AI analysis job/report.
- **Dexter:** post-answer explain endpoint; stub without keys.
- **Guest:** unlimited when `civio.guest_unlimited`; else one pending guest attempt in session.

**Not in GitHub main (MSI ahead):** per-item clock + urgency colors; tutor loop / study bias; possibly further repository/hydration fixes — see desktop patch list below.

---

## 13. UI/UX

- shadcn + Tailwind 4; dark mode; sonner toasts; Recharts analytics; large exam views (`live-exam-view.tsx` ~1.2k lines, `review-exam-view.tsx` ~1.6k).
- Sidebar still labels **Mock Exams**.
- Content shield overlay for copy protection (hooks bug).
- Support widget with QR donations (legacy BMC).
- Traffic overload guard for 429.
- How-it-works / terms / cookie consent (cookie key still hiraya_*).

---

## 14. Mobile

- Responsive Tailwind layouts; `use-mobile` hooks; viewport meta; apple-mobile-web-app meta.
- **Not verified:** real-device QA, touch timer UX, or Capacitor builds (none in repo).

---

## 15. PWA

- `manifest.json` (standalone, icons, theme `#0f172a`) — names still all-caps CIVIO.
- `sw.js`: precache shell; cache-first `/build/assets/`; SWR images; network-first HTML; skips auth routes.
- Precache still lists hiraya logos.
- **Not verified:** Lighthouse PWA score; offline exam taking (HTML network-first only caches successful public pages).

---

## 16. Deployment

- Dockerfile multi-stage-ish: composer --no-dev, npm ci && build, drop node_modules; ServerSideUp entrypoint `scripts/00-laravel-deploy.sh` (migrate --force).
- `conf/nginx/nginx-site.conf` (Render-oriented listen 80).
- GitHub Actions: tests matrix PHP 8.4/8.5; linter runs pint + prettier write + eslint (recent **linter failures** on main).
- Needs PHP runtime + Postgres + env secrets; not a static host.

---

## 17. Cost at 100 / 1k / 10k users

Rough estimates for the §18 stack (Cloud Run + Neon + Cloudflare free tiers). AI off by default. **Estimates, not quotes**; USD→PHP ≈ 58. Assumption: ~20 sessions/user/month, ~60 requests/session, ~0.1 vCPU-s/request, 512 MiB container.

| Scale (MAU) | Requests/mo | Est. monthly | What costs money |
| --- | --- | --- | --- |
| **100** | ~0.1M | **₱0** | Nothing — well inside 2M req / 180k vCPU-s free; Neon scales to zero most of the day |
| **1k** | ~1.2M | **₱0 – ₱600** | Usually still inside Cloud Run free tier; Neon may exceed 100 CU-h if the DB is awake >~13 h/day (Launch ≈ $0.106/CU-h); egress from Asia region is billed beyond small allowances |
| **10k** | ~12M | **≈ ₱3k – ₱6k** (~$50–100) | Cloud Run ≈ $25–35 (CPU + requests over free); Neon Launch ≈ $20–45; egress ≈ $5–30 depending on payload size; Sentry/analytics stay free if within quotas |

Big cost lever: today `/exams` ships the **entire active bank with answers** in Inertia props (verified: all items + `correct_option` + `explanation`). With ~919 items that is roughly 0.3–0.9 MB per exam page load (estimate from ~350 B/item measured on 55 seeded items; real items are longer). Fixing that (§7 B4) cuts egress and CPU sharply. Live Dexter AI adds token cost; keep stub/Workers AI free allocation by default.

---

## 18. Recommended Free Hosting Stack

**One recommendation: keep the Laravel monolith; deploy the existing Docker image to Google Cloud Run + Neon Postgres, fronted by Cloudflare.**

| Concern | Choice | Free-tier limits (checked 2026-10-05; re-verify at signup) | Pay trigger |
| --- | --- | --- | --- |
| Host | **Google Cloud Run** (request-based billing, min-instances 0, max-instances 2–3, budget alert) | 2M requests, 180k vCPU-s, 360k GiB-s per month, per billing account | Sustained >~1.5–3k MAU, or min-instances ≥1 to kill cold starts |
| DB | **Neon Postgres** (Singapore region) | 100 CU-hours/project/month, scale-to-zero after 5 min, 0.5–1 GB storage/project (Neon docs disagree at time of check), 5 GB egress | DB awake most of the day, storage >free cap, need PITR >6 h |
| Auth | **Keep Laravel Fortify + Socialite** (already built, 2FA, passkeys) | $0 | None |
| Storage | None needed now; **Cloudflare R2** if uploads/PDF archival appear | 10 GB free (verify) | Large media |
| Analytics | **Cloudflare Web Analytics** (cookieless) | Free | Need funnels → PostHog free tier |
| Error tracking | **Sentry** Developer plan (Laravel + React SDKs) | ~5k errors/month (verify) | Higher volume / team seats |
| AI gateway | **Cloudflare AI Gateway** (+ Workers AI daily free allocation); provider keys only in server env | Gateway free; Workers AI free daily neurons (verify) | Live Dexter at scale / premium models |
| Email | Resend or Brevo free tier for verify/reset mail | ~100–300/day (verify) | Volume |

Required runtime changes (Phase 1, not done): `SESSION_DRIVER=cookie` or database on Neon; `QUEUE_CONNECTION=sync` (or Cloud Tasks) because scale-to-zero has no resident worker; `CACHE_STORE=database`/file; run migrations as a Cloud Run Job, not on container boot; config:cache safe (remove `env()` calls outside config).

**Why not the others:** Render free web spins down after 15 min (~1 min cold start) and free Render Postgres **expires after 30 days** — not a system of record. Fly.io/Railway have no real free tier for new accounts. Oracle Always Free VM is $0 but you run the server yourself (patching, backups, account-reclaim risk). Static SPA + Supabase/Turso + serverless would mean rewriting Inertia, policies, admin, jobs and ~205 tests — high migration cost for no gain at 100 users.

**Migration difficulty:** Low–medium. Dockerfile already exists (serversideup php-fpm-nginx on 8080); work is env wiring, sessions/queue choice, a migration job, and Cloudflare DNS for civio.ph. Cloud Run needs a GCP billing account (card on file) — set a budget alert and max-instances cap so a traffic spike cannot run up a bill.

---

## 19. Future App Strategy

1. **Web** (Laravel + Inertia) — now.  
2. **PWA** harden (Civio icons, offline review shell, install prompt) — after branding.  
3. **Capacitor / TWA** — only if install metrics demand; wrap same URLs; no native rewrite first.

---

## 20. Proposed Architecture (target)

- Laravel API + Inertia web as system of record.
- **Server grading service** for attempts; exam play payload without answers.
- Optional Dexter via provider interface (§24).
- Event table for learning telemetry (§23) feeding derived learner state (§22).
- Knowledge graph tables (§21) gradually replacing flat category/subcategory-only bank.
- Cloudflare in front (CDN, WAF, Turnstile); Neon PG; queue worker when AI/jobs used.

---

## 21. Knowledge Model

Target hierarchy:

`Exam (Professional | Subprofessional) → Domain → Competency → Concept → Micro-skill → Archetype → Question`

Question metadata: stem/options/key/explanation; language; difficulty; bloom; calculator_forbidden; provenance (author, source_url, license, import_batch); states **`curated | generated | reviewed | approved | deprecated`**; replaces binary active/draft over time. Recalled queue feeds `generated/reviewed` only after editor approval.

---

## 22. Learner Model

- **Raw:** learning events (§23), attempt rows, schedule completions, learn toggles.
- **Derived:** mastery by competency/concept; pacing; streak; readiness (pass-probability proxy); seen/wrong sets per track; Dexter usage counts.
- Store derived snapshots in `learner_states` (or evolve `user_ai_analyses`) recomputed from events — not only from client `cat_scores`.

---

## 23. Learning Event Model

Minimal append-only `learning_events` (user_id nullable, session_id, type, payload jsonb, created_at):

`session_started`, `session_ended`, `item_shown`, `answer_submitted`, `item_flagged`, `hint_requested`, `explanation_opened`, `tutor_message_sent`, `review_started`, `schedule_task_done`, `module_completed`.

Not full event sourcing — attempts remain authoritative for scores once server-graded.

---

## 24. AI Architecture

- Server-only provider interface, e.g. `TutorProvider`: `explain_answer`, `generate_hint`, `classify_mistake`, `summarize_session`, `generate_question_draft`, `moderate_text`.
- Implementations: `StubTutorProvider`, `GeminiTutorProvider`, `GroqTutorProvider`, `WorkersAiTutorProvider`; route via `AiGatewayService`.
- Config: `CIVIO_EXPLAIN_*` / services.*. **Never** `VITE_` for secrets (currently OK).
- Grounding: bank explanation + syllabus citation only; refuse “official CSC paper” claims (already in prompts / recalled validator).
- BYOK later: encrypted per-user keys server-side — not Phase 0.
- AI optional: features degrade to stub/deterministic.

---

## 25. Migration Risks

| Risk | Detail |
| --- | --- |
| **Desktop ahead of GitHub** | MSI Docker has newer patches; replacing `main` with desktop tree will rewrite history of what this audit measured. **Build starts from MSI tree once pushed.** |
| Bank quality | ≈919 items many generic; unique-stem helps mocks but content debt remains |
| Shuffle / scoring bugs | Shipping without server grading preserves wrong Reveal UX |
| Brand / legal | Proprietary archive notice vs public GitHub; attribution required |
| AdSense pub id | Still original owner’s |
| Cold starts on free hosts | Timed exams + 1m spin-up hurt UX |
| Config:cache vs `env()` calls | Production footgun |
| Question cascade deletes | Admin mistakes destructive |
| Guest unlimited in prod | Set `CIVIO_GUEST_UNLIMITED` deliberately |

---

## 26. Phase 0 Plan

*(Do this on the **desktop tree after it lands on GitHub**, not by committing atop today’s audited `main`.)*

1. Dead code / lockfile cleanup; document npm as canonical.
2. Branding Hiraya → **Civio** (Title Case); keep author credits; new logos; fix robots/manifest/sw/PDF.
3. Safe security fixes: delete clear-cache route; remove or CLI-only migrate/rollback; custom questions as draft; document env.
4. README / architecture / setup; `.env.example` comments; `docs/DESKTOP_PATCHES_TO_PORT.md`.
5. Fix tsc + rules-of-hooks so CI green.
6. No Phase 1 features (no knowledge graph, no Capacitor).

---

## 27. Phase 1 Plan

1. Server-side grading + answer schema fix + withhold keys until review.  
2. Port MSI desktop patches listed in `docs/DESKTOP_PATCHES_TO_PORT.md`.  
3. Question bank QA (remove `??`, math operators, shuffle regression tests).  
4. Lazy Inertia pages / bundle split.  
5. Deploy free stack (Cloud Run + Neon + Cloudflare) on civio.ph.  
6. Dexter provider interface cleanup; keep stub default.

---

## 28. Exact Files / Modules Likely to Change

Phase 0: `routes/web.php`, `app/Http/Controllers/Admin/SystemController.php`, `resources/views/app.blade.php`, `public/manifest.json`, `public/sw.js`, `public/robots.txt`, `resources/js/components/layout/*`, `printable-exam.tsx`, `scorecard-view.tsx`, `cookie-consent-banner.tsx`, `global-pdf-exporter.tsx`, `smart-back.ts`, `drills/index.tsx`, `docker-compose.yml`, `env.docker.example`, `.env.example`, `README.md`, `seed_*.php`, `tests/Unit/AiGatewayServiceTest.php`, `use-content-shield.ts`, `admin/announcements/*`, `package.json` / lockfiles, `docs/*`.

Phase 1: `SubmitExamAttemptAction.php`, `StoreExamAttemptRequest.php`, `ExamQuestionResource.php`, `ExamAttemptFormatter.php`, `DeterministicAnalysisService.php`, `use-exam-pool-builder.ts`, `use-exam-hydration.ts`, `use-exam-submission.ts`, `use-exam-persistence.ts`, `StoreCustomQuestionData.php`, `ExplainQuestionService.php`, exam components for timers/tutor.

---

## 29. Exact Sequence of Work

1. Push / replace GitHub `main` with MSI desktop tree (GT-owned).  
2. Branch policy: either protect `main` and use `civio-next`, **or** commit Phase 0 on `main` only if GT explicitly allows (current steering: desktop will replace main first — **do not commit on the audited snapshot**).  
3. Phase 0 cleanup commits (small, logical).  
4. Green CI: pint, eslint, tsc, pest, build.  
5. Phase 1 server grading + desktop patch port.  
6. Content pass on bank.  
7. Deploy preview → civio.ph.  
8. Only then consider PWA polish / Capacitor.

---

## 30. What We Are Missing

- Written license/assignment clarity for the Hiraya → Civio fork.  
- Production `.env` / infra (not in repo — good).  
- Real CSC-aligned professionally curated bank (provenance, difficulty, reviewed state).  
- Server grading and anti-cheat for public launch.  
- Event/learner models (§22–23).  
- Knowledge hierarchy (§21).  
- Mobile field study / accessibility audit (**not verified**).  
- Offline-capable exam PWA (**not verified**).  
- Ownership of AdSense / OAuth / Turnstile / domain DNS.  
- Confirmation of exact MSI diff vs `1302608` (listed from GT notes; **not diffed against MSI disk in this audit**).  
- End-to-end reproduction of `??` operator loss on MSI data (**not verified** here).  
- Branch protection details (API 403 with current token).

---

## Appendix A — Build / Test / Lint Record (this box)

| Command | Result |
| --- | --- |
| `composer install` | **PASS** (exit 0) |
| `npm ci` | **PASS** (exit 0); npm audit later reported 5 vulns |
| `npm run build` | **PASS** (exit 0); warning: `app-*.js` ≈ **3040 kB** (786 kB gzip); ineffective dynamic import note |
| `php artisan test` (Pest) | **PASS** — 205 tests, 937 assertions, ~5.8s |
| `npm run types:check` (`tsc --noEmit`) | **FAIL** — 2 errors in `admin/announcements/index.tsx` (`last_checked_at`) |
| `npm run lint:check` | **FAIL** — 23 errors (17× rules-of-hooks in `use-content-shield.ts`, plus import/order & padding) |
| `npm run format:check` | **FAIL** — 20 files |
| `vendor/bin/pint --test` | **FAIL** — `seed_sample_questions.php`, `seed_topup_questions.php` |
| `composer audit` | 34 advisories / 10 packages |
| `npm audit` | 5 vulnerabilities (1 low, 1 moderate, 3 high) |
| GitHub Actions on `main` | latest tests **success**; linter **failure** (matches local) |

Logs: `/workspace/civio-audit-report/logs/`.

Local sqlite smoke (audit only): migrated, seeded 55 practice questions, `GET /exams?free_attempt=1` 200, forged score POST accepted (**B1**). Dev server stopped after checks. No commits made.

---

## Appendix B — Desktop patches to port later

Copy into repo as `docs/DESKTOP_PATCHES_TO_PORT.md` when Phase 0 starts on the desktop tree:

1. Guest unlimited access — **partially on GitHub** (`CIVIO_GUEST_UNLIMITED`); re-verify against MSI.  
2. Demographics removed from mocks — **on GitHub** (`includeDemographics = false`); re-verify.  
3. Mock button removed — **NOT on GitHub** (sidebar still “Mock Exams”).  
4. Tutor loop with study bias — **NOT on GitHub**.  
5. Exam countdown + per-item clock with urgency colors — **NOT on GitHub** (session timer only).  
6. Repositories incomplete-class fix — **on GitHub** (`QuestionRepository::getActivePool`); re-verify MSI extras.  
7. Sirit / Reveal wrong after shuffle — **OPEN** (B2).  
8. `'??'` lost math operators in explanations — **OPEN** (B6).

Mark each **NOT YET PORTED** until cherry-picked from MSI and covered by tests.

---

*End of audit. No repository changes were committed or pushed.*
