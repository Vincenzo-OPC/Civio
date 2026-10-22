<?php

use App\Services\Exam\MockPoolSelector;

function engClerical(int $id): array
{
    return ['id' => $id, 'stem' => "Clerical item number {$id} unique stem text", 'options' => ["a{$id}", "b{$id}", "c{$id}", "d{$id}"], 'correct' => 0, 'category' => 'Clerical Ability', 'subcategory' => 'Spelling', 'language' => 'English', 'isDemographic' => false];
}

function engFil(int $id, array $options, int $correct, string $stem): array
{
    return ['id' => $id, 'stem' => $stem, 'options' => $options, 'correct' => $correct, 'category' => 'Verbal Ability', 'subcategory' => 'Filipino', 'language' => 'Filipino', 'isDemographic' => false];
}

test('weak-category top-up never adds a key-trap pair the blueprint picks would refuse', function () {
    $bank = array_map('engClerical', range(100, 160));
    $bank[] = engFil(1, ['tuyo', 'napakalaki', 'malago', 'mabango'], 2, 'Kahulugan ng MAYABONG?');
    $bank[] = engFil(2, ['kalbo', 'mabango', 'malago', 'lubos na patay'], 0, 'Kasalungat ng MALABAY?');

    for ($run = 0; $run < 20; $run++) {
        $ids = array_column((new MockPoolSelector)->select($bank, MockPoolSelector::SUBPROFESSIONAL, ['weakCategories' => ['Verbal Ability']])['items'], 'id');
        expect(in_array(1, $ids, true) && in_array(2, $ids, true))->toBeFalse()
            ->and(count($ids))->toBe(count(array_unique($ids)));
    }
});

function engBank(array $sizes): array
{
    $bank = [];
    $id = 1000;
    foreach ($sizes as $cat => $n) {
        for ($i = 0; $i < $n; $i++) {
            $id++;
            $bank[] = ['id' => $id, 'stem' => "{$id} {$cat} question stem", 'options' => ["w{$id}", "x{$id}", "y{$id}", "z{$id}"], 'correct' => 0, 'category' => $cat, 'subcategory' => $cat.' '.($i % 3), 'language' => 'English', 'isDemographic' => false];
        }
    }

    return $bank;
}

dataset('levels', [
    'Subprofessional' => [MockPoolSelector::SUBPROFESSIONAL, ['Verbal Ability' => 120, 'Clerical Ability' => 120, 'Numerical Ability' => 120, 'General Information' => 60, 'Analytical Ability' => 60]],
    'Professional' => [MockPoolSelector::PROFESSIONAL, ['Verbal Ability' => 120, 'Analytical Ability' => 120, 'Numerical Ability' => 120, 'General Information' => 60, 'Clerical Ability' => 60]],
]);

test('full mocks keep the blueprint exactly, even with strong weakness bias', function (string $level, array $sizes) {
    $bank = engBank($sizes);
    $wrong = array_column(array_filter($bank, fn ($q) => $q['category'] === 'Verbal Ability'), 'id');
    $expected = array_column(MockPoolSelector::BLUEPRINT[$level], 'count', 'category');

    for ($run = 0; $run < 10; $run++) {
        $items = (new MockPoolSelector)->select($bank, $level, [
            'weakCategories' => ['Verbal Ability'], 'wrongIds' => $wrong, 'weakSubcategories' => ['Verbal Ability 0'],
        ])['items'];
        $counts = array_count_values(array_column($items, 'category'));
        ksort($counts);
        ksort($expected);

        expect($counts)->toBe($expected)
            ->and(count($items))->toBe(MockPoolSelector::targetFor($level))
            ->and(count(array_unique(array_column($items, 'id'))))->toBe(count($items));
    }
})->with('levels');
