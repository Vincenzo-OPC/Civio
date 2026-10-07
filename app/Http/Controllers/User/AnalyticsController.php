<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\DTOs\Analytics\AnalyticsFilterData;
use App\Http\Controllers\Controller;
use App\Http\Resources\AnalyticsMetricsResource;
use App\Http\Resources\ReadinessReportResource;
use App\Services\AiAnalysisOrchestrator;
use App\Services\AnalyticsService;
use App\Support\LiteMode;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class AnalyticsController extends Controller
{
    public function __construct(
        protected AnalyticsService $analyticsService,
        protected AiAnalysisOrchestrator $aiOrchestrator,
    ) {}

    /**
     * Render the user analytics page with real performance metrics.
     */
    public function index(Request $request): Response
    {
        // Local study: guests see soft-empty analytics (no fake bank demos claimed).
        if (! $request->user()) {
            $empty = (new AnalyticsMetricsResource([
                'filters' => [
                    'track' => (string) $request->query('track', 'Professional'),
                    'runs' => (string) $request->query('runs', 'all'),
                ],
                'avgScore' => 0,
                'totalExams' => 0,
                'strongestArea' => 'Not Started',
                'weakestArea' => 'Not Started',
                'chartData' => [],
                'categories' => [],
                'passingRate' => 0,
                'totalDurationText' => '0 mins',
                'avgDurationText' => '0 mins',
                'totalQuestionsSolved' => 0,
                'daysUntilExam' => null,
                'examDate' => null,
                'examDateRaw' => null,
                'pacingTrend' => [],
                'attemptBreakdowns' => [],
                'cseReadinessIndex' => 0,
                'subtestThresholds' => [],
                'hasSubtestRisk' => false,
                'percentileRank' => 50,
                'coveredCategoriesCount' => 0,
                'mockExamCount' => 0,
            ]))->resolve();

            return $this->render('user/analytics/index', [
                'stats' => $empty,
                'aiAnalysis' => ['status' => 'no_data', 'data' => null],
            ]);
        }

        $userId = $this->requireUser()->id;
        $filters = AnalyticsFilterData::fromRequest($request);

        $metrics = $this->analyticsService->getAnalyticsMetrics($userId, $filters);
        $stats = (new AnalyticsMetricsResource($metrics))->resolve();

        if (LiteMode::enabled($request)) {
            // Lite: text tables instead of charts, and the AI analysis arrives
            // after first paint as a deferred prop.
            return $this->render('user/analytics/index', [
                'stats' => LiteMode::trimAnalyticsStats($stats),
                'aiAnalysis' => Inertia::defer(fn () => $this->aiOrchestrator->resolveAnalysis($userId)),
            ]);
        }

        return $this->render('user/analytics/index', [
            'stats' => $stats,
            'aiAnalysis' => $this->aiOrchestrator->resolveAnalysis($userId),
        ]);
    }

    /**
     * Render the predictive AI Diagnostic Report page.
     */
    public function aiAnalysisReport(Request $request): Response|RedirectResponse
    {
        $userId = $this->requireUser()->id;
        $isAdminOrLocal = app()->environment('local') || (bool) $request->user()?->isAdmin();

        if ($isAdminOrLocal && $request->has('delete')) {
            $this->aiOrchestrator->deleteAnalysis($userId);

            return redirect('/analytics/ai-analysis');
        }

        if ($isAdminOrLocal && $request->has('retry')) {
            $this->aiOrchestrator->retryAnalysis($userId);

            return redirect('/analytics/ai-analysis');
        }

        $attemptId = $request->has('attempt_id') ? (int) $request->query('attempt_id') : null;
        $reportData = $this->aiOrchestrator->resolveReportPageData($userId, $attemptId);

        return $this->render('user/dashboard/ai-analysis', (new ReadinessReportResource($reportData))->resolve());
    }
}
