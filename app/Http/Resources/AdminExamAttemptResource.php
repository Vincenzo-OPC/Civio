<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\ExamAttempt;
use App\Services\ExamAttemptFormatter;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin ExamAttempt
 */
class AdminExamAttemptResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $formatter = app(ExamAttemptFormatter::class);
        $meta = $this->cat_scores['metadata'] ?? [];

        $percentage = round((float) $formatter->calculateWeightedPercentage($this->cat_scores ?? []), 2);
        $trackName = $meta['track'] ?? null;
        $categoryName = 'Full Mock Exam';

        if ($this->category) {
            $categoryName = $this->category->name;
        } elseif ($trackName) {
            $categoryName = $trackName.' Level Reviewer';
        } elseif (isset($meta['category_name'])) {
            $categoryName = $meta['category_name'];
        }

        return [
            'id' => $this->id,
            'user' => [
                'name' => $this->user?->name ?? 'Guest User',
                'email' => $this->user?->email ?? 'Guest',
            ],
            'category' => $categoryName,
            'percentage' => $percentage,
            'created_at' => $this->created_at?->diffForHumans() ?? 'Just now',
            'full_date' => $this->created_at?->format('M j, Y g:i A') ?? 'Unknown',
        ];
    }
}
