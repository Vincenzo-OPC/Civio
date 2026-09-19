<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\LearnModule;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin LearnModule
 */
class AdminDraftModuleResource extends JsonResource
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
            'content' => $this->content,
            'estimated_minutes' => $this->estimated_minutes,
            'category_id' => $this->category_id,
            'subcategory_id' => $this->subcategory_id,
            'category' => $this->category?->name ?? 'General Info',
            'subcategory' => $this->subcategory?->name ?? 'Core Concepts',
            'updated_at' => $this->updated_at?->format('Y-m-d H:i') ?? '',
            'approved' => true,
        ];
    }
}
