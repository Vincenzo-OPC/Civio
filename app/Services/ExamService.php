<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Exam\ExamSessionQueryData;
use App\Http\Resources\ExamQuestionResource;
use App\Http\Resources\ExamScorecardResource;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewItem;
use App\Models\SavedDrillSet;
use App\Repositories\QuestionRepositoryInterface;
use App\Repositories\UserRepositoryInterface;
use App\Services\Exam\MockPoolSelector;
use App\Services\Exam\StrictMockLock;
use App\Services\Learning\ExposureHistory;
use App\Services\Learning\LearningInsightsService;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;
use Inertia\DeferProp;
use Inertia\Inertia;

class ExamService
{
    public function __construct(
        protected QuestionRepositoryInterface $questionRepository,
        protected ExamAttemptService $attemptService,
        protected CategoryService $categoryService,
        protected DeterministicAnalysisService $deterministicService,
        protected UserRepositoryInterface $userRepository
    ) {}

    /**
     * Prepare all data required to initialize the interactive exam simulation session.
     *
     * @return array{
     *     questions: array<int, mixed>,
     *     categories: array<int, mixed>,
     *     savedAttempt: array<string, mixed>|null,
     *     retakeSource: array{attempt_id: int, question_ids: array<int, int>, track: string, mode: string}|null,
     *     aiAnalysis: array{status: string, data: array<string, mixed>|null}|DeferProp
     * }
     */
    public function getExamSessionData(ExamSessionQueryData $query, ?int $userId, bool $lite = false): array
    {
        $activeQuestions = $this->questionRepository->getActivePool();
        $savedAttempt = null;
        $retakeSource = null;
        $attempt = null;
        $includeAnswerKey = false;

        if ($query->attemptId !== null) {
            $attempt = $this->attemptService->getScorecardAttempt(
                attemptId: $query->attemptId,
                userId: $userId,
                pendingGuestId: $query->pendingGuestAttemptId
            );

            $includeAnswerKey = true;
            $savedAttempt = (new ExamScorecardResource($attempt))->resolve();
        } elseif ($query->retakeSame !== null || $query->retakeFresh !== null) {
            $retakeId = $query->retakeSame ?? $query->retakeFresh;
            $mode = $query->retakeSame !== null ? 'same' : 'fresh';

            if ($userId !== null && $retakeId !== null) {
                $retakeSource = $this->attemptService->getRetakeSource($retakeId, $userId, $mode);
                $attempt = $this->attemptService->getScorecardAttempt($retakeId, $userId, null);
            }
        }

        // Lite L1: never ship the whole bank. Full mocks are picked on the
        // server (POST /exams/sessions); this page only carries the items a
        // scorecard, retake or drill actually needs.
        if ($attempt !== null) {
            $wanted = array_map('intval', (array) $attempt->question_ids);
            $selected = $activeQuestions->whereIn('id', $wanted);
        } elseif ($query->isDrill) {
            $selected = $this->drillCandidates($activeQuestions, $query, $userId);
        } else {
            $selected = $activeQuestions->take(0);
        }

        $selected = $selected->take(300);
        $payload = ExamQuestionResource::collectionForExam($selected, $includeAnswerKey);
        $locked = app(StrictMockLock::class)->lockedQuestionIds(
            $userId, request()->hasSession() ? request()->session() : null
        );
        $questions = collect(StrictMockLock::withholdKeys($payload, $locked));

        if (($savedAttempt || $retakeSource) && $attempt) {
            $questions = $questions->sortBy(function ($q) use ($attempt) {
                return array_search($q['id'], $attempt->question_ids);
            })->values();
        } else {
            $questions = $questions->values();
        }

        $categories = $this->categoryService->getCategoryTree();

        $resolveAnalysis = function () use ($userId, $query): array {
            if ($userId === null) {
                return ['status' => 'no_data', 'data' => null];
            }

            $targetAttemptId = $query->attemptId ?? $this->attemptService->getLatestUserAttemptId($userId);

            if (! $targetAttemptId) {
                return ['status' => 'no_data', 'data' => null];
            }

            return [
                'status' => 'ready',
                'data' => $this->deterministicService->generate($userId, $targetAttemptId, true),
            ];
        };

        return [
            'questions' => $questions->all(),
            'categories' => $categories,
            'savedAttempt' => $savedAttempt,
            'retakeSource' => $retakeSource,
            // Lite: the scorecard analysis follows after first paint.
            'aiAnalysis' => $lite ? Inertia::defer($resolveAnalysis) : $resolveAnalysis(),
        ];
    }

    /**
     * Items a drill launch may draw from: hand-picked IDs, else the requested
     * category (by ID, then by name like the client used to match), else the
     * first 30 scored items (the client's old fallback). Keys stay withheld.
     *
     * @param  Collection<int, Question>  $pool
     * @return Collection<int, Question>
     */
    protected function drillCandidates(Collection $pool, ExamSessionQueryData $query, ?int $userId = null): Collection
    {
        $scored = $pool->reject(fn (Question $q) => (bool) ($q->subcategory?->category?->is_demographic ?? false));

        if ($query->focusToday) {
            $focus = $this->todaysFocusCandidates($scored, $userId);

            if ($focus->isNotEmpty()) {
                return $focus;
            }
        }

        // Fresh same-skill never falls back to the ordinary pool: an empty set
        // is the honest answer when nothing new is left on those skills.
        if ($query->freshSameSkill) {
            return $userId !== null ? $this->freshSameSkillCandidates($scored, $userId) : collect();
        }

        if ($query->customQuestionIds !== []) {
            $allowed = $this->permittedCustomIds($query->customQuestionIds, $userId);
            $locked = app(StrictMockLock::class)->lockedQuestionIds(
                $userId, request()->hasSession() ? request()->session() : null
            );
            $custom = $scored->whereIn('id', array_values(array_diff($allowed, $locked)));

            if ($custom->isNotEmpty()) {
                return $custom;
            }
        }

        $matches = collect();

        if ($query->drillCategoryId !== null) {
            $matches = $scored->filter(fn (Question $q) => (int) ($q->subcategory?->category_id ?? 0) === $query->drillCategoryId);
        }

        if ($matches->isEmpty() && $query->drillCategoryName !== null && $query->drillCategoryName !== '') {
            $name = mb_strtolower($query->drillCategoryName);
            $matches = $scored->filter(function (Question $q) use ($name) {
                $category = mb_strtolower($q->subcategory?->category?->name ?? 'General Information');

                return str_contains($category, $name) || str_contains($name, $category);
            });
        }

        return $matches->isNotEmpty() ? $matches : $scored->take(30);
    }

    public const FOCUS_ITEMS = 15;

    public const FOCUS_MIXED_ITEMS = 10;

    /**
     * Today's focus: the subject with the lowest independent accuracy (or, with
     * no history, a weekday rotation), 15 items first, then 10 mixed items from
     * the other subjects for transfer practice. Picked on the server.
     *
     * @param  Collection<int, Question>  $scored
     * @return Collection<int, Question>
     */
    protected function todaysFocusCandidates(Collection $scored, ?int $userId): Collection
    {
        $level = $this->focusLevel($userId);
        $eligible = self::focusSubjectsFor($level);
        $scored = $scored->filter(fn (Question $q) => in_array($q->subcategory?->category?->name, $eligible, true));
        $subjects = $scored->map(fn (Question $q) => $q->subcategory?->category?->name)->filter()->unique()->sort()->values();

        if ($subjects->isEmpty()) {
            return collect();
        }

        $focus = $this->todaysFocusSubject($subjects->all(), $userId);
        $inFocus = fn (Question $q) => ($q->subcategory?->category?->name) === $focus;
        $seen = $userId !== null ? app(ExposureHistory::class)->forUser($userId) : [];
        $locked = array_flip(app(StrictMockLock::class)->lockedQuestionIds(
            $userId, request()->hasSession() ? request()->session() : null
        ));
        $scored = $scored->reject(fn (Question $q) => isset($locked[(int) $q->id]));
        // Unseen items first, then seen ones, so practice meets new questions.
        $order = fn (Collection $c) => $c->shuffle()->sortBy(fn (Question $q) => isset($seen[(int) $q->id]) ? 1 : 0)->values();

        return $order($scored->filter($inFocus))->take(self::FOCUS_ITEMS)
            ->concat($order($scored->reject($inFocus))->take(self::FOCUS_MIXED_ITEMS))
            ->unique('id')
            ->values();
    }

    /** Minimum independent items before a subject is ranked as "weakest". */
    public const FOCUS_MIN_SAMPLE = 10;

    /**
     * Subjects eligible for a level: Analytical is Professional only, Clerical
     * is Subprofessional only. Unknown level: only the shared subjects.
     *
     * @return array<int, string>
     */
    public static function focusSubjectsFor(?string $level): array
    {
        if ($level !== null && isset(MockPoolSelector::BLUEPRINT[$level])) {
            return array_column(MockPoolSelector::BLUEPRINT[$level], 'category');
        }

        return ['General Information', 'Numerical Ability', 'Verbal Ability'];
    }

    public function focusLevel(?int $userId): ?string
    {
        $requested = (string) request()->query('track', '');
        if (isset(MockPoolSelector::BLUEPRINT[$requested])) {
            return $requested;
        }

        if ($userId === null) {
            return null;
        }

        foreach (ExamAttempt::query()->where('user_id', $userId)->latest('id')->limit(20)->get(['cat_scores']) as $a) {
            $track = (string) ($a->cat_scores['metadata']['track'] ?? '');
            if (isset(MockPoolSelector::BLUEPRINT[$track])) {
                return $track;
            }
        }

        return null;
    }

    /**
     * @param  array<int, string>  $subjects
     */
    public function todaysFocusSubject(array $subjects, ?int $userId): string
    {
        if ($userId !== null) {
            $weakest = collect(app(LearningInsightsService::class)->forUser($userId)['mastery'])
                ->filter(fn ($m) => in_array($m['name'], $subjects, true) && $m['total'] >= self::FOCUS_MIN_SAMPLE)
                ->sortBy([['percentage', 'asc'], ['total', 'asc']])
                ->first();

            if ($weakest !== null) {
                return $weakest['name'];
            }
        }

        return $subjects[now('Asia/Manila')->dayOfYear % count($subjects)];
    }

    /** Most items in one fresh same-skill revisit. */
    public const FRESH_SAME_SKILL_LIMIT = 20;

    /**
     * Revisit open mistakes with DIFFERENT questions on the same skill:
     * active items from the subcategories of the learner's pending mistakes
     * that the learner has never been served. Chosen on the server, so no
     * client-supplied IDs are involved.
     *
     * @param  Collection<int, Question>  $scored
     * @return Collection<int, Question>
     */
    /** How many fresh same-skill items a learner could get right now (for an honest empty state). */
    public function freshSameSkillAvailable(int $userId): int
    {
        $scored = $this->questionRepository->getActivePool()
            ->reject(fn (Question $q) => (bool) ($q->subcategory?->category?->is_demographic ?? false));

        return $this->freshSameSkillCandidates($scored, $userId)->count();
    }

    public function freshSameSkillCandidates(Collection $scored, int $userId): Collection
    {
        $mistakeIds = ReviewItem::query()->where('user_id', $userId)->where('status', 'pending')->pluck('question_id')->map(fn ($id) => (int) $id)->all();

        if ($mistakeIds === []) {
            return collect();
        }

        $skills = $scored->whereIn('id', $mistakeIds)->map(fn (Question $q) => (int) $q->subcategory_id)->unique()->all();
        $served = app(ExposureHistory::class)->forUser($userId);
        $locked = array_flip(app(StrictMockLock::class)->lockedQuestionIds(
            $userId, request()->hasSession() ? request()->session() : null
        ));

        return $scored
            ->filter(fn (Question $q) => in_array((int) $q->subcategory_id, $skills, true) && ! isset($served[(int) $q->id]) && ! isset($locked[(int) $q->id]))
            ->shuffle()
            ->take(self::FRESH_SAME_SKILL_LIMIT)
            ->values();
    }

    /** Daily budget of hand-picked IDs a principal may request outside its own history. */
    public const CUSTOM_UNSEEN_DAILY_BUDGET = 100;

    /**
     * Filter client-supplied custom drill IDs (anti answer-key harvesting).
     *
     * IDs the user legitimately holds (own attempts, own saved sets) always pass.
     * Any other ID spends from a per-principal daily budget; once spent, unseen
     * IDs are refused. Drafts never reach here (active pool only) and
     * Strict-locked items are removed by the caller.
     *
     * @param  array<int, int>  $ids
     * @return array<int, int>
     */
    protected function permittedCustomIds(array $ids, ?int $userId): array
    {
        $ids = array_slice(array_values(array_unique(array_map('intval', $ids))), 0, ExamSessionQueryData::MAX_CUSTOM_IDS);
        $owned = [];

        if ($userId !== null) {
            foreach (ExamAttempt::query()->where('user_id', $userId)->latest('id')->limit(200)->pluck('question_ids') as $qids) {
                foreach ((array) $qids as $qid) {
                    $owned[(int) $qid] = true;
                }
            }
            foreach (SavedDrillSet::query()->where('user_id', $userId)->with('questions:id')->get() as $set) {
                foreach ($set->questions as $q) {
                    $owned[(int) $q->id] = true;
                }
            }
        }

        $known = array_values(array_filter($ids, fn (int $id) => isset($owned[$id])));
        $unseen = array_values(array_filter($ids, fn (int $id) => ! isset($owned[$id])));

        if ($unseen === []) {
            return $known;
        }

        $principal = $userId !== null
            ? 'u:'.$userId
            : 'g:'.hash('sha256', request()->hasSession() ? request()->session()->getId() : (string) request()->ip());
        $key = 'custom-ids-budget:'.$principal.':'.now()->toDateString();
        $used = (int) Cache::get($key, 0);
        $grant = array_slice($unseen, 0, max(0, self::CUSTOM_UNSEEN_DAILY_BUDGET - $used));

        if ($grant !== []) {
            Cache::put($key, $used + count($grant), now()->endOfDay());
        }

        return array_values(array_merge($known, $grant));
    }

    /**
     * Record a successful examination booklet PDF export.
     */
    public function trackPdfDownload(int $userId): void
    {
        $this->userRepository->incrementPdfDownloads($userId);
    }
}
