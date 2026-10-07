# Desktop patches to port (MSI → GitHub)

Source of truth for study UX is GT's MSI local Docker tree (`localhost:8080`).
GitHub `main` tip `d3f0368` ("Civio baseline from desktop Hiraya") **is** that
desktop tree. Phase 0.5 (7 Oct 2026, Asia/Manila) re-checked each item against
the desktop sources copied to the box on 5 Oct (`desktop-live-exam-view.tsx`,
`desktop-use-exam-timer.ts`, `desktop-guest-study-bias.ts`,
`desktop-setup-exam-view.tsx`, `desktop-civio-study.ts`) and the MSI note
`Local-Study-Patches.md`. The MSI itself was offline on 7 Oct, so the live
container and the compiled `app-CpqM_WR8.js` bundle were not diffed.

| Patch | Status | Notes |
| --- | --- | --- |
| Guest unlimited access | IN BASELINE | `config/civio.php` + `CIVIO_GUEST_UNLIMITED` |
| Demographics removed from mocks | IN BASELINE | `includeDemographics = false` in pool builder |
| Mock button removed | PORTED (Phase 0.5) | Home shows Start Pro · Start Sub Pro · Practice Drills; the old "Try Mock Test" button and its picker modal are gone. Already in baseline; guarded by `tests/Js/home-launchers.test.ts`. Sidebar "Mock Exams" and the dashboard "Take Mock Exam" menu are the setup page entry points and were not removed. |
| Tutor loop with study bias | PORTED (Phase 0.5) | Scorecard strengths/weaknesses → weak-area drill → next pool biased to misses. Now records from **server** grading (keys stay withheld), drops items once answered correctly, and topic drills lean to past misses / weak subtopics. `resources/js/lib/guest-study-bias.ts`, `tests/Js/study-bias.test.ts`. FSRS not wired here (no per-item review state yet). |
| Exam countdown + per-item clock + urgency colors | PORTED (Phase 0.5) | Exam left 3:10:00 / 2:40:00, amber ≤ 10 min, red ≤ 2 min, auto-submit at 0. This item counts up, resets on move, amber 45–75s, red > 75s. No sound. `resources/js/lib/exam-clock.ts`, `tests/Js/exam-clock.test.ts`. |
| Repositories incomplete-class / cache fix | IN BASELINE (re-verify) | `getActivePool` incomplete-class guard |
| Sirit / Reveal marks wrong after option shuffle | FIXED IN PHASE 0 | ID-keyed answers + original option indices |
| `??` lost math operators | FIXED AT SOURCE (Phase 0.5); MSI rows not yet repaired | Root cause: Windows PowerShell 5.1 `Get-Content file.sql \| docker exec -i … psql` turned each non-ASCII byte into `?`. Seed SQL now sets `client_encoding`, `scripts/import-sql-utf8.ps1` avoids the pipe, and `php artisan civio:repair-bank-encoding` repairs rows idempotently from the UTF-8 seeds. Run it where the bank lives (MSI DB / Neon) with `--dry-run` first; it lists IDs it cannot repair. |

Do not mark PORTED until re-verified from MSI sources and covered by automated tests.
