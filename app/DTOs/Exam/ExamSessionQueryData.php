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
        public bool $freeAttempt = false,
        public bool $isDrill = false,
        public ?int $drillCategoryId = null,
        public ?string $drillCategoryName = null,
        /** @var array<int, int> */
        public array $customQuestionIds = [],
    ) {}

    public static function fromRequest(Request $request): self
    {
        $pendingGuest = $request->session()->get('pending_guest_attempt_id');

        return new self(
            attemptId: $request->filled('attempt_id') ? (int) $request->input('attempt_id') : null,
            retakeSame: $request->filled('retake_same') ? (int) $request->input('retake_same') : null,
            retakeFresh: $request->filled('retake_fresh') ? (int) $request->input('retake_fresh') : null,
            pendingGuestAttemptId: $pendingGuest ? (int) $pendingGuest : null,
            freeAttempt: $request->boolean('free_attempt'),
            isDrill: $request->input('drill') === 'true' || $request->input('drill') === '1',
            drillCategoryId: $request->filled('category_id') && is_numeric($request->input('category_id')) ? (int) $request->input('category_id') : null,
            drillCategoryName: $request->filled('category_name') ? (string) $request->input('category_name') : null,
            customQuestionIds: self::parseIds($request->input('custom_question_ids')),
        );
    }

    /**
     * @return array<int, int>
     */
    private static function parseIds(mixed $raw): array
    {
        if (is_string($raw) && $raw !== '') {
            $decoded = json_decode($raw, true);
            $raw = is_array($decoded) ? $decoded : [];
        }

        if (! is_array($raw)) {
            return [];
        }

        return array_slice(array_values(array_unique(array_map('intval', array_filter($raw, 'is_numeric')))), 0, 2000);
    }
}
