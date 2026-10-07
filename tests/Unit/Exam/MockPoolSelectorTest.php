<?php

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

test('previously wrong items are favoured', function () {
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
