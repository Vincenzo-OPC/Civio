<?php

use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;

function bankQuestion(array $attributes): Question
{
    $category = Category::factory()->create(['name' => 'Numerical Ability', 'is_demographic' => false]);
    $sub = Subcategory::factory()->create(['category_id' => $category->id]);

    return Question::factory()->create(array_merge([
        'subcategory_id' => $sub->id,
        'created_by' => User::factory()->create()->id,
        'status' => 'active',
        'correct_option' => 0,
    ], $attributes));
}

test('repairs ?? rows from the UTF-8 reference, is idempotent, and lists what it cannot fix', function () {
    $reference = tempnam(sys_get_temp_dir(), 'civio-ref').'.sql';
    file_put_contents($reference, <<<'SQL'
        INSERT INTO questions (subcategory_id, language, stem, options, correct_option, explanation) VALUES
        (1, 'English', 'What is 18 ÷ 3 × 2?', '["12","3","9","₱6"]'::jsonb, 0, 'Work left to right: 18 ÷ 3 = 6, then 6 × 2 = 12.');
        INSERT INTO questions (subcategory_id, language, stem, options, correct_option, explanation) VALUES
        (1, 'English', 'Which shape comes next: ▲ ■ ▲ ■ ?', '["▲","■","●","◆"]'::jsonb, 0, 'The pattern alternates.');
        SQL);

    $fromSeed = bankQuestion([
        'stem' => 'What is 18 ?? 3 ?? 2?',
        'options' => ['12', '3', '9', '???6'],
        'explanation' => 'Work left to right: 18 ?? 3 = 6, then 6 ?? 2 = 12.',
    ]);
    $symbolOptions = bankQuestion([
        'stem' => 'Which shape comes next: ??? ??? ??? ??? ?',
        'options' => ['???', '???', '???', '???'],
        'explanation' => 'The pattern alternates.',
    ]);
    $arithmeticOnly = bankQuestion([
        'stem' => 'A clerk files 15 folders a day. How many in 4 days?',
        'options' => ['60', '19', '11', '45'],
        'explanation' => '15 ?? 4 = 60 folders.',
    ]);
    $unknown = bankQuestion([
        'stem' => 'The fee is ???500 per page. What is the total for 2 pages?',
        'options' => ['1000', '500', '250', '2000'],
        'explanation' => 'Multiply the fee by the pages.',
    ]);
    $clean = bankQuestion(['stem' => 'Is 3 × 3 = 9?', 'options' => ['Yes', 'No'], 'explanation' => 'Yes.']);

    $this->artisan('civio:repair-bank-encoding', ['--reference' => [$reference], '--no-default-references' => true])
        ->expectsOutputToContain('Repaired 3 question(s)')
        ->expectsOutputToContain("need a manual fix: {$unknown->id}")
        ->assertSuccessful();

    expect($fromSeed->fresh()->stem)->toBe('What is 18 ÷ 3 × 2?')
        ->and($fromSeed->fresh()->options)->toBe(['12', '3', '9', '₱6'])
        ->and($fromSeed->fresh()->explanation)->toBe('Work left to right: 18 ÷ 3 = 6, then 6 × 2 = 12.')
        ->and($symbolOptions->fresh()->stem)->toBe('Which shape comes next: ▲ ■ ▲ ■ ?')
        ->and($symbolOptions->fresh()->options)->toBe(['▲', '■', '●', '◆'])
        ->and($arithmeticOnly->fresh()->explanation)->toBe('15 × 4 = 60 folders.')
        ->and($unknown->fresh()->stem)->toBe('The fee is ???500 per page. What is the total for 2 pages?')
        ->and($clean->fresh()->stem)->toBe('Is 3 × 3 = 9?');

    // Second run changes nothing.
    $this->artisan('civio:repair-bank-encoding', ['--reference' => [$reference], '--no-default-references' => true])
        ->expectsOutputToContain('Repaired 0 question(s)')
        ->assertSuccessful();

    @unlink($reference);
});

test('dry run reports without saving', function () {
    $reference = tempnam(sys_get_temp_dir(), 'civio-ref').'.json';
    file_put_contents($reference, json_encode([['stem' => 'Simplify 6 × 7.']], JSON_UNESCAPED_UNICODE));

    $row = bankQuestion(['stem' => 'Simplify 6 ?? 7.', 'options' => ['42', '13'], 'explanation' => 'Multiply.']);

    $this->artisan('civio:repair-bank-encoding', ['--dry-run' => true, '--reference' => [$reference], '--no-default-references' => true])
        ->expectsOutputToContain('Would repair 1 question(s)')
        ->assertSuccessful();

    expect($row->fresh()->stem)->toBe('Simplify 6 ?? 7.');

    @unlink($reference);
});
