<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\ExamAttempt;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

class ExamAttemptRepository extends BaseRepository implements ExamAttemptRepositoryInterface
{
    /**
     * Create a new class instance.
     */
    public function __construct(ExamAttempt $model)
    {
        parent::__construct($model);
    }

    public function findUserAttempt(int $attemptId, int $userId): ?ExamAttempt
    {
        return $this->model->newQuery()
            ->where('id', $attemptId)
            ->where('user_id', $userId)
            ->with('category')
            ->first();
    }

    public function findGuestAttempt(int $attemptId): ?ExamAttempt
    {
        return $this->model->newQuery()
            ->where('id', $attemptId)
            ->whereNull('user_id')
            ->with('category')
            ->first();
    }

    /**
     * @return Collection<int, ExamAttempt>
     */
    public function getUserAttempts(int $userId): Collection
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->with('category:id,name')
            ->latest()
            ->get();
    }

    public function getLatestUserAttemptId(int $userId): ?int
    {
        return $this->model->newQuery()
            ->where('user_id', $userId)
            ->latest()
            ->value('id');
    }

    public function deleteUserAttempts(int $userId, array $attemptIds): int
    {
        return $this->model->newQuery()
            ->whereIn('id', $attemptIds)
            ->where('user_id', $userId)
            ->delete();
    }

    public function paginateAdminAttempts(array $filters, int $perPage = 10): LengthAwarePaginator
    {
        $query = $this->model->newQuery()
            ->with(['user', 'category'])
            ->latest();

        if (! empty($filters['user_id'])) {
            $query->where('user_id', $filters['user_id']);
        }

        if (! empty($filters['type'])) {
            if ($filters['type'] === 'mock') {
                $query->whereNull('category_id');
            } elseif ($filters['type'] === 'drill') {
                $query->whereNotNull('category_id');
            }
        }

        return $query->paginate($perPage)->withQueryString();
    }
}
