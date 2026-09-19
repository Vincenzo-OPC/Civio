<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Question;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Cache;

class QuestionRepository extends BaseRepository implements QuestionRepositoryInterface
{
    public function __construct(Question $model)
    {
        parent::__construct($model);
    }

    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateFiltered(array $filters, int $perPage = 10): LengthAwarePaginator
    {
        $query = $this->model->newQuery()
            ->with(['subcategory.category'])
            ->orderBy('id', 'desc');

        if (! empty($filters['status']) && $filters['status'] !== 'all' && $filters['status'] !== 'All Statuses') {
            $query->where('status', strtolower((string) $filters['status']));
        }

        if (! empty($filters['category']) && $filters['category'] !== 'all' && $filters['category'] !== 'All Categories') {
            $query->whereHas('subcategory.category', fn ($q) => $q->where('name', $filters['category']));
        }

        if (! empty($filters['subcategory']) && $filters['subcategory'] !== 'all' && $filters['subcategory'] !== 'All Subcategories') {
            $query->whereHas('subcategory', fn ($q) => $q->where('name', $filters['subcategory']));
        }

        if (! empty($filters['language']) && $filters['language'] !== 'all' && $filters['language'] !== 'All Languages') {
            $query->where('language', $filters['language']);
        }

        if (! empty($filters['search'])) {
            $search = (string) $filters['search'];
            $query->where(fn ($q) => $q->where('stem', 'like', "%{$search}%")
                ->orWhere('explanation', 'like', "%{$search}%")
                ->orWhere('id', $search));
        }

        return $query->paginate($perPage)->withQueryString();
    }

    public function getActivePool(): Collection
    {
        return Cache::rememberForever('questions.active', function () {
            return $this->model->newQuery()
                ->where('status', 'active')
                ->with(['subcategory.category'])
                ->get();
        });
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdateStatus(array $ids, string $status): int
    {
        $count = $this->model->newQuery()->whereIn('id', $ids)->update(['status' => strtolower($status)]);
        Cache::forget('questions.active');

        return $count;
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int
    {
        $count = $this->model->newQuery()->whereIn('id', $ids)->delete();
        Cache::forget('questions.active');

        return $count;
    }
}
