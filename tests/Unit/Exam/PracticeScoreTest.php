<?php

use App\Services\ExamAttemptFormatter;

test('a practice score is the raw item percentage, not a category weight', function () {
    $score = app(ExamAttemptFormatter::class)->calculateWeightedPercentage([
        'categoryScoreMap' => [
            'Verbal Ability' => ['correct' => 1, 'total' => 1],
            'General Information' => ['correct' => 0, 'total' => 1],
        ],
        'metadata' => [
            'correct_count' => 1,
            'total_questions' => 2,
        ],
    ]);

    expect($score)->toBe(50.0);
});

test('an older attempt without metadata sums the stored item counts', function () {
    $score = app(ExamAttemptFormatter::class)->calculateWeightedPercentage([
        'categoryScoreMap' => [
            'Numerical Ability' => ['correct' => 1, 'total' => 4],
        ],
    ]);

    expect($score)->toBe(25.0);
});
