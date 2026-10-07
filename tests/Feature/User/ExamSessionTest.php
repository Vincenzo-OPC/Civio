<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

/**
 * Seed a small Professional bank: every blueprint category with a few items,
 * plus one variant clone and one demographic item that must never be served.
 *
 * @return array{ids: array<int, int>, clone: int, demographic: int}
 */
function seedMockBank(int $perCategory = 6): array
{
    $author = User::factory()->create();
    $ids = [];

    foreach (['Verbal Ability', 'Analytical Ability', 'Numerical Ability', 'General Information'] as $name) {
        $category = Category::factory()->create(['name' => $name, 'is_demographic' => false]);
        $sub = Subcategory::factory()->create(['category_id' => $category->id, 'name' => $name.' basics']);

        for ($i = 0; $i < $perCategory; $i++) {
            $ids[] = Question::factory()->create([
                'subcategory_id' => $sub->id,
                'created_by' => $author->id,
                'status' => 'active',
                'stem' => "{$name} item {$i}: pick the best answer for this one?",
                'options' => ["A {$name} {$i}", "B {$name} {$i}", "C {$name} {$i}", "D {$name} {$i}"],
                'correct_option' => 2,
                'explanation' => 'Because C.',
            ])->id;
        }
    }

    $first = Question::findOrFail($ids[0]);
    $clone = Question::factory()->create([
        'subcategory_id' => $first->subcategory_id,
        'created_by' => $author->id,
        'status' => 'active',
        'stem' => $first->stem.' (variant 2)',
    ])->id;

    $demoCategory = Category::factory()->create(['name' => 'Demographic Profile', 'is_demographic' => true]);
    $demoSub = Subcategory::factory()->create(['category_id' => $demoCategory->id, 'name' => 'Age']);
    $demographic = Question::factory()->create([
        'subcategory_id' => $demoSub->id,
        'created_by' => $author->id,
        'status' => 'active',
    ])->id;

    return ['ids' => $ids, 'clone' => $clone, 'demographic' => $demographic];
}

test('starting a mock sends only the picked items, without keys, and stores their IDs', function () {
    $bank = seedMockBank();

    $response = $this->postJson(route('exams.sessions.store'), ['track' => 'professional']);

    $response->assertOk()->assertJson(['success' => true, 'track' => 'Professional', 'target' => 150, 'short' => true]);

    $questions = collect($response->json('questions'));
    expect($questions)->toHaveCount(24);

    foreach ($questions as $q) {
        expect($q)->not->toHaveKey('correct_option')
            ->and($q)->not->toHaveKey('explanation')
            ->and($q)->toHaveKeys(['id', 'stem', 'options']);
    }

    $servedIds = $questions->pluck('id')->all();
    expect($servedIds)->not->toContain($bank['clone'])
        ->and($servedIds)->not->toContain($bank['demographic'])
        ->and(array_unique($servedIds))->toHaveCount(24);

    $session = ExamSession::findOrFail($response->json('session_id'));
    expect($session->question_ids)->toBe($servedIds)
        ->and($session->user_id)->toBeNull()
        ->and($response->json('notice'))->toContain('This Professional mock has 24 items, not 150.');
});

test('a mock session can be submitted once, only for the items it served', function () {
    seedMockBank(3);
    $user = User::factory()->create();
    $this->actingAs($user);

    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional'])->assertOk();
    $sessionId = $start->json('session_id');
    $ids = collect($start->json('questions'))->pluck('id')->all();

    $payload = fn (array $questionIds) => [
        'exam_session_id' => $sessionId,
        'question_ids' => $questionIds,
        'answers' => collect($questionIds)->mapWithKeys(fn ($id) => [(string) $id => 2])->all(),
        'metadata' => ['track' => 'Professional', 'duration_secs' => 60, 'is_timed' => true],
    ];

    // An item the server never served is rejected.
    $outsider = Question::factory()->create(['status' => 'active'])->id;
    $this->postJson(route('exams.attempts.store'), $payload([...$ids, $outsider]))->assertStatus(422);

    $ok = $this->postJson(route('exams.attempts.store'), $payload($ids))->assertOk();
    expect($ok->json('score'))->toBe(100);
    expect(ExamSession::findOrFail($sessionId)->exam_attempt_id)->toBe($ok->json('attempt_id'));

    // Replaying the same mock is refused.
    $this->postJson(route('exams.attempts.store'), $payload($ids))->assertStatus(409);
    expect(ExamAttempt::count())->toBe(1);
});

test('someone else cannot submit against your mock session', function () {
    seedMockBank(3);
    $owner = User::factory()->create();
    $start = $this->actingAs($owner)->postJson(route('exams.sessions.store'), ['track' => 'Professional'])->assertOk();
    $ids = collect($start->json('questions'))->pluck('id')->all();

    $this->actingAs(User::factory()->create())->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $start->json('session_id'),
        'question_ids' => $ids,
        'answers' => collect($ids)->mapWithKeys(fn ($id) => [(string) $id => 2])->all(),
        'metadata' => ['track' => 'Professional', 'duration_secs' => 60, 'is_timed' => true],
    ])->assertStatus(422)->assertJson(['message' => 'This mock session was not found for you. Start a new mock.']);
});

test('an empty bank gives no items and a clear notice', function () {
    $this->postJson(route('exams.sessions.store'), ['track' => 'subprofessional'])
        ->assertOk()
        ->assertJson([
            'track' => 'Subprofessional',
            'short' => true,
            'questions' => [],
            'notice' => "No Subprofessional practice items are available right now, so a mock can't start.",
        ]);
});

test('track is validated', function () {
    $this->postJson(route('exams.sessions.store'), ['track' => 'drill'])->assertStatus(422);
});

test('a guest can submit the mock their own browser session started', function () {
    seedMockBank(3);
    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional'])->assertOk();
    $ids = collect($start->json('questions'))->pluck('id')->all();

    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $start->json('session_id'),
        'question_ids' => $ids,
        'answers' => collect($ids)->mapWithKeys(fn ($id) => [(string) $id => 0])->all(),
        'metadata' => ['track' => 'Professional', 'duration_secs' => 60, 'is_timed' => true],
    ])->assertOk()->assertJson(['score' => 0]);
});
