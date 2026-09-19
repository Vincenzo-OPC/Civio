<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\LearnModule;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin LearnModule
 */
class LearnModuleResource extends JsonResource
{
    /**
     * @param  mixed  $resource
     */
    public function __construct($resource, protected ?bool $isCompleted = null)
    {
        parent::__construct($resource);
    }

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $userId = $request->user()?->id;
        $isCompleted = $this->isCompleted ?? ($userId ? $this->isCompletedBy($userId) : false);

        return [
            'id' => $this->id,
            'category_id' => $this->category_id,
            'title' => $this->title,
            'slug' => $this->slug,
            'topic' => $this->topic,
            'summary' => $this->summary,
            'content' => $this->content,
            'estimated_minutes' => $this->estimated_minutes,
            'is_published' => (bool) $this->is_published,
            'category' => $this->category?->name ?? 'General Info',
            'subcategory' => $this->subcategory?->name ?? 'Core Concepts',
            'creator_name' => $this->creator?->name ?? 'Expert Reviewer',
            'updated_at' => $this->updated_at?->format('M d, Y') ?? now()->format('M d, Y'),
            'is_completed' => $isCompleted,
        ];
    }
}
