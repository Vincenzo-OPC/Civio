<?php

declare(strict_types=1);

namespace App\Actions\Exam;

use App\DTOs\Exam\SubmitExamAttemptData;
use App\DTOs\Exam\SubmitExamAttemptResult;
use App\Enums\ExamMode;
use App\Models\ExamSession;
use App\Models\Question;
use App\Repositories\ExamAttemptRepositoryInterface;
use App\Services\Exam\MockPoolSelector;
use App\Services\Exam\ReviewMistakeRecorder;
use App\Services\Exam\ReviewScheduleApplier;
use App\Services\Exam\ReviewScheduleReport;
use App\Services\ExamGradingService;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Throwable;

class SubmitExamAttemptAction
{
    public function __construct(
        protected ExamAttemptRepositoryInterface $repository,
        protected ExamGradingService $gradingService,
    ) {}

    public function execute(
        SubmitExamAttemptData $data,
        ?int $userId,
        ?string $clientIp = null,
        bool $hasPendingGuestAttempt = false,
        ?ExamSession $examSession = null,
        ?string $reviewSessionHash = null,
    ): SubmitExamAttemptResult {
        $lockKey = $examSession !== null
            ? 'exam-submit:'.$examSession->id
            : 'practice-submit:'.($userId !== null ? 'user:'.$userId : 'ip:'.$clientIp);
        $lock = Cache::lock($lockKey, 30);

        if (! $lock->get()) {
            return new SubmitExamAttemptResult(false, 429, message: 'Attempt submission already in progress. Please wait.');
        }

        try {
            return DB::transaction(function () use ($data, $userId, $hasPendingGuestAttempt, $examSession, $reviewSessionHash) {
                // Re-read under the row lock: a previously loaded model is not
                // evidence that another request has not already submitted it.
                $session = $examSession !== null
                    ? ExamSession::whereKey($examSession->id)->lockForUpdate()->firstOrFail()
                    : null;

                if ($session !== null && ! $session->isOpen()) {
                    return new SubmitExamAttemptResult(false, 409, message: 'This mock was already submitted.');
                }

                $ids = $session !== null ? array_map('intval', $session->question_ids) : $data->questionIds;
                if (array_diff($data->questionIds, $ids) !== []) {
                    return new SubmitExamAttemptResult(false, 422, message: 'These answers do not match the items the server picked for this mock.');
                }

                // Re-check the database, not the cached pool. A withdrawn item
                // must not be graded or return a key even if it was served earlier.
                $active = Question::with('subcategory.category')
                    ->whereIn('id', $ids)
                    ->where('status', 'active')
                    ->orderBy('id')
                    ->lockForUpdate()
                    ->get()
                    ->keyBy('id');
                // A server-held mock still grades when an item was retired after
                // serving; the grader records it as retired_count, outside the score.
                if ($session === null && $active->count() !== count($ids)) {
                    return new SubmitExamAttemptResult(false, 422, message: 'A practice item is no longer available. Start a new session.');
                }

                $answers = $session?->isExpired()
                    ? (array) ($session->saved_answers ?? [])
                    : $this->gradingService->normalizeAnswers($data->questionIds, $data->answers);
                foreach ($answers as $id => $chosen) {
                    if ($chosen !== null && ! $active->has($id)) {
                        $answers[$id] = null;

                        continue;
                    }
                    if ($chosen !== null && ! array_key_exists($chosen, (array) $active[$id]->options)) {
                        return new SubmitExamAttemptResult(false, 422, message: 'An answer does not match the available options.');
                    }
                }

                $answeredCount = count(array_filter($answers, fn ($answer) => $answer !== null));
                if ($userId === null && $hasPendingGuestAttempt && ! config('civio.guest_unlimited')) {
                    return new SubmitExamAttemptResult(false, 403, message: 'You have already completed your free guest attempt.');
                }

                // Mock submissions always grade the complete served set, including
                // entirely blank submissions. Legacy drills keep their old policy.
                if ($session === null) {
                    if ($userId === null && $answeredCount < count($ids)) {
                        return new SubmitExamAttemptResult(false, 422, message: 'Guest attempt must be complete (all questions answered).');
                    }
                    if ($userId !== null && $answeredCount < count($ids) / 2) {
                        return new SubmitExamAttemptResult(true, 200, message: 'Dummy attempt ignored.');
                    }
                }

                $answers = array_replace(array_fill_keys($ids, null), $answers);
                $meta = $data->clientMetadata;
                $meta['track'] = $session?->track ?? 'Drill';
                if ($session?->isStrict()) {
                    $meta['is_timed'] = true;
                    $meta['deadline_at'] = $session->deadline()?->toISOString();
                    $meta['submitted_after_deadline'] = $session->isExpired();
                    $meta['duration_secs'] = min(
                        MockPoolSelector::timeLimitFor(MockPoolSelector::levelFor($session->track)),
                        max(0, (int) $session->created_at->diffInSeconds(now()))
                    );
                }
                $graded = $this->gradingService->grade($ids, $answers, $meta);
                $attempt = $this->repository->create([
                    'user_id' => $userId,
                    'category_id' => $data->categoryId,
                    'mode' => $session?->mode ?? ExamMode::Study,
                    'question_ids' => $ids,
                    'answers' => $graded['answers'],
                    'cat_scores' => $graded['cat_scores'],
                ]);
                $session?->forceFill(['exam_attempt_id' => $attempt->id])->save();

                $staged = app(ReviewMistakeRecorder::class)->record(
                    $userId,
                    (int) $attempt->id,
                    $session?->isStrict() ?? false,
                    $answers,
                    $active,
                    $reviewSessionHash,
                );

                if ($staged && $userId !== null) {
                    $this->deferSchedule($userId);
                }

                return new SubmitExamAttemptResult(
                    success: true,
                    statusCode: 200,
                    attemptId: $attempt->id,
                    score: $graded['score'],
                    correctCount: $graded['correct_count'],
                    wrongCount: $graded['wrong_count'],
                    skippedCount: $graded['skipped_count'],
                    totalQuestions: $graded['total_questions'],
                    catScores: $graded['cat_scores'],
                    answerKeys: $graded['answer_keys'],
                    answers: $graded['answers'],
                );
            });
        } finally {
            $lock->release();
        }
    }

    private function deferSchedule(int $userId): void
    {
        $apply = function () use ($userId): void {
            $report = app(ReviewScheduleReport::class);

            try {
                $report->status = app(ReviewScheduleApplier::class)->apply($userId);
            } catch (Throwable $exception) {
                report($exception);
                $report->status = ReviewScheduleApplier::FAILED;
            }
        };

        if (app()->runningUnitTests()) {
            $apply();

            return;
        }

        DB::afterCommit($apply);
    }
}
