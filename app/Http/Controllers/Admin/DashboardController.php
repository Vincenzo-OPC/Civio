<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Services\AdminDashboardService;
use Illuminate\Http\Request;
use Inertia\Response;

class DashboardController extends Controller
{
    public function __construct(
        protected AdminDashboardService $dashboardService
    ) {}

    /**
     * Display the dynamic administrator stats overview panel.
     */
    public function index(Request $request): Response
    {
        $overview = $this->dashboardService->getOverview();

        return $this->render('admin/dashboard/index', $overview);
    }
}
