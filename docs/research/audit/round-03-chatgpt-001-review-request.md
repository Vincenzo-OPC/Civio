# Round 03 review request: ChatGPT batch 001 (100 Filipino Verbal drafts)

File: `docs/research/chatgpt-batch-001.json`. Auditor: Grok Bot, 2026-10-13. All 100 stay draft/unreviewed. Independent reviewer: Chief of Staff.

## Method
- `qa.py check_item` on all 100 items: no structural or metadata flags, before or after the fixes. VFIL items have no solver, so every key was read by hand.
- Duplicate check: `check_round` at a 0.65 near-match threshold, against 1,207 bank stems (batches 001-011, the supplements and gap fills 001-003), plus `baseline_hits`. Result: 0 exact and 0 near matches.
- Order items: no key matches the listed order A-B-C-D, and every listed order was checked for defensibility.
- Each answer key, sawikain meaning and ng/nang choice was checked, along with din/rin, daw/raw, may/mayroon and na/-ng. The checks used the UP Diksiyonaryong Filipino senses and the KWF *Ortograpiyang Pambansa* d/r rule.

## Result
- **Keys:** 98 correct as written. 040005 had two defensible answers and is fixed. 040069 and 040070 asked for commentary about KWF instead of testing usage, and are rewritten.
- **Sawikain:** all 15 meanings are standard and correct (nabunutan ng tinik, butas ang bulsa, taingang-kawali, kumukulo ang dugo, nagbubuhat ng sariling bangko, balitang kutsero, isang kahig isang tuka, matalas ang dila, bagsak ang balikat, kabiyak ng dibdib, magdilang-anghel, makapal ang mukha, pasan ang daigdig, gintong puso, nasa alapaap ang isip).
- **ng/nang (040061 to 040065):** all 5 keys are correct (nang for manner, ng for object or possession).

## Fixes applied (logged in each item's notes)
- **CIVIO-VFIL-…-040005:** o2 "pag-aalala" is a dictionary sense of agam-agam (pangamba), so the item had two defensible keys. Replaced with "pagtataka" (FIL-SAME-FIELD).
- **CIVIO-VFIL-…-040018:** Capitalized the wrong word: the sentence marked UUNAHIN but the question asks for KAGYAT. Now KAGYAT is marked.
- **CIVIO-VFIL-…-040044:** o4 "bulok na bulok" is past ripe, not toward the opposite (hilaw); recoded FIL-INTENSITY → FIL-SAME-FIELD.
- **CIVIO-VFIL-…-040047:** Spelling "kanyang" → "kaniyang" (KWF form, used everywhere else in the file).
- **CIVIO-VFIL-…-040069:** Rewritten (same id, still draft): the old item asked what KWF "says" about din/rin with a hedged key. Spec §3.3 tests usage, not commentary. Now an applied item: din after a consonant, rin after a vowel or w/y.
- **CIVIO-VFIL-…-040070:** Rewritten the same way for daw/raw (the old key was a description, and o2/o4 were straw men).

## For CoS to decide (not changed)
1. **Target reuse:**
   - MARUBDOB (040012) and MATATAG (040023) are also targets in filipino-supplement-001 (0009 and 0011).
   - Inside this batch, PAYAPA (040019 and 040027) and MAYABONG (040011 and 040032) each appear as both a synonym and an antonym target, and TUWIRAN is the key of 040003 and the target of 040029.
   - Proposal: replace the second use of each in a later pass.
2. **040092 (order):** the key is C-A-D-B. Distractor C-D-A-B is close, because A ("tiningnan… ang kailangang muwebles") could be read as a later inspection. B's "pinal na inspeksiyon" implies an earlier one, so I kept the key.
3. **040009 MABINI:** the usual sense is "mahinhin / magalang". "Banayad" fits a voice, so I kept it. OK?
4. **040013 KINAUUKULANG:** the key "may kaugnayan" is acceptable. "Angkop / may saklaw" would be tighter.
5. **Balarila codes:** wrong ng/nang pairs are coded FIL-SAME-FIELD in some items and FIL-SPOKEN-FORM in others. Proposal: use FIL-SPOKEN-FORM for all of them.

## Ask
Mark each item PASS / FIX / FAIL, or give a bulk verdict. Then I'll activate the passed items locally. No deploy.
