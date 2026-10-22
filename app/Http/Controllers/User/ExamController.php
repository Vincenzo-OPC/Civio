<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Actions\Exam\SubmitExamAttemptAction;
use App\DTOs\Exam\ExamSessionQueryData;
use App\DTOs\Exam\SubmitExamAttemptData;
use App\Enums\ExamMode;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\ExportPdfRequest;
use App\Http\Requests\User\Exam\StoreExamAttemptRequest;
use App\Models\ExamSession;
use App\Models\Question;
use App\Services\Dexter\DexterEvaluationService;
use App\Services\Exam\ExpoundService;
use App\Services\Exam\MockSessionService;
use App\Services\Exam\PdfExamExportService;
use App\Services\Exam\Reveal\RevealTutor;
use App\Services\Exam\ReviewMistakeRecorder;
use App\Services\Exam\ServedPracticeQuestions;
use App\Services\Exam\StrictMockLock;
use App\Services\ExamService;
use App\Support\LiteMode;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Inertia\Response;

class ExamController extends Controller
{
    public function __construct(
        protected ExamService $examService,
        protected SubmitExamAttemptAction $submitAttemptAction,
        protected MockSessionService $mockSessionService,
        protected StrictMockLock $strictMockLock,
    ) {}

    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response|RedirectResponse
    {
        $query = ExamSessionQueryData::fromRequest($request);
        $data = $this->examService->getExamSessionData($query, auth()->id(), LiteMode::enabled($request));

        // Nothing fresh left on these skills: say so honestly, never an empty drill.
        if ($query->isDrill && $query->freshSameSkill && $data['questions'] === []) {
            return auth()->check()
                ? redirect()->route('reviews.mistakes.index', ['fresh' => 'none'])
                : redirect()->route('login');
        }

        if (($query->isDrill || $data['retakeSource'] !== null) && $data['savedAttempt'] === null) {
            $data['practiceBatchId'] = app(ServedPracticeQuestions::class)->remember(
                $request->session(), auth()->id(), array_column($data['questions'], 'id')
            );
        }

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

        if ($examSession === null
            && ! app(ServedPracticeQuestions::class)->allows($request->session(), $userId, $dto->questionIds)) {
            return response()->json(['success' => false, 'message' => 'Start a practice session before submitting its answers.'], 422);
        }

        $ids = $examSession !== null ? $examSession->question_ids : $dto->questionIds;
        $locked = $this->strictMockLock->lockedQuestionIds($userId, $request->session(), $examSession?->id);
        if (array_intersect($ids, $locked) !== []) {
            return response()->json(['success' => false, 'message' => StrictMockLock::MESSAGE], 423);
        }

        $result = $this->submitAttemptAction->execute(
            data: $dto,
            userId: $userId,
            clientIp: $request->ip(),
            hasPendingGuestAttempt: $hasPendingGuest,
            examSession: $examSession,
            reviewSessionHash: $this->helpToken(
                $request,
                $dto->questionIds,
                $examSession,
                'submit',
                $dto->practiceBatchId,
            ),
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

    /** Authorize and generate a separate booklet, never an active attempt's keys. */
    public function exportPdf(ExportPdfRequest $request, PdfExamExportService $export): JsonResponse
    {
        $authorization = $this->checkPdfExportLimit($request);
        if ($authorization->getStatusCode() !== 200) {
            return $authorization;
        }

        $data = $request->validated();

        if ($this->strictMockLock->lockedQuestionIds($request->user()->id, $request->session()) !== []) {
            return response()->json(['success' => false, 'message' => StrictMockLock::MESSAGE], 423);
        }

        return response()->json([
            'success' => true,
            // A client deduplication ID only; never accepted as authorization.
            'export_token' => Str::uuid()->toString(),
            'questions' => $export->questions($data['track']),
        ])->header('Cache-Control', 'private, no-store');
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
            'chosen_option' => 'sometimes|nullable|integer|min:0|max:7',
            'weak_subcategories' => 'sometimes|array|max:20',
            'weak_subcategories.*' => 'string|max:191',
            'practice_batch_id' => 'sometimes|nullable|string|size:32',
            'exam_session_id' => 'sometimes|nullable|string|size:26',
        ]);

        if ($this->strictMockLock->isLocked((int) $request->question_id, auth()->id(), $request->session())) {
            return response()->json(['success' => false, 'locked' => true, 'message' => StrictMockLock::MESSAGE], 423);
        }

        $question = Question::where('status', 'active')->find($request->question_id);

        if (! $question) {
            return response()->json([
                'success' => false,
                'message' => 'Question not found',
            ], 404);
        }

        // Use Dexter for independent evaluation + conflict detection
        $dexter = app(DexterEvaluationService::class);
        $evaluation = $dexter->evaluate($question);

        $chosen = $request->input('chosen_option');
        $result = is_numeric($chosen)
            ? ((int) $chosen === (int) $question->correct_option ? 'correct' : 'incorrect')
            : 'unanswered';
        $tutor = app(RevealTutor::class)->forQuestion(
            $question,
            $result,
            array_values($request->input('weak_subcategories', [])),
        );

        app(ReviewMistakeRecorder::class)->noteHelp(
            $request->user()?->id,
            (int) $question->id,
            $this->helpToken(
                $request,
                [(int) $question->id],
                $this->claimedStudySession($request, (int) $question->id),
                'reveal',
                $request->string('practice_batch_id')->toString() ?: null,
            ),
        );

        return response()->json([
            'success' => true,
            'question_id' => $question->id,
            'correct_option' => $question->correct_option,
            'explanation' => $question->explanation ?? null,
            'dexter_evaluation' => $evaluation,
            'has_conflict' => $evaluation['answerKeyConflict'] ?? false,
            'tutor' => $tutor,
        ]);
    }

    /**
     * Provide expanded explanation (Expound).
     */
    public function expoundAnswer(Request $request): JsonResponse
    {
        $request->validate([
            'question_id' => 'required|integer|exists:questions,id',
            'practice_batch_id' => 'sometimes|nullable|string|size:32',
            'exam_session_id' => 'sometimes|nullable|string|size:26',
        ]);

        if ($this->strictMockLock->isLocked((int) $request->question_id, auth()->id(), $request->session())) {
            return response()->json(['success' => false, 'locked' => true, 'message' => StrictMockLock::MESSAGE], 423);
        }

        $question = Question::where('status', 'active')->find($request->question_id);

        if (! $question) {
            return response()->json(['success' => false, 'message' => 'Question not found'], 404);
        }

        $expound = app(ExpoundService::class)->forQuestion($question);

        app(ReviewMistakeRecorder::class)->noteHelp(
            $request->user()?->id,
            (int) $question->id,
            $this->helpToken(
                $request,
                [(int) $question->id],
                $this->claimedStudySession($request, (int) $question->id),
                'reveal',
                $request->string('practice_batch_id')->toString() ?: null,
            ),
        );

        return response()->json([
            'success' => true,
            'question_id' => $question->id,
            'explanation' => $expound['explanation'],
            'rule' => $expound['rule'],
            'steps' => $expound['steps'],
        ]);
    }

    /**
     * Server-owned identity for one practice batch or one open Study Mock.
     * A submit prefers the batch the page claimed, then an exact id match,
     * so a later overlapping drill does not steal or drop the explanation.
     *
     * @param  array<int, int>  $questionIds
     */
    private function helpToken(
        Request $request,
        array $questionIds,
        ?ExamSession $examSession = null,
        string $purpose = 'submit',
        ?string $claimedBatch = null,
    ): ?string {
        if ($examSession !== null) {
            return $examSession->isStrict() ? null : hash('sha256', 'exam:'.$examSession->id);
        }

        $userId = $request->user()?->id;

        if ($userId === null) {
            return null;
        }

        $served = app(ServedPracticeQuestions::class);
        $ids = array_values(array_unique(array_map('intval', $questionIds)));

        if ($claimedBatch !== null && $served->ownsBatch($request->session(), $userId, $claimedBatch, $ids)) {
            return hash('sha256', 'batch:'.$claimedBatch);
        }

        if ($purpose === 'submit') {
            $exact = $served->exactBatchId($request->session(), $userId, $ids);

            if ($exact !== null) {
                return hash('sha256', 'batch:'.$exact);
            }
        }

        if (count($ids) === 1) {
            $batch = $served->questionBatchId($request->session(), $userId, $ids[0]);

            if ($batch !== null && $purpose === 'reveal') {
                return hash('sha256', 'batch:'.$batch);
            }

            if ($batch !== null && $purpose === 'submit') {
                return hash('sha256', 'batch:'.$batch);
            }

            $study = ExamSession::query()
                ->where('user_id', $userId)
                ->where('mode', ExamMode::Study->value)
                ->whereNull('exam_attempt_id')
                ->orderByDesc('created_at')
                ->get(['id', 'question_ids'])
                ->first(fn (ExamSession $session): bool => in_array($ids[0], array_map('intval', (array) $session->question_ids), true));

            return $study === null ? null : hash('sha256', 'exam:'.$study->id);
        }

        $batch = $served->coveringBatchId($request->session(), $userId, $ids);

        return $batch === null ? null : hash('sha256', 'batch:'.$batch);
    }

    private function claimedStudySession(Request $request, int $questionId): ?ExamSession
    {
        if ($request->filled('practice_batch_id')) {
            return null;
        }

        $id = $request->input('exam_session_id');

        if (! is_string($id) || strlen($id) !== 26) {
            return null;
        }

        $session = ExamSession::query()->find($id);

        if (! $session instanceof ExamSession || $session->isStrict()) {
            return null;
        }

        if (! $this->mockSessionService->owns($session, $request->user()?->id, $request->session())) {
            return null;
        }

        $ids = array_map('intval', (array) $session->question_ids);

        return in_array($questionId, $ids, true) ? $session : null;
    }
}
