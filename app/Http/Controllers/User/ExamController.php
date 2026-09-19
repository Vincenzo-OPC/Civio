<?php

namespace App\Http\Controllers\User;

use App\Actions\Exam\SubmitExamAttemptAction;
use App\DTOs\Exam\SubmitExamAttemptData;
use App\Http\Controllers\Controller;
use App\Http\Requests\User\Exam\StoreExamAttemptRequest;
use App\Http\Resources\ExamScorecardResource;
use App\Models\Category;
use App\Models\Question;
use App\Models\TrackConfig;
use App\Services\DeterministicAnalysisService;
use App\Services\ExamAttemptFormatter;
use App\Services\ExamAttemptService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;
use Inertia\Inertia;
use Inertia\Response;

class ExamController extends Controller
{
    public function __construct(
        protected ExamAttemptFormatter $formatter,
        protected ExamAttemptService $attemptService,
        protected SubmitExamAttemptAction $submitAttemptAction
    ) {}

    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        // 1. Fetch verified active questions from cached pool (fast in-memory processing)
        $activeQuestionsPool = Cache::rememberForever('questions.active', function () {
            return Question::where('status', 'active')
                ->with(['subcategory.category'])
                ->get()
                ->map(function ($q) {
                    return [
                        'id' => $q->id,
                        'stem' => $q->stem,
                        'options' => $q->options ?? [],
                        'correct_option' => $q->correct_option,
                        'explanation' => $q->explanation ?? '',
                        'category' => $q->subcategory?->category?->name ?? 'General Information',
                        'subcategory' => $q->subcategory?->name ?? '',
                        'language' => (str_contains(strtolower($q->language ?? ''), 'tagalog') || str_contains(strtolower($q->language ?? ''), 'filipino')) ? 'Filipino' : 'English',
                        'isDemographic' => $q->subcategory?->category?->is_demographic ?? false,
                    ];
                })->toArray();
        });

        $questions = collect($activeQuestionsPool);
        $savedAttempt = null;
        $retakeSource = null;
        $attempt = null;

        if ($request->has('attempt_id')) {
            $pendingId = $request->session()->get('pending_guest_attempt_id');
            $attempt = $this->attemptService->getScorecardAttempt(
                attemptId: (int) $request->attempt_id,
                userId: auth()->id(),
                pendingGuestId: $pendingId ? (int) $pendingId : null
            );

            // In-memory filter of cached pool
            $questions = $questions->whereIn('id', $attempt->question_ids);
            $savedAttempt = (new ExamScorecardResource($attempt))->resolve();
        } elseif ($request->filled('retake_same') || $request->filled('retake_fresh')) {
            $attemptId = (int) ($request->input('retake_same') ?? $request->input('retake_fresh'));
            $mode = $request->has('retake_same') ? 'same' : 'fresh';

            $retakeSource = $this->attemptService->getRetakeSource($attemptId, (int) auth()->id(), $mode);
            $attempt = $this->attemptService->getScorecardAttempt($attemptId, (int) auth()->id(), null);
        }

        // Eagerly sort by attempt questions order if loaded via deep-link
        if (($savedAttempt || $retakeSource) && $attempt) {
            $questions = $questions->sortBy(function ($q) use ($attempt) {
                return array_search($q['id'], $attempt->question_ids);
            })->values();
        } else {
            $questions = $questions->values();
        }

        // 2. Fetch categories and tracks configurations
        $categories = Cache::rememberForever('categories.tree', function () {
            return Category::with(['subcategory' => function ($query) {
                $query->orderBy('sort_order');
            }])->orderBy('sort_order')->get()->toArray();
        });

        $tracks = TrackConfig::all();

        $seenQuestionIdsByTrack = $this->formatter->seenQuestionIdsByTrack(auth()->id());
        $wrongQuestionIdsByTrack = $this->formatter->wrongQuestionIdsByTrack(auth()->id());

        $aiAnalysis = [
            'status' => 'no_data',
            'data' => null,
        ];

        if (auth()->check()) {
            $targetAttemptId = $request->query('attempt_id') ? (int) $request->query('attempt_id') : null;
            if (! $targetAttemptId) {
                $targetAttemptId = $this->attemptService->getLatestUserAttemptId((int) auth()->id());
            }

            if ($targetAttemptId) {
                $deterministicService = new DeterministicAnalysisService;
                $analysisData = $deterministicService->generate((int) auth()->id(), $targetAttemptId, true);
                $aiAnalysis = [
                    'status' => 'ready',
                    'data' => $analysisData,
                ];
            }
        }

        return Inertia::render('user/exams/index', [
            'questions' => $questions,
            'categories' => $categories,
            'tracks' => $tracks,
            'savedAttempt' => $savedAttempt,
            'retakeSource' => $retakeSource,
            'seenQuestionIdsByTrack' => $seenQuestionIdsByTrack,
            'wrongQuestionIdsByTrack' => $wrongQuestionIdsByTrack,
            'exams' => [
                ['id' => 1, 'title' => 'Professional Level Reviewer', 'questions' => 170],
                ['id' => 2, 'title' => 'Sub-Professional Level Reviewer', 'questions' => 150],
            ],
            'aiAnalysis' => $aiAnalysis,
        ]);
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
    public function checkPdfExportLimit(Request $request)
    {
        $user = $request->user();

        if (! $user) {
            return response()->json([
                'success' => false,
                'message' => 'You must be logged in to download PDF examination booklets.',
            ], 401);
        }

        if (! $user->can_download_pdf && $user->role !== 'admin') {
            return response()->json([
                'success' => false,
                'message' => 'Your account is not authorized to download PDF examination booklets.',
            ], 403);
        }

        $token = Str::random(40);

        return response()->json([
            'success' => true,
            'message' => 'PDF export authorized.',
            'export_token' => $token,
        ]);
    }

    /**
     * Track a successful PDF download.
     */
    public function trackPdfDownload(Request $request)
    {
        $user = $request->user();

        if ($user) {
            $user->increment('pdf_downloads_count');
        }

        return $this->jsonSuccess();
    }
}
