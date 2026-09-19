<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\SavedDrillSet;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin SavedDrillSet
 */
class SavedDrillSetResource extends JsonResource
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
        $questionsCount = $this->questions_count
            ?? ($this->relationLoaded('questions') ? $this->questions->count() : $this->questions()->count());

        $sampleCategories = $this->relationLoaded('questions')
            ? $this->questions->map(fn ($q) => $q->subcategory?->category?->name)->filter()->unique()->values()->all()
            : [];

        return [
            'id' => $this->id,
            'name' => $this->name,
            'description' => $this->description,
            'color' => $this->color ?? 'blue',
            'questions_count' => (int) $questionsCount,
            'sample_categories' => $sampleCategories,
            'created_at' => $this->created_at?->toIso8601String(),
        ];
    }
}
