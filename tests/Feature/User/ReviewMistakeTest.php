<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\ReviewCard;
use App\Models\ReviewEvent;
use App\Models\ReviewHelp;
use App\Models\ReviewItem;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\Exam\FsrsScheduler;
use App\Services\Exam\ReviewMistakeRecorder;
use App\Services\Exam\ReviewScheduleApplier;
use App\Support\ReviewCopy;
use App\Support\ReviewDueLabel;
use Carbon\Carbon;
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
            ->where('note', ReviewCopy::NOTE)
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
            ->where('note', ReviewCopy::NOTE));

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

test('a later overlapping drill does not drop the explanation on the first drill', function () {
    $user = User::factory()->create();
    $first = reviewQuestion(['stem' => 'First drill item?']);
    $second = reviewQuestion(['stem' => 'Second drill item?']);
    $this->actingAs($user);

    answerDrill($first, 0)->assertOk();
    $this->postJson(route('exams.reveal'), ['question_id' => $first->id])->assertOk();
    $this->get(route('exams.index', [
        'drill' => 'true',
        'custom_question_ids' => json_encode([$first->id, $second->id]),
    ]))->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$first->id],
        'answers' => [(string) $first->id => 1],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();

    expect(ReviewItem::query()->where('question_id', $first->id)->first()->status)->toBe('pending');
});

test('the open drill can claim its own batch after a newer one exists', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);

    answerDrill($question, 0)->assertOk();
    $first = session('civio_practice_served_'.$user->id)[0]['id'];
    $this->postJson(route('exams.reveal'), [
        'question_id' => $question->id,
        'practice_batch_id' => $first,
    ])->assertOk();
    $this->get(route('exams.index', [
        'drill' => 'true',
        'custom_question_ids' => json_encode([$question->id]),
    ]))->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 1],
        'practice_batch_id' => $first,
        'metadata' => ['track' => 'Drill', 'duration_secs' => 12, 'is_timed' => false],
    ])->assertOk();

    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('pending');
});

test('a study mock can claim its own explanation after a newer drill', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);
    answerDrill($question, 0)->assertOk();
    $session = ExamSession::create([
        'user_id' => $user->id,
        'track' => 'Subprofessional',
        'mode' => 'study',
        'question_ids' => [$question->id],
        'started_at' => now(),
        'deadline_at' => now()->addHour(),
    ]);
    $this->get(route('exams.index', [
        'drill' => 'true',
        'custom_question_ids' => json_encode([$question->id]),
    ]))->assertOk();
    $this->postJson(route('exams.reveal'), [
        'question_id' => $question->id,
        'exam_session_id' => $session->id,
    ])->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $session->id,
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 1],
    ])->assertOk();

    expect(ReviewItem::query()->where('question_id', $question->id)->first()->status)->toBe('pending');
});

test('a wrong answer schedules a review and an independent correct moves it later', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);

    answerDrill($question, 0)->assertOk()->assertJsonPath('review_schedule', ReviewScheduleApplier::SAVED);
    $card = ReviewCard::query()->where('question_id', $question->id)->first();
    $firstDue = $card->due_at->copy();

    expect($card->scheduler_version)->toBe(FsrsScheduler::VERSION)
        ->and($card->policy_version)->toBe('civio-fsrs-policy-1')
        ->and($card->last_rating)->toBe('again')
        ->and($firstDue->greaterThan(now()))->toBeTrue()
        ->and(ReviewEvent::query()->where('outcome', 'incorrect')->count())->toBe(1);

    $this->travel(2)->minutes();
    auth()->logout();
    $this->actingAs($user)->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->where('dueLabel', 'Due Today')
            ->where('due.0.question_id', $question->id)
            ->where('due.0.status_label', 'Due for Review')
            ->where('total', 0)
            ->missing('due.0.correct_option'));

    $this->actingAs(User::factory()->create())->getJson(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertJsonCount(0, 'due')
        ->assertJsonCount(0, 'items');

    $this->actingAs($user);
    answerDrill($question, 1)->assertOk();
    $card->refresh();

    expect(ReviewItem::query()->first()->status)->toBe('resolved')
        ->and($card->due_at->greaterThan($firstDue))->toBeTrue()
        ->and($card->last_rating)->toBe('good')
        ->and(ReviewEvent::query()->where('outcome', 'independent_correct')->count())->toBe(1)
        ->and(ReviewCard::query()->count())->toBe(1);
});

test('an assisted correct answer does not move the review date', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);
    answerDrill($question, 0)->assertOk();
    $due = ReviewCard::query()->first()->due_at->copy();
    $this->postJson(route('exams.reveal'), ['question_id' => $question->id])->assertOk();
    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => 1],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 4, 'is_timed' => false],
    ])->assertOk();

    $event = ReviewEvent::query()->where('outcome', 'assisted_correct')->first();

    expect(ReviewItem::query()->first()->status)->toBe('pending')
        ->and(ReviewCard::query()->first()->due_at->equalTo($due))->toBeTrue()
        ->and($event->rating)->toBeNull()
        ->and($event->scheduled)->toBeFalse()
        ->and(ReviewEvent::query()->count())->toBe(2);

    $this->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page->where('scheduleNotice', null));
});

test('a skipped answer and a repeated attempt do not add a successful review', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);
    $response = answerDrill($question, 0)->assertOk();
    $attemptId = (int) $response->json('attempt_id');
    $loaded = Question::query()->with('subcategory.category')->findOrFail($question->id);

    $this->postJson(route('exams.attempts.store'), [
        'question_ids' => [$question->id],
        'answers' => [(string) $question->id => null],
        'metadata' => ['track' => 'Drill', 'duration_secs' => 4, 'is_timed' => false],
    ])->assertOk();

    expect(ReviewEvent::query()->count())->toBe(1);

    app(ReviewMistakeRecorder::class)->record(
        $user->id,
        $attemptId,
        false,
        [$question->id => 0],
        new Collection([$loaded]),
        null,
    );

    expect(ReviewEvent::query()->count())->toBe(1)
        ->and(ReviewCard::query()->count())->toBe(1);
});

test('an inactive question leaves the due list and a strict mock schedules nothing', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);
    answerDrill($question, 0)->assertOk();
    $question->forceFill(['status' => 'draft'])->save();
    $this->travel(2)->minutes();

    $this->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertDontSee($question->stem);

    $strict = reviewQuestion(['stem' => 'Strict item?']);
    $session = ExamSession::create([
        'user_id' => $user->id,
        'track' => 'Professional',
        'mode' => 'strict',
        'question_ids' => [$strict->id],
        'started_at' => now(),
        'deadline_at' => now()->addHour(),
    ]);
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $session->id,
        'question_ids' => [$strict->id],
        'answers' => [(string) $strict->id => 0],
    ])->assertOk();

    expect(ReviewCard::query()->where('question_id', $strict->id)->exists())->toBeFalse()
        ->and(ReviewEvent::query()->where('question_id', $strict->id)->exists())->toBeFalse();
});

test('a review time just after midnight in Manila uses that calendar day', function () {
    expect(ReviewDueLabel::format(Carbon::parse('2026-10-21T16:30:00Z')))
        ->toBe('Oct 22, 2026 12:30 AM');
});

test('the same graded card and clock produce the same due instant', function () {
    $now = Carbon::parse('2026-10-21T04:00:00Z');
    $scheduler = app(FsrsScheduler::class);
    $first = $scheduler->applyMany([
        ['key' => '9', 'card' => null, 'rating' => 'again'],
    ], $now);
    $second = $scheduler->applyMany([
        ['key' => '9', 'card' => null, 'rating' => 'again'],
    ], $now);

    expect($first['9']['due'])->toBe($second['9']['due'])
        ->and($first['9']['state'])->toBe('learning');
});

test('a scheduler failure keeps the answer and a later try saves the reminder', function () {
    $user = User::factory()->create();
    $question = reviewQuestion();
    $this->actingAs($user);
    config(['civio.fsrs_node' => '/bin/false']);

    try {
        answerDrill($question, 0)
            ->assertOk()
            ->assertJsonPath('success', true)
            ->assertJsonPath('review_schedule', ReviewScheduleApplier::FAILED)
            ->assertJsonPath('review_notice', ReviewCopy::REMINDER_FAILED);

        expect(ReviewCard::query()->count())->toBe(0)
            ->and(ReviewItem::query()->first()->status)->toBe('pending')
            ->and(ReviewEvent::query()->first()->scheduled)->toBeFalse()
            ->and(ReviewEvent::query()->first()->rating)->toBe('again');

        $this->get(route('reviews.mistakes.index'))
            ->assertOk()
            ->assertInertia(fn (Assert $page) => $page
                ->where('state', 'open')
                ->where('scheduleNotice', ReviewCopy::REMINDER_FAILED)
                ->where('due', [])
                ->has('items', 1));

        config(['civio.fsrs_node' => 'node']);

        $this->postJson(route('reviews.schedules.retry'))
            ->assertOk()
            ->assertJsonPath('review_schedule', ReviewScheduleApplier::SAVED)
            ->assertJsonPath('review_notice', null);

        $card = ReviewCard::query()->first();

        expect($card)->not->toBeNull()
            ->and($card->due_at->greaterThan(now()))->toBeTrue()
            ->and($card->last_rating)->toBe('again')
            ->and(ReviewEvent::query()->first()->scheduled)->toBeTrue();
    } finally {
        config(['civio.fsrs_node' => 'node']);
    }
});

test('the next saved answer finishes a reminder the scheduler missed', function () {
    $user = User::factory()->create();
    $missed = reviewQuestion(['stem' => 'Missed while the scheduler was down?']);
    $later = reviewQuestion(['stem' => 'Answered after the scheduler recovered?']);
    $this->actingAs($user);
    config(['civio.fsrs_node' => '/bin/false']);

    try {
        answerDrill($missed, 0)->assertJsonPath('review_schedule', ReviewScheduleApplier::FAILED);
        config(['civio.fsrs_node' => 'node']);
        answerDrill($later, 0)->assertJsonPath('review_schedule', ReviewScheduleApplier::SAVED);
    } finally {
        config(['civio.fsrs_node' => 'node']);
    }

    expect(ReviewCard::query()->where('question_id', $missed->id)->where('due_at', '>', now())->exists())->toBeTrue()
        ->and(ReviewCard::query()->where('question_id', $later->id)->exists())->toBeTrue()
        ->and(ReviewEvent::query()->where('scheduled', false)->where('assisted', false)->count())->toBe(0);
});

test('due reviews stay reachable after the first page', function () {
    $user = User::factory()->create();
    $this->actingAs($user);
    $attempt = ExamAttempt::query()->create([
        'user_id' => $user->id,
        'mode' => 'study',
        'question_ids' => [1],
        'answers' => [],
        'cat_scores' => [],
    ]);
    $ids = [];

    foreach (range(1, 21) as $number) {
        $question = reviewQuestion(['stem' => "Due item $number"]);
        $ids[] = (int) $question->id;
        ReviewItem::query()->create([
            'user_id' => $user->id,
            'question_id' => $question->id,
            'source_attempt_id' => $attempt->id,
            'first_wrong_at' => now(),
            'last_result_at' => now(),
            'wrong_count' => 1,
            'status' => 'pending',
            'last_attempt_id' => $attempt->id,
        ]);
        ReviewCard::query()->create([
            'user_id' => $user->id,
            'question_id' => $question->id,
            'scheduler_version' => FsrsScheduler::VERSION,
            'policy_version' => 'civio-fsrs-policy-1',
            'card_state' => ['state' => 1],
            'due_at' => now()->subMinutes(40 - $number),
            'state' => 'learning',
            'last_rating' => 'again',
            'last_reviewed_at' => now(),
            'reps' => 1,
            'lapses' => 1,
        ]);
    }

    $this->get(route('reviews.mistakes.index'))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->has('due', 20)
            ->where('dueTotal', 21)
            ->where('duePage', 1)
            ->where('dueLastPage', 2)
            ->where('total', 0)
            ->where('scheduleNotice', null));

    $this->get(route('reviews.mistakes.index', ['due_page' => 2]))
        ->assertOk()
        ->assertInertia(fn (Assert $page) => $page
            ->has('due', 1)
            ->where('due.0.question_id', $ids[20])
            ->where('total', 0));

    $this->postJson(route('reviews.mistakes.start'), [
        'question_ids' => [$ids[20]],
    ])->assertOk()
        ->assertJsonPath('questions.0.id', $ids[20]);
});
