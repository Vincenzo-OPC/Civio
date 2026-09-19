<?php

namespace App\Http\Controllers\Admin;

use App\DTOs\Feedback\BulkUpdateFeedbackData;
use App\DTOs\Feedback\SubmitFeedbackData;
use App\DTOs\Feedback\UpdateFeedbackStatusData;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\Feedback\BulkDestroyFeedbackRequest;
use App\Http\Requests\Admin\Feedback\BulkUpdateFeedbackRequest;
use App\Http\Requests\Admin\Feedback\StoreFeedbackRequest;
use App\Http\Requests\Admin\Feedback\UpdateFeedbackStatusRequest;
use App\Http\Resources\FeedbackResource;
use App\Models\Feedback;
use App\Services\FeedbackService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Gate;
use Inertia\Response;

class FeedbackController extends Controller
{
    public function __construct(
        protected FeedbackService $service
    ) {}

    public function index(): Response
    {
        $data = $this->service->getAdminFeedbacks(15);

        return $this->render('admin/feedbacks/index', [
            'feedbacks' => FeedbackResource::collection($data['feedbacks']),
            'pending_count' => $data['pending_count'],
        ]);
    }

    public function store(StoreFeedbackRequest $request): RedirectResponse
    {
        $dto = SubmitFeedbackData::fromRequest($request, (int) $request->user()->id);
        $this->service->submitFeedback($dto);

        return $this->backWithSuccess('Feedback submitted successfully.');
    }

    public function updateStatus(UpdateFeedbackStatusRequest $request, Feedback $feedback): RedirectResponse
    {
        Gate::authorize('update', $feedback);

        $dto = UpdateFeedbackStatusData::fromRequest($request);
        $this->service->updateFeedbackStatus($feedback, $dto);

        return $this->backWithSuccess('Feedback status updated for this item and all related reports.');
    }

    public function destroy(Feedback $feedback): RedirectResponse
    {
        Gate::authorize('delete', $feedback);

        $this->service->deleteFeedback($feedback);

        return $this->backWithSuccess('Feedback deleted.');
    }

    public function bulkUpdate(BulkUpdateFeedbackRequest $request): RedirectResponse
    {
        Gate::authorize('manageAny', Feedback::class);

        $dto = BulkUpdateFeedbackData::fromRequest($request);
        $this->service->bulkUpdateStatus($dto);

        return $this->backWithSuccess('Feedback status updated.');
    }

    public function bulkDestroy(BulkDestroyFeedbackRequest $request): RedirectResponse
    {
        Gate::authorize('manageAny', Feedback::class);

        $this->service->bulkDelete((array) $request->validated('ids'));

        return $this->backWithSuccess('Feedback deleted.');
    }
}
