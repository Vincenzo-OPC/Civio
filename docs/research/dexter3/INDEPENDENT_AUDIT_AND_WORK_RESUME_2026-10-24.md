# Dexter 3.0: Independent manifest/source audit and exact Work resumption contract

**Date:** 2026-10-24 (PHT)  
**Base commit independently inspected:** `4067f44be287794e701b49918fc204e5d718cfcc`. Recheck `main` before writes.  
**Purpose:** Eliminate duplicated model work after Work usage exhaustion; audit status/count boundaries, distinguish authoring/QA/activation, and provide a bounded but persistent continuation program.  
**Status:** Independent read-only GitHub-content review; **no application/test command was executed locally**, no new question was mathematically solved by this audit, no signed question import, no runtime deployment, no AI spend.

## Independently verified source-level counts

Method: parse the frozen manifest `docs/research/bank/civio-flat-2100-manifest-2026-10-22.json`, inspect **all 40 source JSON files referenced by the manifest** via the connected GitHub API, compare each manifest record by ID and designated source-file path, and inspect the actual option/explanation contracts. For taxonomy, compare every manifest question's distractor-code values to the exact code set in `config/dexter_misconceptions.php`. These are structural and reference audits; this procedure **did not recompute each manifest SHA-256** (the existing local bank validator does that), independently re-solve all questions, or certify external facts.

- Manifest **2,100 entries / 2,100 unique IDs**: 1,377 `approved`, 685 `draft`, 38 `reviewed`. All 2,100 resolved in the designated source files; **0** ID-to-file reference failures, status mismatches, track mismatches or domain mismatches in this read.
- By domains (approved/draft/reviewed): Numerical **257/105/38**; Analytical **241/159/0**; English verbal **286/114/0**; Filipino verbal **178/122/0**; Clerical **202/98/0**; General Information **213/87/0**.
- Tracks: `both` **934 approved + 387 draft**, `subprofessional` **202 approved + 139 draft + 38 reviewed**, `professional` **241 approved + 159 draft**. Subprofessional-eligible approved labels = 934 + 202 = **1,136**.
- Every matched question had exactly four uniquely identified options, a stored answer ID present in those options, text under `reveal.why_correct`, `reveal.terms`, a shortcut, wrong-option prose and wrong-option codes. **Presence does NOT prove the correct option/rationale or learner misconception is valid.**
- Across the 40 referenced source files there are **2,857 total source-file rows**: **2,100** target manifest rows plus **757 additional rows not selected into this manifest**. Of those 757 *rows*, **101 carry approved**, **11 reviewed**, **645 draft** source labels. Cross-file identity/deduplication for those 757 rows was not established by this pass. They are **NOT a revision to the agreed 2,100 target** or confirmed live/eligible items. The manifest-only approved count is 1,377; counting 101 additional approved *source rows* yields 1,478 labelled rows within these files, NOT a production-approved/unique count. E.g. `docs/batches/batch-008.json` has nine approved-labelled records omitted from the manifest, including `CIVIO-NUM-WP-PCT-CHANGE-000612` and `000623`. The latter's stem says "A electric fan", suggesting at least some historical source material needs editorial correction. Determine why excluded before anyone considers using them.
- The 757 extras comprise 57 + 145 + 459 + 96 entries across four groups of ten source files; approved extras 16+47+0+38=101; reviewed extras 0+11+0+0=11; draft extras 41+87+459+58=645. Preserve separate *in-manifest*, *out-of-manifest* and *live database* denominators.

## Independently verified current Dexter coverage and code gaps

- Inspecting **nine** committed authoring files (`pilot-v0.1.json`, `math25-v0.1.json`, seven newer numerical guide-draft files) and joining their `question_id` values to manifest IDs found **257/257 approved numerical** question IDs with one or more **draft** tutoring bindings, plus 20 original approved-labelled Clerical spelling pilot IDs. **277 distinct bound question IDs** within those nine files. `math25` overlays 25 pre-existing pilot bindings: **25 deliberate cross-file overlaps**, not 25 extra unique questions. This is **coverage**, not approved tutoring, semantic correctness or verified transfer.
- `family-recipes-luna-v0.1.json`: **73** group recipes cover 2,100 candidate records across 70 archetype labels. **11** groups totaling **362** records require real semantic splitting; 62 are provisionally single-recipe groups, not validated families. The eleven: `NUM-WP-RATE` 45; `NUM-FRAC-DEC` 41; `NUM-OPS-FRAC-DEC` 6; `NUM-PROPERTY` 8; `CLR-FILE-POSITION` 92; `CLR-FILE-ORDER` 21; `VEN-SENT-COMP-WORD` 59; `GI-ENV-PRINCIPLE` 27; `ANA-ANALOGY-FORM` 26; `ANA-ANALOGY-PART` 18; `ANA-ANALOGY-SYN` 19.
- **73/73** registry entries have generic `recipe.transfer` wording requesting a distinct, checked *same-method* item. This is a **policy placeholder, not a per-item or distinct-family mapping**, and cannot establish unfamiliar transfer. Do not count that text as teaching/assessment completeness.
- Recomputing unmapped-code counts directly against the PHP Dexter taxonomy: **1,565/2,100 manifest records** have at least one distractor code not recognized by `config/dexter_misconceptions.php`: English verbal **400/400**; Filipino verbal **300/300**; General Information **300/300**; Analytical **398/400**; Clerical **167/300**; Numerical **0/400**. These are *unsupported mappings*, not necessarily incorrect questions. The current code focuses on numerical and selected clerical codes. Build a reviewed, domain-aware taxonomy rather than treating unknown codes as incorrect or assigning a guessed nearest match.
- `bulk-summary.json`: **2,013** records marked family drafts needing binding review; **15** price refined drafts with separate AI critique; **25** math overlays pending flow QA; **27** family recipe candidates pending binding review; **20** initial drafts needing refinement; **0** runtime-approved tutor artifacts. Those statuses measure stages, not mutually independent unique completed educational conversations.
- `price15-v0.3-patch.json` is a hash-bound **draft patch**, NOT a new reviewed/materialized runtime sidecar. A separate AI critic identified seven shortcomings with the price v0.2 flow and followed up on v0.3 changes, but human reviewers did not validate the content. Keep these facts precise.
- Numerical source work previously reported targeted exact checks for all **400** numerical manifest records; English spelling lexicon screen for **133** sources. Those scripts' reported checks were not re-run in this read-only audit. Do not equate them with human/editorial/full-learning validity.
- The existing `ReportIssueModal`, polymorphic `Feedback` model, `FeedbackService`, and `admin/feedbacks` must be **reused**. In current code, the submit request accepts arbitrary client `flaggable_type` as a string and targeting uses client ID; triage status changes can resolve all pending reports against a question. See issue #30 for server authorization/morph whitelist, per-artifact-version triage and fail-closed rollback. Reports are signals, not source-of-truth answer revisions.

## New risk ranking and definition of "done"

A record is:
1. **Indexed** if manifest/source identity validated.
2. **Mechanically validated** only for named tested properties (math, syntax, option correctness, source date, or other domain-specific checks). Log individual verifier and fixture coverage.
3. **Instructionally drafted** if its concept-appropriate interpretations, branching, targeted hints and fallbacks exist.
4. **AI critiqued** if a fresh-context critic produces auditable evidence/counterexamples, not an unsupported confidence number.
5. **Quality-cleared for a limited pilot** only if a separate, explicitly authorized product gate and reproducible targeted checks agree; label the actual reviewer type. No fabricated human decisions.
6. **Runtime eligible** only after correct server authorization, Strict secrecy, stale-hash guards, independent-help accounting, rollout controls and owner activation.
7. **Independently transferred** only when a *fresh, approved, distinct-method/family* question is answered without help, and its shared competencies are stated precisely. Repeated numbers/stems, same-family practice, guided success, and answered-before-reveal have different evidence types.

Severity queues: **P0** answer/key conflict, unsupported or ambiguous single-answer claim, pre-reveal leak, Strict exposure, incorrect authoring source hash, illegal source use; **P1** mathematically correct but misconception misdiagnosed, wrong units/base, vague generic branch, unsupported prerequisite, incorrect transfer label or stale GI law; **P2** wording, tone and duplication with valid canonical answer. A learner report is *not* an automatic verdict. Keep current signed approval policy; an AI cannot self-sign as a human or as GT.

## Exact continuation order for ChatGPT Work, not Codex

**Pass 0: freeze/resume, mostly zero-token automation**
- Read `AGENTS.md`, this file, `BULK_EXECUTION.md`, `bulk-summary.json`, `bulk-validation.json`, `bulk_pipeline.py`, `family-recipes-luna-v0.1.json`, Price v0.3 reconciliation and current Issues #28/#29/#30. Confirm latest HEAD. Do not redo original manifest inventory or regenerate any committed 60/257 bindings.
- If a file-capable checkout is present, rerun bank hash/manifest validators and `validate_bulk.py`; if not, explicitly say the GitHub records were inspected and tests were **not** run. Resume from `bulk-state.json.gz` (never delete or reset).
- Create/update a **small** machine-readable `qa-review-queue-v0.1.json` containing only unresolved cases and `work-resume-state-v0.1.json` recording `base_sha`, `batch_id`, `family_cursor`, counts by verified stage, dependency hashes, committed artifacts, and next action. Do not repeat all questions in model context.

**Pass 1: excluded-source provenance, limited mechanical work**
- For the 757 extra source *rows*, determine unique IDs, cross-source duplicate/replacement lineage, status provenance, and whether excluded intentionally. Flag the **101 approved-labelled extras** separately. Deliver a compact exception summary with IDs of contradictions, not a new 2,857-item bank or a request to import them. No model prose-generation pass needed unless exceptional.
- Reconcile statuses only within the manifest for operational counts. Track the extra rows separately.

**Pass 2: semantic split the eleven groups (362 records)**
- Process all **100 numerical** records in the four mixed NUM groups, beginning with `NUM-FRAC-DEC` (41), then `NUM-WP-RATE` (45), `NUM-OPS-FRAC-DEC` (6), `NUM-PROPERTY` (8). For each record, identify `given_quantities`, `sought_quantity`, `method_signature`, `prerequisite_micro_skill`, `formula_or_rule`, `evidence_scope`. Separate unknown-whole, stage/base interpretation, operations, conversions, combined-work from speed/rate, and distinct fraction skills. Write one lesson per real method, not one per archetype string.
- Then split 113 clerical rows (`CLR-FILE-POSITION` 92 and `CLR-FILE-ORDER` 21) by exact filing convention including prefix/title/word-by-word and domain of official rule.
- Then English word-choice 59, Analytical analogy 63 and GI environmental items 27; order by critical error risk, source specificity and approved learner eligibility. Total 100 + 113 + 59 + 63 + 27 = 362. Add a stable `semantic_family_id` and family-specific golden examples.
- Do not assume all non-split groups are semantically sound; sample across distinct templates to detect hidden mixing.

**Pass 3: taxonomy and diagnosis QA**
- Use the observed **1,565** unmapped-code records as a coverage measure and rank *distinct code types*, not 1,565 repeated model prompts. Build domain-specific proposed code dictionary with definitions, example wrong answers, counterexamples, remediation, code provenance and `unknown/abstain` branch. Compare each offered wrong option with an exact plausible explanation; a selected option alone supports a hypothesis, not confirmed reasoning.
- Prioritize high-risk existing `NUM-WRONG-BASE` misuse on price/ratio unit confusion; `NUM-GIVEN-REUSED` ("rarely the answer" is unsound); `NUM-PCT-ADD` handling of decreases; ambiguous spelling `yield`/`yeld`; cases where discount amount coincides with amount paid. **No canonical code replacements without current bank approval.**
- Per distinct semantic family, create **golden conversation tests**: misread initial stage; correct arithmetic/wrong target; wrong arithmetic/correct setup; percent-as-pesos; intermediate raised price; guessed correct; uncertainty; after hint correct counted assisted; Strict attempt rejected; stale binding; missing transfer fallback. Assess exact response-specific feedback, no overconfident diagnosis, no answer leakage.

**Pass 4: focus AI review on real exceptions, not repeated data**
- Routine: deterministic Python rational/relational solvers, stable hashes, single-key validation, grammar/dictionary screen as *screen*.
- Use separate fresh-context AI review only for P0/P1 exceptions, novel semantic families and a representative controlled sample of ostensibly clean cases. Ask the critic for an explicit counterexample and whether supplied evidence supports each claimed learner error. Preserve reviewer identity as `AI` with model/config/date, source hash and limitation; keep two AI passes distinct from nonexistent humans.
- For GI/current law: verify primary official dated sources; missing citation means source review required, not "factually verified." For English/Filipino/spelling/clerical, honor dialect, ambiguity, actual instructions and applicable conventions.
- All 73 placeholder transfer instructions must be replaced by per-family **role descriptions** (`near_practice`, `cross_context_prerequisite`, `full_target_transfer`, `none`) and, only when justified, an approved unseen candidate ID with family overlap and exposure constraints. An ID remains `null` if suitable approved questions do not exist.

**Pass 5: checkpoint and handoff**
- Use Work's available medium-effort draft mode (Luna if available) for straightforward batches; higher effort/fresh context only for exceptions. No provider/model assumption as runtime guarantee. No use of paid Civio APIs.
- Write tightly versioned sidecars and a *single* consolidated exception queue; avoid verbose per-five-item progress documents and repeated full-bank reads. One method-family checkpoint should target about **25–100 records**, smaller for genuine high-risk exceptions. Commit after a coherent verified family/batch, no force push, `[skip netlify]` for docs-only commits. Preserve all prior 60 pilot, price v0.2, unmaterialized v0.3 patch and other numerical drafts. Use current HEAD/lease protection against concurrent writers.
- Per checkpoint report **exact**: manifest IDs inspected; source extras classified; distinct semantic families resolved; answer computations rerun; new/updated *draft* bindings and IDs; AI-critic-reviewed exceptions; unresolved high-risk cases; transfer mappings by role; runtime approvals (expected 0); validator commands actually run and results; commit SHA; next cursor. Do not conflate these.
- Keep going through available usage without asking permission after every mini-batch; if usage ends, the last committed resume state is the truth. Do not claim background/asynchronous completion.

## Required output artifacts (minimal)

- `docs/research/dexter3/qa-review-queue-v0.1.json`: stable IDs, source/version hashes, `reason_code`, severity, reproducible evidence, reviewer_kind, action needed, status and next recheck. An absence of a field is not a successful check.
- `docs/research/dexter3/work-resume-state-v0.1.json`: HEAD/source ledger digests, confirmed coverage denominators, family cursor and exception counts; continually updated in each verified checkpoint.
- `docs/research/dexter3/semantic-family-splits-v0.1.json`: assignments of all 362 mixed records, recipe IDs and methodological basis, reviewed as draft; retain reference to `bulk-state` without duplicating its full raw content.
- Existing **versioned** lesson/sidecar files extended only where justified, plus a short audit summary including zero unsupported activation claims.

## Suggested acceptance gate for this Work task

- 2,100 manifest IDs preserved, all checked sources still linked; 757 extras separately and explicitly accounted for, not silently promoted.
- All 11 mixed groups have clear, reproducible semantic assignments and human-readable exceptions; no "semantic done" simply because a model wrote one text field.
- All numerical draft IDs retained (257 approved-source coverage), duplicates and 25 overlays handled by precedence/version rules.
- Any new authored diagnosis follows actual learner evidence; every ambiguous code can abstain.
- Golden conversations cover the original-versus-marked-up ₱640 case and reverse `640/1.25=512`; wrong inverse `640*.75=480` fails forward check.
- All outputs remain drafts pending applicable real authorization, and no missing transfer is filled by a near-clone.
- Zero altered canonical keys, statuses, signed manifests, protected services, paid runtime inference, AI kill switches or deployments.

**Important:** This is a scoped independently verified content audit. It is neither human adjudication nor new mathematical verification of every source answer.
