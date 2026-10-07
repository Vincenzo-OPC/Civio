<?php

use App\Services\Exam\MockPoolSelector;
use App\Services\Offline\OfflineEligibilityPlanner;

/**
 * @param  array<string, array<string, int>>  $layout  category => [subcategory => count]
 * @return array<int, array<string, mixed>>
 */
function offlinePlannerBank(array $layout, int &$nextId = 1, string $language = 'English'): array
{
    $rows = [];

    foreach ($layout as $category => $subs) {
        foreach ($subs as $sub => $count) {
            for ($i = 0; $i < $count; $i++) {
                $id = $nextId++;
                $rows[] = [
                    'id' => $id,
                    'stem' => "Item {$id}: {$category} / {$sub} number {$i} in its own words?",
                    'options' => ["A{$id}", "B{$id}", "C{$id}", "D{$id}"],
                    'category' => $category,
                    'subcategory' => $sub,
                    'language' => $language,
                    'isDemographic' => false,
                ];
            }
        }
    }

    return $rows;
}

test('max mock quotas come from the blueprint', function () {
    expect(OfflineEligibilityPlanner::maxQuotas())->toBe([
        'Verbal Ability' => 45,
        'Analytical Ability' => 52,
        'Numerical Ability' => 45,
        'General Information' => 8,
        'Clerical Ability' => 47,
    ]);
});

test('cap is unique items minus ceil(1.5 x max quota), never below zero', function () {
    $id = 1;
    $rows = [
        ...offlinePlannerBank(['Numerical Ability' => ['Arithmetic' => 60, 'Word problems' => 40]], $id),
        ...offlinePlannerBank(['General Information' => ['Constitution' => 20]], $id),
        ...offlinePlannerBank(['Clerical Ability' => ['Filing' => 50]], $id),
    ];

    $plans = (new OfflineEligibilityPlanner)->plan($rows);

    expect($plans['Numerical Ability']['cap'])->toBe(100 - 68)
        ->and($plans['Numerical Ability']['eligible'])->toHaveCount(32)
        ->and($plans['General Information']['cap'])->toBe(20 - 12)
        ->and($plans['Clerical Ability']['cap'])->toBe(0)
        ->and($plans['Clerical Ability']['eligible'])->toBe([])
        ->and($plans['Verbal Ability']['cap'])->toBe(0);
});

test('picks spread across subcategories, lowest ID first, and are deterministic', function () {
    $id = 1;
    $rows = offlinePlannerBank(['General Information' => ['Constitution' => 14, 'Ethics' => 6]], $id);

    $first = (new OfflineEligibilityPlanner)->plan($rows);
    $again = (new OfflineEligibilityPlanner)->plan(array_reverse($rows));

    // cap = 20 - 12 = 8; the big subcategory gives first until both have 6 left.
    expect($first['General Information']['eligible'])->toBe([1, 2, 3, 4, 5, 6, 7, 8])
        ->and($again['General Information']['eligible'])->toBe($first['General Information']['eligible']);

    $rows = offlinePlannerBank(['General Information' => ['A' => 12, 'B' => 12]], $id);
    $eligible = (new OfflineEligibilityPlanner)->plan($rows)['General Information']['eligible'];
    $bySub = array_count_values(array_map(fn (int $i) => $rows[array_search($i, array_column($rows, 'id'))]['subcategory'], $eligible));

    expect($eligible)->toHaveCount(12)->and($bySub)->toBe(['A' => 6, 'B' => 6]);
});

test('never picks demographics, clones, or items with an exact copy', function () {
    $id = 1;
    $rows = offlinePlannerBank(['General Information' => ['Constitution' => 16]], $id);
    $rows[] = [...$rows[0], 'id' => 900, 'stem' => $rows[0]['stem'].' (variant 2)'];
    $rows[] = [...$rows[1], 'id' => 901];
    $rows[] = ['id' => 902, 'stem' => 'Age?', 'options' => ['18', '19'], 'category' => 'Demographic Profile', 'subcategory' => 'Age', 'language' => 'English', 'isDemographic' => true];

    $plan = (new OfflineEligibilityPlanner)->plan($rows)['General Information'];

    // 16 unique keys (901 duplicates item 2's key); cap 4; items 2 and 901 are not candidates.
    expect($plan['unique'])->toBe(16)
        ->and($plan['cap'])->toBe(4)
        ->and($plan['eligible'])->toBe([1, 3, 4, 5])
        ->and($plan['eligible'])->not->toContain(900)
        ->and($plan['eligible'])->not->toContain(901)
        ->and($plan['eligible'])->not->toContain(902);
});

test('already eligible items stay eligible and count toward the cap', function () {
    $id = 1;
    $rows = offlinePlannerBank(['General Information' => ['Constitution' => 16]], $id);
    $rows[15]['offlineEligible'] = true;

    $plan = (new OfflineEligibilityPlanner)->plan($rows)['General Information'];
    expect($plan['existing'])->toBe(1)
        ->and($plan['added'])->toBe([1, 2, 3])
        ->and($plan['eligible'])->toBe([1, 2, 3, 16]);

    foreach ($rows as &$row) {
        $row['offlineEligible'] = true;
    }
    unset($row);

    $over = (new OfflineEligibilityPlanner)->plan($rows)['General Information'];
    expect($over['overCap'])->toBeTrue()->and($over['added'])->toBe([])->and($over['eligible'])->toHaveCount(16);
});

test('a bank marked by the planner still fills full 150 and 145 item mocks', function () {
    $id = 1;
    $rows = [
        ...offlinePlannerBank(['Verbal Ability' => ['Word analogy' => 40, 'Grammar' => 40]], $id),
        ...offlinePlannerBank(['Verbal Ability' => ['Word analogy' => 30, 'Grammar' => 30]], $id, 'Filipino'),
        ...offlinePlannerBank(['Analytical Ability' => ['Logic' => 50, 'Data interpretation' => 50]], $id),
        ...offlinePlannerBank(['Numerical Ability' => ['Arithmetic' => 50, 'Word problems' => 50]], $id),
        ...offlinePlannerBank(['General Information' => ['Constitution' => 20]], $id),
        ...offlinePlannerBank(['Clerical Ability' => ['Filing' => 80]], $id),
    ];

    $eligible = [];
    foreach ((new OfflineEligibilityPlanner)->plan($rows) as $plan) {
        array_push($eligible, ...$plan['eligible']);
    }
    $eligible = array_fill_keys($eligible, true);
    $marked = array_map(fn (array $r) => [...$r, 'offlineEligible' => isset($eligible[$r['id']])], $rows);

    expect(count($eligible))->toBeGreaterThan(0);

    foreach ([MockPoolSelector::PROFESSIONAL => 150, MockPoolSelector::SUBPROFESSIONAL => 145] as $level => $target) {
        $result = (new MockPoolSelector)->select($marked, $level);
        $ids = array_column($result['items'], 'id');

        expect($result['items'])->toHaveCount($target)
            ->and($result['short'])->toBeFalse()
            ->and(array_filter($ids, fn (int $i) => isset($eligible[$i])))->toBe([]);
    }
});
