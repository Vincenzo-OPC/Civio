# Resumable Dexter content production

Checkpoint parent: `70586e4e15455a9e071255ca1bb52656006d107c`. All artifacts here are offline research drafts, not runtime content or bank approvals. The original 60 sidecars and canonical questions remain unchanged.

## Faster workflow now in place

`bulk_pipeline.py` accounts for every one of the 2,100 manifest candidates in a resumable ledger. It reads each source file once, checks source hashes, key/option structure, explanations and distractor-code presence, then queues work by method. Seventy archetype labels yield 73 work groups; these are **not 73 verified conceptual families**.

The owner-selected worker was actually run as `gpt-6-luna`, reasoning effort `medium`. Its registry supplies draft prerequisites, prompts, hints, evidence boundaries and binding instructions for every work group. A recipe is reusable authoring scaffolding, not proof that every question in its group has a valid lesson. Calculation prompts are method checks, not automatically comprehension diagnostics. No Civio provider connection or inference activation was introduced.

Process each group in one batch: inspect conceptual differences, split mixed methods, author once per actual method, bind stable source IDs, verify every binding, and send ambiguous exceptions for stronger review. Continue through the queue without asking the owner after each small slice. Save consolidated checkpoints after meaningful batches rather than producing a separate report per five items.

Fingerprints include the full source record, manifest row, pipeline policy/implementation, misconception taxonomy, and relevant recipe entries. Unchanged records are reused. A source change invalidates that record; a recipe change invalidates only its dependent group. A changed validator/policy may intentionally require a full mechanical pass. No recurring service or new orchestration engine is needed.

## Evidence at this checkpoint

| Check | Result | Meaning |
| --- | ---: | --- |
| Candidates accounted for | 2,100 | Repository manifest, not live database inventory |
| Bank labels | 1,377 approved; 38 reviewed; 685 draft | These labels are preserved, not new independent approvals |
| Mechanical problem records | 0 | Structure and required-field checks only |
| Fresh exact supported-stem math checks | 38 | Explicit percentage/interest contracts; script abstains elsewhere |
| Additional overlay QA | 25 keys, 75 distractor amounts | Five interest and 20 ratio bindings; five keys overlap the 38 above |
| Distinct keys checked by these two passes | 58 | Not an independent audit of all 2,100 answers |
| Records with unmapped taxonomy codes | 1,565 | Integration work; not automatically incorrect answers |
| Runtime tutoring approvals | 0 | Draft production never changes activation eligibility |

See `bulk-summary.json` for current split counts and support stages; `bulk-state.json.gz` contains every ID, source hash, remaining actions and group membership. The ledger uses deterministic standard gzip compression to avoid committing 2.2 MB of repetitive JSON; `gzip -dc docs/research/dexter3/bulk-state.json.gz` reads it, and the pipeline loads it directly. The registry is compact per group, though represented as readable JSON. All 73 group drafts need semantic binding review. Mixed groups explicitly require splitting before binding.

`math25-v0.1.json` advances the five simple-interest and 20 ratio drafts through two reusable flows: interpretation, confirmation, prerequisites, hints, assisted retry and authorized explanation. Full target transfer IDs remain null. The inspected approved ratio subset repeats second-share-from-total; the approved combined-work subset adds fraction/rate prerequisites (the broader NUM-WP-RATE group mixes other methods and is flagged for splitting) and is not automatically beginner transfer. `NUM-WRONG-BASE` currently points to percent remediation in the canonical taxonomy; the ratio overlay proposes a local denominator hypothesis without altering that taxonomy.

Known editorial exception: whole-year interest bindings still contain a month-specific confirmation response. Prune it or use a duration-specific branch before runtime approval. Shared recipes, worked solutions and flows remain author drafts despite passing mathematical and structural checks. Neither the author pass nor Luna drafting supplies human adjudication or learner mastery evidence.

## Run and resume

```bash
python3 docs/research/dexter3/build_math25.py
python3 docs/research/dexter3/bulk_pipeline.py --write
python3 docs/research/dexter3/validate_bulk.py
```

The overlay builder refuses silent changed overwrites. Version reviewed revisions explicitly. The queue never counts missing lessons as complete. `validate_bulk.py` checks complete one-to-one accounting, warm-cache reuse, source/recipe invalidation scope, draft gates, source references, exact overlay calculations and distractors, node reachability, rendered parameters, acyclic paths and budgets. Its results are `bulk-validation.json`.

## Remaining queue and minimal implementation boundary

1. Split flagged numerical groups and verify operation/target meaning across each member. Fix context-sensitive code mappings through the existing approval workflow, rather than relabeling a learner from a selected option.
2. Bind the remaining numerical family drafts with checked solutions, response-specific diagnostic branches and explicit transfer gaps. Then clerical, language, analytical and General Information groups. Dictionary and official primary-source checks remain mandatory; missing evidence is an exception, not a model-confidence pass.
3. Preserve distinct roles for same-family retrieval, genuinely unfamiliar transfer, helped retries and first independent responses. Search approved sources only; different numbers do not establish transfer. Report gaps without generating approved replacements automatically.
4. Stronger review handles conflicts and instructional exceptions; human decisions stay pending until real adjudication. Resume from the ledger rather than repeating inventory or regenerating existing sidecars.
5. Codex implementation remains gated by Issue #28 answer persistence, Issue #29 handoff work and existing security/performance priorities. Reuse the Guide Me contract already in this directory: server-owned state, owner-scoped served Study attempts, one current node and opaque response IDs, no full-sidecar client payload, no Strict Mock tutoring, ordinary authorized explanation fallback, source-current metadata and assistance marked before help. Reuse RevealTutor/MisconceptionDiagnoser/RescueService/SkillGraph/FSRS; no new engine.

No application behavior, canonical bank content, approval status, protected services, billing, inference lock or deployment settings are changed by this checkpoint.

## Verification actually completed

Research checks passed: manifest (2,100 IDs, zero problems), original pilot validator, price-patch validator, 19 bank-gate tests, Python compilation and `validate_bulk.py`. The new overlay pass checks 25 keys and 75 distractor amounts; queue cache fixtures prove 2,100 warm hits, one-record source invalidation and group-scoped recipe invalidation.

Repository pre-publication checks also passed: TypeScript, ESLint, Vite build, and 622 PHP/Pest tests with 5,254 assertions. Local setup required a worktree-specific Composer autoloader, generated Wayfinder forms, a disposable test encryption key and a 1 GB test-process memory setting. These are test-environment setup, not application changes; initial attempts failed before that setup. No browser, learner study or human approval is claimed.

## Numerical batch 1: order of operations and sequences

Checkpoint parent: `8b69fffbba83fc663e6a2389bdae880a325314d8`.

The independent exact-rational screening pass covers all **84** records in two groups: 33 order-of-operations and 51 number sequences. It parsed operations under a restricted AST, checked exact values against all options and stored keys, and matched sequence candidates to the single offered keyed option under conventional rules. All 84 stored keys match; all 84 have canonical explanations and distractor codes for every wrong option. This verifies these answer paths, not whether each distractor is a good diagnosis or whether an explanation teaches effectively.

The 51 sequence items are not one family. Their stored-key methods resolve to 45 growing-gap patterns, two consecutive-square patterns, two previous-two-sum patterns, one square-gap pattern and one prime pattern. In the approved subset, 28 of 29 sequence items use growing gaps and one uses consecutive squares. The bank therefore overstates sequence-method variety. Three stems also admit a different familiar next-term rule whose result is not offered; the answer remains uniquely supported by the choices, but these items should say what kind of pattern to inspect if used outside a multiple-choice context.

The exact term list `11, 15, 20, 26, 33` appears in both `CIVIO-NUM-SEQ-DIFF-000220` and `CIVIO-GF2K02-SEQD-0010`. It is recorded as a duplicate candidate, not silently counted as diverse practice.

A draft Guide Me sidecar now binds reusable rule diagnostics to **59 approved source records**: 30 order-of-operations, 28 growing-gap, and one square-sequence item. The other 25 records were audited but excluded from bindings because their source bank status is draft. The draft asks which rule applies before revealing the arithmetic, includes response-specific teaching and self-report confirmation, and keeps any learner hypothesis provisional. All 59 have no approved distinct-family transfer yet. Existing question IDs, keys, options and source text are unchanged; no item or tutoring draft is runtime eligible.

Re-run:

```bash
python3 docs/research/dexter3/audit_numerical84.py
python3 docs/research/dexter3/build_numerical84_tutoring.py
python3 docs/research/dexter3/validate_numerical84.py
```

The audit is exact and reproducible, but it does not replace the separate editorial review of human-readable diagnostic branches, distractor validity or learning effectiveness. These 59 bindings remain draft pending that review.

## Numerical batch 2: averages, geometry and algebra word problems

Checkpoint parent: `c2f003c6746573e82d8d07ec1206b9ad22aad3ef`.

A deterministic, method-specific pass audited **87 records**: 29 averages, 22 geometry and 36 algebra. All 87 calculations matched the stored key and exactly one choice; the supported stems all include feedback for wrong options. No key conflict was found. The 60 source records labeled approved received draft tutoring bindings; 8 reviewed and 19 draft records were audited but excluded from tutoring bindings.

The 60 approved bindings reuse three concept-specific diagnostics: recovering a group's total from its average before adding a member; finding rectangle perimeter before applying a per-meter rate; and translating present/future age ratios into an equation where both people age. Solutions were recomputed exactly, explanations still point to the unchanged canonical record, and every draft leaves transfer unresolved. Diagnostic responses are assisted and cannot establish mastery or a confirmed misconception.

The bank repeats 12 parameterized stem templates across this 87-item batch. The largest approved pools are 26 new-member average questions, 18 rectangle perimeter-and-cost questions, and 16 age-ratio questions. Repeated templates have different values or names, so this is evidence of narrow practice variety rather than proof that all are exact duplicate records. The separate sequence audit already identified one exact repeated term list.

Run:

```bash
python3 docs/research/dexter3/audit_word_math87.py
python3 docs/research/dexter3/build_word_math87_tutoring.py
python3 docs/research/dexter3/validate_word_math87.py
```

This is answer verification and a draft teaching scaffold, not independent editorial approval. Review calculations for distractors as distinct from checking their explanation presence; assess whether the diagnostic choices represent plausible learner strategies; and find appropriate approved transfer items before any runtime use.

## Numerical batch 3: fraction, decimal, percentage and operation foundations

Checkpoint parent: `d215839e34884296e61bdce7c16961df02f0a74a`.

The exact audit covers **65 records** across five queued groups: 41 fraction/decimal, 6 fraction/decimal operations, 9 basic percentages, 1 decimal and 8 basic operations. Deterministic templates computed all 65 answers with exact rational arithmetic, compared each result against all four choices, and confirmed exactly one matching stored key. The bank records include explanations for each wrong choice; their mathematical validity was not independently recalculated in this pass. No key conflict or unsupported calculation remained. This is key verification, not full editorial or misconception approval.

The 25 records labeled approved received draft tutoring bindings. The 40 records labeled reviewed or draft were audited but excluded from bindings. Of the approved set, 19 share one successive-remainder question structure: take a fraction from the starting quantity, then take a second fraction from what remains. The other six cover fraction addition, decimal multiplication/division, comparing fractions and decimals, fractions of the same whole, and fraction multiplication. They do not yet supply broad approved foundational coverage: several useful basic fraction skills appear only in non-approved records in this audited slice.

Percentage-base coverage is especially limited in the approved items: all nine basic-percentage records here are reviewed or draft, so none was bound to tutoring metadata. The reverse-raise item remains a draft. The 25 tutoring bindings ask about denominator/base interpretation, use an assisted diagnostic, and provide a checked solution. None has an approved transfer mapping. Nothing was activated or approved during this pass.

Run:

```bash
python3 docs/research/dexter3/audit_foundation65.py
python3 docs/research/dexter3/build_foundation65_tutoring.py
python3 docs/research/dexter3/validate_foundation65.py
```

Across the three queued numerical batches, 236 distinct records have targeted exact-key checks and 144 approved-source tutoring bindings are drafted. Remaining numerical groups still include the mixed `NUM-WP-RATE` pool, ratio, multiplication-pattern sequences, percent change and other topics. Do not read the current batch count as completion of the 2,100-item audit.
