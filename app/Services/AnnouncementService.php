<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\Announcement\UpsertAnnouncementData;
use App\Models\Announcement;
use App\Repositories\AnnouncementRepositoryInterface;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

class AnnouncementService
{
    public function __construct(
        protected AnnouncementRepositoryInterface $repository
    ) {}

    public function getPaginatedAnnouncements(int $perPage = 15): LengthAwarePaginator
    {
        return $this->repository->paginateLatest($perPage);
    }

    /**
     * @return Collection<int, Announcement>
     */
    public function getActiveAnnouncements(): Collection
    {
        return $this->repository->getActiveAnnouncements();
    }

    public function createAnnouncement(UpsertAnnouncementData $data): Announcement
    {
        /** @var Announcement $announcement */
        $announcement = $this->repository->create($data->toAttributes());
        $this->repository->clearActiveCache();

        return $announcement;
    }

    public function updateAnnouncement(Announcement $announcement, UpsertAnnouncementData $data): Announcement
    {
        $this->repository->update($announcement->id, $data->toAttributes());
        $this->repository->clearActiveCache();

        return $announcement->refresh();
    }

    public function deleteAnnouncement(Announcement $announcement): void
    {
        $this->repository->delete($announcement->id);
        $this->repository->clearActiveCache();
    }
}
