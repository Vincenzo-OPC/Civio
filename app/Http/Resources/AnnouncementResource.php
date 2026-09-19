<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\Announcement;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Announcement
 */
class AnnouncementResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'message' => $this->message,
            'type' => $this->type,
            'is_active' => (bool) $this->is_active,
            'expires_at' => $this->expires_at?->toIso8601String() ?? (is_string($this->expires_at) ? $this->expires_at : null),
            'created_at' => $this->created_at?->toIso8601String() ?? '',
        ];
    }
}
