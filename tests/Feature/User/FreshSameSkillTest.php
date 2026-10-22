<?php

use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\ReviewItem;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;
use Inertia\Testing\AssertableInertia as Assert;

function freshSkill(): Subcategory
{
    return Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id]);
}

function freshItems(Subcategory $sub, int $n, string $status = 'active'): array
{
    return Question::factory()->count($n)->create(['subcategory_id' => $sub->id, 'status' => $status, 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1])->pluck('id')->all();
}

function freshMistake(User $user, array $attemptIds, int $missed): void
{
    $attempt = ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => $attemptIds, 'answers' => [], 'cat_scores' => []]);
    ReviewItem::create(['user_id' => $user->id, 'question_id' => $missed, 'source_attempt_id' => $attempt->id, 'last_attempt_id' => $attempt->id, 'first_wrong_at' => now(), 'last_result_at' => now(), 'status' => 'pending']);
}

function freshServed($response): array
{
    return collect($response->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();
}

test('a fresh same-skill revisit serves unseen questions from the mistake skill only', function () {
    $user = User::factory()->create();
    $skill = freshSkill();
    [$missed, $seen] = freshItems($skill, 2);
    $fresh = freshItems($skill, 3);
    $draft = freshItems($skill, 1, 'draft');
    $unrelated = freshItems(freshSkill(), 3);
    freshMistake($user, [$missed, $seen], $missed);

    $page = $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1']))->assertOk();
    $ids = freshServed($page);

    expect($ids)->toEqualCanonicalizing($fresh)
        ->and(array_intersect($ids, [$missed, $seen, ...$draft, ...$unrelated]))->toBe([])
        ->and(count($ids))->toBeLessThanOrEqual(ExamService::FRESH_SAME_SKILL_LIMIT);
    expect($page->viewData('page')['props']['questions'][0])->not->toHaveKey('correct_option');
});

test('exposure uses the full history, beyond 200 attempts, and served mock sessions', function () {
    $user = User::factory()->create();
    $skill = freshSkill();
    [$missed, $old, $inSession, $fresh] = freshItems($skill, 4);
    ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => [$old], 'answers' => [], 'cat_scores' => []]);
    $filler = freshItems(freshSkill(), 1)[0];
    for ($i = 0; $i < 205; $i++) {
        ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::Study->value, 'question_ids' => [$filler], 'answers' => [], 'cat_scores' => []]);
    }
    ExamSession::create(['user_id' => $user->id, 'track' => 'Professional', 'mode' => ExamMode::Study->value, 'question_ids' => [$inSession], 'started_at' => now(), 'deadline_at' => now()->addHour()]);
    freshMistake($user, [$missed], $missed);

    $ids = freshServed($this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1'])));

    expect($ids)->toBe([$fresh]);
});

test('nothing fresh left gives an empty set and an honest empty state, never the ordinary pool', function () {
    $user = User::factory()->create();
    $skill = freshSkill();
    [$missed, $seen] = freshItems($skill, 2);
    freshItems(freshSkill(), 5);
    freshMistake($user, [$missed, $seen], $missed);

    $this->actingAs($user)->withoutVite()->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1']))
        ->assertRedirect(route('reviews.mistakes.index', ['fresh' => 'none']));

    $this->get(route('reviews.mistakes.index', ['fresh' => 'none']))->assertInertia(fn (Assert $page) => $page
        ->where('freshSameSkillCount', 0)
        ->where('freshNotice', fn ($n) => str_contains((string) $n, 'No new questions are left')));
});

test('guests get no fallback pool for fresh same-skill', function () {
    freshItems(freshSkill(), 3);
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'fresh_same_skill' => '1']))->assertRedirect(route('login'));
});
