<?php

declare(strict_types=1);

namespace App\Services\Dexter;

use App\Enums\QuestionStatus;
use App\Http\Resources\ExamQuestionResource;
use App\Models\Question;
use App\Services\Exam\Reveal\RevealTutor;
use App\Services\Exam\StrictMockLock;
use App\Services\Learning\ExposureHistory;
use Illuminate\Contracts\Session\Session;

/**
 * Dexter Rescue v0 (ADR-0003): after a WRONG Study-mode answer, show the
 * checked explanation, a diagnosis only when the item's codes are validated,
 * and one fresh approved question of the same skill. The failed item reaches
 * FSRS through the normal Review Mistakes path on submit.
 *
 * Callers must check enabled() and strictActive() first: during an active
 * Strict Mock nothing answer-derived may leave the server.
 */
final class RescueService
{
    public function __construct(
        private readonly SkillGraph $graph,
        private readonly MisconceptionDiagnoser $diagnoser,
        private readonly RevealTutor $tutor,
        private readonly StrictMockLock $lock,
        private readonly ExposureHistory $exposure,
    ) {}

    public static function enabled(): bool
    {
        return config('dexter_rescue.enabled') === true;
    }

    public function strictActive(?int $userId, ?Session $session): bool
    {
        return $this->lock->lockedQuestionIds($userId, $session) !== [];
    }

    /** @return array<string, mixed> */
    public function forWrongAnswer(int $userId, Question $question, int $chosen): array
    {
        $question->loadMissing('subcategory.category');
        $skill = $this->graph->skillFor($question);
        $inPilot = $skill !== null && in_array($skill, (array) config('dexter_rescue.skills', []), true);

        if (! $inPilot || $chosen === (int) $question->correct_option) {
            return ['state' => 'idle', 'skill' => $inPilot ? $skill : null];
        }

        $validated = in_array((int) $question->id, array_map('intval', (array) config('dexter_rescue.validated_question_ids', [])), true);
        $diagnosis = $validated ? $this->diagnoser->diagnose($question, $chosen) : null;
        $taught = $this->tutor->forQuestion($question, 'incorrect');

        return [
            'state' => 'explained',
            'skill' => $skill,
            'skillLabel' => $this->graph->label($skill),
            // Null means: no validated diagnosis. The UI must not claim one.
            'diagnosis' => $diagnosis === null ? null : ['code' => $diagnosis['code'], 'label' => $diagnosis['label'], 'method' => $diagnosis['method']],
            'explanation' => [
                'source' => $diagnosis === null ? 'checked_explanation' : 'validated_diagnosis',
                'concept' => $taught['concept'],
                'steps' => $taught['steps'],
            ],
            'next' => $this->fresh($userId, $question, $skill),
            'review' => 'review_mistakes',
        ];
    }

    /** @return array<string, mixed> */
    private function fresh(int $userId, Question $failed, string $skill): array
    {
        $seen = $this->exposure->forUser($userId);
        $locked = array_flip($this->lock->lockedQuestionIds($userId, null));

        $pick = Question::query()->with('subcategory.category')
            ->where('status', QuestionStatus::Active)
            ->where('archetype', $skill)
            ->where('offline_eligible', false)
            ->whereKeyNot($failed->id)
            ->where('stem', '!=', $failed->stem)
            ->get()
            ->reject(fn (Question $q) => isset($seen[(int) $q->id]) || isset($locked[(int) $q->id]))
            ->shuffle()
            ->first();

        if (! $pick instanceof Question) {
            return ['kind' => 'none', 'message' => "No fresh question for this skill yet. We'll bring this one back in Review Mistakes."];
        }

        return ['kind' => 'fresh_same_skill', 'question' => (new ExamQuestionResource($pick))->resolve()];
    }
}
