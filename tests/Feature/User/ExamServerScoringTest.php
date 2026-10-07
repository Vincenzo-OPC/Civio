<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamGradingService;
use Inertia\Testing\AssertableInertia as Assert;

function seedExamQuestions(int $count = 3): array
{
    $category = Category::factory()->create([
        'name' => 'Verbal Ability',
        'is_demographic' => false,
    ]);
    $sub = Subcategory::factory()->create([
        'category_id' => $category->id,
        'name' => 'Word Analogy',
    ]);
    $author = User::factory()->create();

    $questions = [];
    for ($i = 0; $i < $count; $i++) {
        $questions[] = Question::factory()->create([
            'subcategory_id' => $sub->id,
            'created_by' => $author->id,
            'status' => 'active',
            'options' => ['A'.$i, 'B'.$i, 'C'.$i, 'D'.$i],
            'correct_option' => 1,
            'explanation' => 'Because B'.$i,
            'stem' => "Stem {$i}?",
        ]);
    }

    return $questions;
}

test('forged client score is ignored and server recomputes grade', function () {
    $questions = seedExamQuestions(3);
    $ids = array_map(fn ($q) => $q->id, $questions);

    // Client claims 100% but answers are all wrong (option 0; correct is 1).
    $response = $this->postJson(route('exams.attempts.store'), [
        'question_ids' => $ids,
        'answers' => [
            (string) $ids[0] => 0,
            (string) $ids[1] => 0,
            (string) $ids[2] => 0,
        ],
        'cat_scores' => [
            'categoryScoreMap' => [],
            'metadata' => [
                'track' => 'Professional',
                'correct_count' => 3,
                'total_questions' => 3,
                'skipped_count' => 0,
                'score' => 100,
                'duration_secs' => 60,
                'is_timed' => true,
            ],
        ],
    ]);

    $response->assertOk()->assertJson(['success' => true]);
    expect($response->json('score'))->toBe(0);
    expect($response->json('correct_count'))->toBe(0);
    expect($response->json('wrong_count'))->toBe(3);

    $attempt = ExamAttempt::findOrFail($response->json('attempt_id'));
    expect($attempt->cat_scores['metadata']['score'])->toBe(0);
    expect($attempt->cat_scores['metadata']['correct_count'])->toBe(0);
    expect($attempt->cat_scores['metadata']['graded_by'])->toBe('server');
});

test('server grades perfect answers as 100 regardless of client metadata', function () {
    $questions = seedExamQuestions(2);
    $ids = array_map(fn ($q) => $q->id, $questions);

    $response = $this->postJson(route('exams.attempts.store'), [
        'question_ids' => $ids,
        'answers' => [
            (string) $ids[0] => 1,
            (string) $ids[1] => 1,
        ],
        'metadata' => [
            'track' => 'Drill',
            'score' => 0,
            'correct_count' => 0,
            'duration_secs' => 30,
            'is_timed' => false,
        ],
    ]);

    $response->assertOk();
    expect($response->json('score'))->toBe(100);
    expect($response->json('correct_count'))->toBe(2);
});

test('live exam inertia props withhold correct_option and explanation', function () {
    seedExamQuestions(2);

    $response = $this->withoutVite()->get(route('exams.index'));
    $response->assertOk();

    $response->assertInertia(fn (Assert $page) => $page
        ->component('user/exams/index')
        ->has('questions')
        ->where('questions', function ($questions) {
            $list = collect($questions);
            expect($list->count())->toBeGreaterThan(0);
            foreach ($list as $q) {
                expect($q)->not->toHaveKey('correct_option');
                expect($q)->not->toHaveKey('explanation');
                expect($q)->toHaveKey('stem');
                expect($q)->toHaveKey('options');
            }

            return true;
        })
    );
});

test('scorecard attempt includes answer keys in question props', function () {
    $user = User::factory()->create();
    $questions = seedExamQuestions(2);
    $ids = array_map(fn ($q) => $q->id, $questions);

    $grading = app(ExamGradingService::class);
    $graded = $grading->grade($ids, [
        (string) $ids[0] => 1,
        (string) $ids[1] => 0,
    ], ['track' => 'Professional', 'duration_secs' => 10, 'is_timed' => true]);

    $attempt = ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => $ids,
        'answers' => $graded['answers'],
        'cat_scores' => $graded['cat_scores'],
    ]);

    $this->actingAs($user);
    $response = $this->withoutVite()->get(route('exams.index', ['attempt_id' => $attempt->id]));
    $response->assertOk();

    $response->assertInertia(fn (Assert $page) => $page
        ->component('user/exams/index')
        ->where('questions', function ($questions) {
            foreach (collect($questions) as $q) {
                expect($q)->toHaveKey('correct_option');
                expect($q)->toHaveKey('explanation');
            }

            return true;
        })
    );
});

test('grading resolves original option ids after conceptual shuffle (ID-keyed answers)', function () {
    $questions = seedExamQuestions(1);
    $q = $questions[0];
    // Simulate: display order shuffled so original correct (1) appears at display index 3.
    // Client stores answers keyed by question id with ORIGINAL option index.
    $grading = app(ExamGradingService::class);
    $graded = $grading->grade(
        [$q->id],
        [(string) $q->id => 1],
        ['track' => 'Professional']
    );

    expect($graded['correct_count'])->toBe(1);
    expect($graded['score'])->toBe(100);
    expect($graded['answers'][(string) $q->id])->toBe(1);
});

test('legacy position-keyed answers still grade with backward-compatible read', function () {
    $questions = seedExamQuestions(2);
    $ids = array_map(fn ($q) => $q->id, $questions);
    $grading = app(ExamGradingService::class);
    expect($grading->detectAnswerSchema([0 => 1, 1 => 0], $ids))->toBe('position');
    $graded = $grading->grade($ids, [0 => 1, 1 => 0], ['track' => 'Drill']);

    expect($graded['correct_count'])->toBe(1);
    expect($graded['wrong_count'])->toBe(1);
});

test('reveal endpoint returns correct option for a question', function () {
    $questions = seedExamQuestions(1);
    $q = $questions[0];

    $response = $this->postJson(route('exams.reveal'), [
        'question_id' => $q->id,
    ]);

    $response->assertOk()
        ->assertJsonPath('success', true)
        ->assertJsonPath('correct_option', 1);
});
