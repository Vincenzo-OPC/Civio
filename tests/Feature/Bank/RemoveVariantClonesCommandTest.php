<?php

use App\Enums\QuestionStatus;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\Feedback;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\Cache;

/**
 * @return array{base: Question, clones: list<Question>, user: User}
 */
function variantCloneFamily(int $copies = 5): array
{
    $user = User::factory()->create();
    $category = Category::factory()->create(['name' => 'Verbal Ability', 'is_demographic' => false]);
    $sub = Subcategory::factory()->create(['category_id' => $category->id]);
    $make = fn (string $stem) => Question::factory()->create([
        'subcategory_id' => $sub->id,
        'created_by' => $user->id,
        'status' => 'active',
        'stem' => $stem,
        'options' => ['Careful', 'Careless', 'Loud', 'Late'],
        'correct_option' => 0,
    ]);

    $base = $make('Choose the word closest in meaning to METICULOUS.');
    $clones = [];

    for ($copy = 2; $copy <= $copies + 1; $copy++) {
        $clones[] = $make("Choose the word closest in meaning to METICULOUS. (variant {$copy})");
    }

    return ['base' => $base, 'clones' => $clones, 'user' => $user];
}

test('deletes unreferenced clones and archives referenced ones as draft', function () {
    ['base' => $base, 'clones' => [$inAttempt, $inAnswers, $inDrill, $flagged, $free], 'user' => $user] = variantCloneFamily(5);
    $realLookalike = Question::factory()->create([
        'stem' => 'Which word names a variant spelling of "colour"?',
        'status' => 'active',
    ]);

    ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [$base->id, $inAttempt->id],
        'answers' => [(string) $base->id => 0],
        'cat_scores' => [],
    ]);
    ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [],
        'answers' => [(string) $inAnswers->id => 1],
        'cat_scores' => [],
    ]);
    $set = SavedDrillSet::create(['user_id' => $user->id, 'name' => 'Mine']);
    $set->questions()->attach($inDrill->id);
    Feedback::factory()->create([
        'user_id' => $user->id,
        'flaggable_type' => Question::class,
        'flaggable_id' => $flagged->id,
    ]);
    Cache::forever('questions.active', collect(['stale']));

    $this->artisan('civio:remove-variant-clones')
        ->expectsOutputToContain('Deleted: 1, archived: 4, skipped (already archived): 0. Clones found: 5.')
        ->assertSuccessful();

    expect(Question::find($free->id))->toBeNull();

    foreach ([$inAttempt, $inAnswers, $inDrill, $flagged] as $clone) {
        expect($clone->fresh()->status)->toBe(QuestionStatus::Draft);
    }

    expect($base->fresh()->status)->toBe(QuestionStatus::Active)
        ->and($realLookalike->fresh()->status)->toBe(QuestionStatus::Active)
        ->and(Cache::has('questions.active'))->toBeFalse()
        ->and(Question::where('status', 'active')->pluck('stem')->filter(
            fn ($stem) => preg_match('/\(variant\s*\d+\)/i', $stem)
        ))->toBeEmpty();
});

test('is idempotent: a second run only reports skipped archived rows', function () {
    ['clones' => [$referenced, $free], 'user' => $user] = variantCloneFamily(2);
    ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [$referenced->id],
        'answers' => [],
        'cat_scores' => [],
    ]);

    $this->artisan('civio:remove-variant-clones')
        ->expectsOutputToContain('Deleted: 1, archived: 1, skipped (already archived): 0.')
        ->assertSuccessful();

    $snapshot = Question::orderBy('id')->get(['id', 'status', 'updated_at'])->toArray();

    $this->artisan('civio:remove-variant-clones')
        ->expectsOutputToContain('Deleted: 0, archived: 0, skipped (already archived): 1.')
        ->assertSuccessful();

    expect(Question::orderBy('id')->get(['id', 'status', 'updated_at'])->toArray())->toBe($snapshot)
        ->and(Question::find($free->id))->toBeNull();
});

test('dry run reports counts and changes nothing', function () {
    ['clones' => $clones, 'user' => $user] = variantCloneFamily(8);
    ExamAttempt::create([
        'user_id' => $user->id,
        'question_ids' => [$clones[0]->id],
        'answers' => [],
        'cat_scores' => [],
    ]);
    $before = Question::orderBy('id')->get(['id', 'status', 'stem', 'updated_at'])->toArray();

    $this->artisan('civio:remove-variant-clones', ['--dry-run' => true])
        ->expectsOutputToContain('[dry run] Would delete: 7, would archive: 1, skipped (already archived): 0. Clones found: 8.')
        ->assertSuccessful();

    expect(Question::orderBy('id')->get(['id', 'status', 'stem', 'updated_at'])->toArray())->toBe($before);
});

test('reports zero when there are no clones', function () {
    Question::factory()->count(3)->create(['status' => 'active']);

    $this->artisan('civio:remove-variant-clones')
        ->expectsOutputToContain('No "(variant N)" clones found.')
        ->assertSuccessful();

    expect(Question::count())->toBe(3);
});
