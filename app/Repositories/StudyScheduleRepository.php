<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\StudySchedule;
use Carbon\Carbon;
use Carbon\CarbonInterface;
use Illuminate\Database\Eloquent\Collection;

/**
 * @extends BaseRepository<StudySchedule>
 */
class StudyScheduleRepository extends BaseRepository implements StudyScheduleRepositoryInterface
{
    public function __construct(StudySchedule $model)
    {
        parent::__construct($model);
    }

    /**
     * @return Collection<int, StudySchedule>
     */
    public function getMonthSchedules(int $userId, CarbonInterface $startDate, CarbonInterface $endDate): Collection
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->with(['subcategory.category'])
            ->whereBetween('study_date', [$startDate, $endDate])
            ->get();
    }

    /**
     * @return Collection<int, StudySchedule>
     */
    public function getPastPending(int $userId): Collection
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->with(['subcategory.category'])
            ->where('study_date', '<', Carbon::today())
            ->where('is_done', false)
            ->orderBy('study_date', 'asc')
            ->get();
    }

    public function findDuplicate(int $userId, string $studyDate, string $title): ?StudySchedule
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->whereDate('study_date', $studyDate)
            ->where('title', $title)
            ->first();
    }

    /**
     * @return Collection<int, StudySchedule>
     */
    public function getIncompleteSchedules(int $userId): Collection
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->where('is_done', false)
            ->orderBy('study_date', 'asc')
            ->orderBy('id', 'asc')
            ->get();
    }

    public function bulkUpdateStudyTime(
        int $userId,
        ?string $time,
        ?string $startDate = null,
        ?string $endDate = null,
        ?int $categoryId = null
    ): int {
        $query = $this->model->newQuery()->where('user_id', $userId);

        if (! empty($startDate)) {
            $query->whereDate('study_date', '>=', $startDate);
        }
        if (! empty($endDate)) {
            $query->whereDate('study_date', '<=', $endDate);
        }
        if (! empty($categoryId)) {
            $query->whereHas('subcategory', function ($q) use ($categoryId) {
                $q->where('category_id', $categoryId);
            });
        }

        return $query->update([
            'study_time' => $time ?: null,
        ]);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkRescheduleToDate(int $userId, array $ids, string $targetDate): int
    {
        $query = $this->model->newQuery()
            ->where('user_id', $userId)
            ->where('is_done', false);

        if (! empty($ids)) {
            $query->whereIn('id', $ids);
        } else {
            $query->where('study_date', '<', Carbon::today());
        }

        return $query->update([
            'study_date' => $targetDate,
        ]);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkMarkDone(int $userId, array $ids = []): int
    {
        $query = $this->model->newQuery()->where('user_id', $userId);

        if (! empty($ids)) {
            $query->whereIn('id', $ids);
        } else {
            $query->where('study_date', '<', Carbon::today())
                ->where('is_done', false);
        }

        return $query->update([
            'is_done' => true,
        ]);
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkDelete(int $userId, array $ids = [], ?string $scope = null, ?string $date = null): int
    {
        $query = $this->model->newQuery()->where('user_id', $userId);

        if (! empty($ids)) {
            $query->whereIn('id', $ids);
        } elseif (! empty($scope)) {
            if ($scope === 'overdue') {
                $query->where('study_date', '<', Carbon::today())->where('is_done', false);
            } elseif ($scope === 'completed') {
                $query->where('is_done', true);
            } elseif ($scope === 'date' && ! empty($date)) {
                $query->whereDate('study_date', $date);
            }
        }

        return $query->delete();
    }

    public function destroyAll(int $userId): int
    {
        return $this->model->newQuery()->where('user_id', $userId)->delete();
    }
}
