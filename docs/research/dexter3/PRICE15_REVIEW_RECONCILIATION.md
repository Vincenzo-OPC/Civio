# Price pilot: separate AI review and draft correction patch

23 October 2026, Asia/Manila. Baseline `d405fed2faa08270f48e266e90f0afe52009cf42`.

The separate AI reviewer assessed the frozen packet and recommended revision. Its [original assessment](reviews/ai-review-01.json) and [readable findings](reviews/AI_REVIEW_01.md) are preserved. The author prepared [price15-v0.3-patch.json](price15-v0.3-patch.json) against the exact v0.2 hash. This is a draft content patch applied only in memory for checks. It changes no canonical question, approval label or runtime file.

## What was reviewed

The reviewer checked 15 price items, all 45 price distractor values, both shared interactions, the ₱640/₱900 contrast and four foundation candidates with 12 distractors. No answer/key calculation error was found. Seven findings concern response coverage, reasoning attributed too readily, assistance provenance, stage wording and code precision.

This is a separate **AI** assessment, not either required human review. The agent started without the author's conversation history, but a README search exposed some prior code-mismatch and transfer notes. It discloses that limited blinding and does not claim human or statistical independence. Stored keys were visible; its calculations were recomputed rather than represented as solutions obtained before seeing every key. No human decision, adjudication or learner outcome has been manufactured.

## Disposition of the seven findings

| Reviewer finding | Author response in draft v0.3 | Remaining boundary |
| --- | --- | --- |
| AI01-F01: target options omit the intermediate raised price | Add a raised-price response and a separate follow-up distinguishing mistaken target from unfinished work | Applies to all 12 successive items; draft wording still requires human review |
| AI01-F02: confirmation cannot express a mistaken click or forgotten/other reasoning | Add mistaken-click self-report and neutral forgotten/other response | Neither permits a specific diagnosis from uncertainty |
| AI01-F03: ₱10 answer is treated too readily as fixed-peso reasoning | State the numerical relation neutrally: ₱10 is 10% of ₱100, while this base is ₱200; the answer alone does not establish the method | A code remains a possible hypothesis only, never confirmed by that answer alone |
| AI01-F04: local consistency labels can obscure earlier help | Add one explicit assistance/provenance contract; relabel taught contrast steps as assisted checks | Node responses never update independent knowledge; target already taught means no fresh diagnostic confirmation |
| AI01-F05: hint collapses a two-change timeline | Name starting price, price after raise, and final price after discount separately | Amount saved remains distinct from amount paid |
| AI01-F06: canonical codes lose unit/operation distinctions | Preserve existing sale-code proposals; add a draft local percent-numeral-as-divisor proposal for `926013:o4` | Canonical code correction remains a separate reviewed bank operation |
| AI01-F07: reverse-raise terms are generic and its fixed-peso code is imprecise | Propose beginner terms identifying original 100% and after-raise 120%; retain existing hand method and propose a distinct n3 unit hypothesis | The `0265` source remains draft and its content is not rewritten by this patch |

“Author response” means a proposed correction, not an adjudicator's validated disposition. The AI assessment applies to v0.2; it does not automatically approve changed v0.3 text. Human-review fields stay pending in both old and new artifacts.

The same separate reviewer subsequently performed a [focused AI follow-up on the exact v0.3 patch](reviews/ai-review-01-followup.json). It reports F01–F05 addressed at the draft level, finds no new blocking regression in its focused scope, and preserves the canonical-code and human-review blockers for F06/F07. This is a re-review of corrections, not a second human review, a new blind replication or runtime approval. The follow-up's patch hash and the frozen assessment hash are checked by the validator.

## Additional path corrections

The author's scoped path inspection found three further issues while the separate review was running:

1. Wrong arithmetic responses were routed to price-stage labels, which do not address a tenth/hundredth or percent-unit error. They now lead to a short percent reminder and an assisted 10%-of-₱300 check. A correct check returns to the original question as assisted practice. Continued wrong/unsure responses offer foundational explanation or stopping, with no invented approved prerequisite or mastery result.
2. Every response to the guided ₱900 calculation led to transfer. Wrong and unsure responses now receive a reverse-relation check and a guided exit. Correct ₱720 leads to an explicit choice to try practice, review or stop. Choosing practice still respects the original missing-transfer fallback. No automatic readiness or success event follows a wrong check.
3. Showing all `given_meanings` immediately after the first response could teach the later base question before asking it. The complete inherited meanings block is now restricted to authorized explanation. Individual prompts/feedback can still teach one step at a time, with assistance recorded and no later post-teaching response misrepresented as independent evidence.

These remain bounded authored MCQ interactions. They do not interpret arbitrary free text or prove a psychological cause. The new mini-check is a teaching scaffold, not a scored bank addition or unfamiliar transfer assessment. No existing transfer candidate was promoted.

## How to inspect the draft patch

The patch uses RFC 6902 `add`/`replace` operations and an exact base SHA-256. Its offline validator supports only the needed authoring operations. It is not a new production patch endpoint or tutoring engine. `materialize()` in [validate_price_patch.py](validate_price_patch.py) returns a temporary in-memory v0.3 view; it does not write or replace v0.2.

All 15 source identities, narrow/full hashes and original binding fields are preserved except the explicit meanings visibility rule. Shared flow text and branching change once per lesson, rather than regenerating the remaining bank or all 60 sidecars. Two foundation proposals are editorial suggestions outside the applied operations; no option, answer key, source or approval state is changed.

Run `python3 docs/research/dexter3/validate_price_patch.py --write-report`. Actual results are in [price15-v0.3-check-results.json](price15-v0.3-check-results.json): source preservation, reachable/acyclic/bounded branches, intermediate-target confirmation, targeted arithmetic remediation, reverse-check routing, assistance context, review-packet traceability and twelve invalid-patch rejections. Prior v0.1/v0.2 snapshots, the original review packet and the four-candidate audit remain byte-identical. No application, browser, learner or production tests are claimed.

## Next decision

Review the actual materialized v0.3 text, not only this reconciliation. Obtain the original process's two independent human reviews and adjudication before treating affected metadata as validated. The complete 180-row pilot gate remains separate from this 45-row subset and from any flow-content decision.

Keep the existing Guide Me handoff in [PRICE15_EDITORIAL_REVIEW.md](PRICE15_EDITORIAL_REVIEW.md); the patch refines that content, not the runtime architecture. Issue #28, #29, Strict answer secrecy, the bank signing boundary and the zero-owner-cost gate remain in force. Do not expand the remaining 45 bindings or activate Guide Me based solely on this AI assessment and author correction.
