<?php

use App\Models\User;
use App\Support\LiteMode;
use Inertia\Testing\AssertableInertia as Assert;

beforeEach(function () {
    config(['broadcasting.connections.pusher.key' => 'test-key']);
});

test('without the lite cookie the full props are sent', function () {
    $this->actingAs(User::factory()->create());

    $this->withoutVite()->get(route('dashboard.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->where('civio.lite', false)
            ->where('pusher.key', 'test-key')
            ->has('aiAnalysis')
        );
});

test('the lite cookie defers the dashboard analysis and drops realtime config', function () {
    $this->actingAs(User::factory()->create());

    $this->withoutVite()
        ->withUnencryptedCookie(LiteMode::COOKIE, '1')
        ->get(route('dashboard.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->where('civio.lite', true)
            ->where('pusher.key', null)
            ->missing('aiAnalysis')
            ->has('dailyGoal')
            ->loadDeferredProps(fn (Assert $reload) => $reload->has('aiAnalysis'))
        );
});

test('the lite cookie trims chart-only analytics data and defers the analysis', function () {
    $this->actingAs(User::factory()->create());

    $this->withoutVite()
        ->withUnencryptedCookie(LiteMode::COOKIE, '1')
        ->get(route('analytics.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->has('stats')
            ->missing('stats.attemptBreakdowns')
            ->missing('aiAnalysis')
        );
});

test('the exam page defers its analysis in lite', function () {
    $this->actingAs(User::factory()->create());

    $this->withoutVite()
        ->withUnencryptedCookie(LiteMode::COOKIE, '1')
        ->get(route('exams.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->where('questions', [])
            ->missing('aiAnalysis')
        );
});

test('trimAnalyticsStats removes per-attempt and per-category chart series only', function () {
    $trimmed = LiteMode::trimAnalyticsStats([
        'totalAttempts' => 3,
        'attemptBreakdowns' => [['x' => 1]],
        'chartData' => [['date' => 'Oct 1', 'score' => 80, 'categoryScores' => ['Verbal' => 70]]],
    ]);

    expect($trimmed)->toBe([
        'totalAttempts' => 3,
        'chartData' => [['date' => 'Oct 1', 'score' => 80]],
    ]);
});
