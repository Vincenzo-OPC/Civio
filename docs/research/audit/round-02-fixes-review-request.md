# Round 02 fixes review request (independent reviewer: Chief of Staff)

Everything below is draft. Nothing is activated locally and nothing is deployed. The details are in `audit/round-02-fixes.md`.

1. **Rewrites of approved items:** `docs/research/round-02-fixes.json`, 178 items. Mark each PASS / FIX / FAIL.
   - **93 spelling items.** Check that each misspelling is real and that its error label is right.
     - Watch closely for misspellings that might be accepted variants. I chose against "fulfil", "gage" and "neighbour", and kept "fulfill", "gauge" removed, and "neighbor".
     - Check "humourous": I dropped it.
     - Check that "Februrary" and "aighth" are plausible.
   - **60 Verbal lead-in changes.** Only the lead-in changed. Is the new lead-in natural for its sentence?
   - **25 order-of-operations items.** New expression shapes with recomputed keys, for example (8 × 8 + 16) ÷ 2 = 40 and 9 × 4 − 9 ÷ 3 = 33.
2. **gap-fill-003:** `docs/research/gap-fill-003.json`, 10 new drafts on ARMA Rules 2, 3, 4, 7 and 8. Check the rule readings:
   - Rule 2: "&" is spelled out and is its own unit; a leading "The" goes last; inner minor words stay.
   - Rule 3: a possessive keeps its s; a hyphenated name is one unit.
   - Rule 4: a lone initial files before full names; an acronym is one unit.
   - Rule 7: ascending value; Arabic, then Roman, then words; ordinal endings are ignored.
   - Rule 8: names are indexed as written, minor words included.
   - The Rule 8 items use real school names (UE, UST, USC, Ateneo). OK, or should they be fictional?
3. **Numerical shortcuts:** `docs/research/shortcuts-num-001.json`, 267 shortcuts on approved items, each machine-verified against the key. PASS them in bulk or flag any.
4. **Confirmed applied per your rulings (FYI):**
   - gap-fill-002: 14 fixed, approved and activated locally.
   - VFIL-0007 o2 recoded to FIL-OTHER-TRAIT, and synced.
   - Spec v0.1.6 (§10.5) and v0.1.7 (§10.6, shortcut field).
