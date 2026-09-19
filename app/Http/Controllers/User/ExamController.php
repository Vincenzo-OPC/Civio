<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Actions\Exam\SubmitExamAttemptAction;
use App\DTOs\Exam\ExamSessionQueryData;
use App\DTOs\Exam\SubmitExamAttemptData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\StoreExamAttemptRequest;
use App\Services\ExamService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Inertia\Response;

class ExamController extends Controller
{
    public function __construct(
        protected ExamService $examService,
        protected SubmitExamAttemptAction $submitAttemptAction
    ) {}

    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        $query = ExamSessionQueryData::fromRequest($request);
        $data = $this->examService->getExamSessionData($query, auth()->id());

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

        $result = $this->submitAttemptAction->execute(
            data: $dto,
            userId: $userId,
            clientIp: $request->ip(),
            hasPendingGuestAttempt: $hasPendingGuest
        );

        if (! auth()->check() && $result->attemptId) {
            $request->session()->put('pending_guest_attempt_id', $result->attemptId);
            $request->session()->forget('is_free_attempt_active');
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
}
