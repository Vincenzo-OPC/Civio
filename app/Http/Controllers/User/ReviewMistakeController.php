<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Http\Resources\DrillQuestionResource;
use App\Models\Question;
use App\Models\ReviewCard;
use App\Models\ReviewEvent;
use App\Models\ReviewItem;
use App\Services\Exam\StrictMockLock;
use App\Support\ReviewCopy;
use App\Support\ReviewDueLabel;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Inertia\Response;

class ReviewMistakeController extends Controller
{
    public function __construct(protected StrictMockLock $strictMockLock) {}

    public function index(Request $request): Response|JsonResponse
    {
        $user = $this->requireUser();
        $locked = $this->strictMockLock->lockedQuestionIds($user->id, $request->session());
        $due = $this->cards($user->id, $locked, true);
        $upcoming = $this->cards($user->id, $locked, false);
        $pending = $this->pending($request, array_column($due['items'], 'question_id'));
        $completed = ReviewEvent::query()
            ->where('user_id', $user->id)
            ->where('outcome', 'independent_correct')
            ->count();
        $hasHistory = ReviewCard::query()->where('user_id', $user->id)->exists()
            || ReviewItem::query()->where('user_id', $user->id)->exists();
        $state = ($due['total'] === 0 && $pending['total'] === 0 && $upcoming['items'] === [])
            ? ($hasHistory ? 'complete' : 'empty')
            : 'open';

        $payload = [
            'title' => ReviewCopy::TITLE,
            'note' => ReviewCopy::NOTE,
            'emptyLabel' => ReviewCopy::EMPTY,
            'completeLabel' => ReviewCopy::COMPLETE,
            'dueLabel' => ReviewCopy::DUE,
            'upcomingLabel' => ReviewCopy::UPCOMING,
            'needsLabel' => ReviewCopy::NEEDS,
            'state' => $state,
            'due' => $due['items'],
            'dueTotal' => $due['total'],
            'upcoming' => $upcoming['items'],
            'nextDueLabel' => $upcoming['items'][0]['due_label'] ?? null,
            'completedCount' => $completed,
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
        $dueOwned = ReviewCard::query()
            ->where('user_id', $user->id)
            ->where('due_at', '<=', now())
            ->whereIn('question_id', $requested)
            ->pluck('question_id')
            ->map(fn ($id): int => (int) $id)
            ->reject(fn (int $id): bool => in_array($id, $locked, true));
        $allowed = $owned->merge($dueOwned)->unique()->values();

        if ($allowed->isEmpty()) {
            abort(404);
        }

        $questions = Question::query()
            ->with('subcategory.category')
            ->where('status', 'active')
            ->whereIn('id', $allowed->all())
            ->get();

        return response()->json([
            'questions' => DrillQuestionResource::collection($questions)->resolve($request),
        ]);
    }

    /**
     * @param  list<int>  $except
     * @return array{items: list<array<string, mixed>>, page: int, last_page: int, total: int}
     */
    private function pending(Request $request, array $except): array
    {
        $user = $this->requireUser();
        $locked = $this->strictMockLock->lockedQuestionIds($user->id, $request->session());

        $paginator = ReviewItem::query()
            ->where('user_id', $user->id)
            ->where('status', 'pending')
            ->whereHas('question', fn ($query) => $query->where('status', 'active'))
            ->when($locked !== [], fn ($query) => $query->whereNotIn('question_id', $locked))
            ->when($except !== [], fn ($query) => $query->whereNotIn('question_id', $except))
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
                    'status_label' => 'Needs Review',
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

    /**
     * @param  list<int>  $locked
     * @return array{items: list<array<string, mixed>>, total: int}
     */
    private function cards(int $userId, array $locked, bool $due): array
    {
        $query = ReviewCard::query()
            ->where('user_id', $userId)
            ->whereHas('question', fn ($inner) => $inner->where('status', 'active'))
            ->when($locked !== [], fn ($inner) => $inner->whereNotIn('question_id', $locked))
            ->when($due, fn ($inner) => $inner->where('due_at', '<=', now()))
            ->when(! $due, fn ($inner) => $inner->where('due_at', '>', now()))
            ->with('question.subcategory.category')
            ->orderBy('due_at')
            ->orderBy('id');

        $total = (clone $query)->count();
        $cards = $query->limit($due ? 20 : 5)->get();
        $items = ReviewItem::query()
            ->where('user_id', $userId)
            ->whereIn('question_id', $cards->pluck('question_id'))
            ->get()
            ->keyBy(fn (ReviewItem $item): int => (int) $item->question_id);

        return [
            'total' => $total,
            'items' => $cards->map(function (ReviewCard $card) use ($items, $due): array {
                $question = $card->question;
                $item = $items->get((int) $card->question_id);
                $resolved = $item?->status === 'resolved';

                return [
                    'question_id' => (int) $card->question_id,
                    'stem' => (string) $question?->stem,
                    'subject' => (string) ($question?->subcategory?->category?->name ?? 'Practice'),
                    'wrong_count' => (int) ($item?->wrong_count ?? 0),
                    'due_label' => ReviewDueLabel::format($card->due_at),
                    'status_label' => $due ? 'Due for Review' : ($resolved ? 'Resolved' : 'Needs Review'),
                ];
            })->values()->all(),
        ];
    }
}
