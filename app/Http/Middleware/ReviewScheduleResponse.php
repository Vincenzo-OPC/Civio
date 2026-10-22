<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Services\Exam\ReviewScheduleApplier;
use App\Services\Exam\ReviewScheduleReport;
use App\Support\ReviewCopy;
use Closure;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Adds the scheduler result after the request transaction commits.
 * Listed outside TransactionMiddleware so the JSON is updated after commit
 * and before response compression.
 */
final class ReviewScheduleResponse
{
    public function handle(Request $request, Closure $next): Response
    {
        app(ReviewScheduleReport::class)->reset();

        $response = $next($request);
        $status = app(ReviewScheduleReport::class)->status;

        if (! $response instanceof JsonResponse || $status === null || $status === ReviewScheduleApplier::UNCHANGED) {
            return $response;
        }

        $data = $response->getData(true);

        if (! is_array($data)) {
            return $response;
        }

        $data['review_schedule'] = $status;

        if ($status === ReviewScheduleApplier::FAILED) {
            $data['review_notice'] = ReviewCopy::REMINDER_FAILED;
        }

        $response->setData($data);

        return $response;
    }
}
