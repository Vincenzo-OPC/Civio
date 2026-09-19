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
class ExamAttemptResource extends JsonResource
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

        $trackName = $meta['track'] ?? 'Drill';
        if ($this->category_id !== null && ! $trackName) {
            $trackName = 'Drill';
        }

        $categoryName = 'Full Mock Exam';
        if ($this->category) {
            $categoryName = $this->category->name;
        } elseif (isset($meta['category_name'])) {
            $categoryName = $meta['category_name'];
        }

        $correct = (int) ($meta['correct_count'] ?? 0);
        $total = (int) ($meta['total_questions'] ?? count($this->question_ids ?? []));
        $percentage = round((float) $formatter->calculateWeightedPercentage($this->cat_scores ?? []), 2);
        $durationSecs = (int) ($meta['duration_secs'] ?? 0);
        $durationText = $formatter->formatDurationText($durationSecs);

        $status = 'Completed';
        if ($trackName !== 'Drill') {
            $status = $percentage >= 80 ? 'Pass' : 'Fail';
        }

        $avgTimePerQuestion = $total > 0 && $durationSecs > 0
            ? round($durationSecs / $total, 1)
            : 0;

        return [
            'id' => $this->id,
            'category_id' => $this->category_id,
            'date' => $this->created_at?->format('M d, Y') ?? '',
            'time' => $this->created_at?->format('h:i A') ?? '',
            'track' => $trackName,
            'category' => $categoryName,
            'score' => $percentage,
            'correct' => $correct,
            'wrong' => max(0, $total - $correct),
            'total' => $total,
            'category_scores' => $formatter->formatAttemptCategoryScores($this->cat_scores ?? []),
            'status' => $status,
            'duration' => $durationText,
            'duration_secs' => $durationSecs,
            'avg_time_per_q' => $avgTimePerQuestion,
            'created_at' => $this->created_at?->toIso8601String(),
            'selected_subcategories' => $meta['selected_subcategories'] ?? null,
            'language' => $meta['language'] ?? 'English',
            'question_count' => $meta['question_count'] ?? $total,
            'is_timed' => $meta['is_timed'] ?? true,
        ];
    }
}
