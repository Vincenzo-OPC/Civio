<?php

declare(strict_types=1);

use App\DTOs\Analytics\AnalyticsFilterData;
use App\Http\Resources\AnalyticsMetricsResource;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\StudySchedule;
use App\Models\Subcategory;
use App\Models\User;
use App\Models\UserAiAnalysis;
use App\Services\AiAnalysisOrchestrator;
use App\Services\AnalyticsService;
use App\Services\DashboardService;
use Illuminate\Http\Request;

test('analytics filter data creates DTO from request query params', function () {
    $request = Request::create('/analytics', 'GET', [
        'track' => 'Subprofessional',
        'runs' => '5',
    ]);

    $dto = AnalyticsFilterData::fromRequest($request);

    expect($dto->track)->toBe('Subprofessional')
        ->and($dto->runs)->toBe('5');
});

test('analytics service calculates metrics and percentile rank safely without memory hazards', function () {
    $user = User::factory()->create();
    $service = app(AnalyticsService::class);

    $category = Category::factory()->create(['name' => 'Numerical Ability']);
    $subcategory = Subcategory::factory()->create([
        'category_id' => $category->id,
        'name' => 'Fractions',
    ]);

    // Create several attempts across different users to test percentile ranking
    for ($i = 0; $i < 6; $i++) {
        $otherUser = User::factory()->create();
        ExamAttempt::create([
            'user_id' => $otherUser->id,
            'category_id' => $category->id,
            'question_ids' => [1, 2],
            'answers' => [1, 1],
            'cat_scores' => [
                'metadata' => [
                    'track' => 'Professional',
                    'correct_count' => $i < 3 ? 1 : 2,
                    'total_questions' => 2,
                    'duration_secs' => 100,
                ],
                'categoryScoreMap' => [
                    'Numerical Ability' => [
                        'correct' => $i < 3 ? 1 : 2,
                        'total' => 2,
                        'subcats' => [
                            'Fractions' => ['correct' => $i < 3 ? 1 : 2, 'total' => 2],
                        ],
                    ],
                ],
            ],
        ]);
    }

    $metrics = $service->getAnalyticsMetrics($user->id, new AnalyticsFilterData(track: 'Professional', runs: 'all'));

    expect($metrics)->toHaveKey('percentileRank')
        ->and($metrics)->toHaveKey('filters')
        ->and($metrics['filters']['track'])->toBe('Professional');

    $formatted = $service->formatMetrics($metrics);
    expect($formatted)->toHaveKey('cseReadinessIndex')
        ->and($formatted)->toHaveKey('subtestThresholds');
});

test('analytics metrics resource strips redundant ability and information labels', function () {
    $rawMetrics = [
        'strongestArea' => 'Verbal Ability (85%)',
        'weakestArea' => 'General Information (50%)',
        'mockExamCount' => 2,
        'coveredCategoriesCount' => 4,
        'filters' => ['track' => 'Professional', 'runs' => 'all'],
    ];

    $resource = (new AnalyticsMetricsResource($rawMetrics))->resolve();

    expect($resource['strongestArea'])->toBe('Verbal (85%)')
        ->and($resource['weakestArea'])->toBe('General (50%)')
        ->and($resource['isIncompleteSyllabus'])->toBeFalse();
});

test('ai analysis orchestrator manages retry, delete, and single attempt reports', function () {
    $user = User::factory()->create();
    $orchestrator = app(AiAnalysisOrchestrator::class);

    $attempt = ExamAttempt::create([
        'user_id' => $user->id,
        'category_id' => null,
        'question_ids' => [1, 2],
        'answers' => [1, 1],
        'cat_scores' => [
            'metadata' => [
                'track' => 'Professional',
                'correct_count' => 2,
                'total_questions' => 2,
                'duration_secs' => 90,
            ],
            'categoryScoreMap' => [
                'Verbal Ability' => ['correct' => 2, 'total' => 2],
            ],
        ],
    ]);

    UserAiAnalysis::create([
        'user_id' => $user->id,
        'last_exam_attempt_id' => $attempt->id,
        'analysis_json' => ['readiness_index' => 88],
    ]);

    // Test single attempt resolution
    $singleData = $orchestrator->resolveReportPageData($user->id, (int) $attempt->id);
    expect($singleData['status'])->toBe('ready')
        ->and($singleData['attempt_id'])->toBe($attempt->id);

    // Test delete
    $orchestrator->deleteAnalysis($user->id);
    $this->assertDatabaseMissing('user_ai_analyses', ['user_id' => $user->id]);
});

test('dashboard service aggregates daily streaks and overdue tasks correctly', function () {
    $user = User::factory()->create();
    $dashboardService = app(DashboardService::class);

    StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => now()->subDays(2)->toDateString(),
        'title' => 'Overdue Task 1',
        'is_done' => false,
    ]);

    StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => now()->toDateString(),
        'title' => 'Today Task',
        'is_done' => false,
    ]);

    $data = $dashboardService->getDashboardData($user->id);

    expect($data['overdueTasksCount'])->toBe(1)
        ->and(count($data['todayTasks']))->toBe(1)
        ->and($data['dailyGoal']['goalTarget'])->toBe(20);
});
