<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\DTOs\Drill\BookmarkQuestionData;
use App\DTOs\Drill\UpsertSavedDrillSetData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Drill\SavedDrillSets\AddQuestionToSavedSetRequest;
use App\Http\Requests\User\Drill\SavedDrillSets\StoreSavedDrillSetRequest;
use App\Http\Requests\User\Drill\SavedDrillSets\UpdateSavedDrillSetRequest;
use App\Http\Resources\SavedDrillSetResource;
use App\Models\Question;
use App\Models\SavedDrillSet;
use App\Repositories\SavedDrillSetRepositoryInterface;
use App\Services\DrillService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class SavedDrillSetController extends Controller
{
    public function __construct(
        protected DrillService $drillService,
        protected SavedDrillSetRepositoryInterface $drillSetRepository,
    ) {}

    /**
     * List user's saved drill sets with question counts.
     */
    public function index(Request $request): JsonResponse
    {
        $userId = $this->requireUser()->id;
        $sets = $this->drillSetRepository->getUserSets($userId);

        return response()->json(['sets' => SavedDrillSetResource::collection($sets)]);
    }

    /**
     * Store a new saved drill set.
     */
    public function store(StoreSavedDrillSetRequest $request): JsonResponse|RedirectResponse
    {
        $userId = $this->requireUser()->id;
        $dto = UpsertSavedDrillSetData::fromStoreRequest($request);

        $set = $this->drillService->createSavedSet($userId, $dto);

        if ($request->wantsJson()) {
            return response()->json([
                'status' => 'success',
                'set' => (new SavedDrillSetResource($set))->resolve(),
            ]);
        }

        return $this->backWithSuccess('Practice set created successfully.');
    }

    /**
     * Update an existing saved drill set.
     */
    public function update(UpdateSavedDrillSetRequest $request, SavedDrillSet $savedDrillSet): JsonResponse|RedirectResponse
    {
        $this->authorize('update', $savedDrillSet);

        $dto = UpsertSavedDrillSetData::fromUpdateRequest($request, $savedDrillSet->color);
        $this->drillService->updateSavedSet($savedDrillSet, $dto);

        if ($request->wantsJson()) {
            return response()->json([
                'status' => 'success',
                'set' => (new SavedDrillSetResource($savedDrillSet->fresh()))->resolve(),
            ]);
        }

        return $this->backWithSuccess('Practice set updated successfully.');
    }

    /**
     * Delete a saved drill set.
     */
    public function destroy(SavedDrillSet $savedDrillSet): JsonResponse|RedirectResponse
    {
        $this->authorize('delete', $savedDrillSet);

        $this->drillService->deleteSavedSet($savedDrillSet);

        if (request()->wantsJson()) {
            return response()->json(['status' => 'success', 'message' => 'Practice set deleted.']);
        }

        return $this->backWithSuccess('Practice set deleted.');
    }

    /**
     * Add / bookmark a question into a saved drill set.
     */
    public function addQuestion(AddQuestionToSavedSetRequest $request): JsonResponse
    {
        $userId = $this->requireUser()->id;
        $dto = BookmarkQuestionData::fromRequest($request);

        $result = $this->drillService->bookmarkQuestion($userId, $dto);

        return response()->json($result);
    }

    /**
     * Remove a question from a saved drill set.
     */
    public function removeQuestion(SavedDrillSet $savedDrillSet, Question $question): JsonResponse
    {
        $this->authorize('update', $savedDrillSet);

        $remainingCount = $this->drillService->removeQuestionFromSet($savedDrillSet, (int) $question->id);

        return response()->json([
            'status' => 'success',
            'message' => 'Question removed from practice set.',
            'remaining_count' => $remainingCount,
        ]);
    }

    /**
     * Get full questions for a saved drill set to launch a practice session.
     */
    public function getSetQuestions(SavedDrillSet $savedDrillSet): JsonResponse
    {
        $this->authorize('view', $savedDrillSet);

        $data = $this->drillService->getSetQuestions($savedDrillSet);

        return response()->json($data);
    }
}
