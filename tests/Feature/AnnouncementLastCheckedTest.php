<?php

use App\DTOs\Announcement\UpsertAnnouncementData;
use App\Models\Announcement;
use App\Services\AnnouncementService;

test('announcements keep an honest last-checked time', function () {
    $announcement = app(AnnouncementService::class)->createAnnouncement(
        new UpsertAnnouncementData(
            title: 'Digital exam slots',
            message: 'Prefer CSDEx when a region has open slots. This is a CIVIO study note, not a CSC bulletin.',
            type: 'info',
            isActive: true,
            expiresAt: null,
            lastCheckedAt: '2026-09-23 08:00:00',
        ),
    );

    expect($announcement->last_checked_at?->toDateString())->toBe('2026-09-23');

    $updated = app(AnnouncementService::class)->updateAnnouncement(
        $announcement,
        new UpsertAnnouncementData(
            title: 'Digital exam slots',
            message: 'Still a study note. Re-check csc.gov.ph before you apply.',
            type: 'warning',
            isActive: true,
            expiresAt: null,
            lastCheckedAt: null,
        ),
    );

    expect($updated->last_checked_at)->toBeNull()
        ->and(Announcement::query()->find($announcement->id)?->type)->toBe('warning');
});
