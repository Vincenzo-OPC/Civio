<?php

declare(strict_types=1);

namespace App\Actions\Exam;

use App\DTOs\Exam\SubmitExamAttemptData;
use App\DTOs\Exam\SubmitExamAttemptResult;
use App\Repositories\ExamAttemptRepositoryInterface;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

class SubmitExamAttemptAction
{
    public function __construct(
        protected ExamAttemptRepositoryInterface $repository
    ) {}

    public function execute(
        SubmitExamAttemptData $data,
        ?int $userId,
        ?string $clientIp = null,
        bool $hasPendingGuestAttempt = false
    ): SubmitExamAttemptResult {
        $answeredCount = count(array_filter($data->answers, function ($answer) {
            return $answer !== null && $answer !== '';
        }));

        $totalQuestions = count($data->questionIds);
        $completionRate = $totalQuestions > 0 ? ($answeredCount / $totalQuestions) * 100 : 0;

        if ($userId === null) {
            if ($hasPendingGuestAttempt) {
                return new SubmitExamAttemptResult(
                    success: false,
                    statusCode: 403,
                    message: 'You have already completed your free guest attempt.'
                );
            }

            if ($answeredCount < $totalQuestions) {
                return new SubmitExamAttemptResult(
                    success: false,
                    statusCode: 422,
                    message: 'Guest attempt must be complete (all questions answered).'
                );
            }
        } else {
            // Ignore empty or dummy attempts (less than 50% answered)
            if ($completionRate < 50) {
                return new SubmitExamAttemptResult(
                    success: true,
                    statusCode: 200,
                    attemptId: null,
                    message: 'Dummy attempt ignored.'
                );
            }
        }

        $lockKey = $userId ? "user-exam-attempt-submission-{$userId}" : "guest-exam-attempt-submission-{$clientIp}";
        $lock = Cache::lock($lockKey, 5);

        if (! $lock->get()) {
            return new SubmitExamAttemptResult(
                success: false,
                statusCode: 429,
                message: 'Attempt submission already in progress. Please wait.'
            );
        }

        try {
            $attempt = DB::transaction(function () use ($data, $userId) {
                return $this->repository->create([
                    'user_id' => $userId,
                    'category_id' => $data->categoryId,
                    'question_ids' => $data->questionIds,
                    'answers' => $data->answers,
                    'cat_scores' => $data->catScores,
                ]);
            });

            return new SubmitExamAttemptResult(
                success: true,
                statusCode: 200,
                attemptId: $attempt->id
            );
        } finally {
            $lock->release();
        }
    }
}
