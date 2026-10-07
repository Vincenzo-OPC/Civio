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

### Fixes

- *(analytics)* Safely handle missing keys in ai analysis orchestrator ([c6a173f](https://github.com/Vincenzo-OPC/Civio/commit/c6a173f1386a7d1d6e60b1d598ed5d93fc814228))
- *(view)* Plain-JS inline scripts so system dark mode applies before paint ([51c429b](https://github.com/Vincenzo-OPC/Civio/commit/51c429be12fb167d2c0f6cab1177daaae115db90))

### Performance

- *(lite)* L0 quick wins — on-demand PDF and realtime, light images, no unused fonts, slim precache ([5ea1cd5](https://github.com/Vincenzo-OPC/Civio/commit/5ea1cd57dae46bf009cc68d2f83afc668e87ff9f))

### Docs

- Regenerate CHANGELOG and point L1 rows at c825fe9 ([e1e48c4](https://github.com/Vincenzo-OPC/Civio/commit/e1e48c4bf1e790e5cdfb0dc42dfee7086f2be5af))
- *(agents)* Cursor is not used; Codex, Grok Build and Grok Bot are ([912d318](https://github.com/Vincenzo-OPC/Civio/commit/912d31826add2e2499f4da2906f9a54d1e0d105d))
- *(baseline)* Rename the diff log to CHANGES_SINCE_BASELINE and say baseline everywhere ([bc8d3dd](https://github.com/Vincenzo-OPC/Civio/commit/bc8d3ddd3ea380cdb398b130db7ee9bfe435692e))
- *(baseline)* Civio-only README and docs; fold the desktop patch log; drop old fork notes and audit ([a0019af](https://github.com/Vincenzo-OPC/Civio/commit/a0019af6eb42681221e7361ad873bd940ffa9207))
- Civio code standard and ranked modernization backlog ([fa431e0](https://github.com/Vincenzo-OPC/Civio/commit/fa431e05e2c50962b1ef65b91725a52290be66f4))
- Codex handoff plan, linked first from AGENTS; L2 rows point at 09c62da ([9a68dac](https://github.com/Vincenzo-OPC/Civio/commit/9a68dac822a138f1c41b2315168ae794f17414a7))

### Style

- Pint formatting for exam controller, Inertia middleware, routes and scoring test (no behaviour change) ([476a65a](https://github.com/Vincenzo-OPC/Civio/commit/476a65a95afe45be51c20002cf3f7c04037737e4))
- Pint formatting for the PHP seed scripts (no behaviour change) ([8e16919](https://github.com/Vincenzo-OPC/Civio/commit/8e16919c870ba7b785ed24495295c228291ca0ce))
- Prettier for vite.config.ts ([0470bc3](https://github.com/Vincenzo-OPC/Civio/commit/0470bc3d18088c57ec65047125dfe8458c581279))

### Chores

- *(entire)* Codex and Claude Code hooks, committed .githooks, git-refs settings; drop Cursor hooks ([3fe931b](https://github.com/Vincenzo-OPC/Civio/commit/3fe931b0dc622c9d17aff88a873e411ced4f576b))
- *(brand)* Neutral Civio mark, no author credit in the footer, full legacy storage migration ([08b4640](https://github.com/Vincenzo-OPC/Civio/commit/08b46403669930429ef921a5b5c23c5292f3f775))

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


