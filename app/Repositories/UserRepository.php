<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\ExamAttempt;
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;

class UserRepository extends BaseRepository implements UserRepositoryInterface
{
    public function __construct(User $model)
    {
        parent::__construct($model);
    }

    /**
     * @return Collection<int, User>
     */
    public function getAllWithAttemptCounts(): Collection
    {
        return $this->model->newQuery()
            ->withCount([
                'examAttempts as attempts_count',
                'examAttempts as mock_exams_count' => function ($query) {
                    $query->whereNull('category_id');
                },
                'examAttempts as drills_count' => function ($query) {
                    $query->whereNotNull('category_id');
                },
            ])
            ->latest()
            ->get();
    }

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
    public function getAdminStats(): array
    {
        return [
            'total_users' => $this->model->newQuery()->count(),
            'total_admins' => $this->model->newQuery()->where('role', 'admin')->count(),
            'total_students' => $this->model->newQuery()->whereIn('role', ['user', 'student'])->count(),
            'total_active' => $this->model->newQuery()->where('is_active', true)->count(),
            'total_terms_accepted' => $this->model->newQuery()->whereNotNull('terms_accepted_at')->count(),
            'total_attempts' => ExamAttempt::count(),
            'total_pdf_downloads' => (int) $this->model->newQuery()->sum('pdf_downloads_count'),
        ];
    }

    public function updateUser(int $id, array $attributes): bool
    {
        $user = $this->find($id);

        return $user ? (bool) $user->update($attributes) : false;
    }

    public function deleteUser(int $id): bool
    {
        $user = $this->find($id);

        return $user ? (bool) $user->delete() : false;
    }

    public function incrementPdfDownloads(int $id): void
    {
        $this->model->newQuery()->where('id', $id)->increment('pdf_downloads_count');
    }
}
