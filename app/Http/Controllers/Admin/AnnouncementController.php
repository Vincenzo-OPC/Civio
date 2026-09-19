<?php

namespace App\Http\Controllers\Admin;

use App\DTOs\Announcement\UpsertAnnouncementData;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\Announcement\StoreAnnouncementRequest;
use App\Http\Resources\AnnouncementResource;
use App\Models\Announcement;
use App\Services\AnnouncementService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Gate;
use Inertia\Response;

class AnnouncementController extends Controller
{
    public function __construct(
        protected AnnouncementService $service
    ) {}

    public function index(): Response
    {
        $paginator = $this->service->getPaginatedAnnouncements(15);

        return $this->render('admin/announcements/index', [
            'announcements' => AnnouncementResource::collection($paginator),
        ]);
    }

    public function store(StoreAnnouncementRequest $request): RedirectResponse
    {
        Gate::authorize('create', Announcement::class);

        $dto = UpsertAnnouncementData::fromRequest($request);
        $this->service->createAnnouncement($dto);

        return $this->backWithSuccess('Announcement created successfully.');
    }

    public function update(StoreAnnouncementRequest $request, Announcement $announcement): RedirectResponse
    {
        Gate::authorize('update', $announcement);

        $dto = UpsertAnnouncementData::fromRequest($request);
        $this->service->updateAnnouncement($announcement, $dto);

        return $this->backWithSuccess('Announcement updated successfully.');
    }

    public function destroy(Announcement $announcement): RedirectResponse
    {
        Gate::authorize('delete', $announcement);

        $this->service->deleteAnnouncement($announcement);

        return $this->backWithSuccess('Announcement deleted successfully.');
    }
}
