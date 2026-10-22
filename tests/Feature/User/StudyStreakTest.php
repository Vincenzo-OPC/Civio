<?php

use App\Enums\ExamMode;
use App\Models\ExamAttempt;
use App\Models\User;
use App\Services\DashboardService;

function streakAttempt(User $user, string $when, array $answers): void
{
    $a = ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => array_keys($answers), 'answers' => $answers, 'cat_scores' => []]);
    $a->forceFill(['created_at' => $when])->save();
}

function streakStats(User $user): array
{
    $m = new ReflectionMethod(DashboardService::class, 'getDailyGoalStats');

    return $m->invoke(app(DashboardService::class), $user->id);
}

test('consecutive study days count, a gap breaks the streak, and yesterday keeps it alive', function () {
    $this->travelTo(now()->setDate(2026, 10, 22)->setTime(9, 0));
    $user = User::factory()->create();
    foreach (['2026-10-21 20:00', '2026-10-20 07:30', '2026-10-19 12:00', '2026-10-17 12:00'] as $day) {
        streakAttempt($user, $day, [1 => 1, 2 => 0]);
    }

    expect(streakStats($user)['streak'])->toBe(3);
});

test('a blank submission does not count as a study day or toward today', function () {
    $this->travelTo(now()->setDate(2026, 10, 22)->setTime(9, 0));
    $user = User::factory()->create();
    streakAttempt($user, '2026-10-22 08:00', [1 => null, 2 => null]);
    streakAttempt($user, '2026-10-21 08:00', [1 => 1, 2 => null, 3 => 2]);

    $stats = streakStats($user);

    expect($stats['streak'])->toBe(1)->and($stats['questionsToday'])->toBe(0);
});

test('a streak longer than 60 days is not truncated', function () {
    $this->travelTo(now()->setDate(2026, 10, 22)->setTime(9, 0));
    $user = User::factory()->create();
    for ($i = 0; $i < 75; $i++) {
        streakAttempt($user, now()->subDays($i)->setTime(10, 0)->toDateTimeString(), [1 => 1]);
    }

    expect(streakStats($user)['streak'])->toBe(75);
});
