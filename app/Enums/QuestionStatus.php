<?php

declare(strict_types=1);

namespace App\Enums;

enum QuestionStatus: string
{
    case Active = 'active';
    case Draft = 'draft';

    public function isActive(): bool
    {
        return $this === self::Active;
    }
}
