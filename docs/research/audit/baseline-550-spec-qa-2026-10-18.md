# Baseline 550: full-schema conversion and QA (Grok Bot, 2026-10-18)

- **Conversion:** `python3 scripts/batches/audit/baseline_convert.py` reads `audit/data/baseline-550-2026-10-17.json`, applies the CoS change sets already live on the MSI (`fixes/round-03-baseline-b1b2-cos.json`: 53 updates, 63 retires; `fixes/round-03-baseline-b1-spelling-swaps.json`: 14 swaps that reactivate their rows), and writes `audit/data/baseline-550-spec-2026-10-18.json`.
  - 550 items: **501 active, 49 retired**, matching the MSI baseline count recorded on 17 Oct.
  - Every item has `status: draft` because that's the only non-approved state the schema allows. The real state is in `baseline_state`. **No DB status changed.**
  - Fields the baseline never had (distractor codes, per-option why_wrong, terms, shortcut) are left **empty on purpose**, so QA measures the gap instead of hiding it.
- **qa_file.py:** `python3 scripts/batches/qa_file.py docs/research/audit/data/baseline-550-spec-2026-10-18.json` → exit 1, 2,217 problems:
  - 550 × 3 schema gaps: `reveal.terms` empty, `reveal.shortcut` empty, missing distractor codes / why_wrong. These are expected; every baseline row needs them before it can be approved.
  - 534 "baseline exact/near match": items matching their own seed SQL. These are self-matches and carry no signal.
  - **29 near-duplicates and 2 duplicate stems inside the baseline**: sequences, PRUDENT ×3, SCARCE ×2, compound/complex-sentence frames, analogies 317/467 and 469, and spelling "item 8" frames. Verbal and Analytical ones go into future batches.
  - **#462 (active, Filipino error recognition): options are not distinct.** It reads `pinagkakakitaan` ×2 and `pinagkakitaan` ×2. This is user-visible, needs CoS, and is a proposed retire/fix.
- **explanation_lint.py:** 370 of 550 flagged.
  - By check: BOILERPLATE 163, LONG-KEY 141, KEY-NOT-STATED 95, PLACEHOLDER 76, GI-NO-SECTION 27.
  - Key positions: A 325, B 163, C 53, D 9. This matters in online drills, which don't shuffle choices.
  - Per-domain counts and IDs are in `audit/data/baseline-550-explanation-lint-2026-10-18.csv`.
  - Biggest remaining: Verbal EN (active) has LONG-KEY 40, KEY-NOT-STATED 36 and BOILERPLATE 53. Analytical (active) has PLACEHOLDER 27, KEY-NOT-STATED 24 and LONG-KEY 23.
- **Use:** later baseline batches (B4 word problems, Analytical, Verbal) should start from this file, filling codes and why_wrong item by item. It is not for import.
