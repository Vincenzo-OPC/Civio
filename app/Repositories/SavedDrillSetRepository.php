<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Question;
use App\Models\SavedDrillSet;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;

/**
 * @extends BaseRepository<SavedDrillSet>
 */
class SavedDrillSetRepository extends BaseRepository implements SavedDrillSetRepositoryInterface
{
    public function __construct(SavedDrillSet $model)
    {
        parent::__construct($model);
    }

    /**
     * @return Collection<int, SavedDrillSet>
     */
    public function getUserSets(int $userId): Collection
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->withCount('questions')
            ->with(['questions.subcategory.category'])
            ->orderBy('id', 'desc')
            ->get();
    }

    public function findUserSet(int $setId, int $userId): ?SavedDrillSet
    {
        return $this->model->newQuery()
            ->where('id', $setId)
            ->where('user_id', $userId)
            ->first();
    }

    /**
     * @param  array<string, mixed>  $attributes
     * @param  array<int, int>  $questionIds
     */
    public function createWithQuestions(int $userId, array $attributes, array $questionIds = []): SavedDrillSet
    {
        return DB::transaction(function () use ($userId, $attributes, $questionIds) {
            /** @var SavedDrillSet $set */
            $set = $this->model->newQuery()->create([
                'user_id' => $userId,
                'name' => trim((string) $attributes['name']),
                'description' => $attributes['description'] ?? null,
                'color' => $attributes['color'] ?? 'blue',
            ]);

            if (! empty($questionIds)) {
                $set->questions()->sync($questionIds);
            }

            return $set;
        });
    }

    /**
     * @param  array<string, mixed>  $attributes
     */
    public function updateSet(SavedDrillSet $set, array $attributes): bool
    {
        return $set->update([
            'name' => trim((string) $attributes['name']),
            'description' => array_key_exists('description', $attributes) ? $attributes['description'] : $set->description,
            'color' => $attributes['color'] ?? $set->color,
        ]);
    }

    public function deleteSet(SavedDrillSet $set): bool
    {
        return (bool) $set->delete();
    }

    public function attachQuestion(SavedDrillSet $set, int $questionId): void
    {
        $set->questions()->syncWithoutDetaching([$questionId]);
    }

    public function detachQuestion(SavedDrillSet $set, int $questionId): int
    {
        $set->questions()->detach($questionId);

        return $set->questions()->count();
    }

    /**
     * @return Collection<int, Question>
     */
    public function getActiveQuestions(SavedDrillSet $set): Collection
    {
        return $set->questions()
            ->where('status', 'active')
            ->with(['subcategory.category'])
            ->get();
    }

    public function findOrCreateBookmarkSet(int $userId, ?int $setId = null, ?string $newSetName = null): SavedDrillSet
    {
        if (! empty($setId)) {
            return $this->model->newQuery()
                ->where('id', $setId)
                ->where('user_id', $userId)
                ->firstOrFail();
        }

        if (! empty($newSetName)) {
            return $this->model->newQuery()->create([
                'user_id' => $userId,
                'name' => trim($newSetName),
                'description' => 'Custom practice set created from review items.',
                'color' => 'indigo',
            ]);
        }

        return $this->model->newQuery()->firstOrCreate(
            ['user_id' => $userId, 'name' => 'Bookmarked Items'],
            ['description' => 'Questions bookmarked from past exams and drills.', 'color' => 'blue']
        );
    }
}
