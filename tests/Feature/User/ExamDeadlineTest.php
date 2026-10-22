<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

function deadlineSession(?int $userId = null): ExamSession
{
    $sub = Subcategory::factory()->create([
        'category_id' => Category::factory()->create(['name' => 'Verbal Ability', 'is_demographic' => false])->id,
    ]);
    $ids = Question::factory()->count(3)->create([
        'subcategory_id' => $sub->id, 'status' => 'active',
        'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();

    return ExamSession::create([
        'user_id' => $userId, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => $ids,
        'started_at' => now(), 'deadline_at' => now()->addMinute(),
    ]);
}

function deadlineFinal(ExamSession $session, array $answers = []): array
{
    return ['exam_session_id' => $session->id, 'question_ids' => $session->question_ids, 'answers' => $answers];
}

test('a server-created strict session supplies an absolute authoritative start and deadline', function () {
    $user = User::factory()->create();
    deadlineSession($user->id)->update(['mode' => 'study']);
    $response = $this->actingAs($user)->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk();
    $session = ExamSession::findOrFail($response->json('session_id'));
    expect($session->started_at)->not->toBeNull()
        ->and((int) $session->started_at->diffInSeconds($session->deadline()))->toBe(11400)
        ->and($response->json('deadline_at'))->toBe($session->deadline()->toISOString());
    expect($response->json('questions.0'))->not->toHaveKeys(['correct_option', 'explanation']);
});

test('only the owner can read or save versioned progress', function () {
    $owner = User::factory()->create();
    $session = deadlineSession($owner->id);
    $payload = ['exam_session_id' => $session->id];
    $this->actingAs(User::factory()->create())->postJson(route('exams.sessions.progress'), $payload)->assertNotFound();
    $this->actingAs($owner)->postJson(route('exams.sessions.progress'), $payload)->assertOk()
        ->assertJson(['save_version' => 0])->assertJsonMissingPath('correct_option')
        ->assertHeader('Cache-Control', 'no-store, private');
    $this->postJson(route('exams.sessions.progress'), [
        ...$payload, 'answers' => [$session->question_ids[0] => 1], 'expected_version' => 0,
    ])->assertOk()->assertJson(['save_version' => 1]);
    expect($session->fresh()->saved_answers)->toBe([$session->question_ids[0] => 1]);
});

test('guest progress requires the owning browser and remains usable after signing in', function () {
    $session = deadlineSession();
    $payload = ['exam_session_id' => $session->id];
    $this->postJson(route('exams.sessions.progress'), $payload)->assertNotFound();
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]])
        ->postJson(route('exams.sessions.progress'), $payload)->assertOk();
    $this->actingAs(User::factory()->create())->postJson(route('exams.sessions.progress'), [
        ...$payload, 'answers' => [$session->question_ids[0] => 1], 'expected_version' => 0,
    ])->assertOk();
});

test('stale progress patches cannot overwrite a newer answer and clears are persisted', function () {
    $session = deadlineSession();
    $payload = ['exam_session_id' => $session->id, 'expected_version' => 0];
    $id = $session->question_ids[0];
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    $this->postJson(route('exams.sessions.progress'), [...$payload, 'answers' => [$id => 1]])->assertOk();
    $this->postJson(route('exams.sessions.progress'), [...$payload, 'answers' => [$id => 0]])->assertConflict();
    expect($session->fresh()->saved_answers)->toBe([$id => 1]);
    $this->postJson(route('exams.sessions.progress'), [...$payload, 'expected_version' => 1, 'answers' => [$id => null]])->assertOk();
    expect($session->fresh()->saved_answers)->toBe([$id => null]);
});

test('progress rejects unserved and invalid-option patches, and an inactive-only patch changes nothing', function () {
    $session = deadlineSession();
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    $payload = ['exam_session_id' => $session->id, 'expected_version' => 0];
    foreach ([[999999 => 0], [$session->question_ids[0] => 7], ['01' => 0]] as $answers) {
        $this->postJson(route('exams.sessions.progress'), [...$payload, 'answers' => $answers])->assertUnprocessable();
    }
    Question::whereKey($session->question_ids[0])->update(['status' => 'draft']);
    $this->postJson(route('exams.sessions.progress'), [...$payload, 'answers' => [$session->question_ids[0] => 1]])
        ->assertOk()->assertJson(['withdrawn_ids' => [$session->question_ids[0]], 'save_version' => 0]);
    expect($session->fresh()->save_version)->toBe(0)->and($session->fresh()->saved_answers)->toBeNull();
});

test('late final submission grades only previously saved answers over the complete served set', function (bool $guest) {
    $user = $guest ? null : User::factory()->create();
    $session = deadlineSession($user?->id);
    if ($user) {
        $this->actingAs($user);
    } else {
        $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    }
    $id = $session->question_ids[0];
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'expected_version' => 0, 'answers' => [$id => 1],
    ])->assertOk();
    $this->travel(61)->seconds();
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'expected_version' => 1, 'answers' => [$id => 0],
    ])->assertConflict();
    $this->postJson(route('exams.attempts.store'), deadlineFinal($session, array_fill_keys($session->question_ids, 0)))
        ->assertOk()->assertJson(['score' => 33, 'total_questions' => 3, 'skipped_count' => 2,
            'cat_scores' => ['metadata' => ['submitted_after_deadline' => true, 'is_timed' => true]]]);
    expect(ExamAttempt::first()->answers[$id])->toBe(1);
    $this->postJson(route('exams.attempts.store'), deadlineFinal($session))->assertConflict();
})->with([true, false]);

test('the deadline is exclusive and grace never accepts an answer change', function () {
    $session = deadlineSession();
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    $this->travelTo($session->deadline());
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'expected_version' => 0,
        'answers' => [$session->question_ids[0] => 1],
    ])->assertConflict();
    $this->postJson(route('exams.reveal'), ['question_id' => $session->question_ids[0]])->assertStatus(423);
    $this->travel(11)->minutes();
    $this->postJson(route('exams.reveal'), ['question_id' => $session->question_ids[0]])->assertOk();
    $this->postJson(route('exams.attempts.store'), deadlineFinal($session, array_fill_keys($session->question_ids, 1)))
        ->assertOk()->assertJson(['score' => 0, 'skipped_count' => 3]);
});

test('submitted progress is immutable and an on-time final accepts the latest complete answers', function () {
    $session = deadlineSession();
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    $this->postJson(route('exams.attempts.store'), deadlineFinal($session, array_fill_keys($session->question_ids, 1)))
        ->assertOk()->assertJson(['score' => 100]);
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'expected_version' => 0,
        'answers' => [$session->question_ids[0] => 0],
    ])->assertConflict();
    $this->postJson(route('exams.sessions.progress'), ['exam_session_id' => $session->id])
        ->assertOk()->assertJson(['submitted' => true]);
});

test('another strict mock cannot overlap an open strict mock but Study stays available', function (bool $guest) {
    $user = $guest ? null : User::factory()->create();
    $seed = deadlineSession($user?->id);
    $seed->update(['mode' => 'study']);
    if ($user) {
        $this->actingAs($user);
    }
    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk();
    $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertConflict();
    $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'study'])->assertOk();
    $this->postJson(route('exams.reveal'), ['question_id' => $start->json('questions.0.id')])->assertStatus(423);
})->with([true, false]);

test('later guest Study sessions cannot evict the Strict Mock answer lock or its ownership', function () {
    deadlineSession()->update(['mode' => 'study']);
    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk();
    for ($i = 0; $i < 21; $i++) {
        $this->postJson(route('exams.sessions.store'), ['track' => 'Professional'])->assertOk();
    }
    $this->postJson(route('exams.reveal'), ['question_id' => $start->json('questions.0.id')])->assertStatus(423);
    $this->actingAs(User::factory()->create());
    $this->postJson(route('exams.reveal'), ['question_id' => $start->json('questions.0.id')])->assertStatus(423);
    $this->postJson(route('exams.sessions.progress'), ['exam_session_id' => $start->json('session_id')])->assertOk();
});

test('even an empty progress patch requires a revision and integer inputs are canonicalized', function () {
    $session = deadlineSession();
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]]);
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'answers' => [],
    ])->assertUnprocessable()->assertJsonValidationErrors('expected_version');
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'answers' => [$session->question_ids[0] => '1'], 'expected_version' => '0',
    ])->assertOk();
    expect($session->fresh()->saved_answers)->toBe([$session->question_ids[0] => 1]);
});

test('a patch mixing active and retired answers saves the active ones and reports the retired one', function () {
    $user = User::factory()->create();
    $session = deadlineSession($user->id);
    [$a, $b, $retired] = $session->question_ids;
    Question::whereKey($retired)->update(['status' => 'retired']);

    $this->actingAs($user)->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'answers' => [$a => 1, $b => 0, $retired => 2], 'expected_version' => 0,
    ])->assertOk()->assertJson(['save_version' => 1, 'withdrawn_ids' => [$retired]])
        ->assertJsonMissingPath('correct_option');
    expect($session->fresh()->saved_answers)->toBe([$a => 1, $b => 0]);

    // Resending the same mixed patch does not 422-loop either.
    $this->postJson(route('exams.sessions.progress'), [
        'exam_session_id' => $session->id, 'answers' => [$a => 2, $retired => 2], 'expected_version' => 1,
    ])->assertOk()->assertJson(['save_version' => 2, 'withdrawn_ids' => [$retired]]);
    expect($session->fresh()->saved_answers)->toBe([$a => 2, $b => 0]);
});

test('an expired strict mock with a retired item still grades the saved answers', function () {
    $user = User::factory()->create();
    $session = deadlineSession($user->id);
    [$a, $b, $retired] = $session->question_ids;
    $session->forceFill(['saved_answers' => [$a => 1, $b => 1, $retired => 1], 'save_version' => 1])->save();
    Question::whereKey($retired)->update(['status' => 'retired']);
    $this->travel(2)->minutes();

    $this->actingAs($user)->postJson(route('exams.attempts.store'), deadlineFinal($session))->assertOk();

    $attempt = ExamAttempt::where('user_id', $user->id)->latest('id')->firstOrFail();
    expect($session->fresh()->exam_attempt_id)->toBe($attempt->id)
        ->and($attempt->cat_scores['metadata']['retired_count'])->toBe(1);
});

test('an on-time submit that still carries an answer to a retired item grades the rest once', function () {
    $user = User::factory()->create();
    $session = deadlineSession($user->id);
    [$a, $b, $retired] = $session->question_ids;
    Question::whereKey($retired)->update(['status' => 'retired']);

    $this->actingAs($user)->postJson(route('exams.attempts.store'), deadlineFinal($session, [$a => 1, $b => 0, $retired => 1]))
        ->assertOk();
    $this->postJson(route('exams.attempts.store'), deadlineFinal($session, [$a => 1, $b => 1]))->assertConflict();

    $attempt = ExamAttempt::where('user_id', $user->id)->sole();
    expect(array_keys(array_filter($attempt->answers, fn ($a) => $a !== null)))->not->toContain($retired)
        ->and($attempt->cat_scores['metadata']['retired_count'])->toBe(1)
        ->and($session->fresh()->isOpen())->toBeFalse();
    $this->postJson(route('exams.sessions.progress'), ['exam_session_id' => $session->id])
        ->assertOk()->assertJson(['submitted' => true]);
});

test('the submit response reports withdrawn items so the scorecard can explain them', function () {
    $user = User::factory()->create();
    $session = deadlineSession($user->id);
    [$a, $b, $retired] = $session->question_ids;
    Question::whereKey($retired)->update(['status' => 'retired']);

    $this->actingAs($user)->postJson(route('exams.attempts.store'), deadlineFinal($session, [$a => 1, $b => 1]))
        ->assertOk()
        ->assertJson(['retired_count' => 1, 'total_questions' => 2, 'skipped_count' => 0, 'wrong_count' => 0, 'score' => 100])
        ->assertJson(['retired_ids' => [$retired]])
        ->assertJsonMissing(['id' => $retired]);

    $attempt = ExamAttempt::where('user_id', $user->id)->sole();
    $this->withoutVite()->get(route('exams.index', ['attempt_id' => $attempt->id]))
        ->assertOk()
        ->assertInertia(fn ($page) => $page->where('questions', function ($questions) use ($retired) {
            // A reopened scorecard never ships the withdrawn item or its key.
            expect(collect($questions)->pluck('id')->all())->not->toContain($retired);

            return true;
        }));
});
