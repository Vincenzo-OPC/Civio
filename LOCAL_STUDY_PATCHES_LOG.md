# CSE-Pack LOCAL_STUDY_PATCHES_LOG

## 2026-10-03 local study patch (2026-10-03 23:10:39 +08:00 PT)

- Target: MSI / hiraya-review-app on :8080 and hiraya-review-db; Hermes :8642 was not touched.
- Scope: original local CSE-style practice only. No CSC/reviewer-center/web-item scraping or copying; no git push.

### Sirit / reveal bug

- Root cause: the live exam shuffles options and remaps the in-memory correct_option, but /exams/reveal returns the database key for the original option order. The old client indexed the shuffled options with that unremapped database index, so the displayed choice could be wrong while the explanation belonged to the database answer.
- Fix: live-exam-view.tsx now uses originalOptionIndices to translate the API's original index back to the displayed index before choosing the letter/text; the reveal state is scoped to the question ID, and the typed expound update preserves the answer fields. The live JS was rebuilt with the _php-shim PATH, copied into hiraya-review-app:/var/www/html/public/build, and the service-worker cache was bumped to v7.
- Verification: frontend production build passed; reveal routes are present; the deployed bundle contains the option-index mapping; the component lint passes. Full type-check remains blocked by pre-existing generated Wayfinder module/type errors elsewhere in the repository, not by this reveal component after the local fix.

### Bank expansion

- Inserted: **197 new active items** from the 200-item original batch; 3 exact active-stem duplicates were skipped by the seed guard.
- New active total: **919** (was 722).
- Coverage: Constitution (30), RA 6713 (23), peace/human rights (9), environment (15), English/Filipino verbal (54), analytical (22), numerical (17), clerical filing/spelling (27).
- Integrity checks for inserted rows: 4 options each, valid 0-based correct_option, answer text present in every explanation, and zero ?? artifacts.
- Rejected for fact-check: **0**. Constitutional, RA 6713/SALN, human-rights remedies, and environmental-law facts were limited to well-known rules checked against primary/public government sources; no uncertain legal item was inserted.
- Existing malformed newest rows: repaired broken ??/quote-marker text and answer explanations; corrected affected numeric choices/explanations, including the 10% discount and 6,10,18,34 sequence.
