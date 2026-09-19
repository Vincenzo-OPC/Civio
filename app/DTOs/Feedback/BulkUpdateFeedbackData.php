<?php

declare(strict_types=1);

namespace App\DTOs\Feedback;

use App\Http\Requests\Admin\Feedback\BulkUpdateFeedbackRequest;

readonly class BulkUpdateFeedbackData
{
    /**
     * @param  array<int, int>  $ids
     */
    public function __construct(
        public array $ids,
        public string $status,
    ) {}

    public static function fromRequest(BulkUpdateFeedbackRequest $request): self
    {
        return new self(
            ids: array_map('intval', (array) $request->validated('ids')),
            status: (string) $request->validated('status'),
        );
    }
}
