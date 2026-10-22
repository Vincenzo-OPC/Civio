<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;
use Inertia\Testing\AssertableInertia as Assert;

function skillSub(): Subcategory
{
    return Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id]);
}

function skillItems(Subcategory $sub, int $n, string $status = 'active'): array
{
    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => $status, 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

function skillServed($r): array
{
    return collect($r->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();
}

test('a skill drill serves only that subtopic, fresh items first, without keys or drafts', function () {
    $user = User::factory()->create();
    $sub = skillSub();
    $seen = skillItems($sub, 10);
    $fresh = skillItems($sub, 15);
    $drafts = skillItems($sub, 2, 'draft');
    $other = skillItems(skillSub(), 5);
    ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => $seen, 'answers' => [], 'cat_scores' => []]);

    $r = $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'subcategory_id' => $sub->id]))->assertOk();
    $ids = skillServed($r);

    expect($ids)->toHaveCount(ExamService::SKILL_DRILL_ITEMS)
        ->and(array_slice($ids, 0, 15))->toEqualCanonicalizing($fresh)
        ->and(array_intersect($ids, [...$drafts, ...$other]))->toBe([])
        ->and(count(array_unique($ids)))->toBe(count($ids));
    $r->assertInertia(fn (Assert $p) => $p->missing('questions.0.correct_option')->missing('questions.0.explanation'));
});

test('an unknown subtopic serves nothing rather than another pool', function () {
    skillItems(skillSub(), 5);
    $ids = skillServed($this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'subcategory_id' => 999999]))->assertOk());

    expect($ids)->toBe([]);
});
