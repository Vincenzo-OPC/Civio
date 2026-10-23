# Price pilot: independent-review packet and foundation candidates

23 October 2026, Asia/Manila. Repository baseline `9584106042bdd8d57eaa054f98fb4a1b73470cb0`.

The next actionable checkpoint is ready: [price15-review-packet-v0.1.json](price15-review-packet-v0.1.json) packages the 15 price items, their 45 original wrong-option rows, the proposed v0.2 interactions, the ₱640 contrast and four existing foundation candidates. Reviewer judgments and adjudication remain blank. No independent human decisions were available to record in this session.

This is a review packet, not an import batch or runtime content. It avoids presenting the author's F01–F09 verdicts as reviewer answers. It includes stored keys and explanations so reviewers can compare after solving; it is not an answer-blinded study. Each reviewer must work without inspecting the other reviewer's completed form.

## Four candidates checked, no approval changes

Only these four records were assessed. There was no bank recount, new question generation or regeneration of prior sidecars.

| Existing question ID | Observed status | Role | Verified answer | Independent limitation |
| --- | --- | --- | --- | --- |
| `CIVIO-NUM-PCT-BASIC-926013` | reviewed | Known whole and rate → part | 54 notebooks | Direct percentage amount in a non-price context; does not test inversion |
| `CIVIO-NUM-PCT-BASIC-926014` | reviewed | Known part and whole → rate | 30% | Distinct rate-finding relation; does not test a markup or reverse price |
| `CIVIO-NUM-PCT-BASIC-926015` | reviewed | Known part and rate → whole | 288 files | Inverse prerequisite; given part is 25%, unlike a marked-up price of 125% |
| `CIVIO-B3-NUM-PCT-BASIC-0265` | draft | Final allowance after raise → original | ₱150 | Closest reverse-raise practice, but same inverse-multiplier family as the taught reverse-markup contrast |

All four keys and all twelve distractor values passed exact-fraction calculations. Each solution was checked by two methods and a forward relationship check. The detailed author review is [foundation4-audit-v0.1.json](foundation4-audit-v0.1.json). This establishes mathematical consistency of these records, not educational approval, activation or learner mastery.

Two code distinctions deserve particular attention:

- `926013:o4` gives 360 ÷ 15 = 24. The learner would be using the correct whole with the wrong percent operation; `NUM-WRONG-BASE` is an imprecise description. Proposed local hypothesis: percent-operator interpretation.
- `0265:n3` gives 180 − 20 = 160. This treats 20% as a fixed ₱20; `NUM-OP-SWAP` loses that unit distinction. Proposed local hypothesis: percent-as-pesos.

Four further editorial observations concern multi-error or broad-code interpretations: `926014:o1` requires reversing the ratio and mishandling percentage units; `926014:o4` answers for the complementary group; `926015:o1` treats the given part as a whole; `926015:o4` treats the given part as the remaining 75%. These are candidate explanations to confirm with a learner, not proven diagnoses. None is a new key error.

The reverse-raise candidate already has useful eight-part `method_steps`, including **120% = ₱180 → 10% = ₱15 → 100% = ₱150** and a forward check. Reuse that explanation after proper review instead of rewriting it to make it look new. Its generic concept/micro-skill labels and the fixed-peso distractor classification need editorial attention. Difficulty and estimated seconds remain author labels, not measured calibration.

The three `reviewed` candidates already carry a prior recorded review identity in their source. This session preserves that provenance and does not claim to have performed that historical review. Their current status remains `reviewed`; `review_status: passed` is not an active-import authorization. The draft remains draft.

## How the independent review proceeds

1. Pin this commit and verify the packet hash in [price15-review-preparation-results.json](price15-review-preparation-results.json). Each reviewer creates a separate copy of `review_form_template`, inserts the actual SHA-256 of the packet bytes, and supplies their actual identity, reviewer kind, date and independence declaration. No one signs as human when the reviewer is a model.
2. Independently solve each source question, then compare with its stored key/rationales. Mark each of ten interaction criteria `yes`, `no` or `unclear`, with exact node/response IDs for a concern. Assess all three distractor rows and meaningful family difference. Leave no unresolved ambiguity disguised as `yes`.
3. Review the ₱640 contrast separately: meaning before calculation, direction of operation, wrong-inverse demonstration, new numerical example, and honest assisted/independent evidence. The guided ₱900 example cannot count as an unseen independent test.
4. Review the four candidate sources separately from the 15 tutoring bindings. Record the role each could play after approval. A correct foundation key does not make it approved transfer.
5. Preserve the two completed review records separately. An adjudicator who did not author the content reconciles disagreements, records reasons and identifies precisely which content bytes are accepted, rejected or need editing. Any accepted revision gets a new content hash/version and applicable re-review.

The original [60-item process](../dexter2/pilot/README.md) remains controlling. These 45 wrong-option rows are only a subset of the original 180; completing this subset does not pass the full pilot gate. Each item needs all three distractors adjudicated before it can satisfy the original item gate. That bank-metadata decision also does not, by itself, approve a new tutoring flow. Unsupported interpretation, solution leakage, false independence claims or unresolved ambiguity block the affected flow even when its arithmetic is right.

This session prepared blank forms only. It did not send review requests or attribute decisions to anyone.

## Minimal content path after adjudication

Prefer the four existing candidates over new near-clones. If independently accepted, route their bank activation through [the existing approval boundary](../../BANK_IMPORT_APPROVAL.md), including GT's exact-content authorization where required. The authoring packet is not a signing artifact. Do not promote a candidate, sign for GT or modify a protected database from this research work.

Then use the approved prerequisite relations separately:

- Wrong percentage amount → the direct-part check.
- Correct direct amount but wrong target interpretation → the stage/unknown diagnostic, not automatic basic-arithmetic remediation.
- Given part mistaken for whole → inverse whole check.
- Marked-up final mistaken for original → reverse-raise practice after explicit meaning check.
- A successful reverse-raise near-practice item still needs a distinct family and a genuinely unexposed question before claiming generalization.

Approved full-target transfer remains missing for a reverse percentage in an unfamiliar family, two successive discounts and percentage profit/loss. The four records do not erase those gaps. No transfer field in the existing v0.2 overlay was promoted or filled as approved by this audit.

Keep the existing Guide Me specification in [PRICE15_EDITORIAL_REVIEW.md](PRICE15_EDITORIAL_REVIEW.md). No additional engine or backend specification is needed. Issue #28 must be resolved before new interactive tutoring; #29 remains the separate external Ask improvement. Source/sidecar review and owner activation remain separate from engineering readiness.

## Checks and resumption

Run `python3 docs/research/dexter3/prepare_price_review.py`. It creates the packet and scoped candidate audit, checks 15 price references/45 original rows, four candidate keys/twelve distractor values and byte-for-byte preservation of prior artifacts. It refuses to overwrite changed output. Results are reproducible in [price15-review-preparation-results.json](price15-review-preparation-results.json).

The existing v0.1 and v0.2 sidecars, their builders/validators, canonical question files and reviewer CSV were not edited. Runtime, learner records and approval statuses remain untouched. No application tests or production verification are claimed for this content-only checkpoint.

Next: independent adjudication of this packet and the existing foundation candidates. While that is pending, use the documented gaps to plan only the smallest original content batch needed. Do not mass-process the remaining 45 bindings or activate Guide Me on the strength of author checks alone.
