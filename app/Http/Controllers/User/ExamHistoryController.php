<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\BulkDestroyAttemptsRequest;
use App\Models\ExamAttempt;
use App\Services\ExamAttemptService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class ExamHistoryController extends Controller
{
    public function __construct(
        protected ExamAttemptService $attemptService
    ) {}

    /**
     * Display a listing of past attempts for user.
     */
    public function index(Request $request): Response|RedirectResponse
    {
        $userId = (int) auth()->id();
        $perPage = min(50, max(5, (int) $request->input('per_page', 10)));
        $filters = [
            'search' => $request->input('search'),
            'track' => $request->input('track'),
            'date' => $request->input('date'),
            'page' => $request->input('page', 1),
        ];

        $historyData = $this->attemptService->getUserHistoryData($userId, $filters, $perPage);

        if ($historyData['needs_redirect']) {
            return redirect()->route('history.index', array_merge($request->query(), ['page' => $historyData['redirect_page']]));
        }

        return Inertia::render('user/history/index', [
            'attempts' => $historyData['attempts'],
            'stats' => $historyData['stats'],
            'pagination' => $historyData['pagination'],
            'filters' => [
                'search' => $filters['search'] ?? '',
                'track' => $filters['track'] ?? 'All Tracks',
                'date' => $filters['date'] ?? 'all',
                'per_page' => $perPage,
            ],
        ]);
    }

    /**
     * Delete an exam attempt record.
     */
    public function destroy(ExamAttempt $attempt): RedirectResponse
    {
        Gate::authorize('delete', $attempt);

        $this->attemptService->deleteUserAttempt($attempt);

        return $this->backWithSuccess('Attempt record deleted successfully!');
    }

    /**
     * Delete multiple exam attempt records.
     */
    public function bulkDestroy(BulkDestroyAttemptsRequest $request): RedirectResponse
    {
        $validated = $request->validated();

        $this->attemptService->bulkDeleteUserAttempts((int) auth()->id(), (array) $validated['ids']);

        return $this->backWithSuccess('Selected attempt records deleted successfully!');
    }
}
