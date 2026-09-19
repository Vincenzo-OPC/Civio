<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\User\UpdateUserData;
use App\Models\User;
use App\Repositories\UserRepositoryInterface;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Validation\ValidationException;

class UserService
{
    public function __construct(
        protected UserRepositoryInterface $repository
    ) {}

    /**
     * @return array{
     *     users: Collection<int, User>,
     *     stats: array<string, int>
     * }
     */
    public function getAdminUsersData(): array
    {
        return [
            'users' => $this->repository->getAllWithAttemptCounts(),
            'stats' => $this->repository->getAdminStats(),
        ];
    }

    /**
     * @throws ValidationException
     */
    public function updateUser(int $targetUserId, UpdateUserData $data, int $actingUserId): void
    {
        if ($targetUserId === $actingUserId && $data->hasRole && $data->role !== 'admin') {
            throw ValidationException::withMessages([
                'role' => 'You cannot demote yourself to maintain administrative access.',
            ]);
        }

        if ($targetUserId === $actingUserId && $data->hasIsActive && $data->isActive === false) {
            throw ValidationException::withMessages([
                'is_active' => 'You cannot deactivate your own account while logged in.',
            ]);
        }

        $this->repository->updateUser($targetUserId, $data->toAttributes());
    }

    /**
     * @throws ValidationException
     */
    public function deleteUser(int $targetUserId, int $actingUserId): void
    {
        if ($targetUserId === $actingUserId) {
            throw ValidationException::withMessages([
                'user' => 'You cannot delete your own active administrator account.',
            ]);
        }

        $this->repository->deleteUser($targetUserId);
    }
}
