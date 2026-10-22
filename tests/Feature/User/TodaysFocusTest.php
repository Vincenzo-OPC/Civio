<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;

function focusSubject(string $name, int $n): array
{
    $sub = Subcategory::factory()->create(['category_id' => Category::factory()->create(['name' => $name, 'is_demographic' => false])->id]);

    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

function focusServed($response): array
{
    return collect($response->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();
}

test('today\'s focus serves 15 from the weakest subject then 10 mixed from the others', function () {
    $user = User::factory()->create();
    $num = focusSubject('Numerical Ability', 30);
    $ver = focusSubject('Verbal Ability', 20);
    $cle = focusSubject('Clerical Ability', 20);

    // Numerical: 0/2 independent; Verbal: 2/2.
    ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Strict->value, 'question_ids' => [$num[0], $num[1], $ver[0], $ver[1]],
        'answers' => [(string) $num[0] => 0, (string) $num[1] => 0, (string) $ver[0] => 1, (string) $ver[1] => 1], 'cat_scores' => []]);

    $ids = focusServed($this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1']))->assertOk());

    expect($ids)->toHaveCount(ExamService::FOCUS_ITEMS + ExamService::FOCUS_MIXED_ITEMS)
        ->and(array_intersect(array_slice($ids, 0, 15), $num))->toHaveCount(15)
        ->and(array_intersect(array_slice($ids, 15), $num))->toBe([])
        ->and(array_intersect(array_slice($ids, 15), [...$ver, ...$cle]))->toHaveCount(10);
});

test('a guest gets a weekday-rotation focus subject', function () {
    focusSubject('Numerical Ability', 20);
    focusSubject('Verbal Ability', 20);
    $subject = app(ExamService::class)->todaysFocusSubject(['Numerical Ability', 'Verbal Ability'], null);

    expect($subject)->toBeIn(['Numerical Ability', 'Verbal Ability']);
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'focus_today' => '1']))->assertOk();
});
