<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Question;
use App\Models\SavedDrillSet;
use Illuminate\Database\Eloquent\Collection;

/**
 * @extends BaseRepositoryInterface<SavedDrillSet>
 */
interface SavedDrillSetRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @return Collection<int, SavedDrillSet>
     */
    public function getUserSets(int $userId): Collection;

    public function findUserSet(int $setId, int $userId): ?SavedDrillSet;

    /**
     * @param  array<string, mixed>  $attributes
     * @param  array<int, int>  $questionIds
     */
    public function createWithQuestions(int $userId, array $attributes, array $questionIds = []): SavedDrillSet;

    /**
     * @param  array<string, mixed>  $attributes
     */
    public function updateSet(SavedDrillSet $set, array $attributes): bool;

    public function deleteSet(SavedDrillSet $set): bool;

    public function attachQuestion(SavedDrillSet $set, int $questionId): void;

    public function detachQuestion(SavedDrillSet $set, int $questionId): int;

    /**
     * @return Collection<int, Question>
     */
    public function getActiveQuestions(SavedDrillSet $set): Collection;

    public function findOrCreateBookmarkSet(int $userId, ?int $setId = null, ?string $newSetName = null): SavedDrillSet;
}
