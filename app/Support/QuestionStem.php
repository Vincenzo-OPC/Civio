<?php

declare(strict_types=1);

namespace App\Support;

final class QuestionStem
{
    public static function normalize(?string $stem): string
    {
        $stem = trim((string) $stem);
        $stem = (string) preg_replace('/\s*\(variant\s+\d+\)\s*$/i', '', $stem);
        $stem = (string) preg_replace('/\s+/u', ' ', $stem);

        return mb_strtolower(trim($stem));
    }

    public static function isVariant(?string $stem): bool
    {
        return (bool) preg_match('/\(variant\s+\d+\)\s*$/i', (string) $stem);
    }

    public static function withoutVariantSuffix(?string $stem): string
    {
        $stem = trim((string) $stem);

        return trim((string) preg_replace('/\s*\(variant\s+\d+\)\s*$/i', '', $stem));
    }
}
