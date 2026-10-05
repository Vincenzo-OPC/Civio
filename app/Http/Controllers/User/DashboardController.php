<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Services\DashboardService;
use Illuminate\Http\Request;
use Inertia\Response;

class DashboardController extends Controller
{
    public function __construct(
        protected DashboardService $dashboardService
    ) {}

    /**
     * Render the comprehensive user dashboard command center.
     */
    public function index(Request $request): Response
    {
        // Local study: guests get a soft-empty dashboard shell.
        if (! $request->user()) {
            return $this->render('user/dashboard/index', [
                'stats' => [
                    'daysUntilExam' => null,
                    'examDate' => null,
                    'examDateRaw' => null,
                    'examDescription' => null,
                ],
                'aiAnalysis' => [
                    'status' => 'no_data',
                    'data' => null,
                ],
                'dailyGoal' => [
                    'streak' => 0,
                    'questionsToday' => 0,
                    'goalTarget' => 20,
                ],
                'todayTasks' => [],
                'overdueTasksCount' => 0,
                'recentAttempts' => [],
                'nextModule' => null,
            ]);
        }

        $userId = $this->requireUser()->id;
        $data = $this->dashboardService->getDashboardData($userId);

        return $this->render('user/dashboard/index', $data);
    }
}
