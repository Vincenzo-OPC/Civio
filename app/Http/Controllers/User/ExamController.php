<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Actions\Exam\SubmitExamAttemptAction;
use App\DTOs\Exam\ExamSessionQueryData;
use App\DTOs\Exam\SubmitExamAttemptData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\StoreExamAttemptRequest;
use App\Models\ExamSession;
use App\Models\Question;
use App\Services\Dexter\DexterEvaluationService;
use App\Services\Exam\MockSessionService;
use App\Services\ExamService;
use App\Support\LiteMode;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Inertia\Response;

class ExamController extends Controller
{
    public function __construct(
        protected ExamService $examService,
        protected SubmitExamAttemptAction $submitAttemptAction,
        protected MockSessionService $mockSessionService,
    ) {}

    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        $query = ExamSessionQueryData::fromRequest($request);
        $data = $this->examService->getExamSessionData($query, auth()->id(), LiteMode::enabled($request));

        return $this->render('user/exams/index', $data);
    }

    /**
     * Store a newly created exam attempt.
     */
    public function storeAttempt(StoreExamAttemptRequest $request): JsonResponse
    {
        $dto = SubmitExamAttemptData::fromRequest($request);
        $userId = auth()->id();
        $hasPendingGuest = $request->session()->has('pending_guest_attempt_id');

        $examSession = null;

        if ($dto->examSessionId !== null) {
            $examSession = ExamSession::find($dto->examSessionId);

            if (! $examSession || ! $this->mockSessionService->owns($examSession, $userId, $request->session())) {
                return response()->json([
                    'success' => false,
                    'message' => 'This mock session was not found for you. Start a new mock.',
                ], 422);
            }
        }

        $result = $this->submitAttemptAction->execute(
            data: $dto,
            userId: $userId,
            clientIp: $request->ip(),
            hasPendingGuestAttempt: $hasPendingGuest,
            examSession: $examSession,
        );

        if (! auth()->check() && $result->attemptId) {
            $request->session()->put('pending_guest_attempt_id', $result->attemptId);
            // Local study: keep free-attempt session open so guests can start another mock.
            if (config('civio.guest_unlimited')) {
                $request->session()->put('is_free_attempt_active', true);
            } else {
                $request->session()->forget('is_free_attempt_active');
            }
        }

        return response()->json($result->toResponseArray(), $result->statusCode);
    }

    /**
     * Issue export authorization token for PDF examination booklet export.
     * Rate limiting (1 per day for normal users, unlimited for admins) is handled via route middleware.
     */
    public function checkPdfExportLimit(Request $request): JsonResponse
    {
        $user = $request->user();

        if (! $user) {
            return response()->json([
                'success' => false,
                'message' => 'You must be logged in to download PDF examination booklets.',
            ], 401);
        }

        if (! $user->can_download_pdf && ! $user->isAdmin()) {
            return response()->json([

                'success' => false,
                'message' => 'Your account is not authorized to download PDF examination booklets.',
            ], 403);
        }

        return response()->json([
            'success' => true,
            'message' => 'PDF export authorized.',
            'export_token' => Str::random(40),
        ]);
    }

    /**
     * Track a successful PDF download.
     */
    public function trackPdfDownload(Request $request): JsonResponse
    {
        $userId = $request->user()?->id;

        if ($userId) {
            $this->examService->trackPdfDownload((int) $userId);
        }

        return $this->jsonSuccess();
    }

    /**
     * Reveal the correct answer (Sirit / Reveal mode).
     */
    public function revealAnswer(Request $request): JsonResponse
    {
        $request->validate([
            'question_id' => 'required|integer|exists:questions,id',
        ]);

        $question = Question::find($request->question_id);

        if (! $question) {
            return response()->json([
                'success' => false,
                'message' => 'Question not found',
            ], 404);
        }

        // Use Dexter for independent evaluation + conflict detection
        $dexter = app(DexterEvaluationService::class);
        $evaluation = $dexter->evaluate($question);

        return response()->json([
            'success' => true,
            'question_id' => $question->id,
            'correct_option' => $question->correct_option,
            'explanation' => $question->explanation ?? null,
            'dexter_evaluation' => $evaluation,
            'has_conflict' => $evaluation['answerKeyConflict'] ?? false,
        ]);
    }

    /**
     * Provide expanded explanation (Expound).
     */
    public function expoundAnswer(Request $request): JsonResponse
    {
        $request->validate([
            'question_id' => 'required|integer|exists:questions,id',
        ]);

        $question = Question::find($request->question_id);

        if (! $question) {
            return response()->json(['success' => false, 'message' => 'Question not found'], 404);
        }

        // For now, return the existing explanation or a placeholder.
        // Full AI-powered expound will use DexterEvaluationService later.
        $explanation = $question->explanation
            ?? 'No detailed explanation available for this item yet.';

        return response()->json([
            'success' => true,
            'question_id' => $question->id,
            'explanation' => $explanation,
        ]);
    }
}
