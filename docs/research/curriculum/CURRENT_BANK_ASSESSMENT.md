# Civio bank assessment, 21 October 2026

**The 2,000-question milestone remains incomplete.** Examined main commit: `dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1`. Current main was rechecked before this checkpoint. No protected database, study service, deployment or active bank was touched.

## Verified repository inventory

| Evidence population | Count | What the count means |
|---|---:|---|
| Main primary batch records with stable IDs | 1,577 | Excludes fix overlays and shortcut-only files |
| Declared approved / passed within those records | 1,478 | File labels, not verified active rows or signed release approval |
| Declared rejected within those records | 99 | 88 English + 11 General Information; excluded from 1,478 |
| Historical baseline export | 550 | Dated 17 October; no current runtime status established |
| Main primary plus historical export mechanically screened | 2,127 | 1,577 + 550; not a release count |
| Pinned repository artifacts across main and open content PRs | 146 | Includes snapshots, fixes, seeds and proposals |
| Item occurrences across those artifacts | 4,276 | Versions are counted repeatedly |
| Provisional identity groups across occurrences | 3,705 | Legacy identity mapping is incomplete; not unique approved questions |
| Conflicting identity groups | 294 | Different representations require version reconciliation |

The [source lock](data/source-lock.json) pins every inspected content PR. The [repository inventory](data/repository-inventory.json) has paths, source commits, fingerprints and flags. Open PRs 3-12 include metadata, baseline conversions, replacement drafts, gap batches and lint fixes. They have not been merged or counted as approved. Other open PRs cover styling, security and dashboard work; no concurrent work was overwritten.

Unmerged gap-fill-2000-01 through 05 contain **406 distinct candidate IDs**: Filipino 127, Numerical 80, Analytical 101, Clerical 48, GI 35, English 15. PRs 7 and 12 contain two representations of the same 99 Filipino IDs. Baseline conversion 550 is not 550 new questions. B3/B4 provide 49 replacement drafts. Lint-fix files contain 371 occurrences, primarily replacements; even added passage companions need identity review before counting. The 496-item reparameterized seed is a separate unapproved proposal, not a release collection.

## Independent answer checking and limits

The new [read-only auditor](../../../scripts/batches/audit/curriculum_20261021.py) derives results without importing generator answer tables. [Per-item evidence](data/main-audit.json) binds each result to a path, commit and SHA-256 digest.

| Check | Existing records checked | Result |
|---|---:|---|
| Exact numerical recomputation | 400 | 309 current approved-labeled + 91 historical baseline keys match |
| Data-table arithmetic | 41 | All keys match; all use totals or differences, a narrow interpretation family |
| Syllogisms | 44 | Exhaustive finite set models validate exactly one offered conclusion per item |
| Explicit numerical/date filing | 12 | All keys match the stated sorting rule |
| **Total independently checked existing keys** | **497** | **No key mismatch found in this checked subset** |
| Other main/export records | 1,630 | Answer not independently checked in this pass; includes rejected material |

The syllogism procedure treats universal premises without existential import and permits empty classes. The remaining hand-written syllogism needs a separate semantic mapping. Mathematical sequence checks validate the intended simple recurrence, not uniqueness among all possible mathematical continuations. Arithmetic correctness does not establish natural wording, strong distractors, good explanations or curriculum adequacy.

**Full editorial certification: not established. New independent content approvals: 0. New activations: 0.** No claim is made that all 2,127 records received full semantic review. Remaining language, legal, logical and explanation reviews are real work, not covered by a green script.

Existing `qa_all.py --no-fixes` passed for its 1,000 generated-item scope. Legal quote checks were skipped because its local source cache was unavailable. Its generator lookups and legacy exclusions cannot substitute for this independent audit.

## Defects and repetition

83 records have explicit quality flags: 55 generic/placeholder explanations, 19 indefinite-article errors, 5 implausible lace-border contexts, 1 implausible parent/child age gap, 2 option-text artifacts and 1 duplicate-option item. These categories total 83 in this snapshot. They are not 83 wrong keys.

- **Baseline #462:** repeated options make the answer non-unique. This is one confirmed structurally invalid item represented in two inventoried artifacts. Current active status is unknown. Keep excluded from any release candidate until reconciled and corrected through review.
- **`CIVIO-NUM-WP-ALGEBRA-000025`:** arithmetic yields a father aged 15 and daughter aged 5. Replace the context or retire it; a correct calculation does not rescue the scenario.
- **Baseline #343 / #349:** inspect stray option wording (`von 760` and inconsistent word-form distractor). #349 is an editorial consistency flag, not a numerical key error.
- All remaining exact flagged IDs and evidence are in `data/main-audit.json`. Do not blindly rewrite or deactivate runtime IDs from a historical export.

Duplicate screening found **0 identical normalized stem-plus-option sets** in the 2,127-record main/export population, **3 same-stem groups** with differing options, **1,713 near-similarity candidate pairs**, and **52 identical number-masked stem families**. Candidate pairs overlap and are not 1,713 duplicate questions. The three generic same-stem groups are not proven duplicates. [Full candidate evidence](data/duplicate-screen.json) records the method and passage-sibling exclusions. Semantic near-duplicate adjudication remains open.

Numerical overconcentration is confirmed: 78 percentage-change items; 30 two-share ratio problems; 29 two-worker combined-rate items; 27 mean-with-one-new-person items; 24 perimeter-cost items; 16 age-algebra items; 20 fraction-of-a-remainder items. The six added basic fraction/decimal items improve coverage but do not form a prerequisite curriculum. More order-of-operations and sequence questions in an unmerged batch do not close these gaps.

## Gap to the milestone

| Domain | Current approved-labeled files | Internal proposed target | File-label shortfall |
|---|---:|---:|---:|
| English Verbal | 287 | 300 | 13 |
| Filipino Verbal | 188 | 300 | 112 |
| Numerical | 309 | 400 | 91 |
| Analytical | 251 | 400 | 149 |
| Clerical | 207 | 300 | 93 |
| General Information | 236 | 300 | 64 |
| Total | 1,478 | 2,000 | **522** |

**522 is not the verified release gap.** It excludes potentially usable baseline items and ignores later exclusions, identity conflicts, signature status and coverage floors. Conversely, adding 550 historical baseline rows gives 2,028 raw approved-labeled-plus-baseline records, not a valid release total. The exact gap is `2000 - count(distinct eligible approved item versions)` after adjudication, with duplicates, rejected items and superseded versions excluded. That count is currently **unknown**.

Historical documentation reports 1,978 active and 227 draft database rows on 17 October. This session did not verify those figures. Do not describe them as current.

## Preserved outputs and next gate

- [All 45 Vera records](VERA_45_QUESTION_AUDIT.md): 9 missing correct choices; every source ID retained.
- [Official scope and sources](CSC_COMPETENCY_GAP_MAP.md).
- [Production and approval plan](QUESTION_QUALITY_AND_PRODUCTION_PLAN.md).
- Ten original foundational numerical drafts are saved under `data/`, separate from active bank locations. All remain `draft/unreviewed`, authored by this session and therefore requiring a different reviewer.

Checkpoint tests: 407 Pest tests passed, 3,960 assertions; TypeScript, ESLint, production build and size checks passed. All 98 JavaScript tests passed using `node --import tsx --test tests/Js/*.test.ts`; the npm wrapper was blocked by this environment's IPC socket permission. Initial checks before build/key setup failed from missing generated routes/assets/application key and were rerun after isolated setup. No PHP or frontend application files changed. QA and these results do not approve content.

Product continuation: [educational/product handoff](CODEX_EDUCATIONAL_HANDOFF.md) records scoring disagreement, guest/exposure limits, existing features, design references and prioritized recommendations. [Personal mastery plan](SUBPRO_MASTERY_AND_FORECAST.md) and the 44-node blueprint are proposals, not measured learner results.
