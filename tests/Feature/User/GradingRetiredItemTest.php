<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Services\ExamGradingService;

test('an item retired after it was served does not count against the examinee', function () {
    $sub = Subcategory::factory()->create(['category_id' => Category::factory()->create(['is_demographic' => false])->id]);
    $ids = Question::factory()->count(4)->create([
        'subcategory_id' => $sub->id, 'status' => 'active', 'options' => ['A', 'B', 'C', 'D'], 'correct_option' => 1,
    ])->pluck('id')->all();
    Question::whereKey($ids[3])->update(['status' => 'retired']);

    $result = app(ExamGradingService::class)->grade($ids, array_fill_keys($ids, 1));

    expect($result['score'])->toBe(100)
        ->and($result['total_questions'])->toBe(3)
        ->and($result['skipped_count'])->toBe(0)
        ->and($result['cat_scores']['metadata']['retired_count'])->toBe(1);
});
