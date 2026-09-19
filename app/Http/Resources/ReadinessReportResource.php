<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ReadinessReportResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string|null
     */
    public static $wrap = null;

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $payload = is_array($this->resource) ? $this->resource : (array) $this->resource;

        return [
            'status' => $payload['status'] ?? 'no_data',
            'data' => $payload['data'] ?? null,
            'isLocal' => (bool) ($payload['isLocal'] ?? app()->environment('local')),
            'existingSchedules' => $payload['existingSchedules'] ?? [],
            'lastUpdated' => $payload['lastUpdated'] ?? null,
            ...(! empty($payload['attempt_id']) ? ['attempt_id' => (int) $payload['attempt_id']] : []),
        ];
    }
}
