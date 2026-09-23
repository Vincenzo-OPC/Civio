<?php

declare(strict_types=1);

namespace App\Http\Controllers\Community;

use App\Http\Controllers\Controller;
use App\Http\Requests\Community\StoreRecalledQuestionRequest;
use App\Models\RecalledQuestion;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Response;

class RecalledQuestionController extends Controller
{
    public function store(StoreRecalledQuestionRequest $request): JsonResponse
    {
        $options = array_values(array_filter(
            (array) $request->input('options', []),
            fn ($option) => is_string($option) && trim($option) !== ''
        ));

        $row = RecalledQuestion::query()->create([
            'user_id' => $request->user()?->id,
            'stem' => trim((string) $request->validated('stem')),
            'options' => $options === [] ? null : $options,
            'correct_option' => $request->validated('correct_option'),
            'category' => $request->validated('category'),
            'subcategory' => $request->validated('subcategory'),
            'note' => $request->validated('note'),
            'status' => 'pending',
        ]);

        return response()->json([
            'success' => true,
            'id' => $row->id,
            'message' => 'Saved to the practice queue for moderation. This is a paraphrase, not an official CSC item.',
        ]);
    }

    public function index(): Response
    {
        $rows = RecalledQuestion::query()
            ->with('user:id,name,email')
            ->latest('id')
            ->paginate(20)
            ->withQueryString();

        return $this->render('admin/recalled-questions/index', [
            'recalls' => $rows,
            'pending_count' => RecalledQuestion::query()->where('status', 'pending')->count(),
        ]);
    }

    public function updateStatus(Request $request, RecalledQuestion $recalled): RedirectResponse
    {
        $data = $request->validate([
            'status' => ['required', 'in:pending,approved,rejected'],
            'moderator_note' => ['nullable', 'string', 'max:1000'],
        ]);

        $recalled->update($data);

        return $this->backWithSuccess('Practice-queue status updated. Approved paraphrases are not official CSC questions and are not published until an editor imports them.');
    }
}
