<?php

declare(strict_types=1);

namespace App\Repositories;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Collection;

interface QuestionRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateFiltered(array $filters, int $perPage = 10): LengthAwarePaginator;

    public function getActivePool(): Collection;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdateStatus(array $ids, string $status): int;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int;
}
