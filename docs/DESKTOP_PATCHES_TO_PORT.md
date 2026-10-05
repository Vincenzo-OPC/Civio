# Desktop patches to port (MSI → GitHub)

Source of truth for study UX is GT's MSI local Docker tree (`localhost:8080`).
GitHub `main` tip `d3f0368` ("Civio baseline from desktop Hiraya") **is** that
desktop tree. Re-verify each item against the live MSI container before marking
PORTED. Status below is relative to this baseline at Phase 0 start:

| Patch | Status on this baseline (`d3f0368`) | Notes |
| --- | --- | --- |
| Guest unlimited access | IN BASELINE (re-verify) | `config/civio.php` + `CIVIO_GUEST_UNLIMITED` |
| Demographics removed from mocks | IN BASELINE (re-verify) | `includeDemographics = false` in pool builder |
| Mock button removed | NOT YET PORTED | Sidebar may still show "Mock Exams" — Phase 0.5 |
| Tutor loop with study bias | NOT YET PORTED | Phase 0.5 |
| Exam countdown + per-item clock + urgency colors | PARTIAL | Session timers present; per-item urgency — Phase 0.5 |
| Repositories incomplete-class / cache fix | IN BASELINE (re-verify) | `getActivePool` incomplete-class guard |
| Sirit / Reveal marks wrong after option shuffle | FIXED IN PHASE 0 | ID-keyed answers + original option indices |
| `??` lost math operators in explanations | OPEN (Phase Bank) | See audit B6 |

Do not mark PORTED until cherry-picked / re-verified from MSI and covered by automated tests.
