<?php

use App\DTOs\Exam\ExamSessionQueryData;
use App\Models\Category;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\ExamService;
use Illuminate\Database\QueryException;
use Illuminate\Support\Facades\DB;

function budgetItems(int $count): array
{
    return Question::factory()->count($count)->create([
        'subcategory_id' => Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id])->id,
        'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();
}

function launchCustom($test, array $ids): array
{
    $r = $test->get(route('exams.index', ['drill' => 'true', 'custom_question_ids' => json_encode($ids)]))->assertOk();

    return array_values(array_intersect(collect($r->viewData('page')['props']['questions'])->pluck('id')->map(fn ($i) => (int) $i)->all(), $ids));
}

function spendBudget($test): void
{
    foreach (array_chunk(budgetItems(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET), ExamSessionQueryData::MAX_CUSTOM_IDS) as $chunk) {
        launchCustom($test, $chunk);
    }
}

test('creating a saved set with arbitrary ids does not exempt them from the budget', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite();
    spendBudget($this);

    $harvest = budgetItems(20);
    $this->post(route('drills.saved-sets.store'), ['name' => 'Loot', 'question_ids' => $harvest])->assertSessionHasNoErrors();
    expect(SavedDrillSet::where('user_id', $user->id)->first()->questions()->count())->toBe(20);

    expect(launchCustom($this, $harvest))->toBe([]);
});

test('bookmarking an arbitrary id still works but does not exempt it from the budget', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite();
    spendBudget($this);

    $id = budgetItems(1)[0];
    $this->postJson(route('drills.saved-sets.addQuestion'), ['question_id' => $id, 'new_set_name' => 'Later'])->assertSuccessful();
    expect(SavedDrillSet::where('user_id', $user->id)->whereHas('questions', fn ($q) => $q->whereKey($id))->exists())->toBeTrue();

    expect(launchCustom($this, [$id]))->toBe([]);
});

test('a saved set built within budget remains reviewable after the budget is spent', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite();
    $set = budgetItems(5);
    $this->post(route('drills.saved-sets.store'), ['name' => 'Review', 'question_ids' => $set]);
    expect(launchCustom($this, $set))->toEqualCanonicalizing($set);

    spendBudget($this);
    expect(launchCustom($this, $set))->toEqualCanonicalizing($set);
});

test('repeat requests for the same id are charged once', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite();
    $ids = budgetItems(10);
    foreach (range(1, 5) as $_) {
        launchCustom($this, $ids);
    }
    expect((int) DB::table('custom_drill_budgets')->where('principal', 'u:'.$user->id)->value('used'))->toBe(10)
        ->and(DB::table('custom_drill_grants')->where('principal', 'u:'.$user->id)->count())->toBe(10);
});

test('a grant recorded by a concurrent request is not charged again and cannot overspend', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->withoutVite();
    $p = 'u:'.$user->id;
    $day = now()->toDateString();
    // Another request already spent 99 and granted $raced.
    $raced = budgetItems(1)[0];
    DB::table('custom_drill_budgets')->insert(['principal' => $p, 'day' => $day, 'used' => 99, 'created_at' => now(), 'updated_at' => now()]);
    DB::table('custom_drill_grants')->insert(['principal' => $p, 'question_id' => $raced, 'granted_on' => $day, 'created_at' => now(), 'updated_at' => now()]);

    $fresh = budgetItems(5);
    $served = launchCustom($this, array_merge([$raced], $fresh));

    expect($served)->toContain($raced)
        ->and(count(array_intersect($served, $fresh)))->toBe(1)
        ->and((int) DB::table('custom_drill_budgets')->where('principal', $p)->value('used'))->toBe(100);
});

test('the database refuses a duplicate grant for the same principal and question', function () {
    $row = ['principal' => 'u:1', 'question_id' => 7, 'granted_on' => now()->toDateString(), 'created_at' => now(), 'updated_at' => now()];
    DB::table('custom_drill_grants')->insert($row);
    expect(fn () => DB::table('custom_drill_grants')->insert($row))->toThrow(QueryException::class);
    expect(fn () => DB::table('custom_drill_budgets')->insert(array_merge(['principal' => 'u:1', 'day' => now()->toDateString(), 'used' => 0], ['created_at' => now(), 'updated_at' => now()])))->not->toThrow(QueryException::class);
    expect(fn () => DB::table('custom_drill_budgets')->insert(['principal' => 'u:1', 'day' => now()->toDateString(), 'used' => 0, 'created_at' => now(), 'updated_at' => now()]))->toThrow(QueryException::class);
});

test('guests spend a budget and cannot create saved sets', function () {
    $this->withoutVite();
    $status = $this->post(route('drills.saved-sets.store'), ['name' => 'x', 'question_ids' => budgetItems(1)])->status();
    expect($status)->toBeIn([302, 401, 403, 404]);
    expect(SavedDrillSet::count())->toBe(0);

    $served = [];
    foreach (array_chunk(budgetItems(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET + 10), ExamSessionQueryData::MAX_CUSTOM_IDS) as $chunk) {
        $served = array_merge($served, launchCustom($this, $chunk));
    }
    expect(count(array_unique($served)))->toBe(ExamService::CUSTOM_UNSEEN_DAILY_BUDGET);
});

test('residual: each account has its own budget (multi-account limitation, documented)', function () {
    [$a, $b] = User::factory()->count(2)->create();
    $this->withoutVite();
    $this->actingAs($a);
    spendBudget($this);
    $ids = budgetItems(10);
    expect(launchCustom($this, $ids))->toBe([]);

    $this->actingAs($b);
    expect(launchCustom($this, $ids))->toEqualCanonicalizing($ids);
});
