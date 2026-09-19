<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Learn\LearnFilterData;
use App\DTOs\Learn\UpsertLearnModuleData;
use App\Http\Resources\AdminDraftModuleResource;
use App\Http\Resources\AdminLearnModuleResource;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\LearnModule;
use App\Models\Subcategory;
use App\Repositories\LearnModuleRepositoryInterface;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;

class LearnModuleService
{
    public function __construct(
        protected LearnModuleRepositoryInterface $repository,
        protected StudyPlanAnalyzer $studyPlanAnalyzer,
        protected CategoryService $categoryService
    ) {}

    /**
     * @param  LearnFilterData|array<string, mixed>  $filters
     * @return array{
     *     modules: array<int, mixed>,
     *     pagination: array{current_page: int, per_page: int, total: int, last_page: int},
     *     categories: Collection<int, Category>
     * }
     */
    public function getAdminModules(LearnFilterData|array $filters, ?int $perPage = null): array
    {
        $filterArray = $filters instanceof LearnFilterData ? $filters->toArray() : $filters;
        $resolvedPerPage = $perPage ?? ($filters instanceof LearnFilterData ? $filters->perPage : 10);

        $paginator = $this->repository->paginateAdminFiltered($filterArray, $resolvedPerPage);
        $categories = $this->categoryService->getCategoriesWithSubcategories();

        return [
            'modules' => AdminLearnModuleResource::collection($paginator->items())->resolve(),
            'pagination' => [
                'current_page' => $paginator->currentPage(),
                'per_page' => $paginator->perPage(),
                'total' => $paginator->total(),
                'last_page' => $paginator->lastPage(),
            ],
            'categories' => $categories,
        ];
    }

    /**
     * @param  LearnFilterData|array<string, mixed>  $filters
     * @return array{
     *     drafts: array<int, mixed>,
     *     pagination: array{current_page: int, per_page: int, total: int, last_page: int},
     *     categories: Collection<int, Category>
     * }
     */
    public function getAdminDrafts(LearnFilterData|array $filters, ?int $perPage = null): array
    {
        $filterArray = $filters instanceof LearnFilterData ? $filters->toArray() : $filters;
        $resolvedPerPage = $perPage ?? ($filters instanceof LearnFilterData ? $filters->perPage : 10);

        $paginator = $this->repository->paginateDrafts($filterArray, $resolvedPerPage);
        $categories = $this->categoryService->getCategoriesWithSubcategories();

        return [
            'drafts' => AdminDraftModuleResource::collection($paginator->items())->resolve(),
            'pagination' => [
                'current_page' => $paginator->currentPage(),
                'per_page' => $paginator->perPage(),
                'total' => $paginator->total(),
                'last_page' => $paginator->lastPage(),
            ],
            'categories' => $categories,
        ];
    }

    /**
     * @return array{modules: array<int, mixed>, categories: array<int, mixed>}
     */
    public function getPublishedCatalog(?int $userId): array
    {
        $modulesCollection = $this->repository->getPublishedCatalog();
        $categories = $this->categoryService->getCategoryTree();

        $completedModuleIds = [];
        if ($userId) {
            $attempts = ExamAttempt::where('user_id', $userId)
                ->orderByDesc('created_at')
                ->get();

            if ($attempts->isNotEmpty()) {
                $weakAreas = $this->studyPlanAnalyzer->identifyWeakAreas($attempts);

                if ($weakAreas->isNotEmpty()) {
                    $weakCategoryNames = $weakAreas->pluck('category')->toArray();

                    usort($categories, function ($a, $b) use ($weakCategoryNames) {
                        $posA = array_search($a['name'], $weakCategoryNames);
                        $posB = array_search($b['name'], $weakCategoryNames);

                        if ($posA !== false && $posB !== false) {
                            return $posA <=> $posB;
                        } elseif ($posA !== false) {
                            return -1;
                        } elseif ($posB !== false) {
                            return 1;
                        } else {
                            return ($a['sort_order'] ?? 0) <=> ($b['sort_order'] ?? 0);
                        }
                    });
                }
            }

            $completedModuleIds = $this->repository->getCompletedModuleIdsByUser($userId);
        }

        $modules = $modulesCollection->map(function ($mod) use ($completedModuleIds) {
            return [
                'id' => $mod->id,
                'title' => $mod->title,
                'slug' => $mod->slug,
                'topic' => $mod->topic,
                'summary' => $mod->summary,
                'estimated_minutes' => $mod->estimated_minutes,
                'category' => $mod->category?->name ?? 'General Info',
                'subcategory' => $mod->subcategory?->name ?? 'Core Concepts',
                'is_completed' => in_array($mod->id, $completedModuleIds),
            ];
        })->values()->toArray();

        return [
            'modules' => $modules,
            'categories' => $categories,
        ];
    }

    /**
     * @return array{module: array<string, mixed>, recommended: array<int, mixed>}
     */
    public function getModuleDetail(string $slug, bool $isAdmin, ?int $userId): array
    {
        if ($isAdmin) {
            $mod = $this->repository->findBySlug($slug, publishedOnly: false);
            if (! $mod) {
                abort(404, 'Learning module not found.');
            }

            $module = [
                'id' => $mod->id,
                'category_id' => $mod->category_id,
                'title' => $mod->title,
                'slug' => $mod->slug,
                'topic' => $mod->topic,
                'summary' => $mod->summary,
                'content' => $mod->content,
                'estimated_minutes' => $mod->estimated_minutes,
                'is_published' => (bool) $mod->is_published,
                'category' => $mod->category?->name ?? 'General Info',
                'subcategory' => $mod->subcategory?->name ?? 'Core Concepts',
                'creator_name' => $mod->creator?->name ?? 'Expert Reviewer',
                'updated_at' => $mod->updated_at?->format('M d, Y') ?? now()->format('M d, Y'),
            ];
        } else {
            $module = Cache::rememberForever("learn.module.show.{$slug}", function () use ($slug) {
                $mod = $this->repository->findBySlug($slug, publishedOnly: true);
                if (! $mod) {
                    abort(404, 'Learning module not found.');
                }

                return [
                    'id' => $mod->id,
                    'category_id' => $mod->category_id,
                    'title' => $mod->title,
                    'slug' => $mod->slug,
                    'topic' => $mod->topic,
                    'summary' => $mod->summary,
                    'content' => $mod->content,
                    'estimated_minutes' => $mod->estimated_minutes,
                    'is_published' => (bool) $mod->is_published,
                    'category' => $mod->category?->name ?? 'General Info',
                    'subcategory' => $mod->subcategory?->name ?? 'Core Concepts',
                    'creator_name' => $mod->creator?->name ?? 'Expert Reviewer',
                    'updated_at' => $mod->updated_at?->format('M d, Y') ?? now()->format('M d, Y'),
                ];
            });
        }

        $recommended = $this->repository->getRecommendedModules((int) $module['category_id'], (int) $module['id'], 3)
            ->map(function ($mod) {
                return [
                    'title' => $mod->title,
                    'slug' => $mod->slug,
                    'estimated_minutes' => $mod->estimated_minutes,
                ];
            })->toArray();

        $module['is_completed'] = false;
        if ($userId) {
            $mod = $this->repository->find((int) $module['id']);
            if ($mod) {
                $module['is_completed'] = $mod->isCompletedBy($userId);
            }
        } else {
            $paragraphs = explode("\n\n", (string) $module['content']);
            $module['content'] = implode("\n\n", array_slice($paragraphs, 0, 4));
        }

        return [
            'module' => $module,
            'recommended' => $recommended,
        ];
    }

    public function createModule(UpsertLearnModuleData $dto, int $userId): LearnModule
    {
        $categoryId = $dto->categoryId;
        $subcategoryId = $dto->subcategoryId;

        if (! $categoryId && $dto->categoryName) {
            $cat = Category::firstOrCreate(
                ['slug' => Str::slug($dto->categoryName)],
                ['name' => $dto->categoryName]
            );
            $categoryId = $cat->id;
        }

        if (! $subcategoryId && $dto->subcategoryName && $categoryId) {
            $sub = Subcategory::firstOrCreate(
                [
                    'category_id' => $categoryId,
                    'slug' => Str::slug($dto->subcategoryName),
                ],
                [
                    'name' => $dto->subcategoryName,
                    'language' => 'English',
                ]
            );
            $subcategoryId = $sub->id;
        }

        $slug = $this->repository->generateUniqueSlug($dto->title);

        $module = $this->repository->create([
            'category_id' => $categoryId,
            'subcategory_id' => $subcategoryId,
            'title' => $dto->title,
            'slug' => $slug,
            'topic' => $dto->topic,
            'summary' => $dto->summary,
            'content' => $dto->content,
            'estimated_minutes' => $dto->estimatedMinutes,
            'is_published' => $dto->isPublished,
            'created_by' => $userId,
        ]);

        $this->repository->clearModuleCache();

        return $module;
    }

    public function updateModule(LearnModule $module, UpsertLearnModuleData $dto): LearnModule
    {
        $slug = $module->slug;
        if ($module->title !== $dto->title) {
            $slug = $this->repository->generateUniqueSlug($dto->title, $module->id);
        }

        $categoryId = $dto->categoryId;
        $subcategoryId = $dto->subcategoryId;

        if (! $categoryId && $dto->categoryName) {
            $cat = Category::firstOrCreate(
                ['slug' => Str::slug($dto->categoryName)],
                ['name' => $dto->categoryName]
            );
            $categoryId = $cat->id;
        }

        if (! $subcategoryId && $dto->subcategoryName && $categoryId) {
            $sub = Subcategory::firstOrCreate(
                [
                    'category_id' => $categoryId,
                    'slug' => Str::slug($dto->subcategoryName),
                ],
                [
                    'name' => $dto->subcategoryName,
                    'language' => 'English',
                ]
            );
            $subcategoryId = $sub->id;
        }

        $this->repository->update((int) $module->id, [
            'category_id' => $categoryId ?? $module->category_id,
            'subcategory_id' => $subcategoryId ?? $module->subcategory_id,
            'title' => $dto->title,
            'slug' => $slug,
            'topic' => $dto->topic,
            'summary' => $dto->summary,
            'content' => $dto->content,
            'estimated_minutes' => $dto->estimatedMinutes,
            'is_published' => $dto->isPublished,
        ]);

        $this->repository->clearModuleCache($module);
        $module->refresh();

        return $module;
    }

    public function getModule(int|string $id): LearnModule
    {
        /** @var LearnModule */
        return $this->repository->findOrFail($id, relations: ['category', 'subcategory']);
    }

    public function deleteModule(LearnModule $module): bool
    {
        $deleted = (bool) $this->repository->delete((int) $module->id);
        $this->repository->clearModuleCache($module);

        return $deleted;
    }

    public function toggleModuleCompletion(string $slug, int $userId): bool
    {
        $module = $this->repository->findBySlug($slug, publishedOnly: false);
        if (! $module) {
            abort(404, 'Learning module not found.');
        }

        $completedByUserIds = $module->completed_by_user_ids ?? [];

        if (in_array($userId, $completedByUserIds)) {
            $completedByUserIds = array_values(array_diff($completedByUserIds, [$userId]));
            $isNowCompleted = false;
        } else {
            $completedByUserIds[] = $userId;
            $isNowCompleted = true;
        }

        $module->completed_by_user_ids = $completedByUserIds;
        $module->save();

        return $isNowCompleted;
    }
}
