# Civio architecture

**Civio** is a Laravel 13 + Inertia/React study app for the Philippine Civil Service Exam.
Tutor: **Dexter**. Not official CSC.

```
Browser (Inertia/React 19 + Vite)
  ├─ resources/js/pages/user/*   exams, drills, learn, history, analytics, calendar
  ├─ resources/js/pages/admin/*  questions, users, system, …
  └─ PWA: public/manifest.json + vite-plugin-pwa service worker (NetworkOnly /exams)

Laravel 13
  ├─ Controllers → Services → Repositories → Eloquent
  ├─ Actions (SubmitExamAttemptAction) + ExamGradingService (server grades)
  ├─ App\Ai\Contracts\TutorProvider (Null default; Prism installed for later)
  └─ Optional Sentry (SENTRY_LARAVEL_DSN)

Postgres (Neon planned) / SQLite (tests)
```

Exam flow: active pool → ExamQuestionResource **without** keys → client shuffle
(ID-keyed answers) → POST `/exams/attempts` → server grade → scorecard with keys.
Reveal during play: `POST /exams/reveal`.

See also: `docs/BACKEND_DEVELOPMENT_GUIDE.md`, `docs/LIBRARIES.md`, `AGENTS.md`.
