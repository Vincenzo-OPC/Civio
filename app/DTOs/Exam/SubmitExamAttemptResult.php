<?php

declare(strict_types=1);

namespace App\DTOs\Exam;

readonly class SubmitExamAttemptResult
{
    public function __construct(
        public bool $success,
        public int $statusCode,
        public ?int $attemptId = null,
        public ?string $message = null,
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

        return $data;
    }
}
