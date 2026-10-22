# Question quality and production plan

Date: 21 October 2026. Evidence baseline: `dbdf2bc04fe8d7edde4c8b7cf1e87be01138abe1`. This is a review request, not an approval or import instruction. Existing `BANK_IMPORT_APPROVAL.md`, spec v0.1.9 and the current security-first execution plan govern.

## Concrete content packet

[Ten original numerical drafts](data/original-foundations-10-draft.json) address fraction subtraction/equivalence, fractional budget change, substitution, distribution, elapsed time, reverse ratio, relative efficiency, staff-hours and area from perimeter. Aliases CURR-001 through CURR-010 are recorded in notes. Their stable IDs end 210001 through 210010. They are original authoring, not copied Vera stems or number substitutions. No global originality guarantee is implied by a similarity screen.

[Author derivations](data/original-foundations-10-author-checks.json) and [QA outcomes](data/original-foundations-10-qa.json) preserve exact arithmetic, unique numeric answers and all 24 option permutations per item. None of these checks is an independent reviewer approval.

**Existing full QA is blocked:** `qa_file.py` raises an AttributeError when its NUM-FRAC-DEC solver assumes every fraction question contains `had <integer>`. Per-item checks also expose unsupported rate/algebra/geometry wording. Structural-only checks pass for all ten using an explicitly labeled no-solver view; the published item JSON does not contain `_legacy`. Do not use this structural result to bypass full QA. A separate reviewer can assess the packet now; activation remains blocked until full validation and the signed approval workflow are satisfied.

The parser limitation is educationally important: a validator must fail safely on unsupported questions, not pressure writers into copying its generator templates. Codex should distinguish unsupported derivation from a wrong answer, preserve a manual proof path bound to the item digest, and still require independent review. Do not auto-accept arbitrary expected answers from the author.

## Existing corrections requested

| Priority | Exact target | Required action | Acceptance evidence |
|---|---|---|---|
| P0 | Historical baseline #462 | Reconcile current version; exclude duplicated choices; author a fresh spelling item only if needed | Four distinct choices, orthographic source, single answer, external reviewer |
| P1 | `CIVIO-NUM-WP-ALGEBRA-000025` | Replace implausible family ages or retire the item | Plausible situation, re-solved equation, justified distractors |
| P1 | 55 explanation flags in main-audit.json | Write specific steps, reason for each wrong option and a check | Explanation addresses this item's quantities and concept |
| P1 | 19 article and 5 lace-border flags in main-audit.json | Review wording without altering a key silently | Versioned before/after digest and answer recheck |
| P2 | Historical #343 and #349 | Correct option artifact / consistency after identity reconciliation | No encoding artifact, original key preserved or separately corrected |
| P1 | Number-masked and near-similarity families | Adjudicate retain, revise, reserve for teaching, or exclude from milestone | Family ID and rationale, not automatic deletion by text score |

No source batch or historical export was overwritten. Proposed actions require the independent reviewer to rule item by item. New fixes must be versioned overlays tied to original IDs and hashes. The existing importer is immutable and signed; old instructions describing stem upsert must not override the current gate.

## Full-bank completion sequence

1. Resolve 294 identity conflicts and map baseline IDs to the release collection. Preserve rejected and superseded records outside the count.
2. Reuse this audit's 497 key proofs only for their exact content hashes. Finish semantic answer, distractor, wording and explanation reviews on remaining eligible records. Language reviewers must inspect English and Filipino meanings, not just grammar flags. Verify GI against dated primary sources.
3. Give every item a skill, micro-skill, prerequisite, objective, cognitive demand and family/fact/passage grouping. Track missing metadata separately from incorrect content.
4. Approve a coverage matrix and within-domain family caps before filling raw numerical targets. Keep the proposed six-domain allocation unchanged pending GT's decision.
5. Review the 406 unmerged gap IDs and replacement packets before commissioning more bulk writing. Mark duplicate versions of the same Filipino batch explicitly.
6. Review these ten drafts independently. Require exact recomputation, reverse check, one defensible choice, believable distractors, clear units and hand-solvability. A second AI pass alone does not grant approval.
7. Produce a manifest and independent review report bound to exact hashes. GT approval uses the existing Ed25519 SSHSIG namespace `civio-bank-approval`; author, reviewer and final approver remain separate. Never request or commit a private signing key.
8. Engineering may validate in isolated test storage. No live import or activation is authorized by this report. Obtain the separately required authorized release action, then verify actual count and version status.

## Editorial and psychometric rubric

Correctness, uniqueness, scope and provenance are veto gates. Score quality separately: clarity, explanation usefulness, distractor plausibility, transfer value and accessibility. Use Bloom's remember/understand/apply/analyze dimensions to describe the thinking demanded, not to equate long questions or rare words with difficulty. Evaluate/create tasks belong mainly in learning activities, not forced into every MCQ.

Empirical difficulty is the observed proportion correct on first unaided exposure in a stated sample. Report sample size and uncertainty; do not treat today's editorial easy/medium/hard labels as calibrated. Inspect distractor selection and item-total relationships only in sufficiently sized, comparable administrations. Adaptive samples, repeated exposure and very small subject counts can distort these statistics. Do not fit an IRT model or publish readiness probabilities without an appropriate study.

The full 2,000 milestone requires a verified unique release count, resolved defects, coverage, separate independent review and GT approval, not just a total of JSON rows. The exact remaining release gap is unknown today.
