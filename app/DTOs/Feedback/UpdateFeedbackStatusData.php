<?php

declare(strict_types=1);

namespace App\DTOs\Feedback;

use App\Http\Requests\Admin\Feedback\UpdateFeedbackStatusRequest;

readonly class UpdateFeedbackStatusData
{
    public function __construct(
        public string $status,
    ) {}

    public static function fromRequest(UpdateFeedbackStatusRequest $request): self
    {
        return new self(
            status: (string) $request->validated('status'),
        );
    }
}
