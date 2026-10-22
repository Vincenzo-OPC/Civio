<?php

use App\DTOs\Exam\ExamSessionQueryData;
use App\Enums\ExamMode;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;
use Inertia\Testing\AssertableInertia as Assert;

function leakItems(int $count, string $status = 'active'): array
{
    return Question::factory()->count($count)->create([
        'subcategory_id' => Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id])->id,
        'status' => $status, 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();
}

function servedIds($response): array
{
    return collect($response->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all();
}

test('a single launch serves at most the custom id cap', function () {
    $ids = leakItems(80);
    $r = $this->actingAs(User::factory()->create())->withoutVite()
        ->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($ids)]))->assertOk();
    expect(count(servedIds($r)))->toBeLessThanOrEqual(ExamSessionQueryData::MAX_CUSTOM_IDS);
});

test('arbitrary ids beyond the daily budget are rejected', function () {
    $ids = leakItems(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET + 10);
    $this->actingAs(User::factory()->create())->withoutVite();
    $served = [];
    foreach (array_chunk($ids, ExamSessionQueryData::MAX_CUSTOM_IDS) as $chunk) {
        $r = $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($chunk)]))->assertOk();
        $served = array_merge($served, array_intersect(servedIds($r), $chunk));
    }
    expect(count(array_unique($served)))->toBe(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET);
});

test('ids from the users own attempts pass even after the budget is spent', function () {
    $user = User::factory()->create();
    $mine = leakItems(3);
    ExamAttempt::create(['user_id' => $user->id, 'mode' => ExamMode::cases()[0]->value, 'question_ids' => $mine, 'answers' => [], 'cat_scores' => []]);
    $this->actingAs($user)->withoutVite();
    foreach (array_chunk(leakItems(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET), ExamSessionQueryData::MAX_CUSTOM_IDS) as $chunk) {
        $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($chunk)]));
    }
    $r = $this->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($mine)]))->assertOk();
    expect(servedIds($r))->toEqualCanonicalizing($mine);
});

test('draft ids are never served through custom ids', function () {
    $drafts = leakItems(3, 'draft');
    $r = $this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($drafts)]))->assertOk();
    expect(array_intersect(servedIds($r), $drafts))->toBe([]);
});

test('custom drill payloads never carry answer keys', function () {
    $ids = leakItems(3);
    $this->withoutVite()->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($ids)]))
        ->assertInertia(fn (Assert $page) => $page->missing('questions.0.correct_option'));
});
