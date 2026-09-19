<?php

use App\DTOs\Announcement\UpsertAnnouncementData;
use App\DTOs\Feedback\SubmitFeedbackData;
use App\DTOs\Feedback\UpdateFeedbackStatusData;
use App\DTOs\Support\SupportMessageData;
use App\DTOs\User\UpdateUserData;
use App\Enums\UserRole;
use App\Mail\SupportSubmittedMail;
use App\Models\Feedback;
use App\Models\Question;
use App\Models\User;
use App\Services\AnnouncementService;
use App\Services\FeedbackService;
use App\Services\SupportService;
use App\Services\UserService;
use Illuminate\Support\Facades\Mail;
use Illuminate\Validation\ValidationException;

test('announcement service handles CRUD and cache invalidation', function () {
    $service = app(AnnouncementService::class);

    $announcement = $service->createAnnouncement(new UpsertAnnouncementData(
        title: 'Platform Maintenance',
        message: 'System upgrade scheduled for midnight.',
        type: 'warning',
        isActive: true,
        expiresAt: now()->addDays(2)->toDateTimeString(),
    ));

    expect($announcement->title)->toBe('Platform Maintenance')
        ->and($announcement->is_active)->toBeTrue();

    $updated = $service->updateAnnouncement($announcement, new UpsertAnnouncementData(
        title: 'Maintenance Completed',
        message: 'All systems operational.',
        type: 'success',
        isActive: true,
        expiresAt: now()->addDays(1)->toDateTimeString(),
    ));

    expect($updated->title)->toBe('Maintenance Completed')
        ->and($updated->type)->toBe('success');

    $active = $service->getActiveAnnouncements();
    expect($active)->toHaveCount(1);

    $service->deleteAnnouncement($announcement);
    $activeAfterDelete = $service->getActiveAnnouncements();
    expect($activeAfterDelete)->toBeEmpty();
});

test('feedback service handles submissions, relations, report counts, and bulk updates', function () {
    $service = app(FeedbackService::class);
    $user = User::factory()->create();

    $question = Question::factory()->create();

    $fb1 = $service->submitFeedback(new SubmitFeedbackData(
        userId: $user->id,
        flaggableId: $question->id,
        flaggableType: Question::class,
        reason: 'Typo in stem',
        details: 'Minor wording issue',
    ));

    $user2 = User::factory()->create();
    $fb2 = $service->submitFeedback(new SubmitFeedbackData(
        userId: $user2->id,
        flaggableId: $question->id,
        flaggableType: Question::class,
        reason: 'Incorrect explanation',
        details: 'Check explanation',
    ));

    $adminFeedbacks = $service->getAdminFeedbacks(10);
    expect($adminFeedbacks['pending_count'])->toBe(2)
        ->and($adminFeedbacks['feedbacks']->total())->toBe(2);

    $firstItem = $adminFeedbacks['feedbacks']->items()[0];
    expect($firstItem->total_reports_count)->toBe(2);

    // Updating status should update sibling pending reports for same target
    $service->updateFeedbackStatus($fb1, new UpdateFeedbackStatusData('resolved'));
    expect($fb1->fresh()->status)->toBe('resolved')
        ->and($fb2->fresh()->status)->toBe('resolved')
        ->and($service->getPendingFeedbackCount())->toBe(0);

    // Bulk delete
    $service->bulkDelete([$fb1->id, $fb2->id]);
    expect(Feedback::count())->toBe(0);
});

test('user service prevents self-demotion, self-deactivation, and self-deletion', function () {
    $service = app(UserService::class);
    $admin = User::factory()->create(['role' => 'admin', 'is_active' => true]);

    // Attempt self-demotion
    expect(fn () => $service->updateUser(
        $admin->id,
        new UpdateUserData(role: 'user', hasRole: true),
        $admin->id
    ))->toThrow(ValidationException::class);

    // Attempt self-deactivation
    expect(fn () => $service->updateUser(
        $admin->id,
        new UpdateUserData(isActive: false, hasIsActive: true),
        $admin->id
    ))->toThrow(ValidationException::class);

    // Attempt self-deletion
    expect(fn () => $service->deleteUser($admin->id, $admin->id))
        ->toThrow(ValidationException::class);

    // Modifying another user succeeds
    $student = User::factory()->create(['role' => 'user', 'is_active' => true]);
    $service->updateUser(
        $student->id,
        new UpdateUserData(role: 'admin', isActive: false, hasRole: true, hasIsActive: true),
        $admin->id
    );

    $student->refresh();
    expect($student->role)->toBe(UserRole::Admin)
        ->and($student->is_active)->toBeFalse();

    $service->deleteUser($student->id, $admin->id);
    expect(User::find($student->id))->toBeNull();
});

test('support service sends email with DTO payload', function () {
    Mail::fake();
    $service = app(SupportService::class);

    $service->handleSubmission(new SupportMessageData(
        name: 'Maria Santos',
        email: 'maria@example.com',
        message: 'Inquiry regarding civil service exam schedule.',
    ), '127.0.0.1');

    Mail::assertSent(SupportSubmittedMail::class, function ($mail) {
        return $mail->data['name'] === 'Maria Santos'
            && $mail->data['email'] === 'maria@example.com';
    });
});
