# ADR-0003 (DRAFT): Dexter Rescue loop (deterministic, ₱0)

- Status: **Proposed, awaiting Astra.** Not accepted.
- Date: 2026-10-22 (Asia/Manila)
- Issue: #23 (depends on #20 evidence fixes and #22 metadata pilot)

## Decision drivers

No generative AI (the owner-funded lock stays closed). Reuse the existing services. Use only approved items. Fall back honestly when metadata is missing. Never touch an active Strict Mock.

## Loop and states

`idle → diagnosed → explained → prerequisite_offered (optional) → fresh_attempt → resolved | still_stuck → scheduled_review`

1. **diagnosed**: Study-mode wrong answer, post-reveal only. `MisconceptionDiagnoser::diagnose(question, chosen)` returns a code from `distractor_codes` or null.
2. **explained**: show the item's checked `reveal.why_wrong[chosen]` + the taxonomy `fix` line. No generated text.
3. **prerequisite_offered**: only if `NextSkillRecommender` says `repair_foundation` for this archetype (via `SkillGraph`).
4. **fresh_attempt**: Fresh Same Skill picks a *different* approved MCQ of the same archetype (or of the prerequisite), not seen in the last 7 days, and never a clone of the failed item.
5. **resolved / still_stuck**: an independent answer (no Expound, no reveal before answering) becomes mastery evidence.
6. **scheduled_review**: the failed item enters FSRS (existing Review Mistakes). Today's Focus and LearningInsightsService pick it up.

## Payload (server → client, after the learner has answered)

```json
{"rescue": {"state": "explained", "skill": "NUM-WP-PCT-CHANGE", "code": "NUM-WRONG-BASE",
  "label": "Used the wrong base", "fix": "Percent change divides by the original value.",
  "why_wrong": "<approved reveal text>", "next": {"kind": "fresh_same_skill", "question_id": 1234},
  "prerequisite": null, "evidence": {"independent": 3, "status": "insufficient"}}}
```

`question_id` only; the item is fetched through the normal exam payload (no key). 

## Security

- During an active Strict Mock (StrictMockLock held) the endpoint returns 423 and nothing else. No codes, labels or skill ids, because they leak the answer.
- `distractor_codes` stay `#[Hidden]` on the model. The diagnosis is computed server-side after the answer is stored.
- No API keys, no model calls. `OwnerAiSpendLock` is irrelevant because nothing generative runs.

## Honest fallbacks

- No code or code outside the taxonomy: show `why_wrong` only, labelled "Here's why this option is wrong". No diagnosis claim.
- No fresh item available: "No fresh question for this skill yet. We'll bring this one back in review." Schedule FSRS only.
- Skill not in the graph: skip the prerequisite step.

## Smallest prototype

One Study-mode panel for the 344 rescue-ready approved items (see the audit §5), limited at first to the Subpro pilot archetypes NUM-WP-PCT-CHANGE, NUM-WP-RATIO and CLR-SPELL-WRONG. Steps: diagnose → explain → one fresh item → record an independent answer → FSRS. No prerequisite step in v0.

## Acceptance tests

- Strict active: rescue endpoint 423, response body has no `code`/`skill`/`why_wrong`.
- A wrong answer with a taxonomy code gives the right label/fix; a missing code gives the fallback copy, with no label.
- The fresh item has the same archetype, a different id and stem family, and was not seen in the last 7 days.
- A fresh answer given after Expound is not counted as independent.
- The failed item appears in Review Mistakes with an FSRS due date.
- Lite Mode: the panel renders without motion and under the page bundle budget.
