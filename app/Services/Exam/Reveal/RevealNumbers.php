<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal;

final class RevealNumbers
{
    public static function first(string $text): ?float
    {
        $text = str_replace(',', '', $text);
        if (preg_match('/-?\d+(?:\.\d+)?/', $text, $match) !== 1) {
            return null;
        }

        return (float) $match[0];
    }

    public static function format(float $value): string
    {
        if (abs($value - round($value)) < 0.00001) {
            return number_format((int) round($value));
        }

        return rtrim(rtrim(number_format($value, 2, '.', ''), '0'), '.');
    }

    public static function same(float $left, float $right): bool
    {
        return abs($left - $right) < 0.001;
    }
}
