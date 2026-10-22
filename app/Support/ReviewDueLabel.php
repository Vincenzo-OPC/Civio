<?php

declare(strict_types=1);

namespace App\Support;

use Carbon\CarbonInterface;

/** Review times are stored as instants and read in Philippine time. */
final class ReviewDueLabel
{
    public const ZONE = 'Asia/Manila';

    public static function format(CarbonInterface $due): string
    {
        return $due->copy()->timezone(self::ZONE)->format('M j, Y g:i A');
    }
}
