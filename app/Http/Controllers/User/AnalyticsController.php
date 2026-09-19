<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\DTOs\Analytics\AnalyticsFilterData;
use App\Http\Controllers\Controller;
use App\Http\Resources\AnalyticsMetricsResource;
use App\Http\Resources\ReadinessReportResource;
use App\Services\AiAnalysisOrchestrator;
use App\Services\AnalyticsService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
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
        $userId = $this->requireUser()->id;
        $filters = AnalyticsFilterData::fromRequest($request);

        $metrics = $this->analyticsService->getAnalyticsMetrics($userId, $filters);
        $aiAnalysis = $this->aiOrchestrator->resolveAnalysis($userId);

        return $this->render('user/analytics/index', [
            'stats' => (new AnalyticsMetricsResource($metrics))->resolve(),
            'aiAnalysis' => $aiAnalysis,
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
