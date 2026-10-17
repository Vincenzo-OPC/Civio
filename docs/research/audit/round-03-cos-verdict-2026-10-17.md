# Round 03: CoS verdicts applied (2026-10-17)

The verdicts are from the Chief of Staff (final approval, delegated by GT). Grok Bot applied them on 2026-10-17.

## Codex GI batch 003 (`chatgpt-batch-003.json`)
- 89 approved/passed: 80 accepted (including 060009 after its fix, and the four former holds 060013, 060038, 060039 and 060080) plus 8 variants.
- 11 rejected. They stay as draft with `review_status: rejected` and are not imported.
- 060009: o4 ("majority") was true under Art. VI, Sec. 28(4). It now reads "two-thirds" and is coded GI-NEIGHBOR-NUMBER.
- Variants: each pair shares a `fact_id` (8 facts, 17 items including the bank twins). The mock-builder rule that serves one item per fact_id is app code, so it is written up for Astra or Codex in `docs/FACT_ID_MOCK_RULE_BRIEF.md` rather than implemented here.

## Baseline B1 Clerical and B2 GI (MSI local DB)
The full change set, with old and new values, is in `fixes/round-03-baseline-b1b2-cos.json`. It is built by `scripts/batches/audit/baseline_b1b2_apply.py`, and every update is guarded by id and the exported stem.
- Key corrections:
  - #277: the key is now "Dela Cruz; Del Mundo; Delos Santos; Del Rosario".
  - #287: the key is index 0.
  - #282: "Under L, after 'Leave Application'".
- Retired (status draft, history kept), 63 in total:
  - B1: the 37 duplicates and #292.
  - B1: #308 and #311. CoS allowed "pick a different target, or retire". They were retired, and their new targets are in the pending swap file.
  - B2: the 14 duplicates.
  - B2: the 9 rewrite-or-retire items: #77, 79, 226, 227, 400, 403, 404, 415 and 549. #77, #226 and #227 are covered by the gap-fill-004 drafts on R.A. 7610, 9745 and 9710.
- Fixed: 52 rows in total. This covers the approved B1 and B2 fixes and the explanation punctuation on every retained row.
  - #548: the stem is fixed too.
  - #373: the stem and explanation say "as provided by law" (R.A. 6770, Sec. 15(1), checked on LawPhil). The distractors are now COA, CSC and CHR.
  - #219: the trap is now "Violations of election law without COMELEC recommendation". The stem is narrowed to what Art. VII, Sec. 19 *names*. The election-law limit sits in Art. IX-C, Sec. 5 and is conditional, so there is still only one defensible key.
- **#304 is on hold and unchanged.** CoS asked for "Indispensible", but that word is already one of the four choices, and so is "Indespensable" (my original proposal, which was my error). CoS needs to name a different foil.

## Still pending CoS (inactive)
- `fixes/round-03-baseline-b1-spelling-swaps.json`: 14 proposed targets, covering the 12 bank-overlap rows plus #308 and #311. None of the targets is used anywhere in the bank. They are checked against a dictionary and for keyboard slips.
- gap-fill-004.

## MSI local DB
- Backup: `%TEMP%\civio-r03\civio_local_pre_r03_20261017.dump` (pg_dump -Fc).
- Imported: chatgpt-batch-003 (89 created) and chatgpt-batch-001 (100 updated; they were already active).
- Active counts by subject:

| Subject | Active | of which baseline |
|---|---|---|
| Analytical | 365 | 114 |
| Clerical | 248 | 41 |
| General Information | 337 | 111 |
| Numerical | 400 | 91 |
| Verbal | 532 | 130 |
| **Total** | **1,882** | **487** |
