<?php

use App\Actions\Exam\SubmitExamAttemptAction;
use App\DTOs\Exam\SubmitExamAttemptData;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;
use App\Repositories\QuestionRepositoryInterface;
use App\Services\ExamGradingService;
use Inertia\Testing\AssertableInertia as Assert;

function securityItems(int $count = 3): array
{
    return Question::factory()->count($count)->create([
        'subcategory_id' => Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id])->id, 'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();
}

function securitySubmission(array $ids, ?string $session = null): array
{
    return [
        'exam_session_id' => $session, 'question_ids' => $ids,
        'answers' => array_fill_keys($ids, 1), 'metadata' => ['track' => 'Professional'],
    ];
}

test('arbitrary sessionless ids cannot extract keys or create an attempt', function () {
    $ids = securityItems();
    $this->postJson(route('exams.attempts.store'), securitySubmission($ids))
        ->assertUnprocessable()->assertJsonMissingPath('answer_keys');
    expect(ExamAttempt::count())->toBe(0);
});

test('served practice membership belongs to the browser and principal and expires', function () {
    $ids = securityItems();
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true']))->assertOk();
    $outside = securityItems(1);
    $this->postJson(route('exams.attempts.store'), securitySubmission($outside))->assertUnprocessable();
    $this->actingAs(User::factory()->create())->postJson(route('exams.attempts.store'), securitySubmission($ids))->assertUnprocessable();
    $this->actingAs($user);
    $this->travel(25)->hours();
    $this->postJson(route('exams.attempts.store'), securitySubmission($ids))->assertUnprocessable();
});

test('served drill answers remain server graded and cannot claim mock metadata', function () {
    $ids = securityItems();
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true']))->assertOk();
    $response = $this->postJson(route('exams.attempts.store'), securitySubmission($ids))->assertOk();
    $response->assertJson(['score' => 100, 'total_questions' => 3, 'cat_scores' => ['metadata' => ['track' => 'Drill']]]);
    expect($response->json('answer_keys'))->toHaveCount(3);
});

test('a partial mock grades the complete served set and blanks cannot become a perfect score', function () {
    $ids = securityItems();
    $user = User::factory()->create();
    $session = ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => $ids]);
    $response = $this->actingAs($user)->postJson(route('exams.attempts.store'), securitySubmission([$ids[0]], $session->id))->assertOk();
    $response->assertJson(['score' => 33, 'total_questions' => 3, 'correct_count' => 1, 'skipped_count' => 2]);
    expect(ExamAttempt::first()->question_ids)->toBe($ids);
});

test('a guest mock can be submitted entirely blank against its complete denominator', function () {
    $ids = securityItems();
    $session = ExamSession::create(['track' => 'Professional', 'question_ids' => $ids]);
    $this->withSession([ExamSession::GUEST_SESSION_KEY => [$session->id]])->postJson(route('exams.attempts.store'), [
        ...securitySubmission($ids, $session->id), 'answers' => [],
    ])->assertOk()->assertJson(['score' => 0, 'total_questions' => 3, 'skipped_count' => 3]);
});

test('a stale loaded session cannot create a duplicate attempt', function () {
    $ids = securityItems();
    $user = User::factory()->create();
    $session = ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'question_ids' => $ids]);
    $stale = ExamSession::find($session->id);
    $data = new SubmitExamAttemptData(null, $ids, array_fill_keys($ids, 1));
    $action = app(SubmitExamAttemptAction::class);
    expect($action->execute($data, $user->id, examSession: $session)->success)->toBeTrue()
        ->and($action->execute($data, $user->id, examSession: $stale)->statusCode)->toBe(409)
        ->and(ExamAttempt::count())->toBe(1);
});

test('locked items cannot be graded through another study session or a served drill', function () {
    $ids = securityItems();
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true']))->assertOk();
    $study = ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'question_ids' => $ids]);
    ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => $ids]);
    foreach ([null, $study->id] as $session) {
        $this->postJson(route('exams.attempts.store'), securitySubmission($ids, $session))
            ->assertStatus(423)->assertJsonMissingPath('answer_keys');
    }
    expect(ExamAttempt::count())->toBe(0);
});

test('inactive served items fail closed at submission reveal expound and grading', function () {
    $ids = securityItems();
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true']))->assertOk();
    Question::whereKey($ids[0])->update(['status' => 'draft']);
    $this->postJson(route('exams.attempts.store'), securitySubmission($ids))->assertUnprocessable()->assertJsonMissingPath('answer_keys');
    $this->postJson(route('exams.reveal'), ['question_id' => $ids[0]])->assertNotFound();
    $this->postJson(route('exams.expound'), ['question_id' => $ids[0]])->assertNotFound();
    expect(app(ExamGradingService::class)->grade([$ids[0]], [$ids[0] => 1])['answer_keys'])->toBe([]);
});

test('cached retired items disappear from new drill and exam payloads', function () {
    $ids = securityItems();
    app(QuestionRepositoryInterface::class)->getActivePool();
    Question::whereKey($ids[0])->update(['status' => 'draft']);
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true']))
        ->assertInertia(fn (Assert $page) => $page->where('questions', fn ($qs) => ! collect($qs)->pluck('id')->contains($ids[0])));
});

test('historical feedback withholds keys protected by overlapping strict sessions', function () {
    $ids = securityItems();
    $user = User::factory()->create();
    $attempt = ExamAttempt::create(['user_id' => $user->id, 'question_ids' => $ids, 'answers' => [], 'cat_scores' => []]);
    ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => [$ids[0]]]);
    $this->actingAs($user)->withoutVite()->get(route('exams.index', ['attempt_id' => $attempt->id]))
        ->assertInertia(fn (Assert $page) => $page->where('questions', function ($qs) use ($ids) {
            $byId = collect($qs)->keyBy('id');
            expect($byId[$ids[0]])->not->toHaveKeys(['correct_option', 'explanation']);
            expect($byId[$ids[1]])->toHaveKeys(['correct_option', 'explanation']);

            return true;
        }));
});

test('bank rate limits enforce in testing and do not mix account and IP identities', function () {
    config(['civio.bank_access_per_minute' => 2]);
    $id = securityItems(1)[0];
    $this->postJson(route('exams.reveal'), ['question_id' => $id])->assertOk();
    $this->postJson(route('exams.expound'), ['question_id' => $id])->assertOk();
    $this->postJson(route('exams.reveal'), ['question_id' => $id])->assertTooManyRequests();
    $this->actingAs(User::factory()->create())->postJson(route('exams.reveal'), ['question_id' => $id])->assertOk();
});

test('duplicate ids and options outside the actual question fail validation', function () {
    $ids = securityItems();
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true']))->assertOk();
    $this->postJson(route('exams.attempts.store'), securitySubmission([$ids[0], $ids[0]]))->assertUnprocessable();
    $this->postJson(route('exams.attempts.store'), [...securitySubmission($ids), 'answers' => array_fill_keys($ids, 7)])->assertUnprocessable();
});

test('drill bank pages are bounded and retired saved-set items stay private', function () {
    $ids = securityItems(101);
    $user = User::factory()->create();
    $draft = Question::factory()->create(['status' => 'draft']);
    $set = SavedDrillSet::create(['user_id' => $user->id, 'name' => 'Private set', 'color' => 'blue']);
    $set->questions()->attach([$ids[0], $draft->id]);
    $this->actingAs($user)->withoutVite()->get(route('drills.index'))
        ->assertInertia(fn (Assert $page) => $page
            ->has('questions', 100)->where('bankPage.last', 2)
            ->where('savedDrillSets.0.questions_count', 1));
    $this->get(route('drills.index', ['page' => 2]))
        ->assertInertia(fn (Assert $page) => $page->has('questions', 1)->where('questions.0.id', $ids[100]));
    $this->getJson(route('drills.saved-sets.getSetQuestions', $set))
        ->assertOk()->assertJsonCount(1, 'questions')
        ->assertJsonMissingPath('questions.0.correct_option');
});

test('opening another drill does not revoke an earlier served practice batch', function () {
    $ids = securityItems();
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode([$ids[0]])]))->assertOk();
    $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode([$ids[1]])]))->assertOk();
    $this->postJson(route('exams.attempts.store'), securitySubmission([$ids[0]]))->assertOk()->assertJson(['score' => 100]);
});
