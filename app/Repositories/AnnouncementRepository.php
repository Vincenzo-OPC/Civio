<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Announcement;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Cache;

class AnnouncementRepository extends BaseRepository implements AnnouncementRepositoryInterface
{
    public function __construct(Announcement $model)
    {
        parent::__construct($model);
    }

    /**
     * @return Collection<int, Announcement>
     */
    public function getActiveAnnouncements(): Collection
    {
        return Cache::remember('active_announcements', 300, function () {
            return $this->model->newQuery()
                ->where('is_active', true)
                ->where(function ($q) {
                    $q->whereNull('expires_at')
                        ->orWhere('expires_at', '>', now());
                })
                ->latest()
                ->get();
        });
    }

    public function paginateLatest(int $perPage = 15): LengthAwarePaginator
    {
        return $this->model->newQuery()->latest()->paginate($perPage);
    }

    public function clearActiveCache(): void
    {
        Cache::forget('active_announcements');
    }
}
