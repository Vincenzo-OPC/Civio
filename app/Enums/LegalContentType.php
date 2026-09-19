<?php

declare(strict_types=1);

namespace App\Enums;

enum LegalContentType: string
{
    case Privacy = 'privacy';
    case Terms = 'terms';
}
