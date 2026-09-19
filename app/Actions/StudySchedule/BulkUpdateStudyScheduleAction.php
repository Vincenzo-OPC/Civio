<?php

declare(strict_types=1);

namespace App\Actions\StudySchedule;

use App\Repositories\StudyScheduleRepositoryInterface;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

class BulkUpdateStudyScheduleAction
{
    public function __construct(
        protected StudyScheduleRepositoryInterface $scheduleRepository
    ) {}

    /**
     * @param  array<int, int>  $ids
     */
    public function rescheduleToday(int $userId, array $ids = []): int
    {
        return DB::transaction(function () use ($userId, $ids) {
            return $this->scheduleRepository->bulkRescheduleToDate($userId, $ids, Carbon::today()->toDateString());
        });
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function markDone(int $userId, array $ids = []): int
    {
        return DB::transaction(function () use ($userId, $ids) {
            return $this->scheduleRepository->bulkMarkDone($userId, $ids);
        });
    }

    public function updateStudyTime(
        int $userId,
        ?string $time,
        ?string $startDate = null,
        ?string $endDate = null,
        ?int $categoryId = null
    ): int {
        return DB::transaction(function () use ($userId, $time, $startDate, $endDate, $categoryId) {
            return $this->scheduleRepository->bulkUpdateStudyTime($userId, $time, $startDate, $endDate, $categoryId);
        });
    }

    /**
     * @param  array<int, int>  $ids
     */
    public function delete(int $userId, array $ids = [], ?string $scope = null, ?string $date = null): int
    {
        return DB::transaction(function () use ($userId, $ids, $scope, $date) {
            return $this->scheduleRepository->bulkDelete($userId, $ids, $scope, $date);
        });
    }

    public function destroyAll(int $userId): int
    {
        return DB::transaction(function () use ($userId) {
            return $this->scheduleRepository->destroyAll($userId);
        });
    }
}
