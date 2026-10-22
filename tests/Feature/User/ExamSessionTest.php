<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Repositories\QuestionRepositoryInterface;
use App\Services\Exam\MockPoolSelector;
use App\Services\Exam\MockSessionService;
use App\Services\ExamAttemptFormatter;
use App\Services\Learning\LearningInsightsService;
use Random\Engine\Xoshiro256StarStar;
use Random\Randomizer;

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

test('a mock defaults to study mode and reveal works mid-mock', function () {
    seedMockBank(3);
    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional'])
        ->assertOk()->assertJson(['mode' => 'study', 'time_limit_secs' => 11400]);
    $id = $start->json('questions.0.id');

    expect(ExamSession::findOrFail($start->json('session_id'))->mode->value)->toBe('study');
    $this->postJson(route('exams.reveal'), ['question_id' => $id])->assertOk()->assertJson(['correct_option' => 2]);
    $this->postJson(route('exams.expound'), ['question_id' => $id])->assertOk();
});

test('mode is validated', function () {
    $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'easy'])->assertStatus(422);
});

test('a strict mock locks reveal and expound on the server until submit', function () {
    seedMockBank(3);
    $user = User::factory()->create();
    $this->actingAs($user);

    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Subprofessional', 'mode' => 'strict'])
        ->assertOk()->assertJson(['mode' => 'strict', 'time_limit_secs' => 9600]);
    $ids = collect($start->json('questions'))->pluck('id')->all();

    $this->postJson(route('exams.reveal'), ['question_id' => $ids[0]])
        ->assertStatus(423)->assertJsonMissingPath('correct_option')->assertJson(['locked' => true]);
    $this->postJson(route('exams.expound'), ['question_id' => $ids[0]])
        ->assertStatus(423)->assertJsonMissingPath('explanation');

    // Another learner is not locked out of the same item.
    $this->actingAs(User::factory()->create())
        ->postJson(route('exams.reveal'), ['question_id' => $ids[0]])->assertOk();

    $this->actingAs($user)->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $start->json('session_id'),
        'question_ids' => $ids,
        'answers' => collect($ids)->mapWithKeys(fn ($id) => [(string) $id => 2])->all(),
        'metadata' => ['track' => 'Subprofessional', 'duration_secs' => 60, 'is_timed' => true],
    ])->assertOk();

    expect(ExamAttempt::firstOrFail()->mode->value)->toBe('strict');
    $this->postJson(route('exams.reveal'), ['question_id' => $ids[0]])->assertOk()->assertJson(['correct_option' => 2]);
});

test('a guest strict mock is locked for that browser session', function () {
    seedMockBank(3);
    $start = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk();

    $this->postJson(route('exams.reveal'), ['question_id' => $start->json('questions.0.id')])->assertStatus(423);
});

test('an abandoned strict mock stops locking after its time limit plus grace', function () {
    seedMockBank(3);
    $user = User::factory()->create();
    $start = $this->actingAs($user)->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk();

    $this->travel(11400 + 601)->seconds();

    $this->postJson(route('exams.reveal'), ['question_id' => $start->json('questions.0.id')])->assertOk();
});

/*
 * ADR-0002: Strict is representative, Study is adaptive. The policy is
 * derived on the server and stored with a version on the session and attempt.
 * Route controllers are cached per test, so the service is called directly
 * with a fresh seeded selector for each start.
 */
function startSeeded(int $seed, ?int $userId, string $mode, array $clientBias = []): array
{
    $service = new MockSessionService(
        app(QuestionRepositoryInterface::class),
        app(ExamAttemptFormatter::class),
        new MockPoolSelector(new Randomizer(new Xoshiro256StarStar($seed))),
    );

    return $service->start($userId, 'Professional', $clientBias, null, ExamMode::from($mode));
}

test('strict: wrong history and client weak lists change nothing for the same bank and seed', function () {
    seedMockBank(60);
    $user = User::factory()->create();

    $before = startSeeded(17, $user->id, 'strict');
    ExamSession::query()->delete();

    $wrong = array_slice(Question::pluck('id')->all(), 0, 80);
    ExamAttempt::create(['user_id' => $user->id, 'mode' => 'study', 'question_ids' => $wrong,
        'answers' => array_fill_keys(array_map('strval', $wrong), 0), 'cat_scores' => []]);

    $after = startSeeded(17, $user->id, 'strict', [
        'wrong_ids' => $wrong, 'weak_subcategories' => ['Numerical Ability basics'], 'weak_categories' => ['Numerical Ability'],
    ]);

    expect(array_column($after['questions'], 'id'))->toBe(array_column($before['questions'], 'id'))
        ->and($after['selection_policy'])->toBe('representative')
        ->and($after['selection_policy_version'])->toBe(MockPoolSelector::POLICY_VERSION)
        ->and(ExamSession::firstOrFail()->selection_policy->value)->toBe('representative');
});

test('study stays adaptive: wrong items are favoured compared with strict on the same seed', function () {
    seedMockBank(60);
    $wrong = array_slice(Question::pluck('id')->all(), 60, 40);

    $study = array_column(startSeeded(17, null, 'study', ['wrong_ids' => $wrong])['questions'], 'id');
    $strict = array_column(startSeeded(17, null, 'strict', ['wrong_ids' => $wrong])['questions'], 'id');

    expect(count(array_intersect($wrong, $study)))->toBeGreaterThan(count(array_intersect($wrong, $strict)));
});

test('the attempt records the policy and version, and insights count legacy strict mocks apart', function () {
    seedMockBank(3);
    $user = User::factory()->create();
    $start = $this->actingAs($user)->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])
        ->assertOk()->assertJson(['selection_policy' => 'representative']);
    $ids = $start->json('questions.*.id');

    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $start->json('session_id'),
        'question_ids' => $ids,
        'answers' => collect($ids)->mapWithKeys(fn ($id) => [(string) $id => 2])->all(),
        'metadata' => ['track' => 'Professional', 'duration_secs' => 60, 'is_timed' => true],
    ])->assertOk();

    $attempt = ExamAttempt::where('user_id', $user->id)->firstOrFail();
    expect($attempt->selection_policy->value)->toBe('representative')
        ->and($attempt->selection_policy_version)->toBe(MockPoolSelector::POLICY_VERSION);

    ExamAttempt::create(['user_id' => $user->id, 'mode' => 'strict', 'question_ids' => $ids, 'answers' => [], 'cat_scores' => []]);

    expect(app(LearningInsightsService::class)->forUser($user->id)['strictMockPolicies'])
        ->toBe(['representative' => 1, 'legacy' => 1]);
});

test('a strict mock payload carries no keys, explanations or misconception codes before submit', function () {
    seedMockBank(3);
    Question::query()->update(['archetype' => 'NUM-WP-PCT-CHANGE', 'distractor_codes' => json_encode(['0' => 'NUM-WRONG-BASE'])]);
    $this->actingAs(User::factory()->create());

    $body = $this->postJson(route('exams.sessions.store'), ['track' => 'Professional', 'mode' => 'strict'])->assertOk()->getContent();

    expect($body)->not->toContain('correct_option')
        ->and($body)->not->toContain('distractor_codes')
        ->and($body)->not->toContain('NUM-WRONG-BASE')
        ->and($body)->not->toContain('Because C.');
});
