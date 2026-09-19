<?php

declare(strict_types=1);

namespace App\DTOs\Feedback;

use App\Http\Requests\Admin\Feedback\StoreFeedbackRequest;

readonly class SubmitFeedbackData
{
    public function __construct(
        public int $userId,
        public int $flaggableId,
        public string $flaggableType,
        public string $reason,
        public ?string $details = null,
    ) {}

    public static function fromRequest(StoreFeedbackRequest $request, int $userId): self
    {
        $v = $request->validated();

        return new self(
            userId: $userId,
            flaggableId: (int) $v['flaggable_id'],
            flaggableType: (string) $v['flaggable_type'],
            reason: trim((string) $v['reason']),
            details: ! empty($v['details']) ? trim((string) $v['details']) : null,
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toAttributes(): array
    {
        return [
            'user_id' => $this->userId,
            'flaggable_id' => $this->flaggableId,
            'flaggable_type' => $this->flaggableType,
            'reason' => $this->reason,
            'details' => $this->details,
            'status' => 'pending',
        ];
    }
}
