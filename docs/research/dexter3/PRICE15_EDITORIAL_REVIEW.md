# Price tutoring editorial QA and Guide Me handoff

23 October 2026, Asia/Manila. Baseline: `4934bc2c4551ee6f9823db99f3f8dcf9926e01de`.

**Recommendation: revise and independently adjudicate these 15 bindings before extending the remaining 45 or implementing Guide Me.** This author second pass found no mathematical key errors in the scoped questions, but the original diagnostic design needs better branching, evidence rules and transfer coverage. Issues [#28](https://github.com/Vincenzo-OPC/Civio/issues/28) and [#29](https://github.com/Vincenzo-OPC/Civio/issues/29) were both open when checked. #28 remains the answer-persistence prerequisite; #29 is the separate external Ask handoff improvement and must not be duplicated by a Guide Me project.

## Scope and artifacts

Evaluated **15 bindings: 12 successive price changes and 3 sale prices**, plus the separate ₱640 forward/reverse teaching contrast. This was not a repeat bank inventory. The original 60-item sidecar, coverage report, builder, validator and editorial CSV remain intact. Stable question IDs, both source digests, source keys/options and approval labels are preserved.

- [price15-v0.2.json](price15-v0.2.json): separate draft overlay, 15 per-item reviews against all ten requested criteria, two branching lesson templates, mental methods, per-item family/sibling/candidate mappings, three proposed code refinements, the revised ₱640 interaction and transfer-search evidence.
- [price15-check-results.json](price15-check-results.json): actual deterministic results and artifact hash.
- [build_price15.py](build_price15.py): offline scoped authoring script. It does not regenerate the 60 bindings and refuses to silently overwrite changed overlay content.
- [validate_price15.py](validate_price15.py): reference, arithmetic, authored-flow and rejection checks. It implements no runtime tutor.

## Findings

| Finding | Affected bindings | Evidence and correction |
| --- | ---: | --- |
| F01: generic correct-response feedback | 15 | “Yes. Use that meaning…” does not connect to the chosen interpretation. Replace with brief stage-specific feedback. |
| F02: wrong and unsure feedback identical | 15 | Both receive the same correction. Uncertainty now gets a wording reminder and no hypothesis; an alternative interpretation gets a reason question. |
| F03: no confirmation before teaching | 15 | A possible error is named after one selection. Add a pre-correction self-report; compatible evidence supports only an attempt-level hypothesis. No response proves a persistent misconception. |
| F04: stage meanings can spoil the diagnostic | 15 | `given_meanings` explains the answer to the initial diagnostic if rendered first. Show it only after the learner responds. Hints require an explicit request; full solution requires existing Reveal authorization. |
| F05: interpretation and arithmetic not separately sampled | 15 | Correct stage selection does not establish arithmetic competence. Add an optional 10%-of-₱200 check; skip it only when equivalent actual evidence exists. One success does not establish broad proficiency. |
| F06: intended diagnostic answer always first | 15 | In v0.1 the first option is always the intended response. Specify server-held display order and stable response IDs; no positional cues or client correctness fields. |
| F07: percent-unit confusion coded as wrong base | 3 | `000030:o2`, `000036:o3`, `000224:o1` subtract 15 or 25 pesos. Proposed local hypothesis: `percent-as-pesos`, confirmed by the learner's described operation. Canonical `NUM-WRONG-BASE` remains unchanged. |
| F08: a correct number hides the requested quantity | 3 | In `000038`, `000113`, `000515`, the discount is 50%, so amount saved equals amount paid. Ask which quantity the learner calculated, even after a correct numeric response. |
| F09: equal-rate cancellation needs an explicit base check | 3 | `000001`, `000113`, `000227` have equal increase/decrease percentages. Their original explanations are mathematically correct; this is a diagnostic risk, not a key defect. Ask whether the learner combined rates or used the first base twice. |

There are **zero mathematical errors found**, **three code-to-error mismatches**, six shared diagnostic design weaknesses, and two recurring item-design risks. Do not count these as nine independent faults per item. The 12 successive-change recipes also unnecessarily list decimal multiplication as a prerequisite; fraction benchmarks can solve them without decimal fluency. The overlay makes decimal multipliers optional.

All 45 wrong-option values were recomputed against the operations described by their rationale. The computations agree; the codes remain hypotheses about a possible route, never proof that a learner used that route. A correct original answer does not automatically prove correct reasoning, especially in the three 50% cases.

## Per-item families and transfer decision

Every ID below has prefix `CIVIO-NUM-WP-PCT-CHANGE-`. Full IDs and hashes are stored in the overlay. The twelve successive items all share the same conceptual family: **known starting price → increase → decrease of the new price → final price**. The three sale items share **known pre-sale price → one discount → amount paid**. Context nouns, new numbers and different rates are parameter substitutions, not distinct instructional families.

| ID suffix | Family | Checked final price | Particular risk | Proposed limited candidate |
| --- | --- | ---: | --- | --- |
| 000001 | Successive | ₱240 | Equal rates | 000013, cross-context percent base only |
| 000024 | Successive | ₱792 | Generic branching | 000013, same limit |
| 000030 | Sale | ₱408 | Percent-as-pesos mislabeled | 000124, changed-base extension |
| 000036 | Sale | ₱340 | Percent-as-pesos mislabeled | 000124, changed-base extension |
| 000038 | Successive | ₱520 | Saving equals payment | 000013, cross-context percent base only |
| 000045 | Successive | ₱180 | Generic branching | 000013, same limit |
| 000113 | Successive | ₱180 | Equal rates; saving equals payment | 000013, same limit |
| 000224 | Sale | ₱720 | Percent-as-pesos mislabeled | 000124, changed-base extension |
| 000227 | Successive | ₱1,008 | Equal rates | 000013, cross-context percent base only |
| 000324 | Successive | ₱270 | Generic branching | 000013, same limit |
| 000328 | Successive | ₱540 | Generic branching | 000013, same limit |
| 000415 | Successive | ₱675 | Generic branching | 000013, same limit |
| 000428 | Successive | ₱264 | Generic branching | 000013, same limit |
| 000429 | Successive | ₱468 | Generic branching | 000013, same limit |
| 000515 | Successive | ₱132 | Saving equals payment | 000013, cross-context percent base only |

The transfer search inspected stems of the manifest's 400 numerical candidates for percent signs/words, markup, discount, profit, loss and interest. It retained 48 hits: 37 marked approved, 7 reviewed and 4 draft. This is targeted retrieval, not semantic recertification of 400 answers. The 37 approved hits contain 14 successive price items, 10 sale items and 13 simple-interest items. The record-level search results are preserved; non-manifest or misclassified non-numerical questions were not exhausted.

**Two distinct-family, limited-transfer candidates have approved source labels and checked keys:**

- `CIVIO-NUM-WP-PCT-CHANGE-000013`: ₱20,000 at 6% annual simple interest for 2 years 6 months, interest **₱3,000**. This tests applying a percent to a principal in a different context. It requires simple-interest and time-unit understanding and cannot validate reverse percent or successive changes. It is also one of the original 60 pilot items, so it cannot later be treated as unseen if taught in the interest batch. Eligible only if actual exposure and family history permit.
- `CIVIO-NUM-WP-PCT-CHANGE-000124`: ₱250 raised 20%, then reduced 25%, final **₱225**. This extends a single-sale task to a changed intermediate base after an increase. It is distinct from the three sale-family tasks but is the same family as the twelve successive tasks. Use it as transfer only from the sale lesson with relevant prerequisites, never as unfamiliar transfer from a successive lesson.

`CIVIO-NUM-WP-PCT-CHANGE-000121`, a ₱2,400 backpack at 25% off, answer **₱1,800**, is a checked **same-family practice candidate**, not a distinct-family transfer. Re-answering an exposed ID is retrieval/retention practice. A different unexposed ID in the same frame is near practice. A different family tests only the subskill shared with the teaching task; it does not establish every target competency. “Unfamiliar” is learner-specific and cannot be verified from the bank alone.

**Zero approved full-target distinct-family transfer mappings were established for reverse percentage or for the twelve successive-change bindings.** The search found no approved standalone reverse-markup, successive-discount, or percentage-profit/loss application. Relevant non-approved records include:

- `CIVIO-B3-NUM-PCT-BASIC-0265`, draft: recover the original allowance after a raise. Do not promote or use as approved transfer.
- `CIVIO-NUM-PCT-BASIC-926015`, reviewed: recover a whole from a known percentage part. Useful inverse prerequisite, pending approval.
- `CIVIO-NUM-WP-RATE-926047`, reviewed: profit from unit cost versus selling price. This is ordinary profit arithmetic, not yet a percentage-profit question.
- Basic percent direct amount, rate and whole items remain non-approved under `NUM-PCT-BASIC`; approved age/rate/ratio items are not substitutes merely because they involve multiplication.

Prioritize review of existing inverse/basic-percent drafts, then separately authorize original gaps for two discounts, recover original after markup, and cost-based profit versus selling-price margin. Do not manufacture bank questions in this task.

## Revised ₱640 interaction

The overlay's contrast is an authored learning example, separate from scored bank items. It preserves the actual evidence that the owner could calculate 25% of ₱640 as ₱160. It does not invent a learner event for another student.

1. Ask what ₱640 represents. Wait.
2. If the learner selects already marked up, ask which interpretation led there before giving the correction. Distinguish an assumed final price, overlooking “original,” and uncertainty. No blanket arithmetic diagnosis.
3. Use the already-correct ₱160 to ask whether to add it or recover an earlier price. Establish original ₱640 → marked-up ₱800.
4. Ask which value supplies the 20% discount. Establish intermediate ₱800 → discount ₱160 → final ₱640.
5. Change the wording explicitly: ₱640 **after** a 25% markup. Ask what percentage of the original that represents, then which operation undoes multiplication by 1.25. Original = ₱512.
6. Address subtracting 25% of the final amount only on that response or an explicit request. It yields ₱480; a forward check reaches ₱600, so the inverse operation is wrong. Dividing by 1.25 is correct. For this particular rate, the inverse reduction is 20% of the final, not 25%.
7. Check with different numbers: bag price ₱900 after a 25% markup. Ask which quantity is unknown, then ask for the original. Correct result ₱720; subtracting 25% gives ₱675, which returns only ₱843.75 after markup. These are assisted checks of the same reverse family, not unfamiliar transfer.
8. Request a separate approved, exposure-eligible question without hints. The full reverse target currently has no approved mapping. Offer an eligible limited cross-context percentage-base candidate with its scope labeled, or report the gap and end. Never invent a successful independent outcome.

The data branches on the response and waits between questions. It is a deterministic authored interaction, with no claim to understand arbitrary free text. The wording and path length still require a private learner trial after review; do not force every optional arithmetic check when the required evidence is already recorded.

## Minimal schema additions

Keep the v0.1 canonical references and inherited solution. Use this separate, versioned overlay to add:

| Addition | Purpose |
| --- | --- |
| Stable node/response IDs with explicit next node | Deliver one response-sensitive step at a time |
| `kind`: comprehension, self-report, arithmetic sample, assisted check, hint/action/terminal | Avoid treating uncertainty or a self-report as a graded knowledge answer |
| `evidence` and nullable local `hypothesis` | Separate unknown, possible and compatible attempt-level evidence; no probability or permanent diagnosis |
| Source/base-binding hashes and visibility rules | Detect drift and withhold meanings/solutions until their permitted stage |
| Hint level and request precondition | Prevent automatic dumping of the full method |
| Required concepts versus optional solving methods | Permit fraction/mental approaches without forcing decimal fluency |
| Candidate role, family relation and nullable full-target mapping | Keep practice, narrow transfer, full-target transfer and missing coverage distinct |

Do not add a parallel mastery model, free-text classifier or runtime expression evaluator. The executable validator checks this authored data contract, not a new production JSON-schema integration. Local hypotheses are editorial proposals and must not silently become canonical taxonomy codes.

## Minimal backend specification for later Codex execution

**Reuse boundaries:** `app/Services/Dexter/RescueService.php`, `MisconceptionDiagnoser`, `SkillGraph`, `app/Services/Exam/Reveal/RevealTutor.php`, `app/Services/Learning/ExposureHistory.php`, existing answer/attempt and review records, `SkillEvidenceBuilder`, `FsrsRatingPolicy` and existing FSRS scheduling. Current `RescueController` accepts arbitrary `question_id` and `chosen_option`; it does not establish the needed graded-attempt provenance. Its service eagerly returns an explanation and same-archetype fresh question. Do not reuse that whole payload for the first diagnostic.

**State/transition contract:** `INTERPRET` → optional `CONFIRM` → `GUIDE` (one base/direction/quantity/arithmetic node or requested hint) → `RETRY` → server-authorized `EXPLAIN` → `TRANSFER_OR_GAP` → `DONE`. Stop and authorized Reveal remain explicit exits. Bound the turn count and fall back honestly when exhausted. The ₱640 teaching contrast is served only in an authorized explanation context; it contains worked values and is not a pre-Reveal export payload.

**Authorization order on every start and step:** existing feature gate; authenticated/guest owner resolution; active Strict lock; owned served-and-server-graded Study answer; stable bank identity plus current source/sidecar review eligibility; expected interaction revision/node; allowed response/action. A disabled gate returns current safe disabled behavior. Preserve existing 423 Strict lock. Do not let client-supplied correctness, source ID, next node, hypothesis or review state grant access. Strict remaining sealed includes direct routes, cross-session requests, resume and export. Guest progress may use existing ownership only if supported and tested; otherwise return the current ordinary Study explanation rather than inventing signed-in history.

**Identity caveat:** canonical sidecars use stable string `CIVIO-*` IDs, while the existing Rescue controller and `validated_question_ids` check use integer DB IDs. Resolve through the existing reviewed import identity/ledger and compare content; do not `intval()` a sidecar ID or assume DB IDs are portable. Missing mapping is a safe fallback. Do not change the signed bank import boundary.

**Proposed request:** owned `attempt_id`/served-response identity, interaction token, revision and node/response IDs, idempotency token, or explicit hint/reveal/stop action. These are a proposal, not a new implemented endpoint. A duplicate token returns the same authorized step without duplicate help/review events; an obsolete revision must not overwrite a newer response. Recheck gate and Strict state on every replay. Fix #28 first: no new interactive teaching path accepts an unsaved answer or extends the server deadline.

**Client response allowlist:** current state/token/revision, one prompt, opaque response IDs with text in server-held display order, permitted actions, safe response-specific feedback for the just-processed node, and optionally an honest missing-transfer message. Exclude hidden keys, branch destinations, correctness flags, hypothesis rules, canonical wrong-option codes, all other nodes and future solutions. Release the worked solution only through existing Reveal authorization. No full sidecar in initial JS, offline mock packs or cacheable session payloads. Keep Lite Mode text-first and reuse existing MCQ controls.

**Evidence and review:** record assistance before serving the first diagnostic content; bind it to that item/attempt. Preserve the independent first answer already given, but subsequent corrections stay assisted. Neither a diagnostic selection, self-report nor the guided ₱900 check feeds independent knowledge/BKT. An actual separate unassisted item may contribute its original correctness evidence while retaining a distinct family/exposure category; no family-generalization or mastery claim is inferred. Use the existing completed-answer Review Mistakes/FSRS path once, not once per tutor turn. Assistance must not manufacture a successful FSRS rating or a completed reminder. Retain omission, repeated, assisted and independent outcomes separately.

**Fallbacks:** draft/unreviewed or stale overlay → ordinary authorized explanation without diagnosis; missing identity or served response → refuse the tutoring lookup; unknown cause → wording/concept help without a label; no approved distinct-family unexposed candidate → explain the gap, optionally offer clearly labeled practice; no transfer completion event if none happened. The arbitrary question/code mismatch also blocks diagnosis. Keep Rescue disabled and the validated-ID list unchanged until the separate review/activation process.

**Required later application tests:** owner/cross-account and guest isolation; unserved/ungraded request; Strict locks before lookup and after resume; shuffled stored/display options; stale key/code/full-record hash; duplicate and stale node requests; missing/draft metadata; no hidden fields before Reveal; alternative and unsure paths differ; two consistent pre-correction responses versus post-teaching repetition; known arithmetic with wrong interpretation; correct interpretation with an arithmetic slip; 50%-discount correct-number/wrong-quantity case; no eligible transfer; taught interest-pilot item excluded; hints never inflate independent evidence; first-answer history beyond 50 attempts; FSRS scheduled once; storage/chunk failure per #28; external Ask safety per #29; Lite/keyboard/mobile and unchanged byte budgets. These are acceptance criteria, not tests claimed run here.

## Verification and independent-review packet

`python3 docs/research/dexter3/validate_price15.py --write-report` passed: 15 source-bound items, 45 distractor-value checks, two authored-flow contracts, three approved-source candidate keys, forward/reverse contrast calculations and eight malformed-fixture rejections. It also checks prior deliverables are byte-identical. No full bank recount, old 60-sidecar regeneration, runtime/browser tests, model calls or live learner access occurred.

| Evidence level | Current status |
| --- | --- |
| Mathematically verified | 15 scoped items plus contrast and three limited/practice candidates |
| Structurally validated | New overlay references, branches, hint gates and source digests passed offline checks |
| Editorially plausible | Author second pass documented against ten criteria per binding |
| Independently reviewed | Pending; no independent human reviewer decision supplied |
| Approved for runtime | No; all 15 overlays and both templates remain draft |

For independent adjudication, give reviewers the source question, original rationale/code and v0.2 node text, without presenting this author's conclusion as a required answer. Existing packet has 45 applicable distractor rows for these 15 items. Reviewers independently assess code match, rationale accuracy and meaningful family difference, plus the new interpretation/confirmation/uncertainty branches. Record disagreements and an adjudicator separately under the existing two-reviewer process. This session does not fill those columns. Prototype interaction approval also needs a source-current sidecar decision; source bank approval alone is insufficient.

Next: obtain independent adjudication of this small packet, resolve the three code distinctions through the approved editorial workflow, and review the existing inverse/basic-percent candidates. After #28 is resolved, #29 can proceed as its already-scoped external handoff change. Begin a narrow Guide Me implementation only after the interaction/content gates are accepted. Delay mass expansion of the remaining 45 until this design survives that review.
