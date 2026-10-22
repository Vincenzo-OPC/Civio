<?php

use App\Models\ExamDate;
use App\Models\User;
use App\Services\DashboardService;
use App\Support\CseExamDates;
use Illuminate\Support\Carbon;
use Inertia\Testing\AssertableInertia as Assert;

afterEach(fn () => Carbon::setTestNow());

function examStats(): array
{
    return app(DashboardService::class)->getExamDateStats();
}

test('dashboard counts down to the CSC March 14 2027 sitting with no DB row', function () {
    Carbon::setTestNow(Carbon::parse('2026-10-22 20:30', 'Asia/Manila'));
    $s = examStats();

    expect($s['examDateRaw'])->toBe('2027-03-14')
        ->and($s['examSource'])->toBe('csc')
        ->and($s['daysUntilExam'])->toBe(143)
        ->and($s['examDate'])->toBe('March 14, 2027')
        ->and($s['examSourceUrl'])->toBe(CseExamDates::ANNOUNCEMENT_URL)
        ->and(collect($s['examSittings'])->pluck('date')->all())->toBe(['2027-03-14', '2027-08-08'])
        ->and(collect($s['examMilestones'])->pluck('date')->all())->toBe(['2026-11-02', '2027-03-14', '2027-05-10', '2027-08-08']);
});

test('the November 22 2026 rescheduled exam and closing dates are never offered', function () {
    Carbon::setTestNow(Carbon::parse('2026-10-22 08:00', 'Asia/Manila'));
    $dates = collect(examStats()['examMilestones'])->pluck('date');

    expect($dates)->not->toContain('2026-11-22')
        ->and(collect(examStats()['examMilestones'])->pluck('label'))->not->toContain('Filing closes');
});

test('an outdated or stale active DB row cannot override the CSC calendar', function () {
    Carbon::setTestNow(Carbon::parse('2026-10-22 08:00', 'Asia/Manila'));
    ExamDate::create(['date' => '2026-08-09', 'description' => 'old', 'is_active' => true]);
    ExamDate::create(['date' => '2026-12-01', 'description' => 'arbitrary', 'is_active' => true]);

    expect(examStats()['examDateRaw'])->toBe('2027-03-14')
        ->and(examStats()['examSource'])->toBe('csc');
});

test('exam day stays the target until PH midnight, then rolls to August', function () {
    Carbon::setTestNow(Carbon::parse('2027-03-14 23:59:59', 'Asia/Manila'));
    expect(examStats()['examDateRaw'])->toBe('2027-03-14')
        ->and(examStats()['daysUntilExam'])->toBe(0);

    Carbon::setTestNow(Carbon::parse('2027-03-15 00:00:00', 'Asia/Manila'));
    expect(examStats()['examDateRaw'])->toBe('2027-08-08')
        ->and(collect(examStats()['examMilestones'])->first()['date'])->toBe('2027-05-10');
});

test('PH day is used even when the server clock is UTC', function () {
    // 2027-03-13 16:30 UTC is already 00:30 on exam day in Manila.
    Carbon::setTestNow(Carbon::parse('2027-03-13 16:30:00', 'UTC'));
    expect(examStats()['daysUntilExam'])->toBe(0);
});

test('after the last confirmed sitting it falls back only to a future admin date', function () {
    Carbon::setTestNow(Carbon::parse('2027-08-09 00:00', 'Asia/Manila'));
    expect(examStats()['examDateRaw'])->toBeNull()
        ->and(examStats()['examSittings'])->toBe([]);

    ExamDate::create(['date' => '2027-01-01', 'description' => 'expired', 'is_active' => true]);
    expect(examStats()['examDateRaw'])->toBeNull();

    ExamDate::create(['date' => '2027-12-01', 'description' => 'Admin set', 'is_active' => true]);
    expect(examStats()['examDateRaw'])->toBe('2027-12-01')
        ->and(examStats()['examSource'])->toBe('admin');
});

test('dashboard page carries the countdown data for users and guests', function () {
    Carbon::setTestNow(Carbon::parse('2026-10-22 08:00', 'Asia/Manila'));
    config(['civio.guest_unlimited' => true]);

    $this->withoutVite()->get(route('dashboard.index'))->assertInertia(fn (Assert $p) => $p
        ->where('stats.examDateRaw', '2027-03-14')
        ->has('stats.examSittings', 2));

    $this->actingAs(User::factory()->create())->withoutVite()->get(route('dashboard.index'))
        ->assertInertia(fn (Assert $p) => $p
            ->where('stats.examDateRaw', '2027-03-14')
            ->has('stats.examMilestones', 4));
});
