# Lite mode plan: cheap phones and slow internet

Status (7 Oct 2026): **L0 done except item 6** (nginx/deploy cache config,
pending). **L1 done** (server-picked mocks, Lite toggle, text-first exam and
drill screens, server-side prop trimming). **L2 pending** (offline drill packs,
needs GT decisions). See "L0 results" and "L1 results" below.

Goal: a Civio that works on a ₱3,000 Android phone on prepaid 3G/2G data. The
first exam screen must load fast, a mock must not burn megabytes, and practice
drills should keep working offline, without ever leaking strict-mock answer keys.

## 1. Where we are (measured 7 Oct 2026)

Production build of `main` (`npm run build`, Vite 8 / rolldown). Sizes are
first-load JS and CSS for a cold visit, following the Vite manifest import graph
from `resources/js/app.tsx` plus the page chunk. gzip level 9 and brotli quality
11; real servers compress a little less.

| Page | JS files | JS raw | JS gzip | JS brotli | CSS gzip / brotli |
| --- | ---: | ---: | ---: | ---: | ---: |
| Landing `/` | 23 | 1,541 KB | **443 KB** | 372 KB | 42 / 31 KB |
| Login `/login` | 22 | 1,511 KB | **436 KB** | 366 KB | 42 / 31 KB |
| Dashboard `/dashboard` | 33 | 1,536 KB | **444 KB** | 373 KB | 42 / 31 KB |
| Exam `/exams` (Pro start) | 52 | 1,704 KB | **496 KB** | 419 KB | 42 / 31 KB |

### Largest chunks

| Chunk | gzip | raw | What is in it |
| --- | ---: | ---: | --- |
| `app-*.js` (main entry, **every page**) | 261 KB | 934 KB | **jspdf 318 KB + html2canvas-pro 240 KB + pako 46 KB + fast-png 13 KB + fflate 6 KB** (PDF export, ~67% of the entry), pusher-js 60 KB + laravel-echo 11 KB (admin-only realtime), UI/layout components, Wayfinder routes |
| `vendor-inertia-*.js` (every page) | 95 KB | 307 KB | react-dom 175 KB, @inertiajs/core 74 KB, @inertiajs/react 22 KB, es-toolkit, laravel-precognition |
| `chart-*.js` (analytics only) | 90 KB | 298 KB | recharts 161 KB, redux toolkit, d3-scale/shape, decimal.js |
| `index.es-*.js` (PDF only, lazy) | 47 KB | 148 KB | canvg, core-js, svg-pathdata |
| `html2canvas-*.js` (lazy) | 45 KB | 195 KB | a second html2canvas copy pulled by jspdf |
| `app-*.css` | 42 KB | 324 KB | Tailwind 4 output |
| `vendor-ui-*.js` | 34 KB | 139 KB | Radix select/menu/tooltip/dialog, floating-ui |

All JS + CSS in the build: 255 files, 4.2 MB raw, 1.2 MB gzip.

**Measured quick win (not committed):** moving the jspdf / html2canvas-pro imports
in `printable-exam.tsx` to a dynamic `import()` cut first-load JS gzip from 443 → 259 KB
(landing) and 496 → 312 KB (exam). The main entry dropped from 261 → 77 KB gzip.

### Fonts and images

- Fonts: Instrument Sans via `bunny()` in `vite.config.ts`, weights 400/500/600 ×
  latin + latin-ext. Six woff2 files (70.6 KB) are **all preloaded** on every page.
- Images: `public/images/hero_image.png` is **718 KB** and loads on the landing page.
  It is 49% of that page's transfer. `civio_logo_cropped.png` (65 KB) is fetched twice (favicon
  link and header). PWA icons go up to 176 KB (`icon-512x512.png`).

### PWA precache

`public/build/sw.js` precaches **261 entries: 4.2 MB raw, about 1.27 MB
transferred** (3.9 MB JS, 328 KB CSS, 71 KB fonts). That includes admin pages, the
PDF stack and charts. A first visit downloads all of it in the background, which costs
real money on prepaid data.

### Exam payload

`GET /exams` sends the **whole active bank** in page props (keys withheld, so no
`correct_option` or `explanation`). The client then builds the 150/145 pool.

| Payload (repo seed bank, 550 active items) | raw | gzip | brotli |
| --- | ---: | ---: | ---: |
| Full `/exams` props today | 168 KB | 38.8 KB | 29.7 KB |
| Of which `questions` (550 items) | 162 KB | 37.7 KB | — |
| A 150-item Pro mock only | 44.5 KB | **11.2 KB** | 8.8 KB |

The payload grows with the bank. The MSI bank is roughly 900+ items before clone
removal.

### Lighthouse (mobile)

Lighthouse 12.8.2, default mobile preset: Moto G Power–class emulation (412×823,
DPR 1.75), simulated Slow 4G (150 ms RTT, ~1.6 Mbps), 4× CPU slowdown. Served by
`php artisan serve` behind a local gzip proxy (no brotli, no CDN), repo seed bank,
guest session. Treat the numbers as relative, not absolute.

| Page | Perf | A11y | Best pr. | FCP | LCP | TBT | CLS | Transfer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Landing | 70 | 87 | 96 | 2.7 s | 6.1 s | 150 ms | 0.099 | 1,452 KiB |
| Login | 70 | 87 | 96 | 2.7 s | 6.0 s | 210 ms | 0.061 | 758 KiB |
| Dashboard | 69 | 86 | 96 | 2.9 s | 6.1 s | 220 ms | 0 | 736 KiB |
| Exam (Pro) | 61 | 91 | 96 | 3.4 s | 6.9 s | 360 ms | 0 | 831 KiB |

Rough wire time for today's exam first load (~650 KB: JS 496 + CSS 42 + fonts 71 +
HTML/props 42) is ~3.3 s at 1.6 Mbps, **~13 s at 400 kbps (3G)** and ~21 s at 250 kbps.
CPU time on a slow phone comes on top of that.

### Compression and caching

- The production Docker image (`serversideup/php:8.4-fpm-nginx`) gzips by default
  according to its docs. That was not verified against a live deploy. It has no brotli.
- `conf/nginx/nginx-site.conf` is **not copied into the image** (the Dockerfile
  never references it), so its rules do nothing. It also points at `/sw.js`, but the
  SW now lives at `/build/sw.js`.
- No long-lived `immutable` caching is set for the hashed `/build/assets/*` files.
- `php artisan serve` (MSI-style local use) sends everything uncompressed.

### L0 results (7 Oct 2026)

Same method as above, measured after L0 items 1–5 (production build, local
server behind a gzip proxy, Lighthouse 12.8.2 mobile, simulated Slow 4G, 4× CPU).

| Page | First-load JS gzip before → after | brotli before → after |
| --- | ---: | ---: |
| Landing `/` | 443 → **221 KB** | 372 → 186 KB |
| Login `/login` | 436 → **213 KB** | 366 → 180 KB |
| Dashboard `/dashboard` | 444 → **221 KB** | 373 → 187 KB |
| Exam `/exams` (Pro start) | 496 → **284 KB** | 419 → 243 KB |

| Lighthouse mobile | Perf | FCP | LCP | TBT | Transfer |
| --- | --- | --- | --- | --- | --- |
| Landing before → after | 70 → **85** | 2.7 → 2.1 s | 6.1 → **3.5 s** | 150 → 150 ms | 1452 → **365 KiB** |
| Exam before → after | 61 → **77** | 3.4 → 2.7 s | 6.9 → **4.5 s** | 360 → 190 ms | 831 → **421 KiB** |

- Main entry `app-*.js`: 261 → 57 KB gzip (229 KB raw).
- Fonts: 6 preloaded woff2 files (71 KB) → **0**. They were Instrument Sans, but the
  CSS font stacks are `Inter`/`Outfit` → `system-ui` and never used it.
- Hero: 718 KB PNG → AVIF 26–53 KB / WebP 43–85 KB (`<picture>`, 640/1024 widths)
  with a 161 KB 640 px PNG fallback. The original PNG stays only for `og:image`.
- Logo: 65 KB PNG → 3.5 KB `civio_logo_mark.png` (96 px). It is still requested
  twice on a cold load (Chrome fetches the favicon separately from the header
  `<img>`), but that is now 7 KB instead of 130 KB.
- PWA precache: 261 entries (~1.27 MB gzip) → 100 entries (~408 KB gzip): the app
  shell plus the static import graph of landing, login, dashboard, exams and drills
  (`resources/js/lib/pwa-precache.ts`). Other hashed chunks are cached at runtime
  on first use (`civio-assets`, CacheFirst, 150 entries / 30 days).
- Realtime (laravel-echo + pusher-js) is loaded on demand by `lib/realtime.ts`
  only when a screen subscribes: admins (feedback badge, AI generation), or a user
  waiting for an AI analysis or on Learn.

### L1 results (7 Oct 2026)

Same method as L0, measured after L1 on a 550-item local bank.

| Payload | Before L1 | After L1 |
| --- | ---: | ---: |
| `/exams` page props (guest, setup screen) | 168 KB raw / 38.8 KB gzip / 29.7 KB brotli (whole bank) | **5.7 KB / 1.2 KB / 1.0 KB** (no bank) |
| Pro mock items (`POST /exams/sessions`) | (part of the bank above) | 150 items: 41.0 KB / **10.2 KB gzip** / 8.2 KB brotli |
| Sub mock items | (part of the bank above) | 145 items: 38.2 KB / 9.0 KB gzip / 7.2 KB brotli |
| Drill page (`?drill=true&category_name=Numerical Ability`) | whole bank | that category only (91 items locally) |

Keys stay withheld in all of these (`correct_option` and `explanation` absent).

| First-load JS gzip | L0 | L1 |
| --- | ---: | ---: |
| Landing | 221 KB | 222 KB |
| Login | 213 KB | 214 KB |
| Dashboard | 221 KB | 223 KB |
| Exam | 284 KB | 286 KB |
| Analytics, Lite on | (recharts included) | **223 KB**; the charts chunk (150 KB gzip) loads only when charts are shown |

The +1–2 KB is the Lite mode store, toggle and settings.

| Lighthouse mobile (Lite off) | Perf | FCP | LCP | TBT | Transfer |
| --- | --- | --- | --- | --- | --- |
| Landing L0 → L1 | 85 → **86** | 2.1 → 2.1 s | 3.5 → 3.5 s | 150 → 130 ms | 365 → 367 KiB |
| Exam L0 → L1 | 77 → **79** | 2.7 → 2.6 s | 4.5 → 4.5 s | 190 → 120 ms | 421 → **387 KiB** |

Lighthouse can't switch Lite on by itself (the client re-derives Lite from
localStorage and the connection, and Lighthouse's throttling doesn't set
`effectiveType`), so there is no separate Lite run. In Lite the landing page
also skips the hero (26–53 KB).

## 2. Budgets

Enforced with size-limit (`.size-limit.json`, brotli) and later Lighthouse CI.
Today's size-limit budgets sit just above current numbers. They block regressions
and get tightened after each phase.

| Budget | Today | L0 target | L1 target (Lite on) |
| --- | ---: | ---: | ---: |
| First exam screen JS (gzip) | 496 KB | ≤ 320 KB | **≤ 170 KB** |
| Landing JS (gzip) | 443 KB | ≤ 270 KB | ≤ 150 KB |
| CSS (gzip) | 42 KB | ≤ 42 KB | ≤ 30 KB |
| Web fonts | 71 KB, 6 preloads | ≤ 25 KB, 1–2 preloads | **0** (system fonts) |
| Landing images | ~800 KB | ≤ 120 KB | ≤ 30 KB (no hero) |
| Exam data per mock (gzip) | 38.8 KB, whole bank | same | **≤ 12 KB** (150 items), first page ≤ 4 KB |
| PWA precache transfer | ~1.27 MB | ≤ 500 KB | ≤ 250 KB, or none until opted in |
| Lighthouse mobile perf (landing / exam) | 70 / 61 | ≥ 80 / ≥ 75 | ≥ 90 / ≥ 85 |

"Usable on 2G/3G" means first question visible and answerable within about 6 s on
400 kbps / 300 ms RTT 3G, and within about 10 s on 250 kbps. A full mock should use less than
250 KB of data after the first visit.

## 3. What Lite mode is

**Recommendation: a mode flag on the existing routes, not a separate `/lite`
layout.** A `/lite` tree would duplicate pages, routes, tests and the
security-sensitive exam flow (grading, key withholding, shuffle mapping). A flag
reuses all of it and only swaps presentation and payload size.

- **Detection.** On by default when `navigator.connection.saveData === true` or
  `effectiveType` is `slow-2g`, `2g` or `3g`. Also honour
  `prefers-reduced-motion` for animations only. The Network Information API is
  Chromium-only (most PH Android phones). iOS gets the manual toggle.
- **Manual toggle.** A visible toggle on exam setup and in Settings → Appearance.
  The choice is stored in `localStorage` plus a `civio_lite` cookie, so the server can
  trim props too. Manual choice always beats auto-detect.
- **What it turns off:**
  - CSS animations and transitions, blur, heavy shadows and gradients
  - charts (recharts) → plain text tables
  - decorative icons (keep only functional ones)
  - landing hero and other images
  - hover/viewport prefetch of non-exam pages
  - the PWA precache until the user opts into offline
  - realtime (Echo/Pusher)
  - rich panels (AI analysis cards), which become text
  - There is no rich text editor in the user app today. If one is added, keep it out of Lite.
- **Text-first exam and drill screens:**
  - stem, options as large tap targets, Next/Previous, a compact palette
  - one clock line ("Exam left 2:41:10 · This item 0:42")
  - Reveal/Copy for AI as text buttons
  - same components, simpler markup under `lite`
- **System fonts:** `font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
  in Lite, with no font preloads.

## 4. Offline practice without leaking mock keys

Today `resources/js/sw.ts` makes `/exams`, `/drills`, auth, dashboard and others
NetworkOnly, and live exam JSON never contains keys. Keep both.

Plan for offline **drill packs** only:

1. **Separate, explicitly downloadable packs.** An admin (GT) publishes a
   `drill_pack` (for example 40 Numerical items). Items in a pack are **excluded from strict
   mock pools**, so shipping their keys cannot reveal mock answers. Strict mocks and the
   rest of the bank stay key-less on the client.
2. **Download endpoint** on its own prefix, for example `GET /packs/{pack}/download`, so the
   `/drills` NetworkOnly rule stays untouched. It returns items **with**
   `correct_option` and `explanation`, a version hash and an ETag. It is rate-limited and
   allowed for guests when `CIVIO_GUEST_UNLIMITED` is on.
3. **Service worker** gets a `civio-drill-packs` cache (StaleWhileRevalidate) for
   `/packs/*/download` only, plus the app shell and the drill chunks needed to render.
4. **Client** stores packs in IndexedDB, grades locally (pack keys only), and queues
   attempts. When back online it syncs them with workbox background sync to
   `POST /packs/{pack}/attempts`. The server **re-grades** from its own keys and tags the
   attempt `offline_practice`, so offline results never feed strict-mock readiness.
5. **Limits.** Show the size before download (about 40 items ≈ 12 KB gzip). Cap the
   number of packs. Note that iOS may evict storage after weeks of no use.

Trade-off: the bank has 550 unique items in the repo seed, and Subprofessional
Clerical (81 for 47 slots) and Professional Analytical (114 for 52) are tight. So pack
size per category must leave mocks reachable. **GT decides which items may go offline.**

## 5. Smaller, paged exam payload

Move pool selection to the server: port `utils/mock-pool.ts` to a PHP service with
the same blueprint, unique-only rule and weak-topic bias. Seen and wrong IDs are
already server data. The guest browser bias is sent with the start request. `/exams`
then returns only the chosen 150/145 items, keys still withheld:

- first 25 items in page props (≈ 2–3 KB gzip), the rest via an Inertia deferred prop
  or `GET /exams/session/{id}/items?page=n`.
- Bonus: the client no longer receives the whole bank's text, which is a
  security and scraping win.
- Risk: resume/hydration (`use-exam-hydration.ts`, `use-exam-persistence.ts`) and the
  shuffle mapping must keep working. Port the existing JS tests to Pest.

## 6. Inertia, server and CDN

- **Inertia 3.x** (installed: `@inertiajs/react` 3.2, `inertiajs/inertia-laravel` 3.1)
  still has v2's deferred props, `WhenVisible`, `once()` props and prefetch with `cacheFor`.
  - Defer `aiAnalysis`, analytics and announcements.
  - Make `categories` a `once()` prop.
  - Keep `prefetch` only on exam and drill links. Today `prefetch` is on the dashboard
    link in `app-sidebar.tsx`, `app-header.tsx` and `user-menu-content.tsx`. Turn it off in Lite.
- **Compression:**
  - Keep gzip in nginx.
  - Let Cloudflare serve brotli to browsers (automatic on its edge).
  - Optionally pre-compress `/build/assets` (`.br`/`.gz`) at build time if the server
    gains `gzip_static`/brotli.
- **Caching:**
  - Add an nginx `custom.conf` in the image: `/build/assets/` →
    `Cache-Control: public, max-age=31536000, immutable`.
  - `/build/sw.js` and `/manifest.json` → `no-cache`.
  - HTML and Inertia JSON stay uncached (per user).
  - Cloudflare: cache `/build/*`, `/images/*`, `/icons/*` at the edge; bypass HTML, `/exams*`, `/packs*`.

## 7. Phased plan

### L0: quick wins (hours, low risk, no new UI)

| # | Change | Files | Expected effect | Risk |
| --- | --- | --- | --- | --- |
| 1 | **Done.** Dynamic `import()` for jspdf + html2canvas-pro inside the PDF export | `resources/js/pages/user/exams/components/printable-exam.tsx` | −184 KB gzip on every page (measured) | First PDF export waits for a download; test print/export |
| 2 | **Done** (on demand via `lib/realtime.ts`: admins in the layout; users only on Learn or while an AI analysis is pending). Load laravel-echo / pusher-js only for admins, via dynamic import | `resources/js/layouts/app/app-sidebar-layout.tsx` | ≈ −20 KB gzip everywhere | Admin feedback badge must still update |
| 3 | **Done** (AVIF/WebP 640/1024 + PNG fallback, no `fetchpriority`; logo still 2 requests but 3.5 KB each). Convert `hero_image.png` → AVIF/WebP (~80 KB) with width/height + `fetchpriority`; one small logo; fix the double logo fetch | `public/images/*`, `resources/js/pages/public/welcome.tsx`, `resources/views/app.blade.php`, header logo component | Landing −650 KB | Visual check only |
| 4 | **Done** (all 6 font files removed: Instrument Sans was preloaded but never used by the CSS). Preload only latin 400 (and 600); drop latin-ext preloads; consider 2 weights | `vite.config.ts` (bunny weights), `resources/views/app.blade.php` | −45 KB, fewer requests | Slight font swap |
| 5 | **Done** (allow-list from the Vite import graph of critical routes instead of `globIgnores`, plus runtime caching of other chunks). Precache diet: `globIgnores` for admin, PDF, charts and dev-docs chunks | `vite.config.ts` (`injectManifest`) | Precache ~1.27 MB → ~400 KB | Those pages need the network (they already do) |
| 6 | **Pending.** nginx `custom.conf` with immutable caching for `/build/assets`; delete or fix the unused `conf/nginx/nginx-site.conf` | `Dockerfile`, new `conf/nginx/custom.conf` | Repeat visits ≈ 0 KB JS | Wrong rule could cache HTML; review carefully |
| 7 | Tighten `.size-limit.json` after each item; optional `npm run size` step in CI | `.size-limit.json`, `.github/workflows/tests.yml` | Prevents regressions | None |

### L1: Lite toggle and text-first screens (days) — **Done** (7 Oct 2026)

What shipped (see "L1 results" below for numbers):

- Server-picked mocks: `POST /exams/sessions` → `MockPoolSelector` (PHP port
  of the client rules) → only the 150 / 145 items, keys withheld, IDs stored in
  `exam_sessions` and checked on submit. `/exams` no longer sends the bank.
- `lib/lite-mode.ts` + `useLiteMode()`: auto (Save-Data, slow-2g/2g/3g), manual
  Auto/On/Off in Settings → Appearance, "Lite" switch on the dashboard and exam
  headers; `civio_lite` cookie + `html.lite` class (also set server-side in
  `app.blade.php`, so no flash).
- Lite CSS (no animation/transition/blur/shadow, system fonts), no landing
  hero, analytics text tables with recharts lazy-loaded, realtime skipped, SW
  precache skipped unless the user opts into offline.
- Text-first exam/drill body (`lite-exam-body.tsx`) inside the same
  `LiveExamView` (same state, Reveal, Copy for AI, grading).
- Server: shared `pusher` config nulled, `civio.lite` shared, analytics
  chart-only fields stripped, `aiAnalysis` deferred on dashboard, analytics
  and exams.
- Not done in L1: Lighthouse CI budgets (optional), Lite-only prefetch rules.


| Change | Files | Risk |
| --- | --- | --- |
| `lib/lite-mode.ts` + `useLiteMode()` (auto-detect + manual override, `html.lite` class, cookie) | new `resources/js/lib/lite-mode.ts`, `resources/js/app.tsx`, `app/Http/Middleware/HandleInertiaRequests.php` (share `civio.lite`), settings page | Auto-detect flapping: decide once per session |
| Lite CSS: no animation/transition/blur, system fonts | `resources/css/app.css`, `resources/views/app.blade.php` | Some layouts rely on transitions for open/close |
| Text-first exam and drill views | `live-exam-view.tsx`, `question-palette-panel.tsx`, `exam-timer-display.tsx`, `setup-exam-view.tsx`, `scorecard-view.tsx`, `review-exam-view.tsx`, `pages/user/drills/components/hub-view.tsx` | Biggest UI surface; keep one component tree |
| Charts → text tables in Lite; lazy recharts | `pages/user/analytics/components/*`, `pages/user/dashboard/*` | None functional |
| Server-built, paged mock payload | new PHP mock-pool service, `app/Services/ExamService.php`, `app/Http/Controllers/User/ExamController.php`, `use-exam-hydration.ts`, `use-exam-pool-builder.ts`, `utils/mock-pool.ts` | Must keep grading, key withholding, shuffle mapping, resume; port tests |
| Inertia deferred / `once()` props; prefetch only exam/drill in Lite | `ExamController`, `DashboardController`, `AnalyticsController`, `app-sidebar.tsx`, `app-header.tsx`, `user-menu-content.tsx` | Loading states needed |
| Register the SW only after opt-in when Lite/Save-Data is on | `resources/js/app.tsx` | Fewer users get updates early |
| Lighthouse CI budgets (optional) | `.github/workflows/`, `lighthouserc.json` | Flaky timings; assert on bytes, not ms |

### L2: offline drill packs (a week+, needs GT decisions)

| Change | Files | Risk |
| --- | --- | --- |
| `drill_packs` / `drill_pack_items` tables; pack items excluded from strict mock pools | new migration + model, `app/Repositories/QuestionRepository.php`, admin pages | Shrinks the mock pool; Clerical and Analytical are tight |
| `GET /packs/{pack}/download` (keys included, versioned), `POST /packs/{pack}/attempts` (server re-grades, `offline_practice`) | `routes/web.php`, new controller + Pest tests | Key exposure for pack items by design |
| SW route + cache for packs; background sync queue | `resources/js/sw.ts`, `vite.config.ts` | SW bugs are sticky; ship behind a flag |
| IndexedDB store + local grading + download UI | new `resources/js/lib/offline-packs.ts`, drills hub | Storage quota and eviction on cheap phones |

## 8. Libraries

Only where they clearly help:

- **size-limit** (`ai/size-limit`, ~7k ★): **added** (v12, Node 20+). Budgets in
  `.size-limit.json`, run with `npm run size` after `npm run build`.
- **Workbox** (`GoogleChrome/workbox`, ~13k ★) via **vite-plugin-pwa** (already
  installed). Use `workbox-background-sync` for L2.
- **Lighthouse CI** (`GoogleChrome/lighthouse-ci`, ~7k ★): optional in L1 for
  byte budgets and score floors in CI. It's heavier than size-limit, so add it only when there's a
  staging URL.
- **idb-keyval** (`jakearchibald/idb-keyval`, ~600 B): for L2 pack storage.
- **Preact compat** (`preactjs/preact`): **not recommended now.** It would save ~30–40 KB
  gzip at best. Radix UI, Headless UI, recharts and the React Compiler make compat risky.
  L0 #1 alone saves ~5× more.
- No new image pipeline dependency: convert the few PNGs once (squoosh/sharp CLI) and commit them.

## 9. Decisions for GT

1. ~~Ship L0 now~~ Done (items 1–5); item 6 (nginx cache config) still needs a
   decision because it touches deploy config.
2. ~~Lite as a mode flag vs a `/lite` layout~~ Mode flag, done in L1.
3. ~~Server-built mock pools~~ Done in L1.
4. Which items may ever be downloadable offline (they leave strict mocks), and how many per category.

## How these numbers were measured

- Build: `npm run build`.
- Per-page sizes: Vite manifest import graph with Node `zlib` (gzip 9, brotli 11).
- Chunk contents: a temporary `vite build --sourcemap --outDir /tmp/…` with byte attribution per module.
- Exam payload: `GET /exams?start=professional&free_attempt=1` with `X-Inertia`
  against a fresh DB seeded from this repo (550 items).
- Lighthouse: `npx lighthouse@12` with headless Chrome. Re-measure after each phase
  and update this file.
