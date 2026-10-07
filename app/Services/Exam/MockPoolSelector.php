<?php

declare(strict_types=1);

namespace App\Services\Exam;

use Random\Randomizer;

/**
 * Server-side mock pool selector (Lite L1).
 *
 * A pure PHP mirror of the rules that lived in
 * `resources/js/pages/user/exams/utils/mock-pool.ts`:
 *
 * - unique items only: demographics, "(variant N)" clones and exact copies (same
 *   stem and options under another ID) are dropped, and no item is used twice;
 * - official blueprint per level with per-subcategory quotas (Verbal split
 *   between English and Filipino);
 * - weak-topic bias: previously wrong items first (up to half of each block),
 *   then unseen, then seen-correct; about half of the mock leans to weak
 *   subcategories / categories when unused items exist;
 * - harder-biased shuffle (heuristic difficulty, no DB column);
 * - no padding: a short bank gives a shorter mock and a clear notice;
 * - offline-eligible items (Lite L2 drill packs) never enter a mock.
 *
 * Items are plain arrays shaped like `ExamQuestionResource` (id, stem, options,
 * category, subcategory, language, isDemographic, optional explanation).
 *
 * @phpstan-type Item array{id: int, stem: string, options: array<int, string>, category: string, subcategory: string, language: string, isDemographic: bool, offlineEligible?: bool, explanation?: string}
 * @phpstan-type Bias array{seenIds?: array<int, int>, wrongIds?: array<int, int>, weakSubcategories?: array<int, string>, weakCategories?: array<int, string>}
 */
final class MockPoolSelector
{
    public const PROFESSIONAL = 'Professional';

    public const SUBPROFESSIONAL = 'Subprofessional';

    /** @var array<string, array<int, array{category: string, count: int, splitLanguage?: bool}>> */
    public const BLUEPRINT = [
        self::PROFESSIONAL => [
            ['category' => 'Verbal Ability', 'count' => 45, 'splitLanguage' => true],
            ['category' => 'Analytical Ability', 'count' => 52],
            ['category' => 'Numerical Ability', 'count' => 45],
            ['category' => 'General Information', 'count' => 8],
        ],
        self::SUBPROFESSIONAL => [
            ['category' => 'Verbal Ability', 'count' => 45, 'splitLanguage' => true],
            ['category' => 'Clerical Ability', 'count' => 47],
            ['category' => 'Numerical Ability', 'count' => 45],
            ['category' => 'General Information', 'count' => 8],
        ],
    ];

    /** @var array<string, int> */
    public const TARGETS = [
        self::PROFESSIONAL => 150,
        self::SUBPROFESSIONAL => 145,
    ];

    public const WRONG_PRIORITY = 0.5;

    public const HARD_BIAS = 0.6;

    public const STEM_PREFIX_LEN = 48;

    private Randomizer $random;

    public function __construct(?Randomizer $random = null)
    {
        $this->random = $random ?? new Randomizer;
    }

    public static function levelFor(?string $track): string
    {
        return strtolower((string) $track) === 'subprofessional' ? self::SUBPROFESSIONAL : self::PROFESSIONAL;
    }

    public static function targetFor(string $level): int
    {
        return self::TARGETS[$level] ?? self::TARGETS[self::PROFESSIONAL];
    }

    /** Old seeder filler rows ("... (variant 3)"). Never real questions. */
    public static function isVariantClone(string $stem): bool
    {
        return (bool) preg_match('/\(variant\s*\d+\)/i', $stem);
    }

    public static function isDemographic(array $q): bool
    {
        if (! empty($q['isDemographic'])) {
            return true;
        }

        $cat = strtolower((string) ($q['category'] ?? ''));

        return $cat !== '' && ($cat === 'demographic profile' || str_contains($cat, 'demographic'));
    }

    private static function norm(string $text): string
    {
        return trim((string) preg_replace('/\s+/u', ' ', mb_strtolower($text)));
    }

    /** Same stem and same options = the same item, whatever its ID. */
    public static function exactItemKey(array $q): string
    {
        $options = array_map(
            fn ($o) => self::norm((string) ($o ?? '')),
            is_array($q['options'] ?? null) ? array_values($q['options']) : []
        );

        return self::norm((string) ($q['stem'] ?? ''))."\u{241E}".implode("\u{241F}", $options);
    }

    public static function stemDedupeKey(string $stem): string
    {
        return mb_substr(self::norm($stem), 0, self::STEM_PREFIX_LEN);
    }

    /**
     * Items a mock may draw from: no demographics, no clones, no exact duplicates,
     * and nothing offline-eligible (Lite L2). Offline items' keys can be on a
     * learner's phone, so neither they nor an exact copy under another ID may
     * ever appear in a strict mock.
     *
     * @param  array<int, array<string, mixed>>  $questions
     * @return array<int, array<string, mixed>>
     */
    public static function uniqueSource(array $questions): array
    {
        $seenIds = [];
        $seenKeys = [];
        $out = [];
        $offlineKeys = [];

        foreach ($questions as $q) {
            if (! empty($q['offlineEligible'])) {
                $offlineKeys[self::exactItemKey($q)] = true;
            }
        }

        foreach ($questions as $q) {
            $id = (int) $q['id'];

            if (! empty($q['offlineEligible']) || self::isDemographic($q) || self::isVariantClone((string) $q['stem']) || isset($seenIds[$id])) {
                continue;
            }

            $key = self::exactItemKey($q);

            if (isset($seenKeys[$key]) || isset($offlineKeys[$key])) {
                continue;
            }

            $seenIds[$id] = true;
            $seenKeys[$key] = true;
            $out[] = $q;
        }

        return $out;
    }

    /** Heuristic difficulty (no DB column). Higher = harder. Mirrors exam-utils.ts. */
    public static function estimateDifficulty(array $q): int
    {
        $stem = trim((string) ($q['stem'] ?? ''));
        $explanation = trim((string) ($q['explanation'] ?? ''));
        $options = is_array($q['options'] ?? null) ? array_values($q['options']) : [];
        $cat = strtolower((string) ($q['category'] ?? ''));
        $sub = strtolower((string) ($q['subcategory'] ?? ''));
        $score = 0;

        $score += match (true) {
            str_contains($cat, 'analytical') => 28,
            str_contains($cat, 'numerical') => 26,
            str_contains($cat, 'clerical') => 12,
            str_contains($cat, 'general') => 14,
            str_contains($cat, 'verbal') => 6,
            default => 0,
        };

        if (preg_match('/logic|assumption|conclusion|syllog|data interpretation|table|graph|abstract|spatial/', $sub)) {
            $score += 8;
        }

        if (preg_match('/word analogy|synonym|antonym|vocabulary|spelling/', $sub)) {
            $score -= 4;
        }

        $stemLen = mb_strlen($stem);
        $score += min(22, intdiv($stemLen, 40));

        if ($stemLen < 60) {
            $score -= 10;
        } elseif ($stemLen > 220) {
            $score += 6;
        }

        $optChars = array_sum(array_map(fn ($o) => mb_strlen((string) $o), $options));
        $score += min(12, intdiv($optChars, 80));

        if (count($options) >= 4 && $optChars / max(1, count($options)) > 40) {
            $score += 4;
        }

        $score += min(10, intdiv(mb_strlen($explanation), 80));

        $mathBlob = $stem.' '.implode(' ', array_map('strval', $options));

        if (preg_match('/\d/', $mathBlob) && preg_match('/[%₱$]|ratio|percent|average|fraction|equation|solve|how many|what is \d/iu', $mathBlob)) {
            $score += 10;
        }

        if (preg_match('/[÷×√∑]|\\\\frac|\^|\d+\s*[+\-*\/]\s*\d+/u', $mathBlob)) {
            $score += 6;
        }

        if (preg_match('/according to|passage|paragraph|the author|main idea|inferred/i', $stem)) {
            $score += 8;
        }

        return $score;
    }

    /**
     * @template T
     *
     * @param  array<int, T>  $items
     * @return array<int, T>
     */
    public function shuffle(array $items): array
    {
        return $items === [] ? [] : $this->random->shuffleArray(array_values($items));
    }

    /**
     * Shuffle, then preferentially take from the harder part of the pool with
     * randomness (not a deterministic hard-first sort).
     *
     * @param  array<int, array<string, mixed>>  $pool
     * @return array<int, array<string, mixed>>
     */
    public function shuffleHardBiased(array $pool, float $hardBias = self::HARD_BIAS): array
    {
        if (count($pool) <= 1) {
            return array_values($pool);
        }

        $keyed = array_map(
            fn ($q) => ['q' => $q, 'key' => self::estimateDifficulty($q) + $this->random->nextFloat() * 12],
            array_values($pool)
        );
        usort($keyed, fn ($a, $b) => $b['key'] <=> $a['key']);

        $hardCount = max(1, (int) ceil(count($keyed) * min(1, max(0, $hardBias))));
        $hard = $this->shuffle(array_column(array_slice($keyed, 0, $hardCount), 'q'));
        $easy = $this->shuffle(array_column(array_slice($keyed, $hardCount), 'q'));
        $out = [];
        $hi = 0;
        $ei = 0;

        while ($hi < count($hard) || $ei < count($easy)) {
            $preferHard = $hi < count($hard) && ($ei >= count($easy) || $this->random->nextFloat() < $hardBias);

            if ($preferHard) {
                $out[] = $hard[$hi++];
            } elseif ($ei < count($easy)) {
                $out[] = $easy[$ei++];
            } else {
                $out[] = $hard[$hi++];
            }
        }

        return $out;
    }

    /**
     * Build the scored items for a full mock.
     *
     * @param  array<int, array<string, mixed>>  $questions
     * @param  array<string, mixed>  $bias
     * @return array{items: array<int, array<string, mixed>>, target: int, short: bool}
     */
    public function select(array $questions, string $level, array $bias = []): array
    {
        $level = isset(self::BLUEPRINT[$level]) ? $level : self::PROFESSIONAL;
        $blueprint = self::BLUEPRINT[$level];
        $target = self::targetFor($level);
        $source = self::uniqueSource($questions);

        $seen = array_fill_keys(array_map('intval', $bias['seenIds'] ?? []), true);
        $wrong = array_fill_keys(array_map('intval', $bias['wrongIds'] ?? []), true);
        $weakSub = array_fill_keys(array_map('strval', $bias['weakSubcategories'] ?? []), true);

        $state = new MockPoolState;

        $scored = [];

        foreach ($blueprint as $block) {
            $categoryPool = array_values(array_filter($source, fn ($q) => ($q['category'] ?? '') === $block['category']));
            array_push($scored, ...$this->pickBalanced($state, $categoryPool, $block['count'], (bool) ($block['splitLanguage'] ?? false), $seen, $wrong, $weakSub));
        }

        $levelCategories = array_fill_keys(array_column($blueprint, 'category'), true);
        $biased = $this->raiseWeakCategoryShare($scored, $source, array_map('strval', $bias['weakCategories'] ?? []), $target, $levelCategories);
        $items = $this->shuffle($biased);

        return ['items' => $items, 'target' => $target, 'short' => count($items) < $target];
    }

    /**
     * @param  array<int, array<string, mixed>>  $pool
     * @param  array<int, true>  $seen
     * @param  array<int, true>  $wrong
     * @param  array<string, true>  $weakSub
     * @return array<int, array<string, mixed>>
     */
    private function pickBalanced(MockPoolState $state, array $pool, int $targetCount, bool $splitLanguage, array $seen, array $wrong, array $weakSub): array
    {
        $groups = [];

        foreach ($pool as $q) {
            $key = ($q['subcategory'] ?? '') !== '' ? (string) $q['subcategory'] : 'General';
            $groups[$key][] = $q;
        }

        $names = $this->shuffle(array_map('strval', array_keys($groups)));

        if ($names === []) {
            return [];
        }

        $quotas = $this->quotasForSubcats($names, $groups, $targetCount, $weakSub);
        $picked = [];

        foreach ($names as $name) {
            $quota = $quotas[$name] ?? 0;

            if ($quota <= 0) {
                continue;
            }

            $subPool = $groups[$name];

            if ($splitLanguage || $name === 'Word analogy') {
                $eng = array_values(array_filter($subPool, function ($q) {
                    $lang = strtolower((string) ($q['language'] ?? ''));

                    return $lang === 'english' || $lang === '' || $lang === 'en';
                }));
                $fil = array_values(array_filter($subPool, function ($q) {
                    $lang = strtolower((string) ($q['language'] ?? ''));

                    return str_contains($lang, 'filipino') || str_contains($lang, 'tagalog');
                }));
                $filQuota = $fil !== [] ? min(intdiv($quota, 2), count($fil)) : 0;

                array_push($picked, ...$this->pickFlat($state, $fil, $filQuota, $seen, $wrong));
                array_push($picked, ...$this->pickFlat($state, $eng, $quota - $filQuota, $seen, $wrong, $subPool));
            } else {
                array_push($picked, ...$this->pickFlat($state, $subPool, $quota, $seen, $wrong));
            }
        }

        // Subcategory split left a gap: top up from the same category only.
        if (count($picked) < $targetCount) {
            array_push($picked, ...$this->pickFlat($state, $pool, $targetCount - count($picked), $seen, $wrong));
        }

        return $this->shuffle(array_slice($picked, 0, $targetCount));
    }

    /**
     * @param  array<int, array<string, mixed>>  $pool
     * @param  array<int, true>  $seen
     * @param  array<int, true>  $wrong
     * @param  array<int, array<string, mixed>>  $fallback
     * @return array<int, array<string, mixed>>
     */
    private function pickFlat(MockPoolState $state, array $pool, int $count, array $seen, array $wrong, array $fallback = []): array
    {
        $picked = [];
        $prefixes = [];

        if ($count <= 0) {
            return $picked;
        }

        $push = function (array $items, int $quota, bool $spreadStems) use ($state, &$picked, &$prefixes, $count): void {
            $added = 0;

            foreach ($items as $q) {
                if ($added >= $quota || count($picked) >= $count) {
                    break;
                }

                if (! $state->isFree($q)) {
                    continue;
                }

                $prefix = self::stemDedupeKey((string) $q['stem']);

                if ($spreadStems && $prefix !== '' && isset($prefixes[$prefix])) {
                    continue;
                }

                $picked[] = $q;
                $state->take($q);

                if ($prefix !== '') {
                    $prefixes[$prefix] = true;
                }

                $added++;
            }
        };

        $wrongItems = array_values(array_filter($pool, fn ($q) => isset($wrong[(int) $q['id']])));
        $unseen = array_values(array_filter($pool, fn ($q) => ! isset($seen[(int) $q['id']])));
        $seenCorrect = array_values(array_filter($pool, fn ($q) => isset($seen[(int) $q['id']]) && ! isset($wrong[(int) $q['id']])));
        $wrongQuota = (int) ceil($count * self::WRONG_PRIORITY);
        $wrongOrdered = $this->shuffleHardBiased($this->shuffle($wrongItems));

        // Variety pass: wrong first (weak-topic bias), then unseen, then seen.
        $push($wrongOrdered, $wrongQuota, true);
        $push($this->shuffleHardBiased($unseen), $count, true);
        $push($this->shuffleHardBiased($seenCorrect), $count, true);
        $push($wrongOrdered, $count, true);
        $push($this->shuffleHardBiased($fallback), $count, true);

        // Top-up pass: any remaining distinct item. Still no clones or copies.
        $push($this->shuffleHardBiased([...$unseen, ...$wrongOrdered, ...$seenCorrect]), $count, false);
        $push($this->shuffleHardBiased($fallback), $count, false);

        return $picked;
    }

    /**
     * @param  array<int, string>  $names
     * @param  array<string, array<int, array<string, mixed>>>  $groups
     * @param  array<string, true>  $weakSub
     * @return array<string, int>
     */
    private function quotasForSubcats(array $names, array $groups, int $targetCount, array $weakSub): array
    {
        $quotas = array_fill_keys($names, 0);

        $place = function (array $bucket, int $share) use (&$quotas, $groups): int {
            if ($bucket === [] || $share <= 0) {
                return 0;
            }

            $left = $share;
            $base = intdiv($share, count($bucket));
            $rem = $share % count($bucket);

            foreach ($bucket as $name) {
                $want = $base + ($rem > 0 ? 1 : 0);

                if ($rem > 0) {
                    $rem--;
                }

                $give = min(count($groups[$name] ?? []), $want);
                $quotas[$name] += $give;
                $left -= $give;
            }

            foreach ($bucket as $name) {
                if ($left <= 0) {
                    break;
                }

                $room = count($groups[$name] ?? []) - $quotas[$name];
                $add = min(max(0, $room), $left);
                $quotas[$name] += $add;
                $left -= $add;
            }

            return $share - $left;
        };

        $weakNames = array_values(array_filter($names, fn ($n) => isset($weakSub[$n])));
        $otherNames = array_values(array_filter($names, fn ($n) => ! isset($weakSub[$n])));

        if ($weakNames !== [] && $otherNames !== []) {
            $weakAvailable = array_sum(array_map(fn ($n) => count($groups[$n] ?? []), $weakNames));
            $weakShare = min($weakAvailable, (int) round($targetCount * self::WRONG_PRIORITY));
            $placedWeak = $place($weakNames, $weakShare);
            $place($otherNames, max(0, $targetCount - $placedWeak));
        } else {
            $base = intdiv($targetCount, count($names));
            $rem = $targetCount % count($names);

            foreach ($names as $name) {
                $quotas[$name] = $base + ($rem > 0 ? 1 : 0);

                if ($rem > 0) {
                    $rem--;
                }
            }
        }

        return $quotas;
    }

    /**
     * About half the scored items come from previously weak categories when
     * unused items in those categories remain. Never brings in a duplicate.
     *
     * @param  array<int, array<string, mixed>>  $scored
     * @param  array<int, array<string, mixed>>  $source
     * @param  array<int, string>  $weakCategories
     * @param  array<string, true>  $levelCategories
     * @return array<int, array<string, mixed>>
     */
    private function raiseWeakCategoryShare(array $scored, array $source, array $weakCategories, int $target, array $levelCategories): array
    {
        if ($weakCategories === [] || $scored === []) {
            return $scored;
        }

        $weak = array_fill_keys(array_filter($weakCategories, fn ($c) => isset($levelCategories[$c])), true);

        if ($weak === []) {
            return $scored;
        }

        $isWeak = fn ($q) => isset($weak[(string) ($q['category'] ?? '')]);
        $weakTarget = min($target, (int) round($target * self::WRONG_PRIORITY));
        $result = array_values($scored);
        $weakCount = count(array_filter($result, $isWeak));

        if ($weakCount >= $weakTarget) {
            return $result;
        }

        $usedIds = array_fill_keys(array_map(fn ($q) => (int) $q['id'], $result), true);
        $usedKeys = array_fill_keys(array_map(fn ($q) => self::exactItemKey($q), $result), true);
        $extras = $this->shuffle(array_values(array_filter(
            $source,
            fn ($q) => ! isset($usedIds[(int) $q['id']]) && ! isset($usedKeys[self::exactItemKey($q)]) && $isWeak($q)
        )));
        $extraIdx = 0;

        for ($i = count($result) - 1; $i >= 0 && $weakCount < $weakTarget && $extraIdx < count($extras); $i--) {
            if (! $isWeak($result[$i])) {
                $result[$i] = $extras[$extraIdx++];
                $weakCount++;
            }
        }

        return $result;
    }

    /** User-facing note for a mock that could not reach the official count. */
    public static function shortNotice(string $level, int $itemCount): ?string
    {
        $target = self::targetFor($level);

        if ($itemCount >= $target) {
            return null;
        }

        if ($itemCount <= 0) {
            return "No {$level} practice items are available right now, so a mock can't start.";
        }

        return "This {$level} mock has {$itemCount} items, not {$target}. The question bank only has {$itemCount} unique items for it right now, and repeats are not used to pad it.";
    }
}
