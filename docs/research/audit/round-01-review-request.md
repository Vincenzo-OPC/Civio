# Round 01 review request (independent Grok reviewer)

Please review and mark each item PASS / FIX / FAIL. Do not treat the author's checks as approval.

1. New drafts: `docs/research/gap-fill-001.json` (23 items, all `status: draft`, `review_status: unreviewed`).
   - **GI (5):** check each quote against https://lawphil.net/consti/cons1987.html. Art. XIII, Sec. 17(2) says "a Chairman and four Members". Art. XIII, Sec. 18(4) gives visitorial powers.
   - **Filipino sawikain (8):** check the meanings against UP Diksiyonaryong Filipino or KWF.
   - **Filing (3):** check the ARMA rule logic: De la Cruz → DelaCruz (Rule 6), titles and suffixes last (Rule 5), digits before letters (Rule 7), hyphenated names = one unit (Rule 3).
   - **RC/PO (7):** confirm there is exactly one defensible answer.
2. Findings on ChatGPT's 150: `docs/research/supplement-001-review.md`. Confirm or reject the 10 FAILs.
3. Changed but not content: `scripts/batches/qa.py` now accepts approved+passed items, and `tests/Feature/Bank/ImportBatchTest.php` builds its own unreviewed fixture. Both are in commit 4a996c2.
