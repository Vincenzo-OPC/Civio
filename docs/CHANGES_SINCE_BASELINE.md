# Changes since baseline

The living record of how Civio differs from the baseline (commit `d3f0368`, tag
`baseline`) and the upstream code it was built from. Update it in the same commit
as any change that makes Civio behave differently from the baseline (see "How to
keep this current" below).

## Image smoke, 22 October 2026

A manual GitHub Actions workflow, `image smoke`, builds the production Dockerfile and runs `scripts/fsrs-image-smoke.sh`. It does not push the image or deploy. The host key is a disposable `openssl` value because a clean runner has no Composer install. The build context excludes local SQLite files, logs, sessions, uploads, and secrets, and keeps the storage directory markers. [Run 39631539498](https://github.com/Vincenzo-OPC/Civio/actions/runs/39631539498) passed (`php 8.4.26`, `node v22.23.2`, `sodium loaded`, `fsrs image smoke passed`). [Run 39631088212](https://github.com/Vincenzo-OPC/Civio/actions/runs/39631088212) built the image and then stopped on a missing import while the job stayed green; it is not a pass. An image pass is not a deployment and is not operational production readiness.

## Pre-deployment check, 22 October 2026

The exam screen now receives `can_download_pdf`, so an allowed account can see Download PDF & Answer Key. At 320px the exam setup header wraps instead of clipping How it works. The readiness note is [DEPLOYMENT_READINESS_2026-10-21.md](DEPLOYMENT_READINESS_2026-10-21.md). Smart Review was not deployed.

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

### Homepage positioning (18 October 2026)

| What changed | Why | Commits |
| --- | --- | --- |
| Added the approved public-service education positioning beneath the homepage exam selection headline. | Clarifies Civio's independent mission without implying endorsement or changing the exam workflow. | this commit |

### PDF integrity (17 October 2026)

| What changed | Why | Commits |
| --- | --- | --- |
| Dedicated authorized, throttled PDF export selects its own questions, preserves stored option order, blocks active Strict Mocks, and returns private/no-store keyed payloads. Normal mock sessions remain keyless. The renderer omits the entire answer-key page for any missing or invalid key; permission-gated copy now says Download PDF & Answer Key. | The old export used a keyless mock payload and fabricated A for missing keys. Stored A/B/C/D positions, authorization and Strict Mock protections now have regression tests. | `698ba7c` |
| Astra context assessed against actual code; bounded return-to-mistakes recommendation documented in LEARNING_DELIVERY_RECOMMENDATION.md. | Separate shipped functionality and partial foundations from research ambitions. | `698ba7c` |

### Public pages (17 October 2026)

| What changed | Why | Commits |
| --- | --- | --- |
| New public page `/cse-2027-dates` (footer link, sitemap). Dates come from `App\Support\CseExamDates`, copied from CSC Examination Announcement No. 05, s. 2026 and checked on 17 October 2026: filing opens 2 Nov 2026 and the exam is 14 Mar 2027 (both confirmed); results 11 May 2027 are a CSC target; the closing date and the detailed announcement are shown as unconfirmed. Every row links its CSC source and shows a last-checked date. | Scout's deadline-tracker idea, approved by GT. Brings search visitors to practice. No new dependency; the page is a lazy chunk. | this commit |

### Security and scoring

| What changed | Why | Commits |
| --- | --- | --- |
| Scores are recomputed on the server from the bank (`ExamGradingService`); client `cat_scores` are ignored. | The baseline trusted the browser's score, so results could be forged. | `d19afda` |
| Live exam JSON no longer carries `correct_option` or `explanation` (`ExamQuestionResource` `$includeAnswerKey`). Keys come back only from `/exams/reveal` or after submit. | Answer keys were readable in page props during a mock. | `d19afda` |
| Drill payloads (`DrillQuestionResource`: drills hub, saved-set questions, smart-weakness) no longer carry `correct_option` or `explanation` for bank items; only a learner's own custom questions keep them. Online drills already run on `/exams` with client-shuffled choices (`shuffleOptionsForQuestion`, `originalOptionIndices`), keyless items and server grading on original indexes; that path is unchanged. The custom-builder preview no longer highlights the key for bank items. Pest: `DrillKeyWithholdingTest`. | The drills hub shipped every active key and explanation, including Strict Mock items, in page props. | this PR |
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
| Exam surface uses Civio violet for a selected choice and acid lime only after Reveal. A Strict Mock never shows correctness. Study Mock and drills can pause; a refresh restores the session with the clock stopped until Resume. The question navigator and Tools start closed. Reveal sits under the question tools instead of inside that row. | The live exam used blue cards, showed a permanent number grid, and had no pause. Lime must not mean "selected". | `3b4af15`, `9b65704` |
| The exam clock updates a subscriber instead of re-rendering the question every second, and the saved session is no longer rewritten on each tick. The question paper is the stem and the choices: compact header, bottom-sheet navigator, no marketing card around the item. | A ticking clock was rewriting the 150-item session in localStorage and repainting the paper. The old header was an admin bar. | `f9af6b9` |
| Homepage is the three start actions, the official 150 / 3h 10m and 145 / 2h 40m counts, and a passing rating of at least 80.00. The guide and analytics no longer say CSC requires 70% in every subtest. | The old landing page was a long marketing essay with a fake question count and an unsupported cutoff. | `4396cd3` |
| The public name is Civio, not Civio Review. About, the footer, and the exam guide state the exam facts in plain sentences and drop the founder story and the amber disclaimer box. | The leftover marketing voice did not match the product. | `8075c5f` |
| Footer shows the 2025 BIR registration badge and RSN 000RC20250000000333, labeled as a tax registration, not a CSC approval. Copyright is Civio, all rights reserved. The project license field is proprietary. Public copy no longer promises a pass, a pass probability, or a 54-second official pace. The setup pace matches the mock: about 76 seconds on Professional and about 66 on Subprofessional. | The registration is real, and the old pages sold a result Civio cannot know. | `0023105` |
| Dashboard, guide, study-plan cards, and the analysis text drop the command-center voice, the glow, and the forecast labels. The practice index number is unchanged. It is labeled as not a forecast. | The pages still shouted after the homepage was quieted. | `6771c56` |
| Dashboard leads with one Continue Studying action chosen from server data (next unfinished lesson, else a drill after a recent session, else a Study Mock). The "AI Readiness Predictor" card is no longer shown (component file kept, unused); in its place "Your Study So Far" shows plain counts from stored attempts (`DashboardService::getStudyTotals`: sessions, questions answered, sessions in the last 7 days). Recent sessions, daily goal and next-step launchers stay. | Fernly brief: one dominant next action, real stats only. Handoff F3: the readiness number was `mockAvg × 0.9`, not a forecast. Not browser-verified yet. | this PR |
| The floating coffee support button is gone. The contact page at `/support` stays. | The button asked for optional support. Practice stays free, and there is no donation link. | `1cbc2fb` |
| A dark mode button sits on the mock, the lite exam, and answer review. One click switches light and dark. The header menu (Light, Dark, System) is unchanged. | The mock covers the page header, so the existing theme control was unreachable during an exam. | `7761a1f` |
| The footer is the logo, All Rights Reserved, and a small BIR badge. The long affiliation paragraph and the BIR caption are gone. The header word “Civio” is gone because the mark is already there. The mark is violet on paper, not purple and lime. Public header and the begin button use that violet, not navy. Dark mode is one button, not a Light / Dark / System menu. The setup page no longer says to check the connection. | The top of the page mixed four colors and repeated text the user did not want. | `362fc35` |
| Expound walks an order-of-operations item with PEMDAS instead of repeating the one-line reveal. Other items drop the “matching choice” boilerplate and show the stored work as steps. The Professional and Subprofessional facts on the home and about pages are a spec list, not two paragraphs. | Reveal and Expound were the same sentence, and the exam facts were a block of text. | `43b6661` |
| Reveal is a compact tutor: the key, a one-line concept, then Steps, Shortcut, Common miss, Diagram, and Explain simpler only when that part exists. Numerical patterns are recomputed and shown only when they match the stored key. A miss offers an easier item in the same skill; a correct answer offers a harder one, or a weaker skill when the client sends one. `php artisan civio:audit-explanations` counts empty, thin, and contradictory items and does not rewrite them. | The reveal only restated the answer. | `4e900b6` |
| Home and the mock setup pick Professional or Subprofessional on a time dial: 150 questions in 3 hr 10 min, and 145 in 2 hr 40 min. The ring is that full sitting, not a score. The same dial sits on the live clock and shows time left against the sitting. Motion plays once, and reduced motion turns it off. | The level choice was two static cards, and the duration was easy to miss. | `f9a0dd6` |
| The dial marks are a clock: 12 even ticks, longer at 12, 3, 6 and 9. The home picture is the Study Mock screen (timer, 1 of 150, choice rows), not a separate sample question. Each dial reads “150 questions · 3 hr 10 min” once. | The old marks were one every five minutes, so the longer ones bunched up and did not look like a clock. The sample card was not the exam. | `ec85910` |
| The moving dial ring is lime, not violet, so it sits apart from the purple mark. The exam header keeps one clock: the ring and the time left. The per-item stopwatch is gone. The header uses the Civio wordmark; the favicon and app icon use the separate mark. The guest header no longer repeats Drills, and the dashboard Lite switch sits in the welcome row. | The ring matched the brand purple, the header showed two timers, and the old tile was still the logo. | `ea511cb` |
| Exam header context is a `nav` breadcrumb: mode / subject / topic (topic from `sm` up), session title below. "Question N of M" moved from the header to a small tabular label above the stem. Stem set at 17px/1.7 (20px/1.65 from `md`) within 65ch with `text-pretty` and `overflow-wrap:anywhere` so long words and formulas wrap on phones; choice text gets the same wrapping. Question text unchanged. | Fernly-inspired workspace slice 2. Not browser-verified yet. | this PR |

| Revealed choices pair colour with an icon and words: "Your answer · Correct" (check), "Correct answer" (check) and "Your answer · Incorrect" (cross), so the learner's pick and the key are told apart without relying on colour. Choice colours fade in 150 ms (none under reduced motion or Lite). The exam clock is a compact bordered pill on phones and a hairline ring beside larger tabular digits from `sm` up; untimed sessions show no clock instead of the word "Untimed". Same subscriber snapshot, no new interval. Strict Mock still never shows correctness and still has no Pause. | Fernly-inspired workspace slice 1 (`docs/design/CIVIO_FERNLY_LEARNER_EXPERIENCE_2026.md`). Not browser-verified yet. | this PR |
| The sitting is the lime ring only. Tick marks are gone, and the time is not repeated under the dial. The exam facts are a panel: 80.00 is the mark, then 150 and 145 scored items with their times. Dark pages use the same navy paper as the home. | The ticks fought the ring, the time was written twice, and the passing rating was a paragraph. | `3098b51` |

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
| Ask ChatGPT, beside Copy for AI in study, review and offline drills. It opens chatgpt.com with the same handoff in `?q=`. A long item is copied instead. Hidden in a Strict Mock. The answer stays out until Reveal. | Same job as Chrome's right-click "Ask ChatGPT", without a second copy of the question. | `1433ecf` |
| The same button sits under the revealed answer and inside the review explanation. It shows the ChatGPT knot or the Gemini spark. Settings → Preferences chooses which assistant opens. Civio's own Gemini key is not used. | The question row was not the answer, and the assistant should be a choice. | `16e7eb1` |
| Copy Question is the clipboard button. The Ask button can be ChatGPT, Gemini, Copilot, Grok, or Ask AI, each with its mark. Settings → Preferences chooses it. ChatGPT and Gemini put the question in the box. Copilot and Grok open and the question is copied, because those sites do not fill the box safely. Ask AI only copies. | The old name did not say what was copied, and the Ask menu should match the assistants people already use. | `a647b05` |
| Show Explanation replaces Reveal Answer. The panel is headed Understand the Answer, with Step-by-Step, Exam Tip, Common Mistake, Explain Simpler, and Try Another only when that part exists. Terminal-digit filing and Fibonacci-type sequences are taught only when the stored key matches the recomputed answer. | A correct letter is not a lesson. These two patterns were named in the teaching brief and can be checked without an AI call. | `c9fbca6` |
| Mixture, alphabetical filing, and three grammar rules join the checked lessons. Each one is shown only when the stored answer matches the rule. A pronoun item that is not one of those rules keeps its stored explanation. | The explanation engine should cover clerical and verbal items the same way it covers a perimeter: check first, then teach. | `b31ee80` |
| A number list is taught when the rule is a constant gap, a constant multiplier, or consecutive squares. Mean, median, percent change, simple interest, and a greatest common factor are taught the same way: only when the recomputed value is the stored answer. | Most of the number items in the bank were still a stored sentence. These rules can be checked. | `9256312` |
| The explanation engine, Dexter, Copy Question, and Ask are written up in `docs/ENGINES.md`, linked from the README and the architecture note. About has a short plain version. | The rules were in code and in phase notes, not in one place a reader could open. | `216f824` |
| The homepage now leads with Choose Your Exam, the two sittings as question counts and durations, Practice Modes, and an 80% passing mark. The header reads CSE REVIEWER. Sign In and Create Account replace the old header labels. | The page was already the right product. The type, the numbers, and the mode names needed to be set on purpose. | `d6e673d` |
| Setup, the live exam, the guide, and the scorecard now say Study Mode and Exam Mode. The score ring uses the same violet as the homepage and does not say Passed or Failed. | The homepage names and the exam screens had drifted. A practice rating is not an official result. | `2677ac0` |
| The purple light on the Professional and Subprofessional cards is gone. The homepage sample now runs Report, Show Explanation, Copy Question, and Ask. | The light stayed as a stain after the cursor left. The sample looked like a mock but none of its controls did anything. | `f23f487` |
| Dark mode is black with the logo lime, not navy and violet. The passing ring is lime in dark mode. Copy Question says Question Copied. | The old dark palette fought the wordmark. Lime is the contrast color on black. | `0a6aeef` |
| The homepage header, exam cards, practice modes, and passing panel are frosted glass over a soft wash. The question sample stays solid. Lite mode and reduced transparency turn the frost off. | Glass only reads when something sits behind it. The question text should stay easy to read. | `1de3bc2` |
| Dark mode lime is the wordmark green, #B3F52D. The homepage sample's back, theme, flag, map, Tools, and Pause controls respond. Practice Drills uses the same page color. | The earlier lime was brighter than the logo. The sample chrome looked clickable and did nothing. | `a915211` |
| The previous product name is gone from the app, the notes, and the storage code. Dark mode is flat black, with a solid selected card and the wordmark green as the only bright color. | The old name was still in notes and a storage prefix. Dark mode still carried the old blue buttons and a green fog. | `80c652c` |
| Show Explanation becomes Hide Explanation on the same button. Try Another is gone. | A second Hide sat under the explanation, and Try Another opened a question that was not in the mock. | `896b781` |
| Try Another opens that follow-up item in the current practice. | The old button left the mock and opened the drills list. | `b0d9141` |
| Try Another carries the follow-up item with the explanation, so it can open even when the page did not load the whole bank. | The button looked up a question the exam page no longer sends. | `f739606` |
| Similar Item asks the assistant for one new question and stays on the exam. Explanation actions are buttons. Auto-Next is gone. Flag, the question list, and cross-out explain themselves on hover. | Try Another left the exam and showed an item with no choices. The explanation links looked like plain text. Auto-Next and the word Palette were leftover chrome. | `abd3d53` |
| Report, explanation actions, Copy Question, and Ask sit on the same size chips, with space between them. | On dark, a hairline border disappeared, so the actions still looked like a line of text. | `ca1de88` |
| Study actions share one button: a real fill, a hover state, and lime for Show Explanation in dark mode. | The chips were flat gray boxes with no hover and a purple primary that fought the dark surface. | `139da2a` |
| Study and navigation buttons are filled capsules with no outline. Light primary is black. Dark primary is the logo green. | The bordered gray boxes still looked like form fields, not Apple or Meta controls. | `0da175f` |
| Report, Show Explanation, Copy Question, and Ask use a solid 36px fill. A current-state handoff is in docs/CIVIO_CURRENT_STATE_HANDOFF.md. | The translucent capsule fill still looked like text. | `7741271` |
| The built CSS drops the unused display-p3 and lab copies of the Tailwind palette. The sRGB colors stay. | App CSS was 32.89 kB brotli against a 33 kB cap. | `6cafabb` |
| Exam hints are shorter. The homepage sample says Question List, not Question map. FSRS is documented as unwired. | The hints were long, and the sample used a different name from the exam. | `b989319` |
| Exam setup no longer calls Dexter a tutor. The PDF line that claimed an answer key is gone. The next-agent plan is docs/CIVIO_NEXT_AGENT_EXECUTION_PLAN.md. | The mode cards overstated Dexter, and the booklet key is not actually in the download payload. | `d8d1714` |

### Bank and seeds

| What changed | Why | Commits |
| --- | --- | --- |
| Local practice seeds and ~495 original CSE-style practice items (`scripts/seed_unique_cse_batch_2026-09-30.sql`, `…2026-10-03.sql`, `seed_cse_pack_200_2026-10-03.sql`) plus generators. Not official CSC items. | The baseline shipped no practice bank for local use. | Desktop `718763a`, `f807222`, `d3f0368` |
| Seed scripts moved to `scripts/seeds/` with a README. | Root was cluttered. | `e21d94c` |
| `??` lost math symbols: root cause (PowerShell 5.1 pipe), `client_encoding` in seed SQL, `scripts/import-sql-utf8.ps1`, and `php artisan civio:repair-bank-encoding`. | Stems showed `??` instead of × ÷ ₱ etc. | `22fc855` |
| `questions.source_group` (nullable, indexed; `App\Enums\QuestionSourceGroup`): existing rows tagged `baseline`, except post-baseline drafts (`civio`); questions created by the app default to `civio`; PHP seed scripts set `baseline`; `php artisan civio:tag-source-groups [--dry-run]` tags raw SQL seed rows. Never sent to the browser. Spec v0.1 Section 10 decisions recorded; re-parameterize workflow documented (`docs/QUESTION_SOURCE_GROUPS.md`). No question text changed. | Keep baseline items grouped for later re-parameterizing; new authored items stay drafts until approved. | `ac27f5a` |
| Seeder saves one copy per item; `php artisan civio:remove-variant-clones` deletes or archives old "(variant N)" clones; Postgres SQL for desktop DBs. | Clone filler questions removed (GT approved). | `d8406d8`, `4bce08e` |
| `questions.replaces_question_id` and `php artisan civio:reparameterize-baseline`. The command inserts an active `civio` item matched by the old stem and drafts the original. `scripts/seeds/baseline_reparameterized.json` is the 495-item paraphrase (496 originally; the Sergeant item was dropped on 22 Oct 2026) (numbers recomputed; statutory facts rephrased, not renumbered). Applied on the local preview database only. | The served baseline stems were still the original wording. GT asked for them to be paraphrased on 14 Oct 2026. A second-person spot check is still owed. | `988d862` |

### Branding

| What changed | Why | Commits |
| --- | --- | --- |
| Rebrand to **Civio** (Title Case) in UI, manifest, Blade SEO, README, Docker/env defaults, legal seeder; `civio_logo*.png`; one-time migration of legacy localStorage keys to `civio_*`. Not-official-CSC disclaimer kept; tutor stays Dexter. | Civio is GT's product. | `5fe2d40`, `6277c17` |
| Neutral Civio mark (violet tile, lime "C" and dot) replaces the inherited sun-and-shield art everywhere: `public/favicon.svg` and `images/civio-mark.svg` (under 300 bytes), PWA icons, maskable icons, apple-touch icon, `favicon.ico`, print/PDF logo. Old logo files deleted. Footer "Made with ♥ by …" author credit and link removed; footer split into small typed components. Legacy storage migration moved to `lib/legacy-storage.ts` and now also carries cookie consent, the drills tab and the in-tab back/exam-origin keys (sessionStorage), with JS tests. | One Civio identity; returning users keep their progress and choices. | `08b4640` |

### Performance and PWA

| What changed | Why | Commits |
| --- | --- | --- |
| `pages/dev-docs.tsx` opts out of the React Compiler (`'use no memo'`). | On Node 22 the compiler memoized this large static page and added about 7.8 kB brotli, which pushed the all-chunks budget to 1,043,665 B of 1,040,000 B and failed the CI `size` step (eca4268, 716dc94, 9611b91, fb71fb5). Node 20 bailed out, so local runs passed. Builds are now 1,035,527 B on Node 20 and 22. | `6b48b73` |
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
| Formatting backlog cleared: Prettier on 81 files under `resources/`, Pint on 5 PHP files (trailing newlines, `!` spacing, unused imports, `scripts/_check_demo.php` encoding). No logic changes. | `npm run format:check` and `composer lint:check` now pass, so CI can enforce them. | `fb71fb5` |
| `lint.yml` now checks instead of fixing: it generates Wayfinder routes, then runs `composer lint:check`, `npm run format:check` and `npm run lint:check`. | The old job ran `composer lint`, `npm run format` and `npm run lint` (all fixers), so unformatted code passed CI. Wayfinder output is needed so ESLint's import order resolves `@/routes` the same way it does after a build. | this commit |
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

## Drill key withholding review — 19 October 2026 (PR #2)

Drill hub, saved-set and smart-weakness bank payloads omit keys and explanations. The author exception is limited to an owner's unpublished draft; authoring an active item no longer exposes its key, including during Strict Mock. Guest stems/choices and custom draft creation remain usable. Tests cover all three entry points with/without protected attempts and owner/other/guest draft visibility. Before the fix seven regressions failed; after it 14 targeted cases pass. Full suite: 342 PHP tests (7,628 assertions), 94 JS tests; types, lint, formatting, Pint, build and size pass. JS remains 1,037,085 / 1,040,000 B. Welcome formatting is isolated in `a077dd7`. [Real browser screenshots and evidence](review/2026-10-19/README.md) are local guest builder verification only. PR #2 remains draft pending GT's bank-preview decision; no merge, main push, deployment or study-data change.

## Security execution checkpoint - 20 October 2026

Verified MSI main was clean at efc0d81 and fast-forwarded it to fetched origin/main f2766db. GitHub PRs 1-16 were all OPEN and unmerged. No live service, study database, protected stack, question approval, or deployment was changed.

Implemented F1/F6 answer-access slice: sessionless online drills/retakes require a browser- and principal-scoped served batch (20 recent batches, 300 items each, 24-hour expiry); arbitrary IDs cannot turn submission into a key endpoint. Active status and actual option bounds are checked again before grading. Session-backed mocks grade their entire served set, including blank items, and submissions re-read the session under a database row lock. Client track labels cannot turn drills into mocks. Strict locks cover other submissions and historical question feedback. Reveal/Expound reject inactive items. Reused PR #2's bank-key withholding while preserving an author's own draft response. Cached pool members are revalidated for current active status. Drill browsing is paged at 100; exam candidates and saved-set question responses are bounded at 300; saved-set summaries exclude inactive items. Bank-access limits apply in testing/local environments too, with distinct account/IP identity namespaces.

F2 remains PARTIAL: complete-set scoring and stale-model duplicate protection are implemented; authoritative deadline enforcement, answer autosave, late-final grading from saved answers, and absolute UI recovery clocks are still pending. Do not present Strict Mock timing as protected until that work ships.

Next: finish F2 before the importer review gate, readiness removal, Review Mistakes, composition and repetition work. The 496-item reparameterized file was not imported or approved. No current live-bank count was obtained (live database access is out of scope). Browser screenshots have not been captured.
## Strict deadline checkpoint - 20 October 2026

This supersedes the earlier PARTIAL F2 checkpoint. New Strict sessions persist started_at and deadline_at. Legacy sessions keep the deadline implied by original created_at and track. The authenticated/guest owner can save original-option answer patches with an optimistic save_version; stale writes, unserved IDs, inactive items, invalid options, expiry and submission all fail closed. Final grading uses the complete served set; at or after the exclusive deadline it ignores final-request answers and uses only saved server answers, leaving other items blank. The ten-minute grace protects visibility only and grants no answer-write time.

Strict UI selections save serially, shuffled options map back to stored indices, and recovery fetches the server deadline and saved choices. Remaining time follows the absolute deadline rather than interval ticks or saved timeLeft. A failed save stops further answer changes until recovery and explains that late submission uses saved answers only. Study pause/untimed behavior and offline drills remain separate.

Strict starts are serialized per learner/browser and a second protected Strict session is refused. Guest sessions also carry a server-only hash of their browser session identity, and protected guest session IDs survive the recent-session cap and login. This closes the ownership-list eviction bypass. Starts/submissions now share the always-on bank-access limiter; answer saves have a separate 180/minute limiter.

Verification so far: full PHP suite 368 tests / 7,824 assertions; 96 JS tests and TypeScript passed. Final lint/format/build/size results are recorded below when complete. SQLite regressions cover stale models and revisions; a real concurrent PostgreSQL load test has not been run. No rendered browser screenshots or live migration/deployment are claimed.

Shipped-to-source scope: F1/F2/F6 engineering. Still pending: fail-closed reparameterization importer and independent review gate; removal of fabricated readiness; Review Mistakes; fact/theme/passage composition; item exposure balancing. Do not approve or import the 496-item set. Editorial bank quality is not established by these security fixes. Next bounded slice is the importer review gate. Hosting remains GT's decision. See PAPER_PRACTICE_ASSESSMENT.md for the paper-booklet assessment; no paper flow or Complete Reviewer was built.
Final security verification (20 October 2026): php artisan test passed 369 tests / 7,829 assertions; npm run types:check, npm run test:js (98 tests), npm run lint:check (no warnings), npm run format:check, composer lint:check, npm run build and npm run size all passed in the isolated test checkout. Exam JS is 10,944 / 11,000 bytes; aggregate JS is 1,038,071 / 1,040,000 bytes (Brotli). Budgets were not changed. A pre-existing homepage formatting issue was isolated in 43f9922; the first answer-access security commit is a390683. No rendered browser or real concurrent PostgreSQL load test is claimed. The new migration has only run against test SQLite, not the live study database. No question-bank source or approval status changed.

## Bank import engineering checkpoint - 20 October 2026

Canonical main was clean and synchronized at 06f3d23 before this slice. Both console importers now fail closed on malformed/colliding content and require separately signed GT authorization for active writes. Replacements require unambiguous baseline-only matches plus reviewed original fingerprints. The shared ledger preserves stable revision identities, prevents content overwrites, detects drift, and supports signed promotion of unchanged tracked drafts. Signed record/report/signature/signer digests are retained. Dry run performs equivalent locked validation. All-or-nothing writes and deferred observer cache invalidation are covered by regression tests.

See [BANK_IMPORT_APPROVAL.md](BANK_IMPORT_APPROVAL.md) for the exact approval contract, operational prerequisites and limitations. No real approving key is configured or generated. No bank content/status, live database, deployment or collection changed. The 496-item file remains unapproved and was not imported. A separate reviewed revision workflow for changed legacy content and complete collection versioning remain future work. Verified in the isolated PHP 8.4 / Node 22 runtime: php artisan test 407 passed / 3,960 assertions; 98 JS tests; types, ESLint, Prettier, Pint, build and size passed. Aggregate JS remains 1,038,071 / 1,040,000 bytes and exam JS 10,944 / 11,000 bytes. Five inventory regressions pass separately. The old 496-row assertion loop was replaced with synthetic behavior/security tests; assertion totals are not comparable to the earlier manifest loop. No browser screenshots or concurrent PostgreSQL test are claimed.

## Bank evidence inventory checkpoint - 20 October 2026

Importer boundary shipped in 93633ef. Added a read-only Git-object inventory, five Python regressions, pinned source lock for main 06f3d23 and open PRs #3-12, and a mechanical review/report using the existing PR #12 explanation linter. Inventory covers 143 artifacts / 4,276 file occurrences (not live items), with 294 identity groups needing version reconciliation. Existing qa_all.py --no-fixes passed on 1,000 main batch occurrences, but GI official-text verification was skipped because no source cache was present. No editorial approval or status changed; AUDIT_TRACKER was intentionally left unchanged.

See [bank review queue](research/bank/REVIEW_QUEUE_2026-10-20.md) for source hashes, exact reproduction commands, #462/B3 HOLD/source gaps, PR #12 passage-companion decisions, and the distinction between projection and release approval. Reconciliation/independent content review, sanitized runtime evidence, GT's final exact-content approvals and the provisional 2,000 split remain pending. No collection activation or authored bank content was produced. Next bounded bank slice: independently reconcile the #462 evidence and B3 HOLD/source gaps into a digest-bound decision packet for GT; do not apply fixes or retirements from stale snapshot IDs.

## Research tooling checkpoint, 21 October 2026

Added a read-only curriculum auditor with exact arithmetic and finite set-model checks, plus digest-bound evidence and an unapproved ten-item authoring packet. This changes research tooling only; no application behavior, active questions, database, access policy or deployment changed. See `docs/research/curriculum/CURRENT_BANK_ASSESSMENT.md`.

## Review Mistakes and analytics honesty, 22 October 2026

Published the recovered research commits, then added a signed-in mistake list. A wrong drill or Study Mock answer is stored once per question. An explanation seen on the server blocks that item from clearing. Strict Mocks are ignored. A thin percentile is no longer reported as Top 50%, and a subject that was not in an attempt is left blank instead of scored as zero. The ten numerical drafts were not activated. FSRS was not started.

## Review help stays with the sitting, 22 October 2026

An explanation now counts only in the browser session that opened it, and only when that item is actually answered. Skipping the item no longer erases the help. Another sitting can clear the mistake. The list is paged at 20, so older mistakes stay reachable. A locked Strict Mock item cannot be started from the list. The displayed mock percentage is the raw practice average. It is not adjusted into a pass chance, and the analytics index is no longer capped at 65 or 75.

## Help follows the drill, not the browser, 22 October 2026

Opening a second drill in the same browser no longer inherits an explanation from the first. Help is tied to the server-created served batch, or to the open Study Mock when there is no drill batch. A correct answer on a different drill can resolve the mistake. The practice percentage is the stored count of correct items, not a weighted category formula. Scorecards, analytics, and history say practice score rather than a readiness prediction or a mastered rank.

## Practice labels stay factual, 22 October 2026

The attempt average (mean of each finished run) and the mock-item percentage (correct mock items divided by mock items) are labeled as different counts. A subject with no items is "Not practiced", not a zero and not a critical weakness. The analytics page no longer shows a Top percent rank. "Passing Rate", "Subject Mastery", "Critical Concern", and stage names such as "Exam-Day Simulation" are not shown. A mock score of zero stays zero. "No mock yet" stays an empty ring, not a fake score. Stored attempt rows were not rewritten. Help attribution was rechecked: two drills in one browser do not share an explanation.

## Help stays on the drill that was submitted, 22 October 2026

A later drill that also contains an item no longer makes the earlier drill look unassisted. Submit uses the batch the page claims, then the batch whose ids match exactly. Reveal can claim the open Study Mock with its session id, so a newer drill does not take that explanation. A second drill still does not inherit the first explanation.

## Smart Review, 22 October 2026

A signed-in miss now stores one review card and one append-only review event. The server runs the existing ts-fsrs 5.4.2 package. A wrong answer is Again. An independent correct answer is Good and moves the due time. An assisted correct answer does not. A blank answer and a repeated submit do not add a success. Strict Mocks write nothing. Due reviews appear on Review Mistakes in Philippine time. The reminder is online only. Resolved still does not mean mastered. The public homepage says so in one short section. The catalog is `docs/FEATURE_CATALOG.md`.

## Smart Review runtime, 22 October 2026

The production image no longer deletes Node after the frontend build. It keeps the Node 22 binary and `ts-fsrs`, removes npm, and installs PHP sodium. The scheduler runs after the answer is saved, with a 5 second timeout, and does not hold the question lock while Node runs. One learner lock stops two requests from scheduling the same card together. If scheduling fails, including a repeated failure, the answer stays saved, the reminder stays unfinished, and Review Mistakes does not say Review Complete. An assisted answer and a Strict Mock stay out of that schedule. Due Today is paged at 20. This sandbox cannot unpack OCI layers (`lchown` fails because the user namespace maps only uid 0), so `docker build` was not run. `scripts/fsrs-image-smoke.sh` is the check on a Docker host that can unpack images. The same base filesystem (`serversideup/php:8.4-fpm-nginx`) plus the Node 22.23.2 binary and only `node_modules/ts-fsrs` was checked in a chroot: a wrong answer stored a future due date, an independent correct answer moved it, a missing Node binary left the reminder unscheduled, and restoring Node saved it. PHP sodium was loaded. It is not deployed. GitHub's aggregate JS check failed at 1,040,032 of 1,040,000 bytes. jsPDF's unused `html2canvas` import is no longer shipped. Smart Review is implemented and not production verified.

