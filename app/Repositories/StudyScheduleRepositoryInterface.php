<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\StudySchedule;
use Carbon\CarbonInterface;
use Illuminate\Database\Eloquent\Collection;

/**
 * @extends BaseRepositoryInterface<StudySchedule>
 */
interface StudyScheduleRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @return Collection<int, StudySchedule>
     */
    public function getMonthSchedules(int $userId, CarbonInterface $startDate, CarbonInterface $endDate): Collection;

    /**
     * @return Collection<int, StudySchedule>
     */
    public function getPastPending(int $userId): Collection;

    public function findDuplicate(int $userId, string $studyDate, string $title): ?StudySchedule;

    /**
     * @return Collection<int, StudySchedule>
     */
    public function getIncompleteSchedules(int $userId): Collection;

    public function bulkUpdateStudyTime(
        int $userId,
        ?string $time,
        ?string $startDate = null,
        ?string $endDate = null,
        ?int $categoryId = null
    ): int;

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkRescheduleToDate(int $userId, array $ids, string $targetDate): int;

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkMarkDone(int $userId, array $ids = []): int;

    /**
     * @param  array<int, int>  $ids
     */
    public function bulkDelete(int $userId, array $ids = [], ?string $scope = null, ?string $date = null): int;

    public function destroyAll(int $userId): int;
}
