<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\LearnModule;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;

class LearnModuleRepository extends BaseRepository implements LearnModuleRepositoryInterface
{
    public function __construct(LearnModule $model)
    {
        parent::__construct($model);
    }

    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateAdminFiltered(array $filters, int $perPage = 10): LengthAwarePaginator
    {
        $status = $filters['status'] ?? 'all';
        $category = $filters['category'] ?? 'all';
        $subcategory = $filters['subcategory'] ?? 'all';
        $search = $filters['search'] ?? null;

        $query = $this->model->newQuery()
            ->with(['category', 'subcategory'])
            ->latest();

        if ($status && $status !== 'all' && $status !== 'All Statuses') {
            if ($status === 'ACTIVE' || $status === 'published') {
                $query->where('is_published', true);
            } elseif ($status === 'DRAFT' || $status === 'draft') {
                $query->where('is_published', false);
            }
        }

        if ($category && $category !== 'all' && $category !== 'All Categories') {
            $query->whereHas('category', function ($q) use ($category) {
                $q->where('name', $category);
            });
        }

        if ($subcategory && $subcategory !== 'all' && $subcategory !== 'All Subcategories') {
            $query->whereHas('subcategory', function ($q) use ($subcategory) {
                $q->where('name', $subcategory);
            });
        }

        if ($search) {
            $query->where(function ($q) use ($search) {
                $q->where('title', 'like', "%{$search}%")
                    ->orWhere('topic', 'like', "%{$search}%")
                    ->orWhere('summary', 'like', "%{$search}%");
            });
        }

        return $query->paginate($perPage)->withQueryString();
    }

    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateDrafts(array $filters, int $perPage = 10): LengthAwarePaginator
    {
        $category = $filters['category'] ?? 'all';
        $subcategory = $filters['subcategory'] ?? 'all';
        $search = $filters['search'] ?? null;

        $query = $this->model->newQuery()
            ->with(['category', 'subcategory'])
            ->where('is_published', false)
            ->latest();

        if ($category && $category !== 'all' && $category !== 'All Categories') {
            $query->whereHas('category', function ($q) use ($category) {
                $q->where('name', $category);
            });
        }

        if ($subcategory && $subcategory !== 'all' && $subcategory !== 'All Subcategories') {
            $query->whereHas('subcategory', function ($q) use ($subcategory) {
                $q->where('name', $subcategory);
            });
        }

        if ($search) {
            $query->where(function ($q) use ($search) {
                $q->where('title', 'like', "%{$search}%")
                    ->orWhere('topic', 'like', "%{$search}%")
                    ->orWhere('summary', 'like', "%{$search}%");
            });
        }

        return $query->paginate($perPage)->withQueryString();
    }

    /**
     * @return Collection<int, LearnModule>
     */
    public function getPublishedCatalog(): Collection
    {
        return Cache::rememberForever('learn.modules.published', function () {
            return $this->model->newQuery()
                ->with(['category', 'subcategory'])
                ->where('is_published', true)
                ->latest()
                ->get();
        });
    }

    public function findBySlug(string $slug, bool $publishedOnly = true): ?LearnModule
    {
        $query = $this->model->newQuery()
            ->with(['category', 'subcategory', 'creator'])
            ->where('slug', $slug);

        if ($publishedOnly) {
            $query->where('is_published', true);
        }

        return $query->first();
    }

    /**
     * @return Collection<int, LearnModule>
     */
    public function getRecommendedModules(int $categoryId, int $excludeModuleId, int $limit = 3): Collection
    {
        return Cache::rememberForever("learn.module.recommended.{$excludeModuleId}", function () use ($categoryId, $excludeModuleId, $limit) {
            return $this->model->newQuery()
                ->where('category_id', $categoryId)
                ->where('id', '!=', $excludeModuleId)
                ->where('is_published', true)
                ->take($limit)
                ->get();
        });
    }

    /**
     * @return array<int, int>
     */
    public function getCompletedModuleIdsByUser(int $userId): array
    {
        return $this->model->newQuery()
            ->whereJsonContains('completed_by_user_ids', $userId)
            ->pluck('id')
            ->toArray();
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int
    {
        $deleted = $this->model->newQuery()->whereIn('id', $ids)->delete();
        $this->clearModuleCache();

        return $deleted;
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdatePublishStatus(array $ids, bool $isPublished): int
    {
        $updated = $this->model->newQuery()->whereIn('id', $ids)->update([
            'is_published' => $isPublished,
        ]);
        $this->clearModuleCache();

        return $updated;
    }

    public function generateUniqueSlug(string $title, ?int $ignoreId = null): string
    {
        $slug = Str::slug($title);
        $originalSlug = $slug;
        $count = 1;

        while ($this->model->newQuery()
            ->where('slug', $slug)
            ->when($ignoreId, fn ($q) => $q->where('id', '!=', $ignoreId))
            ->exists()) {
            $slug = $originalSlug.'-'.$count++;
        }

        return $slug;
    }

    public function clearModuleCache(?LearnModule $module = null): void
    {
        Cache::forget('learn.modules.published');
        Cache::forget('categories.tree');
        if ($module) {
            Cache::forget("learn.module.show.{$module->slug}");
            Cache::forget("learn.module.recommended.{$module->id}");
        }
    }
}
