<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\ExamAttempt;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

interface ExamAttemptRepositoryInterface extends BaseRepositoryInterface
{
    public function findUserAttempt(int $attemptId, int $userId): ?ExamAttempt;

    public function findGuestAttempt(int $attemptId): ?ExamAttempt;

    /**
     * @return Collection<int, ExamAttempt>
     */
    public function getUserAttempts(int $userId): Collection;

    public function getLatestUserAttemptId(int $userId): ?int;

    public function deleteUserAttempts(int $userId, array $attemptIds): int;

    public function paginateAdminAttempts(array $filters, int $perPage = 10): LengthAwarePaginator;
}
