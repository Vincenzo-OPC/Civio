<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\ExamAttempt;
use App\Models\ExamDate;
use App\Models\LearnModule;
use App\Models\StudySchedule;
use Carbon\Carbon;
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
     * @return array<string, mixed>
     */
    public function getDashboardData(int $userId): array
    {
        // 1. Exam Date & Countdown
        $examDate = null;
        $examDateRaw = null;
        $examDescription = null;
        $daysUntilExam = null;
        if (Schema::hasTable('exam_dates')) {
            $examDateObj = ExamDate::where('is_active', true)
                ->where('date', '>', now())
                ->orderBy('date')
                ->first();
            if ($examDateObj) {
                $examDate = $examDateObj->date->format('F j, Y');
                $examDateRaw = $examDateObj->date->toDateString();
                $examDescription = $examDateObj->description;
                $daysUntilExam = (int) ceil(now()->diffInDays($examDateObj->date, false));
            }
        }

        // 2. AI Predictor stats
        $aiAnalysis = $this->aiOrchestrator->resolveStrictStatusAndData($userId);

        // 3. Streak & Daily Study Metrics
        $attemptDates = ExamAttempt::where('user_id', $userId)
            ->where('created_at', '>=', now()->subDays(60))
            ->selectRaw('DATE(created_at) as activity_date')
            ->pluck('activity_date');

        $activeDates = $attemptDates->unique()->sortDesc()->values();

        $streak = 0;
        $todayStr = now()->toDateString();
        $yesterdayStr = now()->subDay()->toDateString();
        $startCheck = $activeDates->contains($todayStr) ? now() : ($activeDates->contains($yesterdayStr) ? now()->subDay() : null);

        if ($startCheck) {
            $cursor = $startCheck;
            while ($activeDates->contains($cursor->toDateString()) && $streak < 60) {
                $streak++;
                $cursor = $cursor->subDay();
            }
        }

        // Today's Questions Solved
        $todayAttempts = ExamAttempt::where('user_id', $userId)
            ->whereDate('created_at', Carbon::today())
            ->get();

        $questionsToday = 0;
        foreach ($todayAttempts as $attempt) {
            $meta = $attempt->cat_scores['metadata'] ?? [];
            $questionsToday += (int) ($meta['total_questions'] ?? count($attempt->question_ids ?? []));
        }

        // 4. Today's Scheduled Tasks
        $todayTasks = StudySchedule::where('user_id', $userId)
            ->whereDate('study_date', Carbon::today())
            ->with(['subcategory.category'])
            ->orderBy('study_time', 'asc')
            ->get()
            ->map(function ($task) {
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

        // 5. Recent Attempts (Last 3)
        $recentAttempts = ExamAttempt::where('user_id', $userId)
            ->with('category')
            ->latest()
            ->take(3)
            ->get()
            ->map(function ($attempt) {
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

        // 6. Next Recommended / Uncompleted Learn Module
        $allModules = LearnModule::where('is_published', true)
            ->with(['category', 'subcategory'])
            ->orderBy('id')
            ->get();

        $nextModuleModel = $allModules->first(fn ($m) => ! $m->isCompletedBy($userId));
        $nextModule = $nextModuleModel ? [
            'id' => $nextModuleModel->id,
            'title' => $nextModuleModel->title,
            'slug' => $nextModuleModel->slug,
            'topic' => $nextModuleModel->topic,
            'category_name' => $nextModuleModel->category?->name,
            'estimated_minutes' => $nextModuleModel->estimated_minutes,
        ] : null;

        // 7. Overdue Tasks Count
        $overdueTasksCount = StudySchedule::where('user_id', $userId)
            ->where('study_date', '<', Carbon::today())
            ->where('is_done', false)
            ->count();

        return [
            'stats' => [
                'daysUntilExam' => $daysUntilExam,
                'examDate' => $examDate,
                'examDateRaw' => $examDateRaw,
                'examDescription' => $examDescription,
            ],
            'aiAnalysis' => [
                'status' => $aiAnalysis['status'],
                'data' => $aiAnalysis['data'],
            ],
            'dailyGoal' => [
                'streak' => $streak,
                'questionsToday' => $questionsToday,
                'goalTarget' => 20,
            ],
            'todayTasks' => $todayTasks,
            'overdueTasksCount' => $overdueTasksCount,
            'recentAttempts' => $recentAttempts,
            'nextModule' => $nextModule,
        ];
    }
}
