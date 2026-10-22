<?php

use App\Enums\ExamMode;
use App\Enums\SelectionPolicy;
use App\Services\Exam\MockPoolSelector;
use Random\Engine\Xoshiro256StarStar;
use Random\Randomizer;

/**
 * Build a synthetic bank row set shaped like the selector input.
 *
 * @param  array<string, array<string, int>>  $layout  category => [subcategory => count]
 * @return array<int, array<string, mixed>>
 */
function selectorBank(array $layout, int &$nextId = 1, string $language = 'English'): array
{
    $rows = [];

    foreach ($layout as $category => $subs) {
        foreach ($subs as $sub => $count) {
            for ($i = 0; $i < $count; $i++) {
                $id = $nextId++;
                $rows[] = [
                    'id' => $id,
                    'stem' => "Item {$id}: {$category} / {$sub} question number {$i} with its own wording?",
                    'options' => ["A{$id}", "B{$id}", "C{$id}", "D{$id}"],
                    'category' => $category,
                    'subcategory' => $sub,
                    'language' => $language,
                    'isDemographic' => false,
                    'explanation' => '',
                ];
            }
        }
    }

    return $rows;
}

function fullProBank(): array
{
    $id = 1;

    return [
        ...selectorBank(['Verbal Ability' => ['Word analogy' => 40, 'Grammar' => 40]], $id),
        ...selectorBank(['Verbal Ability' => ['Word analogy' => 30, 'Grammar' => 30]], $id, 'Filipino'),
        ...selectorBank(['Analytical Ability' => ['Logic' => 50, 'Data interpretation' => 50]], $id),
        ...selectorBank(['Numerical Ability' => ['Arithmetic' => 50, 'Word problems' => 50]], $id),
        ...selectorBank(['General Information' => ['Constitution' => 20]], $id),
        ...selectorBank(['Clerical Ability' => ['Filing' => 60]], $id),
    ];
}

function seededSelector(int $seed = 7): MockPoolSelector
{
    return new MockPoolSelector(new Randomizer(new Xoshiro256StarStar($seed)));
}

test('full bank gives exactly 150 unique Professional items with blueprint quotas', function () {
    $result = seededSelector()->select(fullProBank(), MockPoolSelector::PROFESSIONAL);
    $items = $result['items'];

    expect($items)->toHaveCount(150)
        ->and($result['target'])->toBe(150)
        ->and($result['short'])->toBeFalse();

    $ids = array_column($items, 'id');
    expect(array_unique($ids))->toHaveCount(150);

    $perCategory = array_count_values(array_column($items, 'category'));
    ksort($perCategory);
    expect($perCategory)->toBe([
        'Analytical Ability' => 52,
        'General Information' => 8,
        'Numerical Ability' => 45,
        'Verbal Ability' => 45,
    ]);

    // Verbal is split between English and Filipino.
    $filipino = array_filter($items, fn ($q) => $q['category'] === 'Verbal Ability' && $q['language'] === 'Filipino');
    expect(count($filipino))->toBeGreaterThanOrEqual(15);
});

test('Subprofessional targets 145 and uses Clerical instead of Analytical', function () {
    $result = seededSelector()->select(fullProBank(), MockPoolSelector::SUBPROFESSIONAL);
    $perCategory = array_count_values(array_column($result['items'], 'category'));

    expect($result['items'])->toHaveCount(145)
        ->and($perCategory['Clerical Ability'] ?? 0)->toBe(47)
        ->and($perCategory)->not->toHaveKey('Analytical Ability');
});

test('variant clones, exact copies and demographics never reach a mock', function () {
    $bank = fullProBank();
    $copyOf = $bank[0];
    $bank[] = [...$copyOf, 'id' => 90001];
    $bank[] = [...$copyOf, 'id' => 90002, 'stem' => $copyOf['stem'].' (variant 2)'];
    $bank[] = [...$bank[5], 'id' => 90003, 'category' => 'Demographic Profile', 'isDemographic' => true];

    for ($seed = 1; $seed <= 5; $seed++) {
        $ids = array_column(seededSelector($seed)->select($bank, MockPoolSelector::PROFESSIONAL)['items'], 'id');
        expect($ids)->not->toContain(90001)
            ->and($ids)->not->toContain(90002)
            ->and($ids)->not->toContain(90003);
    }

    expect(MockPoolSelector::uniqueSource($bank))->toHaveCount(count($bank) - 3);
});

test('a short bank gives a shorter mock with a clear notice, never padded', function () {
    $id = 1;
    $bank = selectorBank([
        'Verbal Ability' => ['Grammar' => 10],
        'Analytical Ability' => ['Logic' => 10],
        'Numerical Ability' => ['Arithmetic' => 10],
        'General Information' => ['Constitution' => 3],
    ], $id);

    $result = seededSelector()->select($bank, MockPoolSelector::PROFESSIONAL);

    expect($result['items'])->toHaveCount(33)
        ->and($result['short'])->toBeTrue()
        ->and(array_unique(array_column($result['items'], 'id')))->toHaveCount(33)
        ->and(MockPoolSelector::shortNotice(MockPoolSelector::PROFESSIONAL, 33))
        ->toBe('This Professional mock has 33 items, not 150. The question bank only has 33 unique items for it right now, and repeats are not used to pad it.')
        ->and(MockPoolSelector::shortNotice(MockPoolSelector::PROFESSIONAL, 150))->toBeNull();
});

test('previously wrong items are favoured under the adaptive (Study) policy', function () {
    $bank = fullProBank();
    $numerical = array_values(array_filter($bank, fn ($q) => $q['category'] === 'Numerical Ability'));
    $wrongIds = array_map(fn ($q) => $q['id'], array_slice($numerical, 0, 10));

    $ids = array_column(seededSelector(3)->select($bank, MockPoolSelector::PROFESSIONAL, [
        'seenIds' => $wrongIds,
        'wrongIds' => $wrongIds,
    ])['items'], 'id');

    expect(array_intersect($wrongIds, $ids))->toHaveCount(10);
});

test('the same seed gives the same mock', function () {
    $a = array_column(seededSelector(42)->select(fullProBank(), MockPoolSelector::PROFESSIONAL)['items'], 'id');
    $b = array_column(seededSelector(42)->select(fullProBank(), MockPoolSelector::PROFESSIONAL)['items'], 'id');

    expect($a)->toBe($b);
});

test('offline-eligible items and exact copies of them never enter the mock source', function () {
    $id = 1;
    $rows = selectorBank(['General Information' => ['Constitution' => 5]], $id);
    $rows[0]['offlineEligible'] = true;
    $rows[] = [...$rows[0], 'id' => 99, 'offlineEligible' => false];

    $sourceIds = array_column(MockPoolSelector::uniqueSource($rows), 'id');

    expect($sourceIds)->toBe([2, 3, 4, 5]);
});

test('a mock never serves an offline-eligible item', function () {
    $bank = fullProBank();
    $offline = [];

    foreach ($bank as $i => $row) {
        if ($row['id'] % 10 === 0) {
            $bank[$i]['offlineEligible'] = true;
            $offline[$row['id']] = true;
        }
    }

    $items = seededSelector(11)->select($bank, MockPoolSelector::PROFESSIONAL)['items'];

    expect(array_filter(array_column($items, 'id'), fn (int $i) => isset($offline[$i])))->toBe([]);
});

/*
 * ADR-0002 Option A: selection policies.
 */

function heavyHistory(array $bank): array
{
    $ids = array_column($bank, 'id');

    return [
        'seenIds' => array_slice($ids, 0, 300),
        'wrongIds' => array_slice($ids, 0, 150),
        'weakSubcategories' => ['Arithmetic', 'Logic', 'Grammar'],
        'weakCategories' => ['Numerical Ability'],
    ];
}

test('the policy comes from the mode', function () {
    expect(SelectionPolicy::forMode(ExamMode::Strict))->toBe(SelectionPolicy::Representative)
        ->and(SelectionPolicy::forMode(ExamMode::Study))->toBe(SelectionPolicy::Adaptive);
});

test('representative selection is identical with or without learner history', function (string $level) {
    $bank = fullProBank();

    foreach ([1, 9, 42] as $seed) {
        $fresh = seededSelector($seed)->select($bank, $level, [], SelectionPolicy::Representative);
        $veteran = seededSelector($seed)->select($bank, $level, heavyHistory($bank), SelectionPolicy::Representative);

        expect(array_column($veteran['items'], 'id'))->toBe(array_column($fresh['items'], 'id'));
    }
})->with([MockPoolSelector::PROFESSIONAL, MockPoolSelector::SUBPROFESSIONAL]);

test('adaptive selection still changes with history and favours weak areas', function () {
    $bank = fullProBank();
    $history = heavyHistory($bank);
    $fresh = seededSelector(5)->select($bank, MockPoolSelector::PROFESSIONAL, [], SelectionPolicy::Adaptive);
    $biased = seededSelector(5)->select($bank, MockPoolSelector::PROFESSIONAL, $history, SelectionPolicy::Adaptive);

    expect(array_column($biased['items'], 'id'))->not->toBe(array_column($fresh['items'], 'id'));

    $count = fn (array $items, string $sub) => count(array_filter($items, fn ($q) => $q['subcategory'] === $sub));
    expect($count($biased['items'], 'Arithmetic'))->toBeGreaterThan($count($fresh['items'], 'Arithmetic'));
});

test('representative mocks keep the Civio blueprint, FIL/EN split and uniqueness on both tracks', function (string $level, array $expected) {
    $bank = fullProBank();

    for ($seed = 1; $seed <= 5; $seed++) {
        $result = seededSelector($seed)->select($bank, $level, heavyHistory($bank), SelectionPolicy::Representative);
        $items = $result['items'];
        $per = array_count_values(array_column($items, 'category'));
        ksort($per);

        $verbal = array_filter($items, fn ($q) => $q['category'] === 'Verbal Ability');
        $fil = array_filter($verbal, fn ($q) => $q['language'] === 'Filipino');

        expect($per)->toBe($expected)
            ->and(array_unique(array_column($items, 'id')))->toHaveCount(array_sum($expected))
            ->and($result['short'])->toBeFalse()
            // Two Verbal subcategories, each split half Filipino (rounded down).
            ->and(count($verbal) - 2 * count($fil))->toBeGreaterThanOrEqual(0)
            ->and(count($verbal) - 2 * count($fil))->toBeLessThanOrEqual(2);
    }
})->with([
    'Professional' => [MockPoolSelector::PROFESSIONAL, ['Analytical Ability' => 52, 'General Information' => 8, 'Numerical Ability' => 45, 'Verbal Ability' => 45]],
    'Subprofessional' => [MockPoolSelector::SUBPROFESSIONAL, ['Clerical Ability' => 47, 'General Information' => 8, 'Numerical Ability' => 45, 'Verbal Ability' => 45]],
]);

/**
 * Pearson chi-square of per-item pick counts across seeded mocks, for one
 * 100-item Numerical subcategory (quota 45) whose items differ sharply in
 * heuristic difficulty.
 */
function numericalPickChiSquare(SelectionPolicy $policy, int $draws, array $bias = []): float
{
    $rows = [];
    for ($i = 1; $i <= 100; $i++) {
        $rows[] = [
            'id' => $i,
            'stem' => $i % 2 === 0
                ? "Item {$i}: a store raised a price by {$i}% and then gave a discount of 12 percent; what is the percent change in the final price compared with the original price of the item?"
                : "Item {$i}: pick the plain answer.",
            'options' => ["A{$i}", "B{$i}", "C{$i}", "D{$i}"],
            'category' => 'Numerical Ability', 'subcategory' => 'Arithmetic', 'language' => 'English',
            'isDemographic' => false, 'explanation' => '',
        ];
    }

    $counts = array_fill(1, 100, 0);
    $total = 0;
    for ($seed = 1; $seed <= $draws; $seed++) {
        foreach (seededSelector($seed)->select($rows, MockPoolSelector::PROFESSIONAL, $bias, $policy)['items'] as $q) {
            $counts[$q['id']]++;
            $total++;
        }
    }

    $expected = $total / 100;

    return array_sum(array_map(fn ($o) => ($o - $expected) ** 2 / $expected, $counts));
}

test('representative picks are uniform within a subcategory (chi-square, df 99, alpha 0.001)', function () {
    // Critical value of chi-square with 99 degrees of freedom at alpha 0.001 is about 148.2.
    // Sampling without replacement is less variable than the multinomial model, so this is conservative.
    expect(numericalPickChiSquare(SelectionPolicy::Representative, 400))->toBeLessThan(148.2);
});

test('the same chi-square check detects a biased pick (the test has power)', function () {
    $wrong = range(2, 40, 2);
    $history = ['seenIds' => $wrong, 'wrongIds' => $wrong];

    expect(numericalPickChiSquare(SelectionPolicy::Adaptive, 400, $history))->toBeGreaterThan(148.2)
        // Strict ignores that same history.
        ->and(numericalPickChiSquare(SelectionPolicy::Representative, 400, $history))->toBeLessThan(148.2);
});
