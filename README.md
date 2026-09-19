# Hiraya Review — Civil Service Exam Reviewer & AI Study Platform

Hiraya Review is a full-stack, AI-powered web platform built for Philippine Civil Service Examination (CSE) aspirants (Professional & Subprofessional tracks). It helps users practice with realistic mock exams and targeted category drills, generate custom study schedules, track predictive mastery analytics, and study interactive learn modules with automated AI-assisted explanations and diagrams.

---

## What It Does

Traditional Civil Service Exam review materials rely on static PDFs, outdated question banks, and generic scoring without personalized diagnostic feedback. Hiraya Review solves this by combining:

- **Dual-Track Mock Exams & Focused Drills:** Realistic timed mock exams for CSE Professional and Subprofessional levels with official category weightings, question palettes, instant scoring, and granular post-exam answer reviews with SVG diagrams.
- **AI-Powered Question & Visual Generation:** On-demand batch generation of high-quality exam questions with Google Gemini API, complete with subcategory-specific prompt engineering, bilingual support (English & Filipino/Tagalog), custom SVG visuals for Abstract Reasoning, and SVG charts for Data Interpretation.
- **Interactive Learn Modules & Curriculum:** Comprehensive study tutorials featuring a 5-step pedagogy (Core Concepts, Key Rules, Mental Shortcuts, Example Scenarios, and Check Your Understanding MCQs) with embedded SVG visual aids.
- **AI Diagnostic Analytics & Predictive Readiness:** Evaluates historical exam performance to predict CSE pass probability, categorize subject mastery (Mastered, Needs Practice, Critical Concern), estimate time to readiness, and output a personalized 7-day remediation plan.
- **Interactive Study Schedule & Weakness Suggestions:** Visual study calendar with drag-and-drop planning, bulk rescheduling, task completion tracking, and algorithm-driven recommendations auto-generated from weak subcategories.
- **Custom & Saved Drill Sets:** Create custom questions, save drill setups, and bookmark targeted question collections for focused repetition.
- **Syllabus & Exam Dates Management:** Dynamic reference viewer for the official Civil Service Commission (CSC) category/subcategory syllabus and countdown trackers for upcoming nationwide exam dates.
- **Polymorphic Issue Reporting & Triage:** Flag inaccurate questions or learn modules with user-driven feedback workflows and an administrative triage dashboard.
- **Granular Role-Based Access & Admin Control:** Comprehensive admin suite for managing questions, drafts, modules, users, announcements, legal documents, cache flushing, and dynamic view-level role permissions.
- **Guest Free Mock Exam:** Low-barrier, single free mock exam for unauthenticated visitors with frictionless onboarding.
- **Real-Time WebSocket Feedback:** Pusher-powered live updates for asynchronous AI generation jobs and platform alerts.
- **Modern Aesthetic & Theme Customization:** Dark/light mode support built with React 19, Tailwind CSS v4, Lucide icons, and 30+ accessible shadcn/ui primitives.

---

## Tech Stack

- **Backend:** PHP 8.4, Laravel 13, Inertia.js v3 (Server), Laravel Fortify v1 (2FA, Passkeys), Laravel Socialite v5, Laravel Wayfinder v0
- **Frontend:** React 19, TypeScript 5.7, Inertia.js v3 (Client), Tailwind CSS v4, shadcn/ui + Radix UI (30+ primitives), Recharts 3.8, Lucide React, Sonner, DOMPurify, React Compiler
- **Database:** PostgreSQL (Neon / Supabase / Local) with strict Eloquent models & transactions
- **AI Generation & Diagnostics:** Google Gemini API (`gemini-3.7-flash`, `gemini-2.5-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`)
- **Real-time:** Pusher WebSockets + Laravel Echo
- **Security & Bot Protection:** Cloudflare Turnstile, Content Security Policy, DOMPurify SVG sanitization, custom input filters (`NoProfanity`, `NoHtml`, `NoUrls`, `NoEmojis`)
- **Infrastructure & Deployment:** Docker (`serversideup/php:8.4-fpm-nginx`), GitHub Actions CI/CD (Pint, ESLint, Prettier, Pest PHP)

---

## Architecture & Code Highlights

- **Monolithic SPA (Inertia.js v3):** Eliminates API glue code by seamlessly rendering React components from Laravel controllers with typed props and server-side validation.
- **Asynchronous AI Queue Pipeline:** Heavy AI jobs (`GenerateQuestionsJob`, `GenerateLearnModuleJob`, `GenerateUserAnalysisJob`) run asynchronously in queues with real-time websocket updates via Pusher (`AiGenerationCompleted`, `AiGenerationFailed`).
- **Dynamic Role-View Visibility Matrix:** Granular permission system stored in database (`RolePermission`), cached and verified via `CheckViewAccess` middleware for role-based view gating.
- **Global Mutation Transactions:** Relational writes (exam attempts, question banks, study schedules) wrapped in database transactions via `TransactionMiddleware` for ACID integrity.
- **Action-Repository-DTO + JsonResource Pattern:** Modern layered backend architecture separating HTTP validation (FormRequests), typed data transport (PHP 8.4 Input DTOs), business mutations (Single-responsibility Actions), query isolation (BaseRepository), and output presentation (Laravel JsonResources). See [`docs/BACKEND_DEVELOPMENT_GUIDE.md`](docs/BACKEND_DEVELOPMENT_GUIDE.md).
- **Strict Typing & Automated Code Quality:** `declare(strict_types=1)` across PHP files, formatted with Laravel Pint, and verified via Pest PHP v4 feature and unit test suites.

---

## Full Feature Breakdown

### 1. Full Mock Exams, Category Drills & Saved Sets
- **Timed Exam Engine:** Full-length CSE Professional (170 items, 3 hours 10 mins) and Subprofessional (165 items, 2 hours 40 mins) mock exams with realistic timers and auto-submission on expiration.
- **Exam Navigation Palette:** Interactive grid palette indicating answered, unanswered, and flagged questions with instant jump capability.
- **Targeted Category Drills:** Practice specific subject areas (General Information, Verbal Ability, Analytical Ability, Numerical Ability, Clerical Ability) with customizable question counts.
- **Smart Weakness Drills:** 1-click drill generation targeting the user's lowest-scoring subcategories based on historical attempt data.
- **Custom Questions & Saved Drill Sets:** Add personal practice items and bookmark custom question sets for focused revision.
- **Post-Exam Review & Scorecards:** Immediate scoring against the 80% passing benchmark, category breakdown radar, and full question rationales with sanitized SVG diagrams.
- **PDF Export Protection:** Export exam answer sheets to PDF with rate-limited checks (`exams/export-pdf-check`).

### 2. AI Question Generator & Draft Review Pipeline
- **Admin Batch Generation:** Generate syllabus-aligned questions on demand using Google Gemini API (`gemini-3.7-flash` / `gemini-2.5-flash`).
- **Subcategory-Specific Prompting:** 13 dedicated prompt rule sets covering official CSE scopes (e.g. Philippine Constitution, RA 6713, Word Analogy, Number Sequence, Logic).
- **Procedural SVG Visual Generation:** Generates valid, self-contained SVG diagrams for Abstract Reasoning (grid matrices, sequences, analogies, rotations, odd-one-out, cube folding, dot placement, mirror reflections).
- **SVG Chart Generation:** Generates data charts (bar, line, pie, comparative tables) for Data Interpretation questions.
- **Bilingual Support:** Strict language-specific prompt enforcement for Filipino/Tagalog (Wastong Gamit, Pagkilala sa Mali) and English subcategories.
- **Draft Staging & Inline Review:** AI-generated questions are saved in `draft` status for admin verification, inline correction, and bulk activation.

### 3. AI Interactive Learn Modules & Study Curriculum
- **5-Part Pedagogical Structure:** Each module includes Core Concepts, Key Rules, Mental Shortcuts, Real-World Exam Scenarios, and Check Your Understanding (3 interactive MCQs with instant feedback).
- **AI Module Synthesizer:** Admin generator (`GenerateLearnModuleJob`) creates complete study guides with embedded SVG illustrations via Gemini.
- **Public Study Hub:** Unauthenticated visitors can browse published study tutorials (`/learn` and `/learn/{slug}`) with automatic XML sitemap generation (`/sitemap.xml`).
- **User Progress Tracking:** Authenticated users track completed lessons with interactive checkboxes and completion timestamps.

### 4. AI Diagnostic Engine & Predictive Analytics
- **Automated Post-Exam Analysis:** Background job (`GenerateUserAnalysisJob`) evaluates attempt histories to generate deep diagnostic reports.
- **Pass Probability Prediction:** Estimates the statistical likelihood of passing the official CSE based on weighted category performance.
- **Subject Mastery Classification:** Categorizes subcategories into **Mastered**, **Needs Practice**, and **Critical Concern**.
- **Predictive Metrics:** Calculates estimated CSE scaled score and remaining days required to reach exam readiness.
- **Personalized 7-Day Remediation Plan:** Provides daily actionable study tasks with direct links to corresponding Learn Modules and weak subcategories.

### 5. Interactive Study Calendar & Weakness Recommender
- **Visual Schedule Planner:** Drag-and-drop calendar interface with day, week, and month views.
- **Bulk Schedule Controls:** 1-click actions to reschedule overdue tasks to today (`bulk-reschedule-today`), update session times, mark completed, or clear tasks.
- **Algorithmic Study Suggestions:** Analyzes weak subcategories and generates tailored study sessions ready to apply with one click.
- **Preset Curriculum Templates:** Quick-apply structured 30-day and 60-day review roadmaps.

### 6. Performance Dashboard & Historical Scorecards
- **Interactive Visualizations:** Score trends, attempt frequency, and category accuracy breakdowns powered by Recharts.
- **Attempt History Archive:** Searchable log of all past exam attempts with scorecards, duration tracking, and single or bulk deletion.

### 7. User Management & Dynamic View Permissions
- **User Administration:** Admin directory to search users, toggle admin/user roles, activate/deactivate accounts, and delete records.
- **Granular View Permissions:** Configure page-level visibility per role dynamically in the database via the `RolePermission` matrix (`/admin/view-management`).

### 8. Community Support & Issue Feedback System
- **Polymorphic Issue Reporting:** Users can flag questions or learn modules directly from the review interface with specific reasons and notes.
- **Admin Feedback Triage:** Dedicated feedback queue (`/admin/feedbacks`) with status management (`pending`, `reviewed`, `resolved`) and bulk actions.
- **Contextual Support Widget:** Support modal with daily-dismiss local state and direct email dispatch.

### 9. Syllabus Reference, Exam Dates & Announcements
- **Official Syllabus Browser:** Interactive reference hierarchy of CSC categories, subcategories, language tags, and demographic items.
- **Exam Date Countdown:** Admin-configurable exam dates displayed as live countdown banners on user dashboards.
- **Global Announcements:** System-wide broadcast alerts with customizable types and expiration dates.
- **Legal Content Editor:** Admin markdown editor for the Terms of Service and Privacy Policy.

### 10. Authentication, Security & Bot Protection
- **Multi-Factor Authentication:** Laravel Fortify integration supporting email/password, Two-Factor Authentication (2FA), and WebAuthn / Passkeys.
- **Social Login:** Single-click sign-in with **Google** OAuth via Laravel Socialite.
- **Cloudflare Turnstile:** Bot defense on registration, login, support, and guest exam submissions.
- **Tiered Rate Limiting:** Dedicated throttle buckets for views (`global-views`), mutations (`global-mutations`), AI operations (`ai-generation`), and PDF exports (`pdf-export`).
- **Content Sanitization:** Strict XSS prevention using `DOMPurify` for SVG/HTML rendering and custom validation rules (`NoProfanity`, `NoHtml`, `NoUrls`, `NoEmojis`).

---

## 🔌 Third-Party API Integrations

### 1. Google Gemini AI API
- **Batch Question Generation (`app/Jobs/GenerateQuestionsJob.php`):** Formats subcategory prompt schemas and visual constraints, querying Gemini (`gemini-3.7-flash`, `gemini-2.5-flash`) with structured JSON schemas (`responseSchema`) for schema validation. Triggered via `app/Http/Controllers/Admin/QuestionController.php`.
- **Learn Module Generation (`app/Jobs/GenerateLearnModuleJob.php`):** Prompts Gemini to synthesize 5-part curriculum guides with embedded SVG illustrations. Triggered via `app/Http/Controllers/Admin/LearnController.php`.
- **User Exam Diagnostic Analysis (`app/Jobs/GenerateUserAnalysisJob.php`):** Evaluates user attempt history, category score breakdowns, and exam schedules to produce mastery ratings and remedial study plans. Dispatched via `app/Http/Controllers/User/ExamController.php`.

### 2. Pusher & Laravel Echo (Real-Time WebSockets)
- **Event Broadcasting (`app/Events/AiGenerationCompleted.php`, `AiGenerationFailed.php`, `NewFeedbackSubmitted.php`, `LearnModulePublished.php`):** Broadcasts real-time events over private user channels to notify the React frontend when background AI jobs finish.

### 3. Google OAuth (Laravel Socialite)
- **OAuth Controller (`app/Http/Controllers/AuthController.php`):** Handles Google OAuth authentication flow with automatic account provisioning and email verification.

### 4. Cloudflare Turnstile (Bot Protection)
- **Turnstile Service (`app/Services/TurnstileService.php`, `app/Http/Middleware/VerifyTurnstile.php`):** Validates Turnstile challenge tokens on authentication, guest exam submission, and support request endpoints.

---

## Local Development Setup

### 1. Requirements
- PHP 8.4 or higher (with `pdo_pgsql`, `mbstring`, `bcmath`, `fileinfo`, `gd`, `zip`)
- Composer 2.x
- Node.js 20+ & npm
- PostgreSQL 15+

### 2. Install

```bash
# Clone the repository
git clone https://github.com/codebykenth/hiraya-review.git
cd hiraya-review

# Run automated setup
composer setup
```

Or install manually:

```bash
composer install
npm install
cp .env.example .env
php artisan key:generate
```

### 3. Environment Config

Update your `.env` file with database credentials and API keys:

```env
# Application
APP_NAME="Hiraya Review"
APP_ENV=local
APP_URL=http://localhost:8000

# Database
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=cse_reviewer
DB_USERNAME=postgres
DB_PASSWORD=your_password

# AI Services
GEMINI_API_KEY=your_gemini_api_key_here

# Real-time WebSockets
BROADCAST_CONNECTION=pusher
PUSHER_APP_ID=your_pusher_app_id
PUSHER_APP_KEY=your_pusher_app_key
PUSHER_APP_SECRET=your_pusher_app_secret
PUSHER_APP_CLUSTER=ap1
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT=http://localhost:8000/auth/google/callback

# Cloudflare Turnstile (Optional for local dev)
TURNSTILE_SITE_KEY=your_turnstile_site_key
TURNSTILE_SECRET_KEY=your_turnstile_secret_key
```

### 4. Database Setup & Seed

```bash
php artisan migrate:fresh --seed
```

This sets up the database schema and seeds the official Civil Service Examination scope (categories & subcategories).

### 5. Run the Application

```bash
composer run dev
```

This concurrently starts:
- Laravel local server (`http://127.0.0.1:8000`)
- Queue worker (`php artisan queue:listen`)
- Vite dev server with Hot Module Replacement (HMR)

---

## Automated Tests & Code Quality

```bash
# Run feature & unit test suite (Pest PHP)
php artisan test --compact

# Run specific test suite or filter
php artisan test --compact --filter=DashboardTest

# Run PHP code style fixer (Laravel Pint)
vendor/bin/pint --dirty --format agent

# Run frontend linting & formatting checks
npm run lint
npm run format
npm run types:check

# Run complete CI verification suite
composer ci:check
```

---

## Deployment (Docker)

The project includes a production-ready Dockerfile based on `serversideup/php:8.4-fpm-nginx`:

```bash
# Build the Docker image
docker build -t hiraya-review .

# Run the container
docker run -p 8080:8080 --env-file .env hiraya-review
```

Deployment features:
- **Optimized Multi-Stage Assets:** Pre-compiles frontend assets via Vite and strips development dependencies.
- **Automated Entrypoint (`scripts/00-laravel-deploy.sh`):** Handles `config:cache`, `route:cache`, `view:cache`, and `migrate --force` on container startup.
- **Continuous Integration:** GitHub Actions workflows (`.github/workflows/lint.yml` and `tests.yml`) enforce code style, type checking, and automated tests on every push.

---

## Author

Built by [Kenth](https://github.com/codebykenth).
