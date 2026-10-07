<?php

declare(strict_types=1);

namespace App\Support;

use Illuminate\Http\Request;

/**
 * Lite mode (cheap phones, slow data). The browser decides (Save-Data /
 * slow connection auto-detect, or the manual toggle) and mirrors the choice
 * into the plain `civio_lite` cookie, so the server can send lighter props.
 *
 * The cookie only trims presentation data; it never changes grading or what
 * answer keys are sent.
 */
final class LiteMode
{
    public const COOKIE = 'civio_lite';

    public static function enabled(?Request $request = null): bool
    {
        $request ??= request();

        return $request->cookie(self::COOKIE) === '1';
    }

    /**
     * Analytics stats without chart-only fields that the Lite text tables do
     * not use (per-attempt breakdowns and per-point category scores).
     *
     * @param  array<string, mixed>  $stats
     * @return array<string, mixed>
     */
    public static function trimAnalyticsStats(array $stats): array
    {
        unset($stats['attemptBreakdowns']);

        if (isset($stats['chartData']) && is_array($stats['chartData'])) {
            $stats['chartData'] = array_map(function ($point) {
                if (is_array($point)) {
                    unset($point['categoryScores']);
                }

                return $point;
            }, $stats['chartData']);
        }

        return $stats;
    }
}
