<?php

declare(strict_types=1);

use App\Http\Resources\DrillQuestionResource;
use App\Models\Category;
use App\Models\ExamSession;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Http\Request;

/**
 * Drill payloads carry stems and choices only. Keys and explanations for bank
 * items stay on the server; drills run on /exams with shuffled, keyless items
 * and server grading. A learner still sees the key of their own question.
 */
function drillKeySubcategory(): Subcategory
{
    $category = Category::create(['name' => 'Numerical Ability', 'slug' => 'numerical-ability']);

    return Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Word Problems',
        'slug' => 'word-problems',
        'language' => 'English',
    ]);
}

test('drills hub does not ship bank answer keys or explanations', function () {
    $user = User::factory()->create();
    $sub = drillKeySubcategory();
    $bank = Question::factory()->create(['subcategory_id' => $sub->id, 'created_by' => null, 'correct_option' => 2]);
    $own = Question::factory()->create(['subcategory_id' => $sub->id, 'created_by' => $user->id, 'correct_option' => 1]);
    $other = Question::factory()->create(['subcategory_id' => $sub->id, 'created_by' => User::factory()->create()->id]);

    $response = $this->actingAs($user)->get(route('drills.index'));

    $response->assertOk();
    $questions = collect($response->viewData('page')['props']['questions'])->keyBy('id');

    expect($questions[$bank->id])->not->toHaveKeys(['correct_option', 'explanation'])
        ->and($questions[$bank->id]['options'])->toHaveCount(4);

    expect($questions[$other->id])->not->toHaveKeys(['correct_option', 'explanation'])
        ->and($questions[$own->id])->not->toHaveKeys(['correct_option', 'explanation']);
});

test('saved set questions endpoint is keyless for bank items', function () {
    $user = User::factory()->create();
    $sub = drillKeySubcategory();
    $bank = Question::factory()->create(['subcategory_id' => $sub->id, 'created_by' => null]);
    $set = SavedDrillSet::create(['user_id' => $user->id, 'name' => 'Set', 'color' => 'blue']);
    $set->questions()->attach($bank->id);

    $response = $this->actingAs($user)->getJson(route('drills.saved-sets.getSetQuestions', $set));

    $response->assertOk();
    expect($response->json('questions.0'))->toHaveKey('id')
        ->not->toHaveKeys(['correct_option', 'explanation']);
});

test('smart weakness endpoint is keyless for bank items', function () {
    $user = User::factory()->create();
    $sub = drillKeySubcategory();
    Question::factory()->count(3)->create(['subcategory_id' => $sub->id, 'created_by' => null]);

    $response = $this->actingAs($user)->getJson(route('drills.smartWeakness'));

    $response->assertOk();
    foreach ($response->json('questions') as $item) {
        expect($item)->not->toHaveKeys(['correct_option', 'explanation']);
    }
});

test('a learner still gets the key back for the question they create', function () {
    $user = User::factory()->create();
    $sub = drillKeySubcategory();

    $response = $this->actingAs($user)->postJson(route('drills.custom-questions.store'), [
        'subcategory_id' => $sub->id,
        'stem' => 'What comes next: 2, 4, 8, 16?',
        'options' => ['18', '24', '32', '30'],
        'correct_option' => 2,
        'explanation' => 'Each number doubles the previous number.',
    ]);

    $response->assertCreated();
    expect($response->json('question.correct_option'))->toBe(2);
});

test('active bank keys stay hidden from their author across drill entry points', function (string $entry, bool $strict) {
    $user = User::factory()->create();
    $sub = drillKeySubcategory();
    $questions = collect([$user->id, null, User::factory()->create()->id])->map(fn ($author) => Question::factory()->create([
        'subcategory_id' => $sub->id, 'created_by' => $author, 'status' => 'active',
    ]));
    $set = SavedDrillSet::create(['user_id' => $user->id, 'name' => 'Author regression', 'color' => 'blue']);
    $set->questions()->attach($questions->pluck('id')->all());
    if ($strict) {
        ExamSession::create([
            'user_id' => $user->id, 'track' => 'Professional', 'mode' => 'strict',
            'question_ids' => $questions->pluck('id')->all(),
        ]);
    }
    $this->actingAs($user);
    if ($entry === 'hub') {
        $response = $this->get(route('drills.index'))->assertOk();
        $items = collect($response->viewData('page')['props']['questions']);
    } else {
        $url = $entry === 'saved' ? route('drills.saved-sets.getSetQuestions', $set) : route('drills.smartWeakness');
        $items = collect($this->getJson($url)->assertOk()->json('questions'));
    }
    expect($items)->toHaveCount(3)
        ->and($items->pluck('id')->sort()->values()->all())->toBe($questions->pluck('id')->sort()->values()->all());
    foreach ($items as $item) {
        expect($item)->not->toHaveKeys(['correct_option', 'explanation']);
    }
})->with(['hub', 'saved', 'weakness'])->with([false, true]);

test('unpublished custom keys are visible only to their owner', function (string $viewer) {
    $owner = User::factory()->create();
    $draft = Question::factory()->create(['created_by' => $owner->id, 'status' => 'draft', 'correct_option' => 2]);
    $user = match ($viewer) {
        'owner' => $owner,
        'other' => User::factory()->create(),
        default => null,
    };
    $request = Request::create('/drills');
    $request->setUserResolver(fn () => $user);
    $item = (new DrillQuestionResource($draft))->resolve($request);
    if ($viewer === 'owner') {
        expect($item['correct_option'])->toBe(2)->and($item['explanation'])->toBe($draft->explanation);
    } else {
        expect($item)->not->toHaveKeys(['correct_option', 'explanation']);
    }
})->with(['owner', 'other', 'guest']);

test('guest drill hub remains usable without bank keys', function () {
    config(['civio.guest_unlimited' => true]);
    Question::factory()->create(['subcategory_id' => drillKeySubcategory()->id, 'status' => 'active']);
    $response = $this->get(route('drills.index'))->assertOk();
    $items = $response->viewData('page')['props']['questions'];
    expect($items)->toHaveCount(1);
    expect($items[0])->toHaveKeys(['id', 'stem', 'options'])->not->toHaveKeys(['correct_option', 'explanation']);
});
