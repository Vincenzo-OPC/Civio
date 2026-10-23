# Dexter 3.0 content checkpoint: 23 October 2026

**Review packet ready:** [15-item adjudication instructions and four foundation-candidate checks](PRICE15_REVIEW_READY.md). Independent reviewer fields remain blank; this adds review evidence without approving candidates or changing the pilot.

**Next checkpoint:** [15-binding editorial QA, draft v0.2 overlay and Guide Me handoff](PRICE15_EDITORIAL_REVIEW.md). The original v0.1 pilot remains intact. This follow-up is an author second pass, not independent human approval.

**Draft research and tutoring metadata, not an implemented or approved tutor.** Examined main `78df5c26b07b5c94b53482c2f6200ab4a49a1551`. This extends the [Guide Me proposal](../dexter2/SOCRATIC_GUIDE_ME_AND_BANK_ENRICHMENT_2026-10-23.md), [October 23 intelligence review](../dexter2/INTELLIGENCE_REVIEW_2026-10-23.md), [October 22 audit](../DEXTER_2_RESEARCH_AUDIT_2026-10-22.md) and [60-item packet](../dexter2/pilot/README.md). It does not replace the execution roadmap.

## Verified bank state

All 2,100 manifest records resolved in 40 source files. Source content hashes, statuses, unique identities and manifest/CSV consistency passed the existing manifest validator. This is repository evidence, not a live database inventory or a new semantic certification of 2,100 answers.

| Domain | Marked approved | Draft | Reviewed | Total |
| --- | ---: | ---: | ---: | ---: |
| Numerical | 257 | 105 | 38 | 400 |
| Analytical | 241 | 159 | 0 | 400 |
| English | 286 | 114 | 0 | 400 |
| Filipino | 178 | 122 | 0 | 300 |
| Clerical | 202 | 98 | 0 | 300 |
| General Information | 213 | 87 | 0 | 300 |
| Total | 1,377 | 685 | 38 | 2,100 |

**Correction to the historical audit:** 1,136 marked-approved candidates are Subprofessional eligible: 934 `both` plus 202 `subprofessional`. The earlier 934 count omitted the latter because `bank_metadata_audit.py` checks `('sub', 'both')`, while the manifest uses `subprofessional`. Historical output is retained; do not propagate its eligibility total. This does not change approval or live status. The 2,000 verified-and-approved milestone remains unproven; 623 is only the arithmetic shortfall from the 1,377 approved labels, not a verified production deficit.

All 2,100 candidates already have terms, a shortcut, `reveal.why_correct`, a rationale for every wrong option and a distractor code for every wrong option. Missing fields are not the principal problem. Presence does not establish the rationale’s accuracy or diagnostic usefulness. Full counts by archetype/status and the 40 source file digests are in [coverage-v0.1.json](coverage-v0.1.json).

## What this batch adds

[pilot-v0.1.json](pilot-v0.1.json) contains **60 draft item bindings**, preserving source IDs and hashes, across five reusable recipes:

| Recipe | Bindings | Verification in this batch |
| --- | ---: | --- |
| Successive price changes | 12 | Exact fraction arithmetic, additive check, exactly one matching option and key |
| Sale price | 3 | Discount subtraction and remaining-fraction calculation |
| Simple interest | 5 | Annual and monthly calculations, including fractional years |
| Two shares from a total | 20 | Unit-part calculation and independent ratio/sum equations |
| Spelling task direction | 20 | Reference/key/rationale consistency only; dictionary and linguistic review pending |

The 40 mathematical items have no answer/key conflict under these checks. This is not a full independent educational review. All 60 need editorial review; **zero sidecars are independently approved**. The original 180 reviewer rows remain untouched and unadjudicated. There are **zero validated transfer mappings**. No runtime consumer loads these files.

Each binding supplies an initial three-choice diagnostic, explicit correct/incorrect/uncertain feedback, meanings of the givens, worked steps, preserved distractor evidence and review blockers. Shared recipes supply prerequisites, interpretation mistakes, progressive hints and an exam method. All outcome fields are contracts, not learner records. The uncertainty branch assigns no misconception. Recipe-local hypothesis names are proposals, not additions to `config/dexter_misconceptions.php`.

The separate ₱640 instructional contrast diagnoses **original versus already marked-up value** before arithmetic. Forward: 640 → 800 → 640. Reverse: if 640 is after a 25% markup, original = 512. Subtracting 25% of 640 produces 480, whose forward check is 600 and therefore fails. It includes a second question about the discount base. This is a draft teaching example, not a new bank question or an independent transfer assessment. Correctness after seeing any of this help is assisted.

## Coverage and explanation concerns

1. **The old family heuristic overstates diversity.** `bank_metadata_audit.py::stem_family` lowercases before an uppercase-name regex, making name masking ineffective; it also truncates at 80 characters. Pilot hashes inherited from that procedure are not semantic-family approval. All 29 approved `NUM-WP-RATIO` records were inspected: they ask for the second share of a supplied two-person total. All 20 ratio pilot items are that same instructional frame. The 37 approved percentage-change records have just three broad tasks: forward successive price changes, sale price, and simple interest. Do not call renamed numerical clones unfamiliar transfer.
2. **Basic percent is a tagged approval gap:** `NUM-PCT-BASIC` has 0 approved, 6 reviewed and 3 draft candidates. It is not evidence that learners can never encounter a percent fact elsewhere. Explicit foundational assessment/transfer is missing under that graph node. There is no reverse-percent item among the 37 approved percentage-change records inspected.
3. **Foundations need finer mapping:** 19 approved `NUM-FRAC-DEC`, 6 `NUM-OPS-FRAC-DEC`, 30 `NUM-OPS-ORDER`, 16 algebra and 27 rate items are available by broad tag. These counts do not establish coverage of fraction meaning, equal wholes, equivalent fractions, denominators, base identification, unknown quantity or unit reasoning. Review these micro-skills before extending prerequisite gating. Zero approved `NUM-DECIMAL` or `NUM-PROPERTY` records under those specific tags is not proof of zero related content elsewhere.
4. **Specific percentage distractor code mismatch:** `CIVIO-NUM-WP-PCT-CHANGE-000030`, `000036`, `000224` label subtraction of the percentage numeral as pesos `NUM-WRONG-BASE`. Their prose identifies percent-as-money confusion, which is different from taking a percent of the wrong base. Preserve canonical data, flag for an editorial distinction, and ask which unit the learner assigned to the percent numeral. Do not assert a wrong-base diagnosis from that option alone.
5. **Spelling prose needs review:** `CIVIO-CLR-SPELL-WRONG-000090` says `basicly` drops “a letter”; correcting it to `basically` inserts `al`, two letters. The correction is sensible but the explanation is imprecise. The 20 word-specific corrections and all foils still need a dictionary/accepted-variety check. Correct foils do not reveal a specific spelling rule misconception.
6. **Taxonomy wording risks:** `NUM-GIVEN-REUSED` says a given number is rarely the answer; the valid ₱640 forward contrast shows why that is an unsafe elimination strategy. `NUM-PCT-ADD` says multiply by `(1 + rate)` each time without explaining negative rates for cuts. `NUM-WRONG-BASE` can mislead on successive changes if “original” is read as the first price rather than the current step’s base. Proposed content uses explicit stage labels and `(1 − discount)`; taxonomy edits require separate review. Spelling mnemonic exceptions and consonant-doubling exceptions should not be generalized into guaranteed rules.

Items already supported adequately **for the existing explanation format** are not necessarily supported adequately for Socratic diagnosis. This batch avoids rewriting their canonical explanations. The 40 math solutions gain checked scaffolding; the 20 spelling items gain only a task-direction scaffold. No item yet satisfies full approved-tutor-plus-unseen-transfer completion.

## Open-source findings and reuse decision

Primary repository license files and READMEs were inspected on 23 October. Exact observed commits and license blob IDs are retained in [reference-evidence.json](reference-evidence.json). No third-party code or lesson wording was imported. These are architectural recommendations, not measured Civio learning effects.

| Reference | Verified licensing evidence | Pattern useful to Civio | Boundary |
| --- | --- | --- | --- |
| [ai-tutor](https://github.com/NavyashreeNS/ai-tutor) | MIT LICENSE | Separate grading, prerequisite selection and misconception hypotheses; abstain when cause is unknown | Do not import its LLM classifier, confidence penalties or blanket prerequisite assumptions. Its NCERT graph is not a CSC curriculum. |
| [OATutor](https://github.com/CAHLR/OATutor) | MIT code; README separately declares CC BY 4.0 content | Authored problem/step/hint data and skill-linked help | Keep Civio’s stack and bank. Code license does not silently cover lesson attribution obligations. No Firebase or BKT migration. |
| [OpenMath](https://github.com/Galliard7/OpenMath) | README claims Apache 2.0; LICENSE, LICENSE.md and LICENSE.txt were not found | Separate precomputed solutions from interaction; explicit give-up/reveal transition | Code/content reuse remains blocked pending license scope. Its local model/hardware requirements are incompatible with assuming inexpensive phones can run it. Model-verified content is not human approval. |
| [Oppia](https://github.com/oppia/oppia) | Apache-2.0 LICENSE | Branch on learner response and attach feedback to the response, not merely correctness | Use an authored response map; do not import Angular/App Engine or assume lesson rights from code licensing. |
| [pyBKT](https://github.com/CAHLR/pyBKT) | MIT LICENSE | Later offline fitting/evaluation of skill-specific parameters | No runtime dependency or fitting without suitable consented evidence and validation. This content project does not calibrate mastery. |

## Implementation contract for Codex, after existing gates

The proposal below is internally checked, **awaiting independent architecture/editorial review**. Read `AGENTS.md`, [tutor policy](../../DEXTER_TUTOR_POLICY_2026-10-21.md), [feature catalog](../../FEATURE_CATALOG.md), [bank approval rules](../../BANK_IMPORT_APPROVAL.md) and current Issue #28/#27 state before implementation. No runtime work is authorized by this research batch.

| Field | Type / meaning | Rule |
| --- | --- | --- |
| `schema_version`, `status`, `runtime_eligible` | Version string, draft, false | Fail closed on unsupported version or unreviewed artifact |
| `question_id`, `source_file` | Existing canonical reference | Never rewrite keys, choices, source or approval status |
| `source_question_hash` | Existing manifest content digest | Recheck before using metadata |
| `source_record_sha256` | SHA-256 of sorted compact UTF-8 full record JSON | Also catches code/provenance drift omitted by the narrower manifest hash |
| `recipe_id` | Shared recipe lookup | Recipe prerequisites are content descriptors, not automatically registered graph nodes |
| `initial_diagnostic` | Prompt plus 3 stable-ID response branches | Exactly one meaning-correct branch; uncertainty has no hypothesis; wait after one question |
| `distractor_evidence` | Canonical option-ID/code/rationale triples | Hypothesis evidence only; never rely on shuffled display indices |
| `worked_solution`, `math_verification` | Authored steps and exact rational parameters/results | Source key conflict blocks use; numeric check is not pedagogical approval |
| `transfer` | Nullable approved ID, reason and status | Null is a real coverage blocker; never synthesize or pad an assessed bank item |
| `review`, `manual_review` | Null reviewer decisions plus explicit queue | Authors never fill human reviewer fields |
| `outcome_contract` | Reference to assistance/evidence rules | No generated learner events or mastery result |

`validate_pilot.py` is the executable v0.1 structural contract, using standard-library checks; it is not a claim of external JSON Schema certification. Keep the versioned authoring sidecar server-side. Resolve only a validated, source-current binding for an owner-scoped, served/graded Study attempt, then serialize only the current allowed prompt/response. Never ship the whole sidecar, key, hidden branches or worked solution in the initial client bundle, offline mock pack or active Strict session. Preserve existing Strict locks and server-authorized Reveal, including direct requests. An optional Skip/Reveal exit remains available under current rules.

Suggested future states: interpret → targeted diagnostic → small hint → retry → authorized worked solution → eligible fresh transfer → existing review scheduling. A wrong diagnostic response supports a possible interpretation error, not a permanent label. Missing metadata falls back to ordinary explanation; no eligible distinct-family transfer means report the limitation and offer ordinary practice explicitly labeled as practice.

Reuse `RevealTutor`, `MisconceptionDiagnoser`, `RescueService`, `SkillGraph`, `ExposureHistory`, existing attempt models and FSRS. Do not add an app, engine, mode, paid service, visual framework or new grading rule. No inference calls are needed. Learner-specific events must remain account/guest scoped and separate from this public authoring artifact. Diagnostic participation is assistance, not an additional exam answer. Preserve the original graded result; do not retroactively convert it into an unassisted success. A first unaided response recorded before later help can remain historical first-response evidence, while subsequent retries are assisted.

Acceptance fixtures: wrong original/final interpretation despite correct percent arithmetic; correct interpretation with arithmetic error; unsure response without diagnosis; discount-base confusion; forward and reverse operations; stale content/code hash; shuffled options; unserved or other-user attempt; active Strict request; no transfer pool; previously exposed transfer; helped correct vs first independent response; no success inflation after >50 attempts; reload/durable-answer failure; Lite/keyboard/360px and existing bundle budgets. These runtime tests are specified, not run here.

## Prioritized remaining work and resumption

1. **Existing engineering blockers:** finish Issue #28 answer durability, #27 performance, trustworthy first-response history/labels, and removal of generic false validator confidence. The temporary local Issue #28 patch from an earlier session could not be located in this environment; do not assume it is preserved or merged. No runtime files were edited in this batch.
2. **Editorial batch A, 15 price bindings:** independently review 12 successive and 3 sale-price diagnostic interactions, especially the base/unit distinction and ₱640 contrast. Keep the original 180-row packet as the approval evidence source; the sidecar cannot substitute for its two reviewers and adjudicator.
3. **Editorial batch B, 25 bindings:** review 5 interest and 20 ratio scaffolds. Correct family grouping offline, then look across the approved bank for genuine cross-context or reverse-operation transfer. The inspected same-archetype pools do not supply such diversity. Do not approve clones as transfer merely to fill a field.
4. **Editorial batch C, 20 spelling bindings:** validate all words/foils against an appropriate dictionary, correct explanations through the existing bank workflow where needed, and author word-specific diagnostic branches. The current generic direction check is a limited starting point.
5. **Foundational mapping:** inspect the 19+6 fraction/decimal items and 30 order-of-operation items at micro-skill level. Review existing 6 reviewed and 3 draft basic-percent records before authoring more. Identify approved reverse-percent and other transfer gaps honestly; use existing bank approval for any future corrections/activation.
6. **Only after review and owner activation gates:** implement a small Study-only server-authorized interaction and compare it with ordinary Reveal using first independent unseen-family correctness and delayed retention. No pass forecast or mastery fabrication.

Resume by validating the manifest and source digests, then working only the next queued batch. `build_pilot.py` avoids rewriting byte-identical outputs and refuses to overwrite nonempty review decisions; create a new sidecar version after review or source changes. Do not silently regenerate over authored revisions. This is a bounded v0.1 checkpoint, not completion of all tutoring metadata for the bank.

## Checks actually run

- `python3 scripts/batches/qa/validate_flat_2100_manifest.py`: 2,100 IDs, zero problems.
- `python3 docs/research/dexter3/build_pilot.py`: 2,100 source/hash resolutions, 60 bindings, 180 exact distractor links, 40 two-method mathematical checks.
- `python3 docs/research/dexter3/validate_pilot.py`: 60 contract/reference checks, 40 recalculations, ₱640 forward/reverse checks; five malformed fixtures rejected (hash, result, reviewer decision, multiple correct diagnostic choices, runtime activation).
- `python3 scripts/batches/qa/test_bank_gates_2026_10_22.py`: 19 passed.

No runtime/PHP/browser tests or learner study were run for this research-only change. No database, bank status, existing question content, activation flag or deployment setting changed. Independent reviewer decisions remain pending.
