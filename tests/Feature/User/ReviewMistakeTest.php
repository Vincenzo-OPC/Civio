<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\ReviewHelp;
use App\Models\ReviewItem;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\Exam\ReviewMistakeRecorder;
use Illuminate\Support\Collection;
use Illuminate\Testing\TestResponse;
use Inertia\Testing\AssertableInertia as Assert;

function reviewQuestion(array $overrides = []): Question
{
    $sub = Subcategory::factory()->create([
        'category_id' => Category::factory()->create([
            'name' => 'Numerical Ability',
            'is_demographic' => false,
        ])->id,
    ]);

    return Question::factory()->create(array_merge([
        'subcategory_id' => $sub->id,
        'status' => 'active',
        'options' => ['12', '34', '56', '78'],
        'correct_option' => 1,
        'explanation' => 'Because 34.',
        'stem' => 'Which value is larger?',
    ], $overrides));
}

function answerDrill(Question $question, int $choice): TestResponse
{
    test()->get(route('exams.index', [
        'drill' => 'true',
        'custom_question_ids' => json_encode([$question->id]),
    ]))->assertOk();

    return test()->postJson(route('exams.attempts.store'), [
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => $choice],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ]);
}

test('a wrong drill answer is remembered once and a correct one is not', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);

    answerDrill($question, 0)->assertOk();

    $item = ReviewItem::query()->where('user_id', $user->id)->first();
    expect($item)->not->toBeNull()
        ->and($item->status)->toBe('pending')
        ->and($item->wrong_count)->toBe(1);

    app(ReviewMistakeRecorder::class)->record(
        $user->id,
        (int) $item->last_attempt_id,
        false,
        [$question->id => 0],
        new Collection([$question]),
    );

    expect($item->fresh()->wrong_count)->toBe(1);

    $right = reviewQuestion(['stem' => 'A different item?']);
    answerDrill($right, 1)->assertOk();
    expect(ReviewItem::query()->where('question_id', $right->id)->exists())->toBeFalse();
});

test('an explanation blocks only the drill that showed it', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);

    answerDrill($question, 0)->assertOk();
    $this->postJson(route('exams.reveal'), ['question_id' => $question->id])->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 1],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();

    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('pending');

    answerDrill($question, 1)->assertOk();
    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('resolved');
});

test('a strict mock does not create a review item', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $session = ExamSession::create([
        'user_id' => $user->id,
        'track' => 'Professional',
        'mode' => 'strict',
        'question_ids' => [$question->id],
        'started_at' => now(),
        'deadline_at' => now()->addHour(),
    ]);

    $this->actingAs($user)->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $session->id,
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 0],
    ])->assertOk();

    expect(ReviewItem::query()->count())->toBe(0);
});

test('review mistakes stay with the owner and hide the answer key', function () {
    $owner = User::factory()->create();
    $other = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($owner);
    answerDrill($question, 0)->assertOk();

    auth()->logout();
    $this->actingAs($owner)->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('user/drills/mistakes')
            ->where('note', 'This is practice history. A later correct answer, given without an explanation, clears the item.')
            ->where('items.0.stem', 'Which value is larger?')
            ->missing('items.0.correct_option'));

    $this->actingAs($other)->getJson(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertJsonCount(0, 'items');

    $this->actingAs($other)->postJson(route('reviews.mistakes.start'), [
        'question_ids' => [$question->id],
    ])->assertNotFound();

    $payload = $this->actingAs($owner)->postJson(route('reviews.mistakes.start'), [
        'question_ids' => [$question->id],
    ])->assertOk()->json('questions.0');

    expect($payload)->not->toHaveKey('correct_option')
        ->and($payload)->not->toHaveKey('explanation');
});

test('an empty review list and a draft stay out of the practice history', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->component('user/drills/mistakes')
            ->has('items', 0)
            ->where('note', 'This is practice history. A later correct answer, given without an explanation, clears the item.'));

    $draft = reviewQuestion(['status' => 'draft', 'stem' => 'Hidden draft stem']);
    $attemptId = ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [$draft->id],
        'answers' => [0],
        'cat_scores' => [],
    ])->id;
    ReviewItem::query()->create([
        'user_id' => $user->id,
        'question_id' => $draft->id,
        'source_attempt_id' => $attemptId,
        'first_wrong_at' => now(),
        'last_result_at' => now(),
        'wrong_count' => 1,
        'status' => 'pending',
        'last_attempt_id' => $attemptId,
    ]);

    $this->get(route('reviews.mistakes.index'))->assertOk()->assertDontSee('Hidden draft stem');
});

test('a skipped item keeps its explanation until that same drill is answered', function () {
    $user = User::factory()->create();
    $other = reviewQuestion(['stem' => 'Answered companion?']);
    $missed = reviewQuestion(['stem' => 'Seen but skipped?']);
    $this->actingAs($user);

    $this->get(route('exams.index', [
        'drill' => 'true',
        'custom_question_ids' => json_encode([$other->id, $missed->id]),
    ]))->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$other->id, $missed->id],
        'answers' => [
            (string) $other->id => 0,
            (string) $missed->id => 0,
        ],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();
    $this->postJson(route('exams.reveal'), ['question_id' => $missed->id])->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$other->id, $missed->id],
        'answers' => [
            (string) $other->id => 1,
            (string) $missed->id => null,
        ],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();

    expect(ReviewHelp::query()->where('question_id', $missed->id)->exists())->toBeTrue();

    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$missed->id],
        'answers' => [(string) $missed->id => 1],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();
    expect(ReviewItem::query()->where('question_id', $missed->id)->first()->status)->toBe('pending');

    answerDrill($missed, 1)->assertOk();
    $item = ReviewItem::query()->where('question_id', $missed->id)->first();
    expect($item->status)->toBe('resolved');

    answerDrill($missed, 0)->assertOk();
    expect($item->fresh()->status)->toBe('pending')
        ->and($item->fresh()->wrong_count)->toBe(2);
});

test('older mistakes stay reachable and a locked item cannot be retried', function () {
    $user = User::factory()->create();
    $this->actingAs($user);
    $questions = [];

    for ($i = 0; $i < 21; $i++) {
        $question = reviewQuestion(['stem' => "Mistake {$i}"]);
        $attemptId = ExamAttempt::create([
            'user_id' => $user->id,
            'question_ids' => [$question->id],
            'answers' => [0],
            'cat_scores' => [],
        ])->id;
        ReviewItem::query()->create([
            'user_id' => $user->id,
            'question_id' => $question->id,
            'source_attempt_id' => $attemptId,
            'first_wrong_at' => now()->subMinutes(21 - $i),
            'last_result_at' => now()->subMinutes(21 - $i),
            'wrong_count' => 1,
            'status' => 'pending',
            'last_attempt_id' => $attemptId,
        ]);
        $questions[] = $question;
    }

    $this->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->has('items', 20)
            ->where('lastPage', 2)
            ->where('total', 21));

    $this->get(route('reviews.mistakes.index', ['page' => 2]))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page->has('items', 1));

    $locked = $questions[0];
    ExamSession::create([
        'user_id' => $user->id,
        'track' => 'Professional',
        'mode' => 'strict',
        'question_ids' => [$locked->id],
        'started_at' => now(),
        'deadline_at' => now()->addHour(),
    ]);

    $this->postJson(route('reviews.mistakes.start'), [
        'question_ids' => [$locked->id],
    ])->assertNotFound();
});

test('a study mock explanation does not assist the next drill', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $seed = ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [$question->id],
        'answers' => [0],
        'cat_scores' => [],
    ]);
    ReviewItem::query()->create([
        'user_id' => $user->id,
        'question_id' => $question->id,
        'source_attempt_id' => $seed->id,
        'first_wrong_at' => now(),
        'last_result_at' => now(),
        'wrong_count' => 1,
        'status' => 'pending',
        'last_attempt_id' => $seed->id,
    ]);
    $session = ExamSession::create([
        'user_id' => $user->id,
        'track' => 'Professional',
        'mode' => 'study',
        'question_ids' => [$question->id],
        'started_at' => now(),
        'deadline_at' => now()->addHour(),
    ]);
    $this->actingAs($user);
    $this->postJson(route('exams.reveal'), ['question_id' => $question->id])->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $session->id,
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 1],
    ])->assertOk();

    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('pending');

    answerDrill($question, 1)->assertOk();
    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('resolved');
});
