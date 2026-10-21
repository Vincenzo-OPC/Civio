<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Http\Resources\DrillQuestionResource;
use App\Models\Question;
use App\Models\ReviewItem;
use App\Services\Exam\StrictMockLock;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Inertia\Response;

class ReviewMistakeController extends Controller
{
    public function __construct(protected StrictMockLock $strictMockLock) {}

    public function index(Request $request): Response|JsonResponse
    {
        $pending = $this->pending($request);

        $payload = [
            'title' => 'Review Mistakes',
            'note' => 'This is practice history. A later correct answer, given without an explanation, clears the item.',
            'items' => $pending['items'],
            'page' => $pending['page'],
            'lastPage' => $pending['last_page'],
            'total' => $pending['total'],
        ];

        if ($request->wantsJson()) {
            return response()->json($payload);
        }

        return $this->render('user/drills/mistakes', $payload);
    }

    public function start(Request $request): JsonResponse
    {
        $user = $this->requireUser();
        $requested = array_values(array_unique(array_map('intval', (array) $request->input('question_ids', []))));
        $locked = $this->strictMockLock->lockedQuestionIds($user->id, $request->session());
        $owned = ReviewItem::query()
            ->where('user_id', $user->id)
            ->where('status', 'pending')
            ->whereIn('question_id', $requested)
            ->pluck('question_id')
            ->map(fn ($id): int => (int) $id)
            ->reject(fn (int $id): bool => in_array($id, $locked, true))
            ->values();

        if ($owned->isEmpty()) {
            abort(404);
        }

        $questions = Question::query()
            ->with('subcategory.category')
            ->where('status', 'active')
            ->whereIn('id', $owned->all())
            ->get();

        return response()->json([
            'questions' => DrillQuestionResource::collection($questions)->resolve($request),
        ]);
    }

    /**
     * @return array{items: list<array{question_id: int, stem: string, subject: string, wrong_count: int}>, page: int, last_page: int, total: int}
     */
    private function pending(Request $request): array
    {
        $user = $this->requireUser();
        $locked = $this->strictMockLock->lockedQuestionIds($user->id, $request->session());

        $paginator = ReviewItem::query()
            ->where('user_id', $user->id)
            ->where('status', 'pending')
            ->whereHas('question', fn ($query) => $query->where('status', 'active'))
            ->when($locked !== [], fn ($query) => $query->whereNotIn('question_id', $locked))
            ->with('question.subcategory.category')
            ->orderByDesc('last_result_at')
            ->orderByDesc('id')
            ->paginate(20)
            ->withQueryString();

        $items = $paginator->getCollection()
            ->map(function (ReviewItem $item): array {
                $question = $item->question;

                return [
                    'question_id' => (int) $item->question_id,
                    'stem' => (string) $question?->stem,
                    'subject' => (string) ($question?->subcategory?->category?->name ?? 'Practice'),
                    'wrong_count' => (int) $item->wrong_count,
                ];
            })
            ->values()
            ->all();

        return [
            'items' => $items,
            'page' => $paginator->currentPage(),
            'last_page' => $paginator->lastPage(),
            'total' => $paginator->total(),
        ];
    }
}
