<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\Announcement;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

interface AnnouncementRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * @return Collection<int, Announcement>
     */
    public function getActiveAnnouncements(): Collection;

    public function paginateLatest(int $perPage = 15): LengthAwarePaginator;

    public function clearActiveCache(): void;
}
