<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\LearnModule;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

interface LearnModuleRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateAdminFiltered(array $filters, int $perPage = 10): LengthAwarePaginator;

    /**
     * @param  array<string, mixed>  $filters
     */
    public function paginateDrafts(array $filters, int $perPage = 10): LengthAwarePaginator;

    /**
     * @return Collection<int, LearnModule>
     */
    public function getPublishedCatalog(): Collection;

    public function findBySlug(string $slug, bool $publishedOnly = true): ?LearnModule;

    /**
     * @return Collection<int, LearnModule>
     */
    public function getRecommendedModules(int $categoryId, int $excludeModuleId, int $limit = 3): Collection;

    /**
     * @return array<int, int>
     */
    public function getCompletedModuleIdsByUser(int $userId): array;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int;

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdatePublishStatus(array $ids, bool $isPublished): int;

    public function generateUniqueSlug(string $title, ?int $ignoreId = null): string;

    public function clearModuleCache(?LearnModule $module = null): void;
}
