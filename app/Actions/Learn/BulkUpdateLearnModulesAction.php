<?php

declare(strict_types=1);

namespace App\Actions\Learn;

use App\Models\Category;
use App\Models\Subcategory;
use App\Repositories\LearnModuleRepositoryInterface;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class BulkUpdateLearnModulesAction
{
    public function __construct(
        protected LearnModuleRepositoryInterface $repository
    ) {}

    /**
     * Commit a list of approved draft modules into published status.
     *
     * @param  array<int, array<string, mixed>>  $modulesData
     */
    public function commitApprovedDrafts(array $modulesData, int $userId): int
    {
        return DB::transaction(function () use ($modulesData, $userId) {
            $savedCount = 0;

            foreach ($modulesData as $mData) {
                $categoryName = (string) ($mData['category'] ?? 'General Information');
                $subcategoryName = (string) ($mData['subcategory'] ?? 'Core Concepts');

                $category = Category::firstOrCreate(
                    ['slug' => Str::slug($categoryName)],
                    ['name' => $categoryName]
                );

                $subcategory = Subcategory::firstOrCreate(
                    [
                        'category_id' => $category->id,
                        'slug' => Str::slug($subcategoryName),
                    ],
                    [
                        'name' => $subcategoryName,
                        'language' => 'English',
                    ]
                );

                $dbModule = null;
                if (! empty($mData['id'])) {
                    $dbModule = $this->repository->find((int) $mData['id']);
                }

                if ($dbModule) {
                    $this->repository->update((int) $dbModule->id, [
                        'category_id' => $category->id,
                        'subcategory_id' => $subcategory->id,
                        'title' => (string) $mData['title'],
                        'topic' => (string) $mData['topic'],
                        'summary' => (string) $mData['summary'],
                        'content' => (string) $mData['content'],
                        'estimated_minutes' => (int) ($mData['estimated_minutes'] ?? 15),
                        'is_published' => true,
                    ]);
                } else {
                    $slug = $this->repository->generateUniqueSlug((string) $mData['title']);

                    $this->repository->create([
                        'category_id' => $category->id,
                        'subcategory_id' => $subcategory->id,
                        'title' => (string) $mData['title'],
                        'slug' => $slug,
                        'topic' => (string) $mData['topic'],
                        'summary' => (string) $mData['summary'],
                        'content' => (string) $mData['content'],
                        'estimated_minutes' => (int) ($mData['estimated_minutes'] ?? 15),
                        'is_published' => true,
                        'created_by' => $userId,
                    ]);
                }

                $savedCount++;
            }

            $this->repository->clearModuleCache();

            return $savedCount;
        });
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkUpdateStatus(array $ids, bool $isPublished): int
    {
        return $this->repository->bulkUpdatePublishStatus($ids, $isPublished);
    }

    /**
     * @param  array<int, int|string>  $ids
     */
    public function bulkDelete(array $ids): int
    {
        return $this->repository->bulkDelete($ids);
    }
}
