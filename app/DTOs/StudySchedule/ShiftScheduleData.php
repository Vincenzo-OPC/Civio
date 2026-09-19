<?php

declare(strict_types=1);

namespace App\DTOs\StudySchedule;

use App\Http\Requests\User\StudySchedule\ShiftStudyScheduleRequest;

readonly class ShiftScheduleData
{
    public function __construct(
        public string $mode,
        public int $days = 1,
        public ?string $fromDate = null,
    ) {}

    public static function fromRequest(ShiftStudyScheduleRequest $request): self
    {
        $v = $request->validated();

        return new self(
            mode: (string) $v['mode'],
            days: isset($v['days']) ? (int) $v['days'] : 1,
            fromDate: isset($v['from_date']) ? (string) $v['from_date'] : null,
        );
    }
}
