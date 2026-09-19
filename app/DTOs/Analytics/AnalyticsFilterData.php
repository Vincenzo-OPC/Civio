<?php

declare(strict_types=1);

namespace App\DTOs\Analytics;

use Illuminate\Http\Request;

readonly class AnalyticsFilterData
{
    public function __construct(
        public string $track = 'Professional',
        public string $runs = 'all',
    ) {}

    public static function fromRequest(Request $request): self
    {
        return new self(
            track: (string) $request->query('track', 'Professional'),
            runs: (string) $request->query('runs', 'all'),
        );
    }
}
