<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\LearnModule;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin LearnModule
 */
class AdminLearnModuleResource extends JsonResource
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
            'slug' => $this->slug,
            'topic' => $this->topic,
            'summary' => $this->summary,
            'estimated_minutes' => $this->estimated_minutes,
            'is_published' => (bool) $this->is_published,
            'category' => $this->category?->name ?? 'General Info',
            'subcategory' => $this->subcategory?->name ?? 'Core Concepts',
            'updated_at' => $this->updated_at?->format('Y-m-d H:i') ?? '',
        ];
    }
}
