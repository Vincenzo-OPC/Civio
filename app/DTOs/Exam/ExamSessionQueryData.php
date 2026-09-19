<?php

declare(strict_types=1);

namespace App\DTOs\Exam;

use Illuminate\Http\Request;

readonly class ExamSessionQueryData
{
    public function __construct(
        public ?int $attemptId = null,
        public ?int $retakeSame = null,
        public ?int $retakeFresh = null,
        public ?int $pendingGuestAttemptId = null,
        public bool $freeAttempt = false
    ) {}

    public static function fromRequest(Request $request): self
    {
        $pendingGuest = $request->session()->get('pending_guest_attempt_id');

        return new self(
            attemptId: $request->filled('attempt_id') ? (int) $request->input('attempt_id') : null,
            retakeSame: $request->filled('retake_same') ? (int) $request->input('retake_same') : null,
            retakeFresh: $request->filled('retake_fresh') ? (int) $request->input('retake_fresh') : null,
            pendingGuestAttemptId: $pendingGuest ? (int) $pendingGuest : null,
            freeAttempt: $request->boolean('free_attempt')
        );
    }
}
