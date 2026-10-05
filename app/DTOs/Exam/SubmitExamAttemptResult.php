<?php

declare(strict_types=1);

namespace App\DTOs\Exam;

readonly class SubmitExamAttemptResult
{
    /**
     * @param  array<string, mixed>|null  $catScores
     * @param  array<int, array{id: int, correct_option: int, explanation: string}>|null  $answerKeys
     * @param  array<string, int|null>|null  $answers
     */
    public function __construct(
        public bool $success,
        public int $statusCode,
        public ?int $attemptId = null,
        public ?string $message = null,
        public ?int $score = null,
        public ?int $correctCount = null,
        public ?int $wrongCount = null,
        public ?int $skippedCount = null,
        public ?int $totalQuestions = null,
        public ?array $catScores = null,
        public ?array $answerKeys = null,
        public ?array $answers = null,
    ) {}

    /**
     * @return array<string, mixed>
     */
    public function toResponseArray(): array
    {
        $data = ['success' => $this->success];

        if ($this->attemptId !== null || $this->message === 'Dummy attempt ignored.') {
            $data['attempt_id'] = $this->attemptId;
        }

        if ($this->message !== null) {
            $data['message'] = $this->message;
        }

        if ($this->score !== null) {
            $data['score'] = $this->score;
            $data['correct_count'] = $this->correctCount;
            $data['wrong_count'] = $this->wrongCount;
            $data['skipped_count'] = $this->skippedCount;
            $data['total_questions'] = $this->totalQuestions;
            $data['cat_scores'] = $this->catScores;
            $data['answer_keys'] = $this->answerKeys;
            $data['answers'] = $this->answers;
        }

        return $data;
    }
}
