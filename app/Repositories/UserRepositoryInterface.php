<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\User;
use Illuminate\Database\Eloquent\Collection;

interface UserRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @return Collection<int, User>
     */
    public function getAllWithAttemptCounts(): Collection;

    /**
     * @return array{
     *     total_users: int,
     *     total_admins: int,
     *     total_students: int,
     *     total_active: int,
     *     total_terms_accepted: int,
     *     total_attempts: int,
     *     total_pdf_downloads: int
     * }
     */
    public function getAdminStats(): array;

    public function updateUser(int $id, array $attributes): bool;

    public function deleteUser(int $id): bool;

    public function incrementPdfDownloads(int $id): void;
}
