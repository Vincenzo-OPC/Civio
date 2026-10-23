<?php

use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\User;
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Support\Facades\DB;

/**
 * Issue #26: civio:prune-exam-sessions. Every row is placed in time with a
 * raw update so Eloquent timestamps cannot hide the age being tested.
 */
function pruneSession(array $attrs = [], ?int $ageDays = 60, ?int $updatedDays = null): ExamSession
{
    $session = ExamSession::query()->create(array_merge([
        'track' => 'professional',
        'mode' => 'study',
        'question_ids' => [1, 2, 3],
    ], $attrs));

    if ($ageDays !== null) {
        DB::table('exam_sessions')->where('id', $session->id)->update([
            'created_at' => now()->subDays($ageDays),
            'updated_at' => now()->subDays($updatedDays ?? $ageDays),
        ]);
    }

    return $session;
}

beforeEach(fn () => config()->set('civio.prune_exam_sessions', [
    'retention_days' => 45, 'min_days' => 31, 'max_days' => 365, 'batch_size' => 500,
]));

it('deletes an abandoned guest session older than 45 days', function () {
    $old = pruneSession(ageDays: 46);

    $this->artisan('civio:prune-exam-sessions')
        ->expectsOutputToContain('Deleted 1 abandoned exam session(s) older than 45 days.')
        ->assertSuccessful();

    expect(ExamSession::find($old->id))->toBeNull();
});

it('keeps sessions inside the 30-day study recovery window and the 45-day margin', function () {
    $fresh = pruneSession(ageDays: 29);
    $edge = pruneSession(ageDays: 44);

    $this->artisan('civio:prune-exam-sessions')->assertSuccessful();

    expect(ExamSession::find($fresh->id))->not->toBeNull()
        ->and(ExamSession::find($edge->id))->not->toBeNull();
});

it('uses last activity, not creation time', function () {
    $resumed = pruneSession(ageDays: 120, updatedDays: 10);
    $started = pruneSession(['started_at' => now()->subDays(5)], ageDays: 120);

    $this->artisan('civio:prune-exam-sessions')->assertSuccessful();

    expect(ExamSession::find($resumed->id))->not->toBeNull()
        ->and(ExamSession::find($started->id))->not->toBeNull();
});

it('never deletes a session linked to a submitted attempt, nor the attempt', function () {
    $attempt = ExamAttempt::create(['user_id' => User::factory()->create()->id, 'question_ids' => [1], 'answers' => [], 'cat_scores' => []]);
    $linked = pruneSession(['exam_attempt_id' => $attempt->id], ageDays: 400);

    $this->artisan('civio:prune-exam-sessions', ['--days' => 31])->assertSuccessful();

    expect(ExamSession::find($linked->id))->not->toBeNull()
        ->and(ExamAttempt::find($attempt->id))->not->toBeNull();
});

it('keeps learner-owned sessions because exposure history depends on them', function () {
    $user = User::factory()->create();
    $owned = pruneSession(['user_id' => $user->id], ageDays: 400);

    $this->artisan('civio:prune-exam-sessions')->assertSuccessful();

    expect(ExamSession::find($owned->id))->not->toBeNull();
});

it('never deletes an active or unexpired Strict Mock session', function () {
    $running = pruneSession(['mode' => 'strict', 'started_at' => now()->subMinutes(5), 'deadline_at' => now()->addHours(2)], ageDays: null);
    $futureDeadline = pruneSession(['mode' => 'strict', 'deadline_at' => now()->addDay()], ageDays: 90);
    $recentDeadline = pruneSession(['mode' => 'strict', 'deadline_at' => now()->subDays(10)], ageDays: 90);
    $expiredLongAgo = pruneSession(['mode' => 'strict', 'started_at' => now()->subDays(90), 'deadline_at' => now()->subDays(90)], ageDays: 90);

    $this->artisan('civio:prune-exam-sessions')->assertSuccessful();

    expect(ExamSession::find($running->id))->not->toBeNull()
        ->and(ExamSession::find($futureDeadline->id))->not->toBeNull()
        ->and(ExamSession::find($recentDeadline->id))->not->toBeNull()
        ->and(ExamSession::find($expiredLongAgo->id))->toBeNull();
});

it('does not change anything on a dry run and reports the real count', function () {
    pruneSession(ageDays: 60);
    pruneSession(ageDays: 70);
    pruneSession(ageDays: 5);

    $this->artisan('civio:prune-exam-sessions', ['--dry-run' => true])
        ->expectsOutputToContain('Dry run: 2 abandoned exam session(s) older than 45 days would be deleted.')
        ->assertSuccessful();

    expect(ExamSession::count())->toBe(3);
});

it('is idempotent', function () {
    pruneSession(ageDays: 60);
    $keep = pruneSession(ageDays: 5);

    $this->artisan('civio:prune-exam-sessions')->expectsOutputToContain('Deleted 1 ')->assertSuccessful();
    $this->artisan('civio:prune-exam-sessions')->expectsOutputToContain('Deleted 0 ')->assertSuccessful();

    expect(ExamSession::pluck('id')->all())->toBe([$keep->id]);
});

it('deletes in bounded batches until done', function () {
    config()->set('civio.prune_exam_sessions.batch_size', 2);
    foreach (range(1, 5) as $i) {
        pruneSession(ageDays: 50 + $i);
    }
    $keep = pruneSession(ageDays: 1);

    $queries = 0;
    DB::listen(function ($q) use (&$queries) {
        if (str_starts_with(strtolower($q->sql), 'delete')) {
            $queries++;
        }
    });

    $this->artisan('civio:prune-exam-sessions')->expectsOutputToContain('Deleted 5 ')->assertSuccessful();

    expect($queries)->toBe(3)
        ->and(ExamSession::pluck('id')->all())->toBe([$keep->id]);
});

it('clamps --days below the 31-day floor so the recovery window is protected', function () {
    $day32 = pruneSession(ageDays: 32);
    $day20 = pruneSession(ageDays: 20);

    $this->artisan('civio:prune-exam-sessions', ['--days' => 1])
        ->expectsOutputToContain('using 31')
        ->assertSuccessful();

    expect(ExamSession::find($day20->id))->not->toBeNull()
        ->and(ExamSession::find($day32->id))->toBeNull();
});

it('clamps env retention to the bounds and above the maximum', function () {
    config()->set('civio.prune_exam_sessions.retention_days', 5);
    config()->set('civio.prune_exam_sessions.min_days', 1);
    $day20 = pruneSession(ageDays: 20);

    $this->artisan('civio:prune-exam-sessions')->expectsOutputToContain('using 31')->assertSuccessful();
    expect(ExamSession::find($day20->id))->not->toBeNull();

    $day400 = pruneSession(ageDays: 400);
    $day300 = pruneSession(ageDays: 300);
    $this->artisan('civio:prune-exam-sessions', ['--days' => 9999])->expectsOutputToContain('using 365')->assertSuccessful();
    expect(ExamSession::find($day300->id))->not->toBeNull()
        ->and(ExamSession::find($day400->id))->toBeNull();
});

it('rejects a non-numeric --days', function () {
    pruneSession(ageDays: 60);

    $this->artisan('civio:prune-exam-sessions', ['--days' => 'abc'])->assertFailed();

    expect(ExamSession::count())->toBe(1);
});

it('leaves bank questions and attempts untouched', function () {
    $question = Question::factory()->create();
    $attempt = ExamAttempt::create(['user_id' => User::factory()->create()->id, 'question_ids' => [1], 'answers' => [], 'cat_scores' => []]);
    pruneSession(ageDays: 90);

    $this->artisan('civio:prune-exam-sessions')->assertSuccessful();

    expect(Question::find($question->id))->not->toBeNull()
        ->and(ExamAttempt::find($attempt->id))->not->toBeNull();
});

it('is scheduled daily in the Laravel scheduler', function () {
    $event = collect(app(Schedule::class)->events())
        ->first(fn ($e) => str_contains((string) $e->command, 'civio:prune-exam-sessions'));

    expect($event)->not->toBeNull()
        ->and($event->expression)->toBe('30 3 * * *');
});
