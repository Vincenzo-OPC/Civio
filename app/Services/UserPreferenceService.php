<?php

declare(strict_types=1);

namespace App\Services;

use App\Enums\AnalysisMode;
use App\Jobs\GenerateUserAnalysisJob;
use App\Models\ExamAttempt;
use App\Models\UserAiAnalysis;
use Illuminate\Support\Facades\Cache;

class UserPreferenceService
{
    public function __construct(
        protected DeterministicAnalysisService $deterministicService
    ) {}

    /**
     * Get the current analysis mode for the user.
     */
    public function getAnalysisMode(int $userId): string
    {
        $aiAvailable = (bool) config('services.ai.analysis_enabled');
        $mode = Cache::get("user-analysis-mode-{$userId}", 'ai');

        if (! $aiAvailable && $mode === 'ai') {
            $mode = 'instant';
        }

        return $mode;
    }

    public function isAiAvailable(): bool
    {
        return (bool) config('services.ai.analysis_enabled');
    }

    /**
     * Switch the user's analysis mode and trigger appropriate regeneration.
     */
    public function switchAnalysisMode(int $userId, AnalysisMode|string $mode): void
    {
        $modeEnum = $mode instanceof AnalysisMode ? $mode : (AnalysisMode::tryFrom($mode) ?? AnalysisMode::Instant);
        Cache::forever("user-analysis-mode-{$userId}", $modeEnum->value);

        if ($modeEnum === AnalysisMode::Instant) {
            $this->regenerateInstantAnalysis($userId);
        } elseif ($modeEnum === AnalysisMode::Ai) {
            $this->triggerAiRegeneration($userId);
        }
    }

    private function regenerateInstantAnalysis(int $userId): void
    {
        $latestAttemptId = ExamAttempt::where('user_id', $userId)->latest()->value('id');

        if (! $latestAttemptId) {
            return;
        }

        UserAiAnalysis::updateOrCreate(
            ['user_id' => $userId],
            [
                'last_exam_attempt_id' => $latestAttemptId,
                'analysis_json' => $this->deterministicService->generate($userId, $latestAttemptId),
            ]
        );
    }

    private function triggerAiRegeneration(int $userId): void
    {
        $latestMockAttemptId = ExamAttempt::where('user_id', $userId)
            ->whereNull('category_id')
            ->latest()
            ->value('id');

        if (! $latestMockAttemptId || ! config('services.ai.analysis_enabled')) {
            return;
        }

        UserAiAnalysis::where('user_id', $userId)->delete();
        Cache::forget("ai-analysis-failed-{$userId}");
        Cache::forget("ai-analysis-generating-{$userId}");
        Cache::put("ai-analysis-generating-{$userId}", true, 60);
        GenerateUserAnalysisJob::dispatchAfterResponse($userId, $latestMockAttemptId);
    }
}
