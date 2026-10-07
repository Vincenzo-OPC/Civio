<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\StartExamSessionRequest;
use App\Services\Exam\MockSessionService;
use Illuminate\Http\JsonResponse;

class ExamSessionController extends Controller
{
    public function __construct(protected MockSessionService $service) {}

    /**
     * Start a full mock: the server picks the items (unique only, blueprint
     * quotas, weak-topic bias) and returns only those, keys withheld.
     */
    public function store(StartExamSessionRequest $request): JsonResponse
    {
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
        );

        return response()->json(['success' => true, ...$payload]);
    }
}
