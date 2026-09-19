<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Enums\QuestionStatus;
use App\Models\Question;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Question
 */
class QuestionResource extends JsonResource
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
            'stem' => $this->stem,
            'category' => $this->subcategory?->category?->name ?? 'Analytical Ability',
            'subcategory' => $this->subcategory?->name ?? 'Word analogy',
            'options' => $this->options ?? [],
            'correct_option' => (int) $this->correct_option,
            'explanation' => $this->explanation,
            'language' => $this->language ?? 'English',
            'status' => strtoupper($this->status instanceof QuestionStatus ? $this->status->value : (string) $this->status),
            'updated_at' => $this->updated_at?->format('Y-m-d H:i:s'),

        ];
    }
}
