<?php

declare(strict_types=1);

namespace App\Enums;

enum QuestionLanguage: string
{
    case English = 'English';
    case Filipino = 'Filipino';

    public static function fromRaw(?string $raw): self
    {
        $normalized = strtolower((string) $raw);

        if (str_contains($normalized, 'tagalog') || str_contains($normalized, 'filipino')) {
            return self::Filipino;
        }

        return self::English;
    }
}
