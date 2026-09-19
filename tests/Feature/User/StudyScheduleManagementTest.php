<?php

declare(strict_types=1);

use App\Actions\StudySchedule\BulkUpdateStudyScheduleAction;
use App\Actions\StudySchedule\ShiftStudyScheduleAction;
use App\DTOs\StudySchedule\ShiftScheduleData;
use App\DTOs\StudySchedule\UpsertStudyScheduleData;
use App\Http\Resources\StudyScheduleResource;
use App\Models\StudySchedule;
use App\Models\User;
use App\Repositories\StudyScheduleRepositoryInterface;
use App\Services\StudyScheduleService;
use Carbon\Carbon;

test('study schedule repository manages and finds duplicates', function () {
    $user = User::factory()->create();
    $repo = app(StudyScheduleRepositoryInterface::class);

    $schedule = $repo->create([
        'user_id' => $user->id,
        'study_date' => Carbon::tomorrow()->toDateString(),
        'study_time' => '14:30:00',
        'title' => 'Vocabulary Review',
        'is_done' => false,
    ]);

    expect($schedule)->toBeInstanceOf(StudySchedule::class)
        ->and($schedule->title)->toBe('Vocabulary Review');

    $duplicate = $repo->findDuplicate($user->id, Carbon::tomorrow()->toDateString(), 'Vocabulary Review');
    expect($duplicate)->not->toBeNull()
        ->and($duplicate->id)->toBe($schedule->id);

    $missing = $repo->findDuplicate($user->id, Carbon::tomorrow()->toDateString(), 'Non-existent');
    expect($missing)->toBeNull();
});

test('upsert study schedule data DTO creates schedules via service', function () {
    $user = User::factory()->create();
    $service = app(StudyScheduleService::class);

    $dto = new UpsertStudyScheduleData(
        studyDate: Carbon::tomorrow()->toDateString(),
        studyTime: '18:00',
        title: 'Clerical Operations',
        description: 'Filing & indexing review',
        subcategoryId: null,
        isDone: false
    );

    $result = $service->createSchedule($user->id, $dto);

    expect($result['is_duplicate'])->toBeFalse()
        ->and($result['schedule'])->toBeInstanceOf(StudySchedule::class)
        ->and($result['schedule']->title)->toBe('Clerical Operations');

    // Trying to create the duplicate via service
    $dupResult = $service->createSchedule($user->id, $dto);
    expect($dupResult['is_duplicate'])->toBeTrue()
        ->and($dupResult['duplicate']->id)->toBe($result['schedule']->id);
});

test('shift study schedule action shifts incomplete items', function () {
    $user = User::factory()->create();
    $action = app(ShiftStudyScheduleAction::class);

    $twoDaysAgo = Carbon::today()->subDays(2)->toDateString();
    $yesterday = Carbon::today()->subDay()->toDateString();

    $s1 = StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => $twoDaysAgo,
        'title' => 'Grammar Drill 1',
        'is_done' => false,
    ]);

    $s2 = StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => $yesterday,
        'title' => 'Grammar Drill 2',
        'is_done' => false,
    ]);

    $data = new ShiftScheduleData(mode: 'start_today');
    $count = $action->execute($user->id, $data);

    expect($count)->toBe(2)
        ->and($s1->fresh()->study_date->toDateString())->toBe(Carbon::today()->toDateString())
        ->and($s2->fresh()->study_date->toDateString())->toBe(Carbon::today()->addDay()->toDateString());
});

test('bulk update study schedule action reschedules and marks completed', function () {
    $user = User::factory()->create();
    $action = app(BulkUpdateStudyScheduleAction::class);

    $s1 = StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => Carbon::yesterday()->toDateString(),
        'title' => 'Reading Comprehension',
        'is_done' => false,
    ]);

    $count = $action->markDone($user->id, [$s1->id]);
    expect($count)->toBe(1)
        ->and($s1->fresh()->is_done)->toBeTrue();

    $rescheduledCount = $action->rescheduleToday($user->id, [$s1->id]);
    expect($rescheduledCount)->toBe(0); // Already marked done, not overdue pending
});

test('study schedule resource formats model correctly', function () {
    $user = User::factory()->create();
    $schedule = StudySchedule::create([
        'user_id' => $user->id,
        'study_date' => '2026-09-25',
        'study_time' => '15:45:00',
        'title' => 'Logic & Reasoning',
        'description' => 'Syllogism practice',
        'is_done' => false,
    ]);

    $resource = (new StudyScheduleResource($schedule))->resolve();

    expect($resource['title'])->toBe('Logic & Reasoning')
        ->and($resource['study_date'])->toBe('2026-09-25')
        ->and($resource['study_time'])->toBe('15:45')
        ->and($resource['is_done'])->toBeFalse();
});
