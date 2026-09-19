<?php

declare(strict_types=1);

namespace App\Services;

use App\Http\Resources\ExamAttemptResource;
use App\Models\ExamAttempt;
use App\Repositories\ExamAttemptRepositoryInterface;
use Illuminate\Database\Eloquent\Collection;

class ExamAttemptService
{
    public function __construct(
        protected ExamAttemptRepositoryInterface $repository,
        protected ExamAttemptFormatter $formatter
    ) {}

    public function getScorecardAttempt(int $attemptId, ?int $userId, ?int $pendingGuestId): ExamAttempt
    {
        if ($userId === null) {
            if ($pendingGuestId === null || $pendingGuestId !== $attemptId) {
                abort(403, 'Unauthorized access to scorecard.');
            }

            $attempt = $this->repository->findGuestAttempt($attemptId);
        } else {
            $attempt = $this->repository->findUserAttempt($attemptId, $userId);
        }

        if (! $attempt) {
            abort(404, 'Attempt not found.');
        }

        return $attempt;
    }

    /**
     * @return array{attempt_id: int, question_ids: array<int, int>, track: string, mode: string}
     */
    public function getRetakeSource(int $attemptId, int $userId, string $mode): array
    {
        $attempt = $this->repository->findUserAttempt($attemptId, $userId);

        if (! $attempt) {
            abort(404, 'Attempt not found.');
        }

        $meta = $attempt->cat_scores['metadata'] ?? [];

        return [
            'attempt_id' => $attempt->id,
            'question_ids' => $attempt->question_ids,
            'track' => $meta['track'] ?? 'Professional',
            'mode' => $mode,
        ];
    }

    public function getLatestUserAttemptId(int $userId): ?int
    {
        return $this->repository->getLatestUserAttemptId($userId);
    }

    /**
     * @param  array{
     *     search?: ?string,
     *     track?: ?string,
     *     date?: ?string,
     *     page?: int|string
     * }  $filters
     * @return array{
     *     attempts: array<int, mixed>,
     *     stats: array<string, mixed>,
     *     pagination: array{current_page: int, per_page: int, total: int, last_page: int},
     *     needs_redirect: bool,
     *     redirect_page: int
     * }
     */
    public function getUserHistoryData(int $userId, array $filters, int $perPage = 10): array
    {
        $allUserAttempts = $this->repository->getUserAttempts($userId);
        $stats = $this->calculateHistoryStats($allUserAttempts);

        $filteredAttempts = $allUserAttempts;

        $dateFilter = $filters['date'] ?? null;
        if ($dateFilter === '7') {
            $filteredAttempts = $filteredAttempts->filter(fn ($a) => $a->created_at >= now()->subDays(7));
        } elseif ($dateFilter === '30') {
            $filteredAttempts = $filteredAttempts->filter(fn ($a) => $a->created_at >= now()->subDays(30));
        }

        $trackFilter = $filters['track'] ?? null;
        if ($trackFilter && $trackFilter !== 'All Tracks') {
            $filteredAttempts = $filteredAttempts->filter(function ($attempt) use ($trackFilter) {
                $meta = $attempt->cat_scores['metadata'] ?? [];
                $trackName = $meta['track'] ?? ($attempt->category_id !== null ? 'Drill' : 'Professional');

                return strtolower($trackName) === strtolower($trackFilter);
            });
        }

        $search = $filters['search'] ?? null;
        if ($search) {
            $searchLower = strtolower($search);
            $filteredAttempts = $filteredAttempts->filter(function ($attempt) use ($searchLower) {
                $meta = $attempt->cat_scores['metadata'] ?? [];
                $trackName = $meta['track'] ?? ($attempt->category_id !== null ? 'Drill' : 'Professional');
                $categoryName = $attempt->category?->name ?? $meta['category_name'] ?? 'Full Mock Exam';

                return str_contains(strtolower($categoryName), $searchLower) ||
                    str_contains(strtolower($trackName), $searchLower) ||
                    str_contains(strtolower((string) $attempt->id), $searchLower);
            });
        }

        $page = (int) ($filters['page'] ?? 1);
        $totalItems = $filteredAttempts->count();
        $lastPage = max(1, (int) ceil($totalItems / $perPage));
        $needsRedirect = $page > $lastPage && $totalItems > 0;

        $pageItems = $filteredAttempts->slice(($page - 1) * $perPage, $perPage)->values();
        $paginatedAttempts = ExamAttemptResource::collection($pageItems)->resolve();

        return [
            'attempts' => $paginatedAttempts,
            'stats' => $stats,
            'pagination' => [
                'current_page' => $page,
                'per_page' => $perPage,
                'total' => $totalItems,
                'last_page' => $lastPage,
            ],
            'needs_redirect' => $needsRedirect,
            'redirect_page' => $lastPage,
        ];
    }

    /**
     * @param  Collection<int, ExamAttempt>  $attempts
     * @return array<string, mixed>
     */
    public function calculateHistoryStats(Collection $attempts): array
    {
        $totalAttempts = $attempts->count();
        if ($totalAttempts === 0) {
            return [
                'total_attempts' => 0,
                'total_exams' => 0,
                'total_drills' => 0,
                'avg_score' => 0,
                'pass_rate' => 0,
                'total_duration' => '0m',
                'streak' => 0,
                'trend' => 0,
            ];
        }

        $totalDurationSecs = 0;
        $examDurationSecs = 0;
        $drillDurationSecs = 0;
        $totalScores = 0;
        $examScoresSum = 0;
        $drillScoresSum = 0;
        $mockExamCount = 0;
        $passedMockCount = 0;
        $drillCount = 0;
        $scoresList = [];

        foreach ($attempts as $attempt) {
            $meta = $attempt->cat_scores['metadata'] ?? [];
            $trackName = $meta['track'] ?? 'Drill';
            if ($attempt->category_id !== null && ! $trackName) {
                $trackName = 'Drill';
            }

            $percentage = $this->formatter->calculateWeightedPercentage($attempt->cat_scores ?? []);
            $totalScores += $percentage;
            $scoresList[] = [
                'score' => $percentage,
                'track' => $trackName,
                'created_at' => $attempt->created_at,
            ];

            $durationSecs = (int) ($meta['duration_secs'] ?? 0);
            $totalDurationSecs += $durationSecs;

            if ($trackName !== 'Drill') {
                $mockExamCount++;
                $examScoresSum += $percentage;
                $examDurationSecs += $durationSecs;
                if ($percentage >= 80) {
                    $passedMockCount++;
                }
            } else {
                $drillCount++;
                $drillScoresSum += $percentage;
                $drillDurationSecs += $durationSecs;
            }
        }

        $avgScore = round($totalScores / $totalAttempts, 1);
        $examAvgScore = $mockExamCount > 0 ? round($examScoresSum / $mockExamCount, 1) : 0;
        $drillAvgScore = $drillCount > 0 ? round($drillScoresSum / $drillCount, 1) : 0;
        $passRate = $mockExamCount > 0 ? round(($passedMockCount / $mockExamCount) * 100, 1) : 0;

        $streak = 0;
        foreach ($scoresList as $item) {
            if ($item['track'] !== 'Drill') {
                if ($item['score'] >= 80) {
                    $streak++;
                } else {
                    break;
                }
            } else {
                if ($item['score'] >= 75) {
                    $streak++;
                } else {
                    break;
                }
            }
        }

        $recent5 = array_slice($scoresList, 0, 5);
        $prev5 = array_slice($scoresList, 5, 5);
        $recentAvg = count($recent5) > 0 ? array_sum(array_column($recent5, 'score')) / count($recent5) : 0;
        $prevAvg = count($prev5) > 0 ? array_sum(array_column($prev5, 'score')) / count($prev5) : $recentAvg;
        $trend = round($recentAvg - $prevAvg, 1);

        return [
            'total_attempts' => $totalAttempts,
            'total_exams' => $mockExamCount,
            'total_drills' => $drillCount,
            'avg_score' => $avgScore,
            'exam_avg_score' => $examAvgScore,
            'drill_avg_score' => $drillAvgScore,
            'pass_rate' => $passRate,
            'total_duration' => $this->formatter->formatDurationText($totalDurationSecs),
            'exam_duration' => $this->formatter->formatDurationText($examDurationSecs),
            'drill_duration' => $this->formatter->formatDurationText($drillDurationSecs),
            'streak' => $streak,
            'trend' => $trend,
        ];
    }

    public function deleteUserAttempt(ExamAttempt $attempt): bool
    {
        return (bool) $attempt->delete();
    }

    /**
     * @param  array<int, int>  $attemptIds
     */
    public function bulkDeleteUserAttempts(int $userId, array $attemptIds): int
    {
        return $this->repository->deleteUserAttempts($userId, $attemptIds);
    }
}
