# Review of ChatGPT supplements 001 (150 drafts) — audit round 01

Reviewer: CSE (Grok Bot), 2026-10-13. Read-only: no source JSON was edited and nothing was activated.
Files: `filipino-supplement-001.json` (80), `subprofessional-general-info-supplement-001.json` (30), `subprofessional-clerical-supplement-001.json` (40).
Method: `scripts/batches/qa.py` `check_item`, `check_round` (vs batches 001-011) and `baseline_hits` (vs baseline seed stems); independent re-sort of all 20 filing items; every GI claim grepped against the lawphil text fetched today (R.A. 9003, 8749, 9275, 9147, 9729, 11313, 1987 Constitution); manual read of every Filipino item.

## Totals

| | Items | Key correct, one right answer | Content FAIL (must change) | Release-ready as is |
|---|---|---|---|---|
| Filipino Verbal | 80 | 80 | 10 | 0 |
| GI | 30 | 30 | 0 (10 need distractor fixes) | 0 |
| Clerical | 40 | 40 | 0 | 0 |
| **Total** | **150** | **150** | **10** | **0** |

All 150 keys are right and every GI claim matches the official text. None are release-ready, because every item fails the spec metadata rules (below). Treat the 140 non-failing items as "PASS content, FIX metadata".

## Systemic issues (all 150 items)

1. `reveal.terms` is empty on all 150 items (spec §5).
2. Distractor codes are not in the spec: `VFIL-PLAUSIBLE-DISTRACTOR` (240 uses), `GI-WRONG-LAW-OR-CLAIM` (90), `CLR-WRONG-POSITION` (60), `SPL-ERROR` (60). Recode to `FIL-*`, `GI-*`, `CLR-FILE-ORDER` + `distractor_subreason`, and `SPL-DOUBLE/DROP/IE-EI/SOUND`.
3. `why_wrong` is one generic sentence repeated for every wrong choice ("Hindi ito ang pinakamalapit na kahulugan…", "This option does not match…"). The spec needs a specific reason for each choice.
4. Filing items (20) do not carry the required ARMA wording or rule number in `source` (spec §10.2), and every wrong choice has the same code (§10.3 rule 3/4).

## Failing items (content must change)

| ID | Reason | Suggested fix |
|---|---|---|
| CIVIO-VFIL-20261013-0026 | "naipagtagumpay" is not natural standard Filipino. | Use "naisakatuparan" or "natapos". |
| CIVIO-VFIL-20261013-0038 | The key produces "Sa kabila sa maikling abiso", which is ungrammatical (needs "ng"). | Change the stem to "_____ ng maikling abiso, …". |
| CIVIO-VFIL-20261013-0046 | Choice d ("…may mga tungkuling dapat gampanan nilang lahat") is also acceptable, so there are two right answers. The Reveal also says "unang pagpipilian", which names a position. | Give d a clear error, and reword the Reveal without naming a position. |
| CIVIO-VFIL-20261013-0050 | The Reveal says "unang pangungusap", but the key is c, so the Reveal doesn't match the key (spec §8.2 bug). | "Malinaw ang simuno… sa pangungusap na 'Ipinadala ng opisina…'". |
| CIVIO-VFIL-20261013-0075 to -0080 (6) | Every key is 1-2-3-4, and the sentences are already listed in the right order, which gives the answer away. | Shuffle the sentence labels (P/Q/R/S), vary the keys, and give each wrong order its own PO/LOG code. |

## Items needing a fix (key OK)

- **VFIL-0019:** distractor "matibay-tibay" is the stem word itself, so it is implausible. Replace it, for example with "mabigat".
- **VFIL completion set:** "upang" is the key in 6 of 20 completion items (0029, 0030, 0034, 0036, 0042, 0051 grammar). Vary the connectors.
- **GI implausible distractors**, which make the item a giveaway: 0005 (embassies, courts, ad agencies), 0010, 0013, 0014, 0017, 0019, 0023, 0024 and 0028 ("Only …" options). Replace them with sibling laws or terms (`GI-SIBLING-TERM`, `GI-WRONG-BODY`).
- **GI-0029:** only the key says "of the 1987 Constitution", which cues the answer. Make all four options parallel.
- **CLR spelling 0021 to 0040:** the stem "the word meaning the office term '…' in a government memo" is awkward. Use "Which word is spelled correctly?" plus a context sentence.

## Verified OK

- **GI law text (lawphil, fetched 2026-10-13):**
  - R.A. 9003, Sec. 10: LGUs are "primarily responsible".
  - R.A. 8749: "polluters must pay" and "participation of an informed and active public".
  - R.A. 9275, Sec. 4: "primarily apply to … pollution from land based sources", plus fresh, brackish and marine waters.
  - R.A. 9147: definitions of "endemic species" and "habitat".
  - R.A. 9729: "Anthropogenic causes … resulting from human activities", and Sec. 4 creates the Climate Change Commission.
  - R.A. 11313: terminals and online harassment.
  - 1987 Constitution: Art. II, Sec. 16 and Art. III, Sec. 1.
- **Filing:** all 20 re-sorted independently. CLR-0008 "Bañez" files as "Banez" (ñ = n), and the key Bayani (last) holds.
- **Spelling:** all 20 keys are the standard spelling, and every distractor is misspelled.
- **Duplicates:** nothing duplicates batches 001-011. The baseline "matches" for VFIL-0047 and VFIL-0048 are only the generic stem "Alin ang wastong pangungusap?", and their options differ, so they are not duplicates.

## Coverage notes

- **Filipino has no sawikain (idiom) items.** Spec §3.3 targets 15%.
- **Human rights is thin in GI:** 2 items, and no Commission on Human Rights items.
- Partly addressed by the round 01 gap fill (`gap-fill-001.json`).
