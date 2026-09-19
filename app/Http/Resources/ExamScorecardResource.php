<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\ExamAttempt;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin ExamAttempt
 */
class ExamScorecardResource extends JsonResource
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
            'category_id' => $this->category_id,
            'question_ids' => $this->question_ids,
            'answers' => $this->answers,
            'cat_scores' => $this->cat_scores,
            'created_at' => $this->created_at?->toIso8601String(),
        ];
    }
}
