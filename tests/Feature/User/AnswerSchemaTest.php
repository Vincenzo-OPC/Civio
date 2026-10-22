<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamGradingService;

/** Three items whose ids overlap served positions 0-2 (fresh database). */
function smallIdItems(): array
{
    $sub = Subcategory::factory()->create([
        'category_id' => Category::factory()->create(['name' => 'Verbal Ability', 'is_demographic' => false])->id,
    ]);
    $ids = Question::factory()->count(3)->create([
        'subcategory_id' => $sub->id, 'status' => 'active',
        'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();

    // The point of this file: ids small enough to also be valid positions.
    expect(min($ids))->toBeLessThan(3);

    return $ids;
}

test('the grader never reads small question ids as positions', function () {
    $ids = smallIdItems();
    // Answer the first two items by id; the third is blank.
    $graded = app(ExamGradingService::class)->grade($ids, [$ids[0] => 1, $ids[1] => 1]);

    expect($graded['correct_count'])->toBe(2)
        ->and($graded['skipped_count'])->toBe(1)
        ->and($graded['answers'])->toBe([(string) $ids[0] => 1, (string) $ids[1] => 1, (string) $ids[2] => null])
        ->and($graded['cat_scores']['metadata']['answer_schema'])->toBe('question_id');
});

test('positions are read only when declared, and an unknown schema is refused', function () {
    $ids = smallIdItems();
    $grading = app(ExamGradingService::class);
    $byPosition = $grading->grade($ids, [0 => 1, 2 => 0], [], ExamGradingService::SCHEMA_POSITION);

    expect($byPosition['answers'])->toBe([(string) $ids[0] => 1, (string) $ids[1] => null, (string) $ids[2] => 0]);
    expect(fn () => $grading->grade($ids, [], [], 'guess'))->toThrow(InvalidArgumentException::class);
});

test('a strict mock with small ids grades a partial id-keyed submit by id', function () {
    $user = User::factory()->create();
    $ids = smallIdItems();
    $session = ExamSession::create([
        'user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => $ids,
        'started_at' => now(), 'deadline_at' => now()->addHour(),
    ]);

    $this->actingAs($user)->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $session->id, 'question_ids' => $ids, 'answers' => [$ids[0] => 1, $ids[1] => 1],
    ])->assertOk()->assertJson(['score' => 67, 'correct_count' => 2, 'skipped_count' => 1]);
});

test('a strict mock refuses position-keyed or unserved answer keys', function () {
    $user = User::factory()->create();
    $ids = smallIdItems();
    $session = fn () => ExamSession::create([
        'user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict', 'question_ids' => $ids,
        'started_at' => now(), 'deadline_at' => now()->addHour(),
    ]);
    $this->actingAs($user);

    $first = $session();
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $first->id, 'question_ids' => $ids, 'answers' => [0 => 1], 'answer_schema' => 'position',
    ])->assertUnprocessable();
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $first->id, 'question_ids' => $ids, 'answers' => [999999 => 1],
    ])->assertUnprocessable();
    $this->postJson(route('exams.attempts.store'), [
        'exam_session_id' => $first->id, 'question_ids' => $ids, 'answers' => [$ids[0] => 1], 'answer_schema' => 'guess',
    ])->assertUnprocessable();

    expect($first->fresh()->isOpen())->toBeTrue()->and(ExamAttempt::count())->toBe(0);
});

test('stored attempts are read with their recorded schema, not re-guessed', function () {
    $ids = smallIdItems();
    $grading = app(ExamGradingService::class);
    // Saved by id, partial: inference would read key 1 as position 1.
    $answers = [(string) $ids[0] => 1, (string) $ids[1] => 0];

    expect($grading->chosenForQuestion($answers, $ids, $ids[0], 'question_id'))->toBe(1)
        ->and($grading->chosenForQuestion($answers, $ids, $ids[1], 'question_id'))->toBe(0)
        ->and($grading->chosenForQuestion($answers, $ids, $ids[2], 'question_id'))->toBeNull();
});
