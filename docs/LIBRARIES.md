# Civio libraries

Chosen open-source libraries for Civio, why they fit, and status.
Stats checked via GitHub API on **2026-10-05** (Asia/Manila). Only repos actually inspected are listed.

## Adopted now (Phase 0)

| Library | Repo | Stars | Last push | License | Why / status |
| --- | --- | --- | --- | --- | --- |
| **vite-plugin-pwa** | [vite-pwa/vite-plugin-pwa](https://github.com/vite-pwa/vite-plugin-pwa) | 4281 | 2026-10-04 | MIT | Replace hand-written `public/sw.js` with injectManifest SW: versioned precache, NetworkFirst HTML, **NetworkOnly for `/exams` and auth**. Prompt-to-update. **Adopted.** |
| **ts-fsrs** | [open-spaced-repetition/ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs) | 806 | 2026-10-03 | MIT | FSRS spaced-repetition scheduler for Phase 1 reviews. Wrapper at `resources/js/lib/review/fsrs.ts` (not UI-wired yet). Pin **5.x** (stable); v6 still beta. **Adopted (lib only).** |
| **Prism** | [prism-php/prism](https://github.com/prism-php/prism) | 2426 | 2026-03-20 | MIT | Unified Laravel LLM interface (OpenAI/Anthropic/Gemini/xAI/…). Installed; Civio uses `App\Ai\Contracts\TutorProvider` with **NullTutorProvider** default (no keys). Live Prism drivers later. **Adopted (foundation).** |
| **sentry-laravel** | [getsentry/sentry-laravel](https://github.com/getsentry/sentry-laravel) | 1351 | 2026-10-05 | MIT | Error monitoring. **Disabled unless `SENTRY_LARAVEL_DSN` is set.** **Adopted (opt-in).** |

## Strong fits — later

| Library | Repo | Stars | Last push | License | Verdict |
| --- | --- | --- | --- | --- | --- |
| **KaTeX** | [KaTeX/KaTeX](https://github.com/KaTeX/KaTeX) | 20428 | 2026-10-04 | MIT | Fast math rendering for CSE numerical stems / Dexter. Prefer over MathJax for SPA size. **Later** (Phase Bank / explain UI). |
| **Playwright** | [microsoft/playwright](https://github.com/microsoft/playwright) | 97106 | 2026-10-03 | Apache-2.0 | E2E for exam shuffle/submit/reveal. Baseline had ad-hoc `_pw/` junk (removed). **Later** (after Phase 0 CI green). |
| **Laravel Pennant** | [laravel/pennant](https://github.com/laravel/pennant) | 596 | 2026-08-13 | MIT | Feature flags (guest unlimited, AI tutor, PWA). **Later** when flags multiply. |
| **Inertia SSR** | [inertiajs/inertia](https://github.com/inertiajs/inertia) (+ [inertia-laravel](https://github.com/inertiajs/inertia-laravel) 2482★, pushed 2026-10-01, MIT) | 8128 | 2026-10-02 | MIT | Repo already has `resources/js/ssr.tsx` / `build:ssr`. Full SSR on Cloud Run needs Node sidecar — **later** after hosting shape is fixed. |
| **Ziggy** | [tighten/ziggy](https://github.com/tighten/ziggy) | 4320 | 2026-09-21 | MIT | Named Laravel routes in JS. Civio already uses **Wayfinder** — **no** (duplicate). |
| **spatie/laravel-backup** | [spatie/laravel-backup](https://github.com/spatie/laravel-backup) | 6026 | 2026-09-14 | MIT | DB/file backups once Neon+Cloud Run land. **Later** (ops). |

## Evaluated — no / not now

| Library | Repo | Stars | Last push | License | Verdict |
| --- | --- | --- | --- | --- | --- |
| **MathJax** | [mathjax/MathJax](https://github.com/mathjax/MathJax) | 10925 | 2026-07-03 | Apache-2.0 | Heavier than KaTeX for our React exam UI. Prefer KaTeX later. **No (for now).** |
| **silviolleite/laravelpwa** | (404 on GitHub API 2026-10-05) | — | — | — | Classic Laravel PWA package appears unmaintained / missing. Prefer **vite-plugin-pwa**. **No.** |

## Already in tree (keep)

Laravel 13, Inertia React 3, Fortify, Socialite, Wayfinder, Pest 4, Pint, Tailwind 4, shadcn/Radix, Dexter stub services, existing `AiGatewayService`.
