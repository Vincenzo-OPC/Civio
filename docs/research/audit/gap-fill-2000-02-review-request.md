# gap-fill-2000-02 — Numerical + Filipino reading/order (108 drafts) — review request for Chief of Staff

Grok Bot, 2026-10-18. File `docs/research/gap-fill-2000-02.json`, generator `scripts/batches/gapfill/gap_fill_2000_02.py`. All items are draft/unreviewed. Nothing is imported.

**Why.** The release manifest (`scripts/batches/release/release_manifest.py`) showed these shortfalls: Numerical basic operations 55, number sequence 16, FIL reading 10, FIL paragraph order 14. This batch fills them with small buffers.

| Subtopic | Archetype | Drafts | Need | Buffer |
|---|---|---|---|---|
| Basic operations (MDAS, parentheses, whole numbers) | NUM-OPS-ORDER | 60 | 55 | +5 |
| Number sequence | NUM-SEQ-DIFF 11, NUM-SEQ-MULT 9 | 20 | 16 | +4 |
| Filipino reading | VFIL-PAGBASA | 12 | 10 | +2 |
| Filipino paragraph order | VFIL-PAGSUSUNOD | 16 | 14 | +2 |

**Standards applied.**
- **Basic operations.** Eight expression shapes, 7–8 items each. Each item has three coded distractors, and each distractor is the actual result of a named mistake:
  - NUM-ORDER-OPS: working left to right or dropping the parentheses
  - NUM-OP-SWAP: using the wrong operation
  - NUM-PARTIAL: stopping one step early
  - why_correct starts with "Answer: K." and then shows every step.
- **Sequences.** NUM-SEQ-DIFF items have growing jumps. Their distractors repeat the last jump, skip a step, or reuse the first jump. NUM-SEQ-MULT items follow "× m then ± c". Their distractors forget the constant, use a fixed jump, or add the constant twice.
- **Reading.** 12 original passages on public-service and community topics. Each wrong option is coded RC-OPPOSITE, RC-NOT-IN-TEXT, or RC-EXTREME / RC-TOO-NARROW, and why_correct points to the supporting sentence.
- **Paragraph order.** 16 four-sentence procedures, with the sentences shown shuffled (never already in order). The three distractors are a misplaced opener, a swap of the middle pair, and the outcome placed before the last step. Each has its own code.
- Spelling follows KWF. There is no long-key giveaway, and answer positions are 27/27/27/27.

**QA.**
- `qa_file.py` found 0 problems. The solvers recomputed all 80 numerical keys, and no stem near-duplicates an existing bank item.
- `explanation_lint.py` flagged 0 items.
- `qa_fil.py` is GREEN.

**Reviewer focus.**
- A few NUM-ORDER-OPS distractors are negative (e.g. −12). They are kept because that is what dropping the parentheses really produces.
- Reading items 2, 5 and 6 use RC-NOT-IN-TEXT for two of their wrong options.
- In the paragraph-order items, the "outcome before last step" distractor sometimes describes a plausible-sounding order. Check that each key is the only defensible order.

Accept, revise or reject each ID.
