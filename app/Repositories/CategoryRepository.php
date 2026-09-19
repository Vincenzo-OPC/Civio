<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Category;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;

class CategoryRepository extends BaseRepository implements CategoryRepositoryInterface
{
    public function __construct(Category $model)
    {
        parent::__construct($model);
    }

    /**
     * @return Collection<int, Category>
     */
    public function getWithSubcategories(string $orderBy = 'sort_order'): Collection
    {
        return $this->model->newQuery()
            ->with(['subcategory' => function ($query) use ($orderBy) {
                $query->orderBy($orderBy);
            }])
            ->orderBy($orderBy)
            ->get();
    }

    /**
     * @return array<int, mixed>
     */
    public function getTree(): array
    {
        return Cache::rememberForever('categories.tree', function () {
            return $this->model->newQuery()
                ->with(['subcategory' => function ($query) {
                    $query->orderBy('sort_order');
                }])
                ->orderBy('sort_order')
                ->get()
                ->toArray();
        });
    }

    /**
     * @return array<int, array{id: int, name: string, question_count: int}>
     */
    public function getCategoryDistributionStats(): array
    {
        $categories = $this->model->newQuery()
            ->with(['subcategory' => function ($query) {
                $query->withCount('questions');
            }])
            ->orderBy('sort_order')
            ->get();

        return $categories->map(function (Category $category) {
            $questionCount = (int) $category->subcategory->sum('questions_count');

            return [
                'id' => (int) $category->id,
                'name' => (string) $category->name,
                'question_count' => $questionCount,
            ];
        })->values()->all();
    }

    public function count(): int
    {
        return $this->model->newQuery()->count();
    }
}
