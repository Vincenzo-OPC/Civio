<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Category;
use Illuminate\Database\Eloquent\Collection;

interface CategoryRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @return Collection<int, Category>
     */
    public function getWithSubcategories(string $orderBy = 'sort_order'): Collection;

    /**
     * @return array<int, mixed>
     */
    public function getTree(): array;

    /**
     * @return array<int, array{id: int, name: string, question_count: int}>
     */
    public function getCategoryDistributionStats(): array;

    public function count(): int;
}
