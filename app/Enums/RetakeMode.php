<?php

declare(strict_types=1);

namespace App\Enums;

enum RetakeMode: string
{
    case Same = 'same';
    case Fresh = 'fresh';
}
