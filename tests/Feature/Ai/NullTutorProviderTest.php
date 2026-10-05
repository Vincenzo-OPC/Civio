<?php

use App\Ai\Contracts\TutorProvider;
use App\Ai\Providers\NullTutorProvider;

test('container resolves TutorProvider to Null by default', function () {
    $provider = app(TutorProvider::class);
    expect($provider)->toBeInstanceOf(NullTutorProvider::class);
    expect($provider->name())->toBe('null');
});

test('null provider explainAnswer falls back to bank explanation', function () {
    $provider = new NullTutorProvider;
    $result = $provider->explainAnswer([
        'stem' => 'What is 2+2?',
        'options' => ['3', '4', '5', '6'],
        'correct_option' => 1,
        'explanation' => 'Basic arithmetic.',
    ]);

    expect($result['provider'])->toBe('null');
    expect($result['explanation'])->toBe('Basic arithmetic.');
});

test('null provider generateHint returns safe stub', function () {
    $provider = new NullTutorProvider;
    $result = $provider->generateHint([
        'stem' => 'Pick the analogy',
        'options' => ['A', 'B', 'C', 'D'],
    ]);

    expect($result['hint'])->not->toBeEmpty();
    expect($result['provider'])->toBe('null');
});

test('null provider classifyMistake distinguishes wrong vs correct', function () {
    $provider = new NullTutorProvider;
    $wrong = $provider->classifyMistake([
        'stem' => 'x',
        'options' => ['a', 'b'],
        'correct_option' => 1,
        'chosen_option' => 0,
    ]);
    $right = $provider->classifyMistake([
        'stem' => 'x',
        'options' => ['a', 'b'],
        'correct_option' => 1,
        'chosen_option' => 1,
    ]);

    expect($wrong['classification'])->toBe('incorrect_selection');
    expect($right['classification'])->toBe('correct');
});
