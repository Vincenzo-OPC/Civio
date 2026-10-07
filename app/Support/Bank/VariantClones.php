<?php

declare(strict_types=1);

namespace App\Support\Bank;

/**
 * "(variant N)" clones were copies of a real item with a numbered suffix,
 * created by the old local seeder so mock quotas could be met. They are not
 * real questions and must never enter a pool.
 */
final class VariantClones
{
    public const PATTERN = '/\(variant\s*\d+\)/i';

    public static function isClone(?string $stem): bool
    {
        return is_string($stem) && preg_match(self::PATTERN, $stem) === 1;
    }
}
