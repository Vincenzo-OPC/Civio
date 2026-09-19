<?php

declare(strict_types=1);

use App\DTOs\Drill\BookmarkQuestionData;
use App\Http\Resources\DrillQuestionResource;
use App\Http\Resources\SavedDrillSetResource;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;
use App\Repositories\SavedDrillSetRepositoryInterface;
use App\Services\DrillService;

test('saved drill set repository creates, lists, and detaches questions correctly', function () {
    $user = User::factory()->create();
    $repo = app(SavedDrillSetRepositoryInterface::class);

    $category = Category::create(['name' => 'General Info', 'slug' => 'general-info']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Constitution',
        'slug' => 'constitution',
        'language' => 'English',
    ]);
    $question = Question::factory()->create(['subcategory_id' => $subcategory->id]);

    $set = $repo->createWithQuestions($user->id, [
        'name' => 'Civics Focus',
        'description' => 'Philippine Constitution drill set',
        'color' => 'indigo',
    ], [$question->id]);

    expect($set)->toBeInstanceOf(SavedDrillSet::class)
        ->and($set->name)->toBe('Civics Focus');

    $sets = $repo->getUserSets($user->id);
    expect($sets)->toHaveCount(1)
        ->and($sets->first()->questions_count)->toBe(1);

    $remaining = $repo->detachQuestion($set, $question->id);
    expect($remaining)->toBe(0);
});

test('drill service calculates smart weakness based on low-accuracy subcategories', function () {
    $user = User::factory()->create();
    $service = app(DrillService::class);

    $category = Category::create(['name' => 'Numerical', 'slug' => 'numerical']);
    $weakSubcat = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Fractions & Decimals',
        'slug' => 'fractions-decimals',
        'language' => 'English',
    ]);
    $strongSubcat = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Basic Algebra',
        'slug' => 'basic-algebra',
        'language' => 'English',
    ]);

    Question::factory()->count(3)->create(['subcategory_id' => $weakSubcat->id, 'status' => 'active']);
    Question::factory()->count(3)->create(['subcategory_id' => $strongSubcat->id, 'status' => 'active']);

    // Record an attempt with low score in Fractions (30% < 65%) and high score in Algebra (90%)
    ExamAttempt::create([
        'user_id' => $user->id,
        'category_id' => $category->id,
        'question_ids' => [1, 2, 3],
        'answers' => [1, 0, 1],
        'cat_scores' => [
            'categoryScoreMap' => [
                'Numerical' => [
                    'subcats' => [
                        'Fractions & Decimals' => ['correct' => 3, 'total' => 10],
                        'Basic Algebra' => ['correct' => 9, 'total' => 10],
                    ],
                ],
            ],
        ],
    ]);

    $result = $service->getSmartWeaknessQuestions($user->id);

    expect($result['weak_subcategories'])->toContain('Fractions & Decimals')
        ->and($result['weak_subcategories'])->not->toContain('Basic Algebra')
        ->and(count($result['questions']))->toBeGreaterThanOrEqual(1);
});

test('drill service bookmarks question into default Bookmarked Items set when no set is specified', function () {
    $user = User::factory()->create();
    $service = app(DrillService::class);
    $question = Question::factory()->create();

    $dto = new BookmarkQuestionData(questionId: $question->id);
    $result = $service->bookmarkQuestion($user->id, $dto);

    expect($result['status'])->toBe('success')
        ->and($result['set_name'])->toBe('Bookmarked Items')
        ->and($result['question_id'])->toBe($question->id);

    $this->assertDatabaseHas('saved_drill_sets', [
        'user_id' => $user->id,
        'name' => 'Bookmarked Items',
    ]);
});

test('user cannot view, update, delete, or detach from another user saved drill set', function () {
    $owner = User::factory()->create();
    $stranger = User::factory()->create();
    $question = Question::factory()->create();

    $set = SavedDrillSet::create([
        'user_id' => $owner->id,
        'name' => 'Owner Practice Set',
        'color' => 'rose',
    ]);
    $set->questions()->attach($question->id);

    // 1. Stranger cannot get set questions
    $this->actingAs($stranger)->getJson(route('drills.saved-sets.getSetQuestions', $set))
        ->assertForbidden();

    // 2. Stranger cannot update set
    $this->actingAs($stranger)->putJson(route('drills.saved-sets.update', $set), [
        'name' => 'Hacked Name',
    ])->assertForbidden();

    // 3. Stranger cannot remove question
    $this->actingAs($stranger)->deleteJson(route('drills.saved-sets.removeQuestion', [$set, $question]))
        ->assertForbidden();

    // 4. Stranger cannot delete set
    $this->actingAs($stranger)->deleteJson(route('drills.saved-sets.destroy', $set))
        ->assertForbidden();
});

test('saved drill set and drill question resources format payloads cleanly', function () {
    $user = User::factory()->create();
    $category = Category::create(['name' => 'Verbal Ability', 'slug' => 'verbal-ability']);
    $subcategory = Subcategory::create([
        'category_id' => $category->id,
        'name' => 'Grammar & Correct Usage',
        'slug' => 'grammar-correct-usage',
        'language' => 'English',
    ]);
    $question = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'created_by' => $user->id,
    ]);

    $set = SavedDrillSet::create([
        'user_id' => $user->id,
        'name' => 'Grammar Review Set',
        'color' => 'purple',
    ]);
    $set->questions()->attach($question->id);

    $setResource = (new SavedDrillSetResource($set))->resolve();
    expect($setResource['name'])->toBe('Grammar Review Set')
        ->and($setResource['color'])->toBe('purple')
        ->and($setResource['questions_count'])->toBe(1);

    $questionResource = (new DrillQuestionResource($question))->resolve();
    expect($questionResource['id'])->toBe($question->id)
        ->and($questionResource['category'])->toBe('Verbal Ability')
        ->and($questionResource['isCustom'])->toBeTrue();
});
