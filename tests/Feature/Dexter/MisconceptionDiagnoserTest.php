<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Services\Dexter\MisconceptionDiagnoser;

function dexterQuestion(array $attrs = []): Question
{
    $user = User::factory()->create();
    $category = Category::create(['name' => 'Numerical Ability', 'slug' => 'num-'.uniqid()]);
    $sub = Subcategory::create(['category_id' => $category->id, 'name' => 'Word problems', 'slug' => 'wp-'.uniqid()]);

    return Question::create(array_merge([
        'subcategory_id' => $sub->id,
        'stem' => 'A P800 bag is discounted 25%. What is the sale price?',
        'options' => ['P600', 'P200', 'P775', 'P1,000'],
        'correct_option' => 0,
        'created_by' => $user->id,
        'explanation' => '25% of 800 is 200; 800 - 200 = 600.',
        'status' => 'active',
        'archetype' => 'NUM-WP-PCT-CHANGE',
        'distractor_codes' => ['1' => 'NUM-PARTIAL', '2' => 'NUM-GIVEN-REUSED', '3' => 'NUM-OP-SWAP'],
    ], $attrs));
}

test('every taxonomy code has learner text', function () {
    foreach (config('dexter_misconceptions.codes') as $entry) {
        expect($entry['label'])->not->toBe('')->and($entry['method'])->not->toBe('');
    }
});

test('a wrong choice is diagnosed from its stored code', function () {
    $d = app(MisconceptionDiagnoser::class)->diagnose(dexterQuestion()->fresh(), 1);

    expect($d['code'])->toBe('NUM-PARTIAL')
        ->and($d['label'])->toBe('Stopped one step early')
        ->and($d['version'])->toBe(config('dexter_misconceptions.version'));
});

test('correct, skipped, untagged and unknown codes give no diagnosis', function () {
    $diag = app(MisconceptionDiagnoser::class);
    $q = dexterQuestion();

    expect($diag->diagnose($q, 0))->toBeNull()
        ->and($diag->diagnose($q, null))->toBeNull()
        ->and($diag->diagnose(dexterQuestion(['distractor_codes' => null]), 1))->toBeNull()
        ->and($diag->diagnose(dexterQuestion(['distractor_codes' => ['1' => 'MADE-UP']]), 1))->toBeNull();
});

test('QA problems flag bad indexes, codes on the key and unknown codes', function () {
    $diag = app(MisconceptionDiagnoser::class);

    expect($diag->problems(dexterQuestion()))->toBe([])
        ->and($diag->problems(dexterQuestion(['distractor_codes' => null])))->toBe([]);

    $problems = $diag->problems(dexterQuestion(['distractor_codes' => ['0' => 'NUM-PARTIAL', '7' => 'NUM-UNIT', '2' => 'NOPE']]));
    expect($problems)->toHaveCount(3);
});

test('distractor codes never serialize to a client', function () {
    expect(dexterQuestion()->toArray())->not->toHaveKey('distractor_codes');
});
