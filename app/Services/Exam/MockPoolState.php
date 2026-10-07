<?php

declare(strict_types=1);

namespace App\Services\Exam;

/**
 * Shared "already used" state for one mock: an item, or an exact copy of it
 * under another ID, appears at most once.
 */
final class MockPoolState
{
    /** @var array<int, true> */
    private array $ids = [];

    /** @var array<string, true> */
    private array $keys = [];

    /** @param array<string, mixed> $q */
    public function isFree(array $q): bool
    {
        return ! isset($this->ids[(int) $q['id']]) && ! isset($this->keys[MockPoolSelector::exactItemKey($q)]);
    }

    /** @param array<string, mixed> $q */
    public function take(array $q): void
    {
        $this->ids[(int) $q['id']] = true;
        $this->keys[MockPoolSelector::exactItemKey($q)] = true;
    }
}
