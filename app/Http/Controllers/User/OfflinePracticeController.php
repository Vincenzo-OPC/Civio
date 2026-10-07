<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Actions\Offline\SyncOfflinePracticeAction;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Offline\SyncOfflineAttemptsRequest;
use Illuminate\Http\JsonResponse;

/** Lite L2: sync queued offline drill answers; the server re-grades them. */
class OfflinePracticeController extends Controller
{
    public function store(SyncOfflineAttemptsRequest $request, SyncOfflinePracticeAction $action): JsonResponse
    {
        $userId = $request->user()?->getAuthIdentifier();

        return response()->json([
            'success' => true,
            ...$action->handle($request->ownerKey(), $userId === null ? null : (int) $userId, $request->answers()),
        ]);
    }
}
