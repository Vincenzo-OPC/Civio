<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class AnalyticsMetricsResource extends JsonResource
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
        $metrics = is_array($this->resource) ? $this->resource : (array) $this->resource;

        $strongestArea = (string) ($metrics['strongestArea'] ?? 'Not Started');
        $weakestArea = (string) ($metrics['weakestArea'] ?? 'Not Started');

        $cleanedStrongest = str_replace([' Ability', ' Information'], '', $strongestArea);
        $cleanedWeakest = str_replace([' Ability', ' Information'], '', $weakestArea);

        $mockExamCount = (int) ($metrics['mockExamCount'] ?? 0);
        $coveredCategoriesCount = (int) ($metrics['coveredCategoriesCount'] ?? 0);
        $isIncompleteSyllabus = ($mockExamCount === 0 && $coveredCategoriesCount < 3);

        return [
            'filters' => [
                'track' => $metrics['filters']['track'] ?? 'Professional',
                'runs' => $metrics['filters']['runs'] ?? 'all',
            ],
            'avgScore' => (int) ($metrics['avgScore'] ?? 0),
            'totalExams' => (int) ($metrics['totalExams'] ?? 0),
            'strongestArea' => $cleanedStrongest,
            'weakestArea' => $cleanedWeakest,
            'chartData' => $metrics['chartData'] ?? [],
            'categories' => $metrics['categories'] ?? [],
            'passingRate' => (int) ($metrics['passingRate'] ?? 0),
            'totalDuration' => (string) ($metrics['totalDurationText'] ?? '0 mins'),
            'avgDuration' => (string) ($metrics['avgDurationText'] ?? '0 mins'),
            'totalQuestionsSolved' => (int) ($metrics['totalQuestionsSolved'] ?? 0),
            'daysUntilExam' => $metrics['daysUntilExam'] ?? null,
            'examDate' => $metrics['examDate'] ?? null,
            'examDateRaw' => $metrics['examDateRaw'] ?? null,
            'pacingTrend' => $metrics['pacingTrend'] ?? [],
            'attemptBreakdowns' => $metrics['attemptBreakdowns'] ?? [],
            'cseReadinessIndex' => (int) ($metrics['cseReadinessIndex'] ?? 0),
            'subtestThresholds' => $metrics['subtestThresholds'] ?? [],
            'hasSubtestRisk' => (bool) ($metrics['hasSubtestRisk'] ?? false),
            'percentileRank' => (int) ($metrics['percentileRank'] ?? 50),
            'isIncompleteSyllabus' => $isIncompleteSyllabus,
            'coveredCategoriesCount' => $coveredCategoriesCount,
            'mockExamCount' => $mockExamCount,
        ];
    }
}
