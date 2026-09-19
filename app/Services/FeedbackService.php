<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Feedback\BulkUpdateFeedbackData;
use App\DTOs\Feedback\SubmitFeedbackData;
use App\DTOs\Feedback\UpdateFeedbackStatusData;
use App\Events\NewFeedbackSubmitted;
use App\Models\Feedback;
use App\Repositories\FeedbackRepositoryInterface;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;

class FeedbackService
{
    public function __construct(
        protected FeedbackRepositoryInterface $repository
    ) {}

    /**
     * @return array{
     *     feedbacks: LengthAwarePaginator,
     *     pending_count: int
     * }
     */
    public function getAdminFeedbacks(int $perPage = 15): array
    {
        $paginator = $this->repository->paginateWithRelations($perPage);
        $counts = $this->repository->getReportCounts();

        foreach ($paginator->items() as $feedback) {
            $groupKey = $feedback->flaggable_type.'_'.$feedback->flaggable_id;
            $feedback->total_reports_count = $counts[$groupKey]->aggregate_count ?? 1;
        }

        return [
            'feedbacks' => $paginator,
            'pending_count' => $this->repository->getPendingCount(),
        ];
    }

    public function submitFeedback(SubmitFeedbackData $data): Feedback
    {
        /** @var Feedback $feedback */
        $feedback = $this->repository->create($data->toAttributes());

        NewFeedbackSubmitted::dispatch($feedback);
        $this->repository->clearFeedbackCache();

        return $feedback;
    }

    public function updateFeedbackStatus(Feedback $feedback, UpdateFeedbackStatusData $data): void
    {
        $feedback->update(['status' => $data->status]);
        $this->repository->updateStatusForTarget(
            (string) $feedback->flaggable_type,
            (int) $feedback->flaggable_id,
            $data->status
        );
        $this->repository->clearFeedbackCache();
    }

    public function deleteFeedback(Feedback $feedback): void
    {
        $this->repository->delete($feedback->id);
        $this->repository->clearFeedbackCache();
    }

    public function bulkUpdateStatus(BulkUpdateFeedbackData $data): void
    {
        $this->repository->bulkUpdateStatus($data->ids, $data->status);
        $this->repository->clearFeedbackCache();
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): void
    {
        $this->repository->bulkDelete($ids);
        $this->repository->clearFeedbackCache();
    }

    public function getPendingFeedbackCount(): int
    {
        return $this->repository->getPendingCount();
    }
}
