<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Feedback;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;

class FeedbackRepository extends BaseRepository implements FeedbackRepositoryInterface
{
    public function __construct(Feedback $model)
    {
        parent::__construct($model);
    }

    public function paginateWithRelations(int $perPage = 15): LengthAwarePaginator
    {
        return $this->model->newQuery()
            ->with(['user', 'flaggable'])
            ->latest()
            ->paginate($perPage);
    }

    /**
     * @return Collection<string, mixed>
     */
    public function getReportCounts(): Collection
    {
        return $this->model->newQuery()
            ->selectRaw('flaggable_type, flaggable_id, count(*) as aggregate_count')
            ->groupBy('flaggable_type', 'flaggable_id')
            ->get()
            ->keyBy(fn ($item) => $item->flaggable_type.'_'.$item->flaggable_id);
    }

    public function getPendingCount(): int
    {
        return Cache::remember('pending_feedback_count', 60, function () {
            return $this->model->newQuery()->where('status', 'pending')->count();
        });
    }

    public function updateStatusForTarget(string $flaggableType, int $flaggableId, string $newStatus): int
    {
        return $this->model->newQuery()
            ->where('flaggable_type', $flaggableType)
            ->where('flaggable_id', $flaggableId)
            ->where('status', 'pending')
            ->update(['status' => $newStatus]);
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdateStatus(array $ids, string $newStatus): int
    {
        $targets = $this->model->newQuery()
            ->whereIn('id', $ids)
            ->get(['flaggable_type', 'flaggable_id']);

        $updated = $this->model->newQuery()->whereIn('id', $ids)->update(['status' => $newStatus]);

        foreach ($targets as $target) {
            $this->model->newQuery()
                ->where('flaggable_type', $target->flaggable_type)
                ->where('flaggable_id', $target->flaggable_id)
                ->where('status', 'pending')
                ->update(['status' => $newStatus]);
        }

        return $updated;
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int
    {
        return $this->model->newQuery()->whereIn('id', $ids)->delete();
    }

    public function clearFeedbackCache(): void
    {
        Cache::forget('pending_feedback_count');
    }
}
