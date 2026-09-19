<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\Feedback;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Feedback
 */
class FeedbackResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $flaggable = $this->flaggable;
        $flaggableData = null;

        if ($flaggable) {
            $questionText = null;
            $options = [];

            if (str_ends_with((string) $this->flaggable_type, 'Question')) {
                $questionText = $flaggable->stem ?? null;
                $options = $flaggable->options ?? [];
            } elseif (str_ends_with((string) $this->flaggable_type, 'LearnModule')) {
                $questionText = $flaggable->title ?? null;
            }

            $flaggableData = [
                'id' => $flaggable->id,
                'question_text' => $questionText,
                'title' => $flaggable->title ?? null,
                'options' => $options,
            ];
        }

        return [
            'id' => $this->id,
            'user_id' => $this->user_id,
            'flaggable_id' => $this->flaggable_id,
            'flaggable_type' => $this->flaggable_type,
            'reason' => $this->reason,
            'details' => $this->details,
            'status' => $this->status,
            'total_reports_count' => (int) ($this->total_reports_count ?? 1),
            'created_at' => $this->created_at?->toIso8601String() ?? '',
            'user' => [
                'id' => $this->user?->id,
                'name' => $this->user?->name ?? 'Anonymous',
                'email' => $this->user?->email ?? '',
            ],
            'flaggable' => $flaggableData,
        ];
    }
}
