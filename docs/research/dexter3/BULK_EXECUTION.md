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
