<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\Category;
use App\Repositories\CategoryRepositoryInterface;
use Illuminate\Database\Eloquent\Collection;

class CategoryService
{
    public function __construct(
        protected CategoryRepositoryInterface $repository
    ) {}

    /**
     * Categories with subcategories ordered by sort_order (admin learn/question curation).
     *
     * @return Collection<int, Category>
     */
    public function getCategoriesWithSubcategories(string $orderBy = 'sort_order'): Collection
    {
        return $this->repository->getWithSubcategories($orderBy);
    }

    /**
     * Cached category tree for exam setup (sorted by sort_order with subcategories).
     *
     * @return array<int, mixed>
     */
    public function getCategoryTree(): array
    {
        return $this->repository->getTree();
    }

    /**
     * Syllabus view: categories with subcategories ordered by name.
     *
     * @return Collection<int, Category>
     */
    public function getSyllabusTree(): Collection
    {
        return $this->repository->getWithSubcategories('name');
    }

    /**
     * Question distribution stats per category (admin dashboard).
     *
     * @return array<int, array{id: int, name: string, question_count: int}>
     */
    public function getCategoryDistributionStats(): array
    {
        return $this->repository->getCategoryDistributionStats();
    }

    public function count(): int
    {
        return $this->repository->count();
    }
}
