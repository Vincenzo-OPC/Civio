# Changelog

All notable changes to Civio since the baseline (tag `baseline`, d3f0368).
Generated from Conventional Commits by [git-cliff](https://git-cliff.org); do not
edit by hand, run `npm run changelog`. For everything that differs from the
baseline, see `docs/CHANGES_SINCE_BASELINE.md`.

## [Unreleased]

### Features

- *(lite)* L1 server-picked mocks, Lite mode flag and text-first exam screen ([c825fe9](https://github.com/Vincenzo-OPC/Civio/commit/c825fe973bd1cc44791d87758139a6c825f40316))
- *(bank)* Questions.source_group groups baseline and Civio-authored items ([ac27f5a](https://github.com/Vincenzo-OPC/Civio/commit/ac27f5a9fa3bc9bf84839ee93767218e469989ca))
- *(lite)* L2 offline drill packs ([09c62da](https://github.com/Vincenzo-OPC/Civio/commit/09c62daa2c843ff187dd5b6b44801290f4410089))
- *(exams)* Split Exam Simulation into Study Mock and Strict Mock ([6edbadc](https://github.com/Vincenzo-OPC/Civio/commit/6edbadcd013f14814764c924aecf2b610a2a804a))
- *(bank)* Civio:import-batch command for approved item batches (idempotent, never offline-eligible) ([4a7f1d1](https://github.com/Vincenzo-OPC/Civio/commit/4a7f1d139914b42010eafe628051c5ed93f5b187))
- *(bank)* Batch generator pipeline with per-round QA; batch-002 (100 draft items) ([b894c84](https://github.com/Vincenzo-OPC/Civio/commit/b894c846e07d46a98cd946efcf158f52a34202c0))
- *(bank)* Apply CoS rulings to the generator and QA (spec v0.1.4) ([0138aff](https://github.com/Vincenzo-OPC/Civio/commit/0138affc1a38903c057ee7dae453e69538c2af20))

### Fixes

- *(analytics)* Safely handle missing keys in ai analysis orchestrator ([c6a173f](https://github.com/Vincenzo-OPC/Civio/commit/c6a173f1386a7d1d6e60b1d598ed5d93fc814228))
- *(view)* Plain-JS inline scripts so system dark mode applies before paint ([51c429b](https://github.com/Vincenzo-OPC/Civio/commit/51c429be12fb167d2c0f6cab1177daaae115db90))
- *(bank)* Clerical template pick by rng (was locked to filing); spelling-misspelled items off (no spec code); rebuild batches [skip netlify] ([6647cd8](https://github.com/Vincenzo-OPC/Civio/commit/6647cd890076540a90ed054efaab100af1e12d1f))

### Performance

- *(lite)* L0 quick wins — on-demand PDF and realtime, light images, no unused fonts, slim precache ([5ea1cd5](https://github.com/Vincenzo-OPC/Civio/commit/5ea1cd57dae46bf009cc68d2f83afc668e87ff9f))

### Docs

- Regenerate CHANGELOG and point L1 rows at c825fe9 ([e1e48c4](https://github.com/Vincenzo-OPC/Civio/commit/e1e48c4bf1e790e5cdfb0dc42dfee7086f2be5af))
- *(agents)* Cursor is not used; Codex, Grok Build and Grok Bot are ([912d318](https://github.com/Vincenzo-OPC/Civio/commit/912d31826add2e2499f4da2906f9a54d1e0d105d))
- *(baseline)* Rename the diff log to CHANGES_SINCE_BASELINE and say baseline everywhere ([bc8d3dd](https://github.com/Vincenzo-OPC/Civio/commit/bc8d3ddd3ea380cdb398b130db7ee9bfe435692e))
- *(baseline)* Civio-only README and docs; fold the desktop patch log; drop old fork notes and audit ([a0019af](https://github.com/Vincenzo-OPC/Civio/commit/a0019af6eb42681221e7361ad873bd940ffa9207))
- Civio code standard and ranked modernization backlog ([fa431e0](https://github.com/Vincenzo-OPC/Civio/commit/fa431e05e2c50962b1ef65b91725a52290be66f4))
- Codex handoff plan, linked first from AGENTS; L2 rows point at 09c62da ([9a68dac](https://github.com/Vincenzo-OPC/Civio/commit/9a68dac822a138f1c41b2315168ae794f17414a7))
- Record measured AI self-improvement roadmap [skip netlify] ([89dd651](https://github.com/Vincenzo-OPC/Civio/commit/89dd651eca114adc9edbc7d4d42524e038ebe1e5))
- *(agents)* Surface evolutionary research and safety boundaries [skip netlify] ([65f3d9e](https://github.com/Vincenzo-OPC/Civio/commit/65f3d9eab04f6207b1aab099a87fb10f2d249294))
- Connect agent entrypoints to RSI roadmap [skip netlify] ([50793b5](https://github.com/Vincenzo-OPC/Civio/commit/50793b5821d6bf4d73539144b75bdfad0d0b2d68))
- Connect agent entrypoints to RSI roadmap [skip netlify] ([e3c693a](https://github.com/Vincenzo-OPC/Civio/commit/e3c693ad44f745510d5de995d32c8e888d9f14d4))
- *(spec)* Drop uncited Civio Filing Rules v1 per CoS CSC-citation condition (v0.1.2) [skip netlify] ([65e37c6](https://github.com/Vincenzo-OPC/Civio/commit/65e37c6170088679c874da8bb1ecc5cfc314f468))
- *(spec)* Adopt ARMA simplified filing rules as Civio Filing Rules v2 (v0.1.3) [skip netlify] ([bf010c9](https://github.com/Vincenzo-OPC/Civio/commit/bf010c9285c50f36c99f0490219ba1c799dbf5f9))
- *(batches)* Draft batch-001, 10 original items for CoS review [skip netlify] ([f213bd1](https://github.com/Vincenzo-OPC/Civio/commit/f213bd12be6b42530729153d39069a05bc453c77))
- *(batches)* Batch-001 CoS PASS (final), add NUM-OTHER-SHARE, ANA-OTHER-RELATION and draft status to spec [skip netlify] ([fc05c0c](https://github.com/Vincenzo-OPC/Civio/commit/fc05c0c5c066dea8e8cadd3d4a82eb964982a0de))
- *(batches)* Draft batch-002, 10 original items weighted to Numerical and Analytical [skip netlify] ([c48e576](https://github.com/Vincenzo-OPC/Civio/commit/c48e576b88ba53970131cb89bf6a1ad9f7268c32))
- *(bank)* Batch-003, 100 generated draft items (QA clean) [skip netlify] ([dd71168](https://github.com/Vincenzo-OPC/Civio/commit/dd71168a80cee7d8092f7ac8078a84c21d4e09c3))
- *(bank)* Batch-004, 100 generated draft items (QA clean) [skip netlify] ([1111190](https://github.com/Vincenzo-OPC/Civio/commit/1111190dfd2706fe0d3069a82928613275defdae))
- *(bank)* Batch-005, 100 generated draft items (QA clean) [skip netlify] ([e8498d6](https://github.com/Vincenzo-OPC/Civio/commit/e8498d6657d8001c0c7a39710b80a11cd3d835d5))
- *(bank)* Batch-006, 100 generated draft items (QA clean) [skip netlify] ([f174062](https://github.com/Vincenzo-OPC/Civio/commit/f174062c5bd07e06ce6e5addeb829cfe4c2f8d1a))
- *(bank)* Batch-007, 100 generated draft items (QA clean) [skip netlify] ([d2b6d7c](https://github.com/Vincenzo-OPC/Civio/commit/d2b6d7c15fe3269168ca409e03aaa5f5c72fad3a))
- *(bank)* Batch-008, 100 generated draft items (QA clean) [skip netlify] ([8f79c0d](https://github.com/Vincenzo-OPC/Civio/commit/8f79c0dd12e169625fb1ea678cdc4248708ab26c))
- *(bank)* Batch-009, 100 generated draft items (QA clean) [skip netlify] ([841d8a1](https://github.com/Vincenzo-OPC/Civio/commit/841d8a196039cd1df0ffd2e69df40b41b7e7a851))
- *(bank)* Batch-010, 100 generated draft items (QA clean) [skip netlify] ([61652d0](https://github.com/Vincenzo-OPC/Civio/commit/61652d083babd965609e0ba7a5a0f9b6be8ed50c))
- *(bank)* Batch-011, 100 generated draft items (QA clean) [skip netlify] ([1851b5e](https://github.com/Vincenzo-OPC/Civio/commit/1851b5ed363cc228693cdf9396036bf77a061d9c))
- *(bank)* Rebuild batch-002..011 under the CoS rulings (1,000 items, QA green) [skip netlify] ([66a285d](https://github.com/Vincenzo-OPC/Civio/commit/66a285d144db35d1c03085a55318fec7bf78a23f))

### Style

- Pint formatting for exam controller, Inertia middleware, routes and scoring test (no behaviour change) ([476a65a](https://github.com/Vincenzo-OPC/Civio/commit/476a65a95afe45be51c20002cf3f7c04037737e4))
- Pint formatting for the PHP seed scripts (no behaviour change) ([8e16919](https://github.com/Vincenzo-OPC/Civio/commit/8e16919c870ba7b785ed24495295c228291ca0ce))
- Prettier for vite.config.ts ([0470bc3](https://github.com/Vincenzo-OPC/Civio/commit/0470bc3d18088c57ec65047125dfe8458c581279))

### Chores

- *(entire)* Codex and Claude Code hooks, committed .githooks, git-refs settings; drop Cursor hooks ([3fe931b](https://github.com/Vincenzo-OPC/Civio/commit/3fe931b0dc622c9d17aff88a873e411ced4f576b))
- *(brand)* Neutral Civio mark, no author credit in the footer, full legacy storage migration ([08b4640](https://github.com/Vincenzo-OPC/Civio/commit/08b46403669930429ef921a5b5c23c5292f3f775))
- *(entire)* Refresh Codex and Claude Code hooks for Entire 0.11.4 ([faa9cb9](https://github.com/Vincenzo-OPC/Civio/commit/faa9cb9d6e45eed3ee25fcd06b59bc31a17e3cf2))

### Other

- Batches 002-011 rebuild: topic floors, pronoun rescan, CLR-SPELL-CORRECT-FOIL, spec approvals [skip netlify] ([6452cdf](https://github.com/Vincenzo-OPC/Civio/commit/6452cdfbd8213de0fea163941882e0558ca066d6))

## [0.1.5-phase0.5] - 2026-10-07

### Features

- *(exam)* Pure exam-clock urgency helpers with unit tests ([518ee08](https://github.com/Vincenzo-OPC/Civio/commit/518ee088075d99a106cee98e6f82e4040b3c4e6d))
- *(study)* Tutor loop records weak topics from server grading; drills lean weak ([a4df9f8](https://github.com/Vincenzo-OPC/Civio/commit/a4df9f8d08355ed9af1bd8b3a2b40368afaeaa64))
- *(ai-handoff)* Clean Copy for AI formatter with tests ([3ab87d2](https://github.com/Vincenzo-OPC/Civio/commit/3ab87d2ddf666b3067ef10c55d8474326e79b4c5))
- *(exams)* Copy for AI button beside Reveal and in review ([3ba17ab](https://github.com/Vincenzo-OPC/Civio/commit/3ba17abf6b23f4309039744d0c9a5f65356cf16a))
- *(bank)* Civio:remove-variant-clones deletes or archives clone rows ([4bce08e](https://github.com/Vincenzo-OPC/Civio/commit/4bce08e360691e11227e11ad90425f6f1f98115a))
- *(exams)* Mocks use unique items only, no variant fill or padding ([ba88fa5](https://github.com/Vincenzo-OPC/Civio/commit/ba88fa5c7bf0ddcab9af9fffc13bb3a53aa7fc30))

### Fixes

- *(ui)* Restore mojibake punctuation on scorecard and submit dialog ([4f4eb21](https://github.com/Vincenzo-OPC/Civio/commit/4f4eb2158a5bab6e66263a2fd899294d2ede340c))
- *(bank)* Root-cause and repair the ?? lost math symbols ([22fc855](https://github.com/Vincenzo-OPC/Civio/commit/22fc855f2f6e93242de18d7d0ef1c62ba5b5275d))
- *(seed)* Save one copy per practice item, no (variant N) clones ([d8406d8](https://github.com/Vincenzo-OPC/Civio/commit/d8406d808e3cd5a4a7fd6182f31688a9d4e78f94))

### Tests

- Guard the desktop home launchers (no redundant Mock button) ([76f0542](https://github.com/Vincenzo-OPC/Civio/commit/76f05428a7e1ffd370f78f140aa41866572baf1b))

### Docs

- Add AI study and spelling system ([e4e3d4c](https://github.com/Vincenzo-OPC/Civio/commit/e4e3d4ce0c8962cd597de7dd3afc7fe944cf7012))
- Link AI study and spelling system ([db70d6a](https://github.com/Vincenzo-OPC/Civio/commit/db70d6aeea90bd9f195c701242c9e6447c6fa5db))
- Add 2026 AI product standard and benchmark ([4cffde5](https://github.com/Vincenzo-OPC/Civio/commit/4cffde5ada05e46cc420ec7507dd0cfe25f3e9ba))
- Keep Reveal fallback and align AI study standard ([c503e45](https://github.com/Vincenzo-OPC/Civio/commit/c503e459f4ef6e2d96aa23780f2b8f544031e725))
- Link 2026 AI product standard ([b3046dc](https://github.com/Vincenzo-OPC/Civio/commit/b3046dc4a30f51d863725640cc8b0ec2214e42b6))
- Add external AI handoff and Copy for AI workflow ([29caf02](https://github.com/Vincenzo-OPC/Civio/commit/29caf02a37ca44565c4ff39c32154fdc0d92fa4d))
- Link external AI handoff spec ([59cb4a4](https://github.com/Vincenzo-OPC/Civio/commit/59cb4a42135d75967880a646caabc9ba13eda070))
- Require clean semantic Copy for AI export ([d62b7bc](https://github.com/Vincenzo-OPC/Civio/commit/d62b7bc76ef26b98bd7b7c02856a3da4f451f2df))
- Add Copy for AI MVP implementation proposal ([1d4c96d](https://github.com/Vincenzo-OPC/Civio/commit/1d4c96dd1ae4b952c04a7554320ee6e059a77437))
- Mark Phase 0.5 desktop patches ported and update phase status ([9ab859c](https://github.com/Vincenzo-OPC/Civio/commit/9ab859cc89b848e5434d5f9b94e2cb133c8e4237))
- Note Copy for AI MVP shipped; Ask Tutor still a stub ([9f3891c](https://github.com/Vincenzo-OPC/Civio/commit/9f3891c6acbeb6090463cb6df7f61e53683a8666))
- Variant clone removal, MSI cleanup SQL, unique pool counts ([9bf7508](https://github.com/Vincenzo-OPC/Civio/commit/9bf7508d856bba7a4e1f3b9a3a749b54f2bed861))
- Track every difference from the baseline; honest Entire status ([f28f717](https://github.com/Vincenzo-OPC/Civio/commit/f28f717e80e42aa59ed7d1bfc642363730a2d200))
- Lite mode plan for cheap phones and slow internet ([db775f7](https://github.com/Vincenzo-OPC/Civio/commit/db775f77a0bc52c5f332098b3f2c107ea8de5f1a))

### Style

- Prettier on guest-study-bias ([891b720](https://github.com/Vincenzo-OPC/Civio/commit/891b7209c7c51fad1467402c540c8dedd8135bfd))

### Chores

- Make test:js glob work under sh and clear lint baseline ([ed5aa64](https://github.com/Vincenzo-OPC/Civio/commit/ed5aa64a91eb538d21f851c16332a9009676f0fc))
- Remove two leftover .bak-demo copies missed by the junk cleanup ([ba8c622](https://github.com/Vincenzo-OPC/Civio/commit/ba8c6229bf9f6b01440b76a8cd45a7202a012a9e))
- Add git-cliff changelog config and size-limit bundle budgets ([9dcdf3b](https://github.com/Vincenzo-OPC/Civio/commit/9dcdf3b40b3dc3d0165563f484fae44c574f36ff))

## [0.1.0-phase0] - 2026-10-05

### Security

- Server-side grading, withhold keys, ID-keyed answers ([d19afda](https://github.com/Vincenzo-OPC/Civio/commit/d19afdaa3e65e58ae558475a8d3cdc7049c6a09e))
- Lock dangerous routes; draft custom questions; nullOnDelete ([761a3bd](https://github.com/Vincenzo-OPC/Civio/commit/761a3bdc73ac7dd595f59564098d47377a6b10de))

### Features

- Add vite-plugin-pwa, ts-fsrs, Prism tutor stub, Sentry opt-in ([9fe51a4](https://github.com/Vincenzo-OPC/Civio/commit/9fe51a4daf8f9f32d53ffda7f2321aa4554e9e04))

### Performance

- Lazy-load Inertia pages to code-split the main bundle ([6277c17](https://github.com/Vincenzo-OPC/Civio/commit/6277c172297e9226427c6722052eb0869db50738))

### Tests

- Align Pest with guest unlimited and draft custom questions ([ce41c82](https://github.com/Vincenzo-OPC/Civio/commit/ce41c82ea98a59a4b443c4a7d149f45a775c33a2))

### Chores

- Add Codex/Claude agent setup, Entire, and Phase 0 docs ([d66d2aa](https://github.com/Vincenzo-OPC/Civio/commit/d66d2aa9f91220db9d39180f4beca3d926c65be5))
- Remove legacy ads/donations and committed debug junk ([e21d94c](https://github.com/Vincenzo-OPC/Civio/commit/e21d94c31a97dcbabf2d3088572b5d87c957caca))
- Rebrand to Civio across UI, meta, and docs ([5fe2d40](https://github.com/Vincenzo-OPC/Civio/commit/5fe2d40bcd3a2ff8f0db5e30ffe847a22987a46e))
- Green tsc/eslint — stub content-shield, timer hooks, ignores ([acedd26](https://github.com/Vincenzo-OPC/Civio/commit/acedd262380ea8f0caa04f046bcca10e26b8758a))
- Remove hand-written public/sw.js after vite-plugin-pwa ([647e484](https://github.com/Vincenzo-OPC/Civio/commit/647e4840158e1e26fa1d4edc7cbe4f28640be4fa))


