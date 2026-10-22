<?php

declare(strict_types=1);

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Models\ExamSession;
use App\Models\Question;
use App\Services\Exam\MockSessionService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\Rule;

final class ExamProgressController extends Controller
{
    /** Read or atomically save original-option answers. Never returns keys. */
    public function __invoke(Request $request, MockSessionService $sessions): JsonResponse
    {
        $data = $request->validate([
            'exam_session_id' => ['required', 'string', 'size:26'],
            'answers' => ['sometimes', 'array', 'max:300'],
            'answers.*' => ['nullable', 'integer', 'min:0', 'max:7'],
            'expected_version' => [Rule::requiredIf($request->has('answers')), 'integer', 'min:0'],
        ]);

        return DB::transaction(function () use ($request, $data, $sessions) {
            $withdrawn = [];
            $session = ExamSession::whereKey($data['exam_session_id'])->lockForUpdate()->firstOrFail();
            abort_unless($sessions->owns($session, $request->user()?->id, $request->session()), 404);

            if (array_key_exists('answers', $data)) {
                abort_unless($session->isOpen(), 409, 'This mock was already submitted.');
                abort_if($session->isExpired(), 409, 'The server deadline has passed. Submit to grade your saved answers.');
                abort_unless((int) $session->save_version === (int) $data['expected_version'], 409, 'Progress changed in another request. Reload to recover the saved answers.');

                $ids = array_map('intval', $session->question_ids);
                $patch = array_map(fn ($answer) => $answer === null ? null : (int) $answer, $data['answers']);
                abort_if(array_diff(array_map('intval', array_keys($patch)), $ids) !== [], 422, 'Answer was not served in this mock.');
                foreach (array_keys($patch) as $id) {
                    abort_unless((string) (int) $id === (string) $id, 422);
                }
                // An item withdrawn mid-mock must never block the rest of the
                // patch: its answer is dropped and reported, the others save.
                $items = Question::whereIn('id', array_keys($patch))->where('status', 'active')->get()->keyBy('id');
                $withdrawn = array_values(array_map('intval', array_filter(
                    array_keys($patch), fn ($id) => ! $items->has((int) $id)
                )));
                $patch = array_filter($patch, fn ($id) => $items->has((int) $id), ARRAY_FILTER_USE_KEY);
                foreach ($patch as $id => $answer) {
                    abort_if($answer !== null && ! array_key_exists($answer, (array) $items[$id]->options), 422);
                }

                if ($patch !== [] || $withdrawn === []) {
                    $session->forceFill([
                        'saved_answers' => array_replace((array) ($session->saved_answers ?? []), $patch),
                        'save_version' => (int) $session->save_version + 1,
                    ])->save();
                }
            }

            // Every served item withdrawn since the mock started, not only the
            // ones in this patch, so a resumed screen can label them too.
            $served = array_map('intval', $session->question_ids);
            $withdrawn = array_values(array_unique([...$withdrawn, ...array_diff(
                $served,
                Question::whereIn('id', $served)->where('status', 'active')->pluck('id')->map(fn ($id) => (int) $id)->all(),
            )]));
            sort($withdrawn);

            return response()->json([
                'success' => true,
                'deadline_at' => $session->deadline()?->toISOString(),
                'server_now' => now()->toISOString(),
                'answers' => (object) ($session->saved_answers ?? []),
                'save_version' => (int) $session->save_version,
                'submitted' => ! $session->isOpen(),
                'withdrawn_ids' => $withdrawn,
            ])->header('Cache-Control', 'private, no-store');
        });
    }
}
