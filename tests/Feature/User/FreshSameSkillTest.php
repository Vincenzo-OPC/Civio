<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewItem;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;

function freshSkill(): Subcategory
{
    return Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id]);
}

function freshItems(Subcategory $sub, int $n, string $status = 'active'): array
{
    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => $status, 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

test('a fresh same-skill revisit serves unseen questions from the mistake skill only', function () {
    $user = User::factory()->create();
    $skill = freshSkill();
    $other = freshSkill();
    [$missed, $seen] = freshItems($skill, 2);
    $fresh = freshItems($skill, 3);
    $draft = freshItems($skill, 1, 'draft');
    $unrelated = freshItems($other, 3);

    $attempt = ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => [$missed, $seen], 'answers' => [], 'cat_scores' => []]);
    ReviewItem::create(['user_id' => $user->id, 'question_id' => $missed, 'source_attempt_id' => $attempt->id, 'last_attempt_id' => $attempt->id, 'first_wrong_at' => now(), 'last_result_at' => now(), 'status' => 'pending']);

    $page = $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1']))->assertOk();
    $ids = collect($page->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();

    expect($ids)->toEqualCanonicalizing($fresh)
        ->and(array_intersect($ids, [$missed, $seen, ...$draft, ...$unrelated]))->toBe([])
        ->and(count($ids))->toBeLessThanOrEqual(ExamService::FRESH_SAME_SKILL_LIMIT);
    expect($page->viewData('page')['props']['questions'][0])->not->toHaveKey('correct_option');
});

test('without pending mistakes a fresh same-skill request falls back to the normal drill', function () {
    freshItems(freshSkill(), 3);
    $this->actingAs(User::factory()->create())->withoutVite()
        ->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1']))->assertOk();
});
