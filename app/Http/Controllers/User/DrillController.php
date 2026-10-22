<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\DTOs\Drill\StoreCustomQuestionData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Drill\StoreCustomDrillQuestionRequest;
use App\Http\Resources\DrillQuestionResource;
use App\Services\DrillService;
use App\Services\ExamService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Inertia\Response as InertiaResponse;

class DrillController extends Controller
{
    public function __construct(
        protected DrillService $drillService
    ) {}

    /**
     * Render the dynamic diagnostic drills interface.
     */
    public function index(Request $request): InertiaResponse
    {
        $userId = auth()->id();
        $data = $this->drillService->getDrillsIndexData($userId, max(1, $request->integer('page', 1)));

        // Today's Focus needs the learner's level (Analytical vs Clerical).
        $data['focusLevel'] = app(ExamService::class)->focusLevel($userId);

        return $this->render('user/drills/index', $data);
    }

    /**
     * Get weak subcategory questions for Smart Weakness Drill.
     */
    public function smartWeakness(Request $request): JsonResponse
    {
        $userId = $this->requireUser()->id;
        $data = $this->drillService->getSmartWeaknessQuestions($userId);

        return response()->json($data);
    }

    /**
     * Store a custom user-created question for practice drills.
     */
    public function storeCustomQuestion(StoreCustomDrillQuestionRequest $request): JsonResponse
    {
        $userId = $this->requireUser()->id;
        $dto = StoreCustomQuestionData::fromRequest($request);

        $question = $this->drillService->createCustomQuestion($userId, $dto);

        return response()->json([
            'message' => 'Question created successfully.',
            'question' => (new DrillQuestionResource($question))->resolve(),
        ], 201);
    }
}
