<?php

use App\Support\QuestionStem;

test('question stems ignore variant suffixes', function () {
    expect(QuestionStem::normalize('The supreme law (variant 3)'))
        ->toBe(QuestionStem::normalize('The supreme law'));
    expect(QuestionStem::isVariant('The supreme law (variant 8)'))->toBeTrue();
    expect(QuestionStem::withoutVariantSuffix('The supreme law (variant 2)'))
        ->toBe('The supreme law');
});
