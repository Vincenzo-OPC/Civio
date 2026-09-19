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
        $userId = $this->requireUser()->id;
        $data = $this->dashboardService->getDashboardData($userId);

        return $this->render('user/dashboard/index', $data);
    }
}
