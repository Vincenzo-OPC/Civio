<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\ExamAttempt;
use App\Models\ExamDate;
use App\Models\LearnModule;
use App\Models\StudySchedule;
use App\Support\CseExamDates;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Schema;

class DashboardService
{
    public function __construct(
        protected ExamAttemptFormatter $formatter,
        protected AiAnalysisOrchestrator $aiOrchestrator,
    ) {}

    /**
     * Aggregate full command center data for user dashboard.
     *
     * @return array{
     *     stats: array<string, mixed>,
     *     aiAnalysis: array{status: string, data: mixed},
     *     dailyGoal: array{streak: int, questionsToday: int, goalTarget: int},
     *     todayTasks: Collection<int, array<string, mixed>>,
     *     overdueTasksCount: int,
     *     recentAttempts: Collection<int, array<string, mixed>>,
     *     nextModule: array<string, mixed>|null,
     *     studyTotals: array{sessions: int, questionsAnswered: int, sessionsThisWeek: int}
     * }
     */
    public function getDashboardData(int $userId, bool $includeAnalysis = true): array
    {
        $data = [
            'stats' => $this->getExamDateStats(),
            'dailyGoal' => $this->getDailyGoalStats($userId),
            'todayTasks' => $this->getTodayTasks($userId),
            'overdueTasksCount' => $this->getOverdueTasksCount($userId),
            'recentAttempts' => $this->getRecentAttempts($userId),
            'nextModule' => $this->getNextModule($userId),
            'studyTotals' => $this->getStudyTotals($userId),
        ];

        if ($includeAnalysis) {
            $data = ['aiAnalysis' => $this->getAiAnalysis($userId), ...$data];
        }

        return $data;
    }

    /**
     * @return array{status: string, data: mixed}
     */
    public function getAiAnalysis(int $userId): array
    {
        $aiAnalysis = $this->aiOrchestrator->resolveStrictStatusAndData($userId);

        return [
            'status' => $aiAnalysis['status'],
            'data' => $aiAnalysis['data'],
        ];
    }

    /**
     * Exam countdown data. The hand-checked CSC calendar (CseExamDates) is the
     * source of truth; an admin ExamDate row is only a fallback when no
     * confirmed CSC sitting remains, and only if its PH day has not passed.
     * A stale or expired row can never override the CSC calendar.
     *
     * @return array{daysUntilExam: int|null, examDate: string|null, examDateRaw: string|null, examDescription: string|null, examSource: 'csc'|'admin'|null, examSittings: list<array{date: string, sitting: string, label: string}>, examMilestones: list<array{date: string, sitting: string, label: string, kind: string}>, examSourceTitle: string, examSourceUrl: string, examLastChecked: string}
     */
    public function getExamDateStats(): array
    {
        $tz = CseExamDates::TIMEZONE;
        $today = Carbon::now($tz)->startOfDay();
        $calendar = CseExamDates::upcoming(Carbon::now());

        $sittings = $calendar['sittings'];
        $source = $sittings === [] ? null : 'csc';
        $description = $sittings === [] ? null : $sittings[0]['sitting'];

        if ($sittings === [] && Schema::hasTable('exam_dates')) {
            $row = ExamDate::where('is_active', true)
                ->whereDate('date', '>=', $today->toDateString())
                ->orderBy('date')
                ->first();

            if ($row) {
                $sittings = [[
                    'date' => $row->date->toDateString(),
                    'sitting' => (string) ($row->description ?? 'Exam date set by admin'),
                    'label' => 'Exam day',
                ]];
                $source = 'admin';
                $description = $row->description;
            }
        }

        $next = $sittings[0] ?? null;
        $nextDay = $next ? Carbon::parse($next['date'], $tz)->startOfDay() : null;

        return [
            'daysUntilExam' => $nextDay ? (int) $today->diffInDays($nextDay, false) : null,
            'examDate' => $nextDay?->format('F j, Y'),
            'examDateRaw' => $next['date'] ?? null,
            'examDescription' => $description,
            'examSource' => $source,
            'examSittings' => $sittings,
            'examMilestones' => $calendar['milestones'],
            'examSourceTitle' => $calendar['source_title'],
            'examSourceUrl' => $calendar['source_url'],
            'examLastChecked' => $calendar['last_checked'],
        ];
    }

    /**
     * @return array{streak: int, questionsToday: int, goalTarget: int}
     */
    protected function getDailyGoalStats(int $userId): array
    {
        // A study day needs at least one answered item: opening and submitting
        // a blank drill does not keep a streak alive or count toward the goal.
        $answeredByDay = [];
        ExamAttempt::where('user_id', $userId)
            ->where('created_at', '>=', now()->subDays(400))
            ->select(['id', 'created_at', 'answers'])
            ->chunkById(500, function ($rows) use (&$answeredByDay) {
                foreach ($rows as $attempt) {
                    $answered = count(array_filter((array) $attempt->answers, fn ($v) => $v !== null && $v !== ''));
                    if ($answered > 0) {
                        $day = $attempt->created_at->timezone(config('app.timezone'))->toDateString();
                        $answeredByDay[$day] = ($answeredByDay[$day] ?? 0) + $answered;
                    }
                }
            });

        $streak = 0;
        $cursor = isset($answeredByDay[now()->toDateString()]) ? now() : (isset($answeredByDay[now()->subDay()->toDateString()]) ? now()->subDay() : null);

        while ($cursor !== null && isset($answeredByDay[$cursor->toDateString()])) {
            $streak++;
            $cursor = $cursor->subDay();
        }

        $questionsToday = $answeredByDay[now()->toDateString()] ?? 0;

        return [
            'streak' => $streak,
            'questionsToday' => $questionsToday,
            'goalTarget' => 20,
        ];
    }

    /**
     * @return Collection<int, array<string, mixed>>
     */
    protected function getTodayTasks(int $userId): Collection
    {
        return StudySchedule::where('user_id', $userId)
            ->whereDate('study_date', Carbon::today())
            ->with(['subcategory.category'])
            ->orderBy('study_time', 'asc')
            ->get()
            ->map(function (StudySchedule $task): array {
                return [
                    'id' => $task->id,
                    'title' => $task->title,
                    'description' => $task->description,
                    'study_time' => $task->study_time ? Carbon::parse($task->study_time)->format('h:i A') : null,
                    'is_done' => (bool) $task->is_done,
                    'subcategory_name' => $task->subcategory?->name,
                    'category_name' => $task->subcategory?->category?->name,
                ];
            });
    }

    /**
     * @return Collection<int, array<string, mixed>>
     */
    protected function getRecentAttempts(int $userId): Collection
    {
        return ExamAttempt::where('user_id', $userId)
            ->with('category')
            ->latest()
            ->take(3)
            ->get()
            ->map(function (ExamAttempt $attempt): array {
                $meta = $attempt->cat_scores['metadata'] ?? [];
                $scorePercentage = (float) $this->formatter->calculateWeightedPercentage($attempt->cat_scores ?? []);
                $isTrackExam = empty($attempt->category_id);
                $trackName = $meta['track'] ?? ($isTrackExam ? 'Mock Exam' : 'Practice Drill');
                $totalQuestions = (int) ($meta['total_questions'] ?? count($attempt->question_ids ?? []));
                $timeTakenSeconds = (int) ($meta['time_taken_seconds'] ?? 0);

                return [
                    'id' => $attempt->id,
                    'title' => $attempt->category?->name ?? ($trackName.' - '.($meta['exam_type'] ?? 'General')),
                    'score_percentage' => round($scorePercentage, 1),
                    'passed' => $scorePercentage >= 80,
                    'is_mock' => $isTrackExam,
                    'total_questions' => $totalQuestions,
                    'duration_text' => $this->formatter->formatDurationText($timeTakenSeconds),
                    'created_at_human' => $attempt->created_at ? $attempt->created_at->diffForHumans() : 'Recently',
                ];
            });
    }

    /**
     * Plain counts from stored, submitted attempts. No scores, rates or forecasts.
     *
     * @return array{sessions: int, questionsAnswered: int, sessionsThisWeek: int}
     */
    protected function getStudyTotals(int $userId): array
    {
        $attempts = ExamAttempt::where('user_id', $userId)
            ->get(['id', 'question_ids', 'cat_scores', 'created_at']);
        $weekAgo = now()->subDays(7);

        return [
            'sessions' => $attempts->count(),
            'questionsAnswered' => (int) $attempts->sum(
                fn (ExamAttempt $a): int => (int) ($a->cat_scores['metadata']['total_questions'] ?? count($a->question_ids ?? [])),
            ),
            'sessionsThisWeek' => $attempts->filter(
                fn (ExamAttempt $a): bool => $a->created_at !== null && $a->created_at->greaterThanOrEqualTo($weekAgo),
            )->count(),
        ];
    }

    /**
     * @return array<string, mixed>|null
     */
    protected function getNextModule(int $userId): ?array
    {
        $allModules = LearnModule::where('is_published', true)
            ->with(['category', 'subcategory'])
            ->orderBy('id')
            ->get();

        $nextModuleModel = $allModules->first(fn (LearnModule $m): bool => ! $m->isCompletedBy($userId));

        return $nextModuleModel ? [
            'id' => $nextModuleModel->id,
            'title' => $nextModuleModel->title,
            'slug' => $nextModuleModel->slug,
            'topic' => $nextModuleModel->topic,
            'category_name' => $nextModuleModel->category?->name,
            'estimated_minutes' => $nextModuleModel->estimated_minutes,
        ] : null;
    }

    protected function getOverdueTasksCount(int $userId): int
    {
        return StudySchedule::where('user_id', $userId)
            ->where('study_date', '<', Carbon::today())
            ->where('is_done', false)
            ->count();
    }
}
