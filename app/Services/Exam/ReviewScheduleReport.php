<?php

declare(strict_types=1);

namespace App\Services\Exam;

/** One request's scheduler result. The container keeps a single instance. */
final class ReviewScheduleReport
{
    public ?string $status = null;

    public function reset(): void
    {
        $this->status = null;
    }
}
