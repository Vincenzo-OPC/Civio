<?php

declare(strict_types=1);

namespace App\Services\Exam;

/**
 * Shared "already used" state for one mock: an item, or an exact copy of it
 * under another ID, appears at most once. For Filipino items it also keeps
 * apart two items where one item's key is the other's distractor (CoS round 03),
 * so one item cannot give away the other's answer.
 */
final class MockPoolState
{
    /** @var array<int, true> */
    private array $ids = [];

    /** @var array<string, true> */
    private array $keys = [];

    /** @var array<string, true> */
    private array $answerTexts = [];

    /** @var array<string, true> */
    private array $trapTexts = [];

    /** @param array<string, mixed> $q */
    public function isFree(array $q): bool
    {
        if (isset($this->ids[(int) $q['id']]) || isset($this->keys[MockPoolSelector::exactItemKey($q)])) {
            return false;
        }

        [$answer, $traps] = self::answerAndTraps($q);

        if ($answer !== null && isset($this->trapTexts[$answer])) {
            return false;
        }

        foreach ($traps as $t) {
            if (isset($this->answerTexts[$t])) {
                return false;
            }
        }

        return true;
    }

    /** @param array<string, mixed> $q */
    public function take(array $q): void
    {
        $this->ids[(int) $q['id']] = true;
        $this->keys[MockPoolSelector::exactItemKey($q)] = true;

        [$answer, $traps] = self::answerAndTraps($q);

        if ($answer !== null) {
            $this->answerTexts[$answer] = true;
        }

        foreach ($traps as $t) {
            $this->trapTexts[$t] = true;
        }
    }

    /**
     * Normalized key text and distractor texts of a Filipino word item. Only word or phrase
     * options count (letters, no digits or slashes), so order codes, numbers and paired
     * markers such as "ng / nang" never block each other.
     *
     * @param  array<string, mixed>  $q
     * @return array{0: string|null, 1: array<int, string>}
     */
    private static function answerAndTraps(array $q): array
    {
        $lang = strtolower((string) ($q['language'] ?? ''));

        if (! isset($q['correct']) || ! str_contains($lang, 'filipino')) {
            return [null, []];
        }

        $answer = null;
        $traps = [];

        foreach (array_values((array) ($q['options'] ?? [])) as $i => $text) {
            $t = mb_strtolower(trim((string) preg_replace('/\s+/u', ' ', (string) $text)));

            if (mb_strlen($t) < 4 || ! preg_match('/\p{L}/u', $t) || preg_match('/[\d\/]/u', $t)) {
                continue;
            }

            if ($i === (int) $q['correct']) {
                $answer = $t;
            } else {
                $traps[] = $t;
            }
        }

        return [$answer, $traps];
    }
}
