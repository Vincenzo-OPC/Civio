<?php

declare(strict_types=1);

namespace App\Repositories;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

interface FeedbackRepositoryInterface extends BaseRepositoryInterface
{
    public function paginateWithRelations(int $perPage = 15): LengthAwarePaginator;

    /**
     * @return Collection<string, mixed>
     */
    public function getReportCounts(): Collection;

    public function getPendingCount(): int;

    public function updateStatusForTarget(string $flaggableType, int $flaggableId, string $newStatus): int;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdateStatus(array $ids, string $newStatus): int;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int;

    public function clearFeedbackCache(): void;
}
