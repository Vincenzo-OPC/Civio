<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Resources\AdminExamAttemptResource;
use App\Models\User;
use App\Repositories\ExamAttemptRepositoryInterface;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class AttemptController extends Controller
{
    public function __construct(
        protected ExamAttemptRepositoryInterface $repository
    ) {}

    /**
     * Display a paginated list of all exam attempts.
     */
    public function index(Request $request): Response
    {
        $filters = $request->only(['user_id', 'type']);

        $attempts = $this->repository
            ->paginateAdminAttempts($filters, 10)
            ->through(fn ($attempt) => (new AdminExamAttemptResource($attempt))->resolve());

        $users = User::orderBy('name')->get(['id', 'name', 'email']);

        return Inertia::render('admin/attempts/index', [
            'attempts' => $attempts,
            'filters' => $filters,
            'users' => $users,
        ]);
    }
}
