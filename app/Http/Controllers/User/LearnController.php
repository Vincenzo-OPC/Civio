<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Services\LearnModuleService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Response;

class LearnController extends Controller
{
    public function __construct(
        protected LearnModuleService $service
    ) {}

    /**
     * Display a grouped index of all published learning modules.
     */
    public function index(Request $request): Response
    {
        $data = $this->service->getPublishedCatalog(auth()->id());

        return $this->render('user/learn/index', [
            'modules' => $data['modules'],
            'categories' => $data['categories'],
        ]);
    }

    public function show(string $slug): Response
    {
        $isAdmin = (bool) auth()->user()?->isAdmin();
        $data = $this->service->getModuleDetail($slug, $isAdmin, auth()->id());

        return $this->render('user/learn/show', [
            'module' => $data['module'],
            'recommended' => $data['recommended'],
        ]);
    }

    /**
     * Toggle the completion status of a learning module for the authenticated user.
     */
    public function toggleComplete(Request $request, string $slug): RedirectResponse
    {
        $userId = auth()->id();
        if (! $userId) {
            return redirect()->back();
        }

        $this->service->toggleModuleCompletion($slug, (int) $userId);

        return redirect()->back();
    }
}
