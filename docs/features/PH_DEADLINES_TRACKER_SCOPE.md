# PH Deadlines Tracker — Scope (MVP)

**Status:** Scope only. No implementation in this change.  
**Branch:** `grok/deadlines-tracker-scope`  
**Related:** Execution plan § "CSE 2027 dates page" — `/cse-2027-dates` already exists (`app/Support/CseExamDates.php`). Extend that surface; do not invent a parallel dates system.

## Goal

Earn organic SEO from Filipinos searching CSE / PRC / filing-window dates, then route them into Civio study (mocks, drills). Civio is **not** CSC/PRC-affiliated — state that on every public dates page.

## MVP pages

| Page | Purpose |
| --- | --- |
| `/cse-2027-dates` (existing) | CSE schedule + filing windows; keep as hub |
| Filing-window detail (same page or `/cse-2027-dates#filing`) | When applications open/close |
| PRC dates (new, deferred until GT ok) | Board exam calendars — stub "coming soon" only until verified rows exist |

### Confirmed CSE anchors (user-provided; still re-verify on CSC before UI copy goes live)

| Event | Date |
| --- | --- |
| CSE exam | **14 March 2027** |
| Application / filing opens | **2 November 2026** |

All other CSE/PRC rows: **TBD — verify** on the official CSC Examination Advisories / PRC pages. Never invent dates.

## Data source policy

- **Official CSC and PRC pages only.** No reviewers, news, Facebook, or social.
- Each row: `event`, `date` (or null if unconfirmed), `source_url`, `last_checked` (ISO date), `status` (`confirmed` \| `unconfirmed`).
- Prefer extending `app/Support/CseExamDates.php` (and a sibling `PrcExamDates.php` later).
- Tests already enforce official sources for CSE (`tests/Feature/Public/CseDatesTest.php`); keep that bar for any new public dates page.

## Where it fits in the app

- **Public, guest-readable** Inertia pages (same pattern as `/cse-2027-dates`).
- Link from homepage / Study Hub footer and SEO landing copy — not inside the live exam workspace.
- Lite Mode: text-first, no heavy charts.
- Do **not** restore permanent sidebar, invent Civio Pro, or add long CSC blocks into the exam UI (execution plan "Do not restore").

## SEO basics

- Unique `<title>` / meta description per page (e.g. "CSE 2027 exam date and filing schedule").
- Canonical URL; `robots` indexable.
- One H1; plain-language filing + exam dates above the fold.
- Disclaimer: independent study tool, not CSC/PRC.
- Optional: JSON-LD `Event` only for **confirmed** rows with dates.

## Bot-update routine (idea)

Weekly (or after GT ping): open CSC Examination Advisories + PRC calendar → compare to support classes → update `LAST_CHECKED` always; update dates only when the official page changes → PR with source URL in the commit body. No scraping of unofficial sites; no auto-deploy of unverified dates.

## Acceptance criteria

1. Public CSE dates page shows Mar 14 2027 exam and Nov 2 2026 filing open **only after** CSC re-check recorded in `last_checked`.
2. Every displayed date has `source_url` + `last_checked`; unconfirmed rows labeled clearly.
3. Disclaimer present; no CSC/PRC affiliation claim.
4. Existing Pest dates tests stay green; new rows covered.
5. Bundle budget / Lite Mode unaffected (static content, no new animation lib).
6. No deploy without GT authorization.

## Out of scope (MVP)

- Push/email reminders, accounts for "watch this deadline".
- Scholarship / LGU / agency filing calendars.
- Paid tiers or affiliate clutter on dates pages.
- Auto-scraping or LLM-invented dates.
- Merging into exam timer / Strict Mock UI.
- Full PRC board coverage before GT approves the PRC page.

## Next implementation slice (when GT says go)

1. Re-verify Nov 2 2026 / Mar 14 2027 on CSC; bump `LAST_CHECKED`.  
2. Tighten copy + SEO meta on `/cse-2027-dates`.  
3. Add internal links from marketing/home.  
4. PRC stub only after GT yes.
