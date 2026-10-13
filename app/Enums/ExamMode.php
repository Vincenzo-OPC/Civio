<?php

declare(strict_types=1);

namespace App\Enums;

/**
 * How a full-length mock is taken.
 *
 * - Study: Reveal, explanations and Copy for AI per item; timer optional.
 * - Strict: exam rehearsal. Timer always on, and the server withholds every
 *   key and explanation for the mock's items until it is submitted.
 */
enum ExamMode: string
{
    case Study = 'study';
    case Strict = 'strict';

    public static function fromRaw(?string $value): self
    {
        return self::tryFrom(strtolower(trim((string) $value))) ?? self::Study;
    }

    public function label(): string
    {
        return match ($this) {
            self::Study => 'Study Mock',
            self::Strict => 'Strict Mock',
        };
    }
}
