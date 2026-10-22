<?php

declare(strict_types=1);

namespace App\Http\Controllers\User\Dexter;

use App\Http\Controllers\Controller;
use App\Models\Question;
use App\Services\Dexter\RescueService;
use App\Services\Exam\StrictMockLock;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * POST /dexter/rescue (ADR-0003). Study Mode only, behind DEXTER_RESCUE_ENABLED.
 * Order matters: the gate, then the Strict lock, then any lookup, so neither
 * a disabled gate nor an active Strict Mock reveals anything about the item.
 */
class RescueController extends Controller
{
    public function __construct(private readonly RescueService $rescue) {}

    public function store(Request $request): JsonResponse
    {
        if (! RescueService::enabled()) {
            return response()->json(['enabled' => false], 404);
        }

        if ($this->rescue->strictActive($request->user()?->id, $request->session())) {
            return response()->json(['locked' => true, 'message' => StrictMockLock::MESSAGE], 423);
        }

        $validated = $request->validate([
            'question_id' => 'required|integer',
            'chosen_option' => 'required|integer|min:0|max:7',
        ]);

        $question = Question::query()->where('status', 'active')->find((int) $validated['question_id']);
        if ($question === null) {
            return response()->json(['message' => 'Question not found'], 404);
        }

        return response()->json(['rescue' => $this->rescue->forWrongAnswer((int) $request->user()->id, $question, (int) $validated['chosen_option'])]);
    }
}
