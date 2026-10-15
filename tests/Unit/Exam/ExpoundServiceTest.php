<?php

declare(strict_types=1);

use App\Models\Question;
use App\Services\Exam\ExpoundService;

it('walks an order-of-operations stem with PEMDAS', function () {
    $question = new Question([
        'stem' => 'Evaluate: 15 - 3 times 4 + 6',
        'options' => ['12', '9', '18', '3'],
        'correct_option' => 1,
        'explanation' => 'Multiplication first: 15 - 12 + 6 = 9.',
    ]);

    $expound = (new ExpoundService)->forQuestion($question);
    $text = implode("\n", $expound['steps']);

    expect($expound['rule'])->toContain('PEMDAS')
        ->and($text)->toContain('3 × 4 = 12.')
        ->and($text)->toContain('15 − 12 = 3.')
        ->and($text)->toContain('3 + 6 = 9.');
});

it('walks a worded evaluate stem left to right', function () {
    $question = new Question([
        'stem' => 'Evaluate 18 minus 4 multiplied by 3, then add 6.',
        'options' => ['48', '12', '16', '60'],
        'correct_option' => 1,
        'explanation' => 'Short stored line.',
    ]);

    $text = implode("\n", (new ExpoundService)->forQuestion($question)['steps']);

    expect($text)->toContain('4 × 3 = 12.')
        ->and($text)->toContain('6 + 6 = 12.');
});

it('keeps the stored explanation when the walk disagrees with the key', function () {
    $question = new Question([
        'stem' => 'Evaluate: 15 - 3 times 4 + 6',
        'options' => ['1', '2', '3', '4'],
        'correct_option' => 0,
        'explanation' => 'Stored work stays. The matching choice is “1.” “2”, “3”, “4” do not follow the same steps.',
    ]);

    $expound = (new ExpoundService)->forQuestion($question);

    expect($expound['rule'])->toBeNull()
        ->and($expound['steps'])->toBe(['Stored work stays.']);
});

it('splits a stored explanation and drops the choice boilerplate', function () {
    $question = new Question([
        'stem' => 'What is 20 percent of 200 forms?',
        'options' => ['41', '60', '40', '39'],
        'correct_option' => 2,
        'explanation' => '20 percent is 20/100. 200 times 20, divided by 100, is 40. The matching choice is “40.” “41”, “60”, “39” do not follow the same steps.',
    ]);

    $expound = (new ExpoundService)->forQuestion($question);

    expect($expound['steps'])->toBe([
        '20 percent is 20/100.',
        '200 times 20, divided by 100, is 40.',
    ]);
});
