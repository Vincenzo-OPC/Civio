# Competitor comparison: online CSE reviewers vs Civio (2026-10-22)

Learn-only. I read each public landing page on 22 Oct 2026 (Asia/Manila). Nothing was copied (see the SOURCE_RIGHTS_LEDGER). These are observations from public pages only: I didn't run deep sessions, and the claims are the sites' own.

| Dimension | cseexamreviewer.com | cse-examination.vercel.app | soda-cse-reviewer.vercel.app | Civio (repo at a0b36c4) |
|---|---|---|---|---|
| Coverage | CSE Verbal, Numerical, Logical, GI quizzes (+ other exams) | Prof and SubPro, 4 sections each | Prof/SubPro, category drill | Blueprint mocks per level; drills by category/subcategory; EN/FIL split; Clerical for SubPro |
| Mock structure | Topic quizzes, not full mocks | Full timed mocks (170 / 165 items) | Timed category exams | Server-picked full mocks (150 / 145 scored, demographic items excluded), Study vs Strict modes, short-bank notice |
| Timing | Not shown | 3 h 10 m / 2 h 40 m | Timed | Official limits; wall-clock deadline; throttle-safe warnings (4806240) |
| Solutions | Not visible on landing page | Explanations in Study Reviewer | Explanations + "techniques" | Explanations; Study Mock reveal; assisted vs independent tracking |
| Weakness tracking | None visible | None visible | "Mistakes Locker" re-drill | Review Mistakes + FSRS schedule; weak-category/subcategory bias in mocks; fresh same-skill revisit (a0b36c4) |
| Feedback | Quiz score | Score | Instant | Per-category scorecard, pacing trend (sec/question + accuracy) |
| Mobile | Responsive | Responsive | Mobile-first, streaks | Lite mode, bundle budgets, offline drill packs |
| Reliability signals | Cloudflare gate; bundles many exams | Unclear sourcing | Stale countdown (shows past Aug 9 exam); self-published testimonials | Answer keys withheld server-side; custom-ID leak closed (31e76ec); HOLD-file screening |

## What Civio should learn (without copying)
1. **Habit loop (SODA):** a daily streak and a visible next-exam countdown. Civio has a countdown; a daily focus streak fits the passer insight "one subtest a day".
2. **Exam-day guide (cse-examination):** one page with requirements, what to bring and prohibited items, linked to csc.gov.ph rather than copied.
3. **No-timer Study Reviewer:** Civio's Study mode already covers this. Make "learn first, time later" an explicit path.
4. **Avoid their weaknesses:** stale dates, unverifiable testimonials, unclear provenance, and keys exposed client-side.
