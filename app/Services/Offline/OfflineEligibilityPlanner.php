<?php

declare(strict_types=1);

namespace App\Services\Offline;

use App\Services\Exam\MockPoolSelector;

/**
 * Decides which items may go into offline drill packs (Lite L2). Pure.
 *
 * Per category: offline_cap = max(0, unique_active_items - ceil(1.5 x max mock quota)),
 * where the max quota is the largest count that category has in any mock
 * blueprint (Verbal 45, Analytical 52, Numerical 45, Clerical 47, General
 * Information 8). Categories with no mock quota get no offline items.
 *
 * - Never demographics, "(variant N)" clones, or items that have an exact copy
 *   under another ID (the copy could still reach a mock).
 * - Monotonic: items already marked stay marked (their keys may already be on
 *   phones), and count toward the cap.
 * - Deterministic: new picks come from the subcategory with the most remaining
 *   candidates (ties: lowest ID), lowest ID first, so small subcategories keep
 *   their items for mocks.
 *
 * @phpstan-type Row array{id: int, stem: string, options: array<int, string>, category: string, subcategory: string, isDemographic?: bool, offlineEligible?: bool}
 * @phpstan-type CategoryPlan array{category: string, unique: int, maxQuota: int, reserve: int, cap: int, existing: int, added: array<int, int>, eligible: array<int, int>, leftForMocks: int, overCap: bool}
 */
final class OfflineEligibilityPlanner
{
    public const RESERVE_FACTOR = 1.5;

    /** @return array<string, int> category => largest mock quota across levels */
    public static function maxQuotas(): array
    {
        $max = [];

        foreach (MockPoolSelector::BLUEPRINT as $blocks) {
            foreach ($blocks as $block) {
                $max[$block['category']] = max($max[$block['category']] ?? 0, (int) $block['count']);
            }
        }

        return $max;
    }

    /**
     * @param  array<int, array<string, mixed>>  $rows  active questions
     * @return array<string, array<string, mixed>> category => plan
     */
    public function plan(array $rows): array
    {
        $quotas = self::maxQuotas();
        $keyCounts = [];

        foreach ($rows as $row) {
            if (! self::isExcluded($row)) {
                $key = MockPoolSelector::exactItemKey($row);
                $keyCounts[$key] = ($keyCounts[$key] ?? 0) + 1;
            }
        }

        /** @var array<string, array<string, true>> $uniqueKeys */
        $uniqueKeys = [];
        /** @var array<string, array<int, int>> $existing */
        $existing = [];
        /** @var array<string, array<string, array<int, int>>> $candidates category => subcategory => ids */
        $candidates = [];

        usort($rows, fn (array $a, array $b): int => (int) $a['id'] <=> (int) $b['id']);

        foreach ($rows as $row) {
            if (self::isExcluded($row)) {
                continue;
            }

            $category = (string) $row['category'];
            $key = MockPoolSelector::exactItemKey($row);
            $uniqueKeys[$category][$key] = true;

            if (! empty($row['offlineEligible'])) {
                $existing[$category][] = (int) $row['id'];

                continue;
            }

            if ($keyCounts[$key] === 1) {
                $candidates[$category][(string) ($row['subcategory'] ?? '')][] = (int) $row['id'];
            }
        }

        $categories = array_unique([...array_keys($quotas), ...array_keys($uniqueKeys)]);
        sort($categories);
        $plans = [];

        foreach ($categories as $category) {
            $unique = count($uniqueKeys[$category] ?? []);
            $maxQuota = $quotas[$category] ?? 0;
            $reserve = (int) ceil(self::RESERVE_FACTOR * $maxQuota);
            $cap = $maxQuota > 0 ? max(0, $unique - $reserve) : 0;
            $kept = $existing[$category] ?? [];
            $added = self::pickSpread($candidates[$category] ?? [], max(0, $cap - count($kept)));
            $eligible = [...$kept, ...$added];
            sort($eligible);

            $plans[$category] = [
                'category' => $category,
                'unique' => $unique,
                'maxQuota' => $maxQuota,
                'reserve' => $reserve,
                'cap' => $cap,
                'existing' => count($kept),
                'added' => $added,
                'eligible' => $eligible,
                'leftForMocks' => $unique - count($eligible),
                'overCap' => count($kept) > $cap,
            ];
        }

        return $plans;
    }

    /** @param array<string, mixed> $row */
    private static function isExcluded(array $row): bool
    {
        return MockPoolSelector::isDemographic($row) || MockPoolSelector::isVariantClone((string) ($row['stem'] ?? ''));
    }

    /**
     * Take $count ids, each time from the subcategory with the most candidates left.
     *
     * @param  array<string, array<int, int>>  $bySubcategory  ids ascending
     * @return array<int, int>
     */
    private static function pickSpread(array $bySubcategory, int $count): array
    {
        $picked = [];

        while ($count > 0) {
            $best = null;

            foreach ($bySubcategory as $sub => $ids) {
                if ($ids === []) {
                    continue;
                }

                if ($best === null
                    || count($ids) > count($bySubcategory[$best])
                    || (count($ids) === count($bySubcategory[$best]) && $ids[0] < $bySubcategory[$best][0])) {
                    $best = $sub;
                }
            }

            if ($best === null) {
                break;
            }

            $picked[] = array_shift($bySubcategory[$best]);
            $count--;
        }

        sort($picked);

        return $picked;
    }
}
