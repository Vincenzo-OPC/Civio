<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;

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

    if ($questions->has($other->id)) {
        expect($questions[$other->id])->not->toHaveKeys(['correct_option', 'explanation']);
    }

    if ($questions->has($own->id)) {
        expect($questions[$own->id]['correct_option'])->toBe(1);
    }
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
