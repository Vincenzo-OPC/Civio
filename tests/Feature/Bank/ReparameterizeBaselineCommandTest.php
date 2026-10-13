<?php

use App\Enums\QuestionSourceGroup;
use App\Enums\QuestionStatus;
use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

test('reparameterize command drafts the prior stem and serves the new item', function () {
    $rows = json_decode((string) file_get_contents(base_path('scripts/seeds/baseline_reparameterized.json')), true, 512, JSON_THROW_ON_ERROR);

    expect($rows)->toBeArray()->toHaveCount(496);

    $stems = array_column($rows, 'stem');
    expect($stems)->toHaveCount(496)->and(array_unique($stems))->toHaveCount(496);

    foreach ($rows as $row) {
        expect($row['options'])->toHaveCount(4)
            ->and(array_unique($row['options']))->toHaveCount(4)
            ->and($row['correct_option'])->toBeGreaterThanOrEqual(0)
            ->and($row['correct_option'])->toBeLessThan(4)
            ->and($row['stem'])->not->toBe($row['prior_stem'])
            ->and($row['explanation'])->not->toBeEmpty()
            ->and($row['stem'])->not->toContain('(variant');
    }

    $sample = $rows[0];
    $user = User::factory()->create();
    $category = Category::factory()->create(['name' => 'General Information', 'is_demographic' => false]);
    $subcategory = Subcategory::factory()->create(['category_id' => $category->id]);

    $old = Question::factory()->create([
        'subcategory_id' => $subcategory->id,
        'created_by' => $user->id,
        'status' => 'active',
        'source_group' => QuestionSourceGroup::Baseline,
        'stem' => $sample['prior_stem'],
        'options' => ['One', 'Two', 'Three', 'Four'],
        'correct_option' => 0,
    ]);

    $this->artisan('civio:reparameterize-baseline')
        ->expectsOutputToContain('Inserted: 1')
        ->assertSuccessful();

    $old->refresh();
    $replacement = Question::query()->where('stem', $sample['stem'])->first();

    expect($old->status)->toBe(QuestionStatus::Draft)
        ->and($replacement)->not->toBeNull()
        ->and($replacement->status)->toBe(QuestionStatus::Active)
        ->and($replacement->source_group)->toBe(QuestionSourceGroup::Civio)
        ->and($replacement->replaces_question_id)->toBe($old->id)
        ->and($replacement->correct_option)->toBe($sample['correct_option']);

    $this->artisan('civio:reparameterize-baseline')
        ->expectsOutputToContain('Inserted: 0')
        ->assertSuccessful();

    expect(Question::query()->where('stem', $sample['stem'])->count())->toBe(1);
});
