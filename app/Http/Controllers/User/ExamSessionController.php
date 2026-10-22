<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Enums\ExamMode;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\StartExamSessionRequest;
use App\Services\Exam\MockSessionService;
use Illuminate\Http\JsonResponse;

class ExamSessionController extends Controller
{
    public function __construct(protected MockSessionService $service) {}

    /**
     * Start a full mock: the server picks the items (unique only, blueprint
     * Civio blueprint quotas; weak-topic bias in Study only) and returns only those,
     * keys withheld. Strict ignores the client bias (ADR-0002).
     * `mode` is `study` (default) or `strict`.
     */
    public function store(StartExamSessionRequest $request): JsonResponse
    {
        // Public free-attempt policy: a limited guest who already submitted
        // cannot open more mock sessions (they could not submit them anyway).
        if (auth()->guest() && ! config('civio.guest_unlimited')
            && $request->session()->has('pending_guest_attempt_id')) {
            return response()->json([
                'success' => false,
                'message' => 'You have already completed your free guest attempt.',
            ], 403);
        }

        $validated = $request->validated();
        $bias = (array) ($validated['bias'] ?? []);

        $payload = $this->service->start(
            userId: auth()->id(),
            track: (string) $validated['track'],
            clientBias: [
                'wrong_ids' => array_values(array_map('intval', (array) ($bias['wrong_ids'] ?? []))),
                'weak_subcategories' => array_values(array_map('strval', (array) ($bias['weak_subcategories'] ?? []))),
                'weak_categories' => array_values(array_map('strval', (array) ($bias['weak_categories'] ?? []))),
            ],
            session: $request->session(),
            mode: ExamMode::fromRaw(isset($validated['mode']) ? (string) $validated['mode'] : null),
        );

        return response()->json(['success' => true, ...$payload]);
    }
}
