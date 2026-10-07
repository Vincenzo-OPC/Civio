<?php

use App\Http\Resources\ExamQuestionResource;
use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

function unicodeMathQuestion(): Question
{
    $category = Category::factory()->create(['name' => 'Numerical Ability', 'is_demographic' => false]);
    $sub = Subcategory::factory()->create(['category_id' => $category->id, 'name' => 'Basic operations']);

    return Question::factory()->create([
        'subcategory_id' => $sub->id,
        'created_by' => User::factory()->create()->id,
        'status' => 'active',
        'stem' => "Compute 12 × 3 ÷ 4 − √16 + 2².\nIs ₱1,250 ≤ ₱1,300 ≥ ₱1,200? (Señora’s “quick” check — ½ · ° …)",
        'options' => ['5', '7 × 1', '₱9 − 2', '≥ 11'],
        'correct_option' => 0,
        'explanation' => '12 × 3 = 36; 36 ÷ 4 = 9; 9 − √16 = 5; 5 + 2² = 9. Mga tanong: ñ, “ ”, ‘ ’, —.',
    ]);
}

test('a stem with Unicode math symbols round-trips intact through the database', function () {
    $question = unicodeMathQuestion();
    $original = $question->getAttributes();

    $fresh = Question::query()->findOrFail($question->id);

    expect($fresh->stem)->toBe($question->stem)
        ->and($fresh->stem)->toContain('×', '÷', '−', '√', '²', '≤', '≥', '₱', 'ñ', '“', '—')
        ->and($fresh->stem)->not->toContain('??')
        ->and($fresh->options)->toBe(['5', '7 × 1', '₱9 − 2', '≥ 11'])
        ->and($fresh->explanation)->toBe($question->explanation)
        ->and($original['stem'])->toBe($fresh->getRawOriginal('stem'));
});

test('Unicode math symbols survive the exam resource and JSON transport', function () {
    $question = unicodeMathQuestion()->load('subcategory.category');

    $live = ExamQuestionResource::collectionForExam([$question])[0];
    $review = ExamQuestionResource::collectionForExam([$question], includeAnswerKey: true)[0];

    $decodedLive = json_decode(json_encode($live, JSON_THROW_ON_ERROR), true);
    $decodedReview = json_decode(json_encode($review, JSON_THROW_ON_ERROR), true);

    expect($decodedLive['stem'])->toBe($question->stem)
        ->and($decodedLive['options'])->toBe(['5', '7 × 1', '₱9 − 2', '≥ 11'])
        ->and($decodedLive)->not->toHaveKey('correct_option')
        ->and($decodedReview['explanation'])->toBe($question->explanation);
});

test('reveal returns the explanation with math symbols intact', function () {
    $question = unicodeMathQuestion();

    $this->postJson(route('exams.reveal'), ['question_id' => $question->id])
        ->assertOk()
        ->assertJsonPath('explanation', $question->explanation);
});
