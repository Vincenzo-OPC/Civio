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
        $cached = Cache::get('active_announcements');
        if ($cached instanceof Collection && ! $cached->contains(fn ($item) => $item instanceof \__PHP_Incomplete_Class)) {
            return $cached;
        }

        $announcements = $this->model->newQuery()
            ->where('is_active', true)
            ->where(function ($q) {
                $q->whereNull('expires_at')
                    ->orWhere('expires_at', '>', now());
            })
            ->latest()
            ->get();

        Cache::put('active_announcements', $announcements, 300);

        return $announcements;
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
