<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Enums\ExamMode;
use App\Enums\QuestionLanguage;
use App\Enums\SelectionPolicy;
use App\Http\Resources\ExamQuestionResource;
use App\Models\ExamSession;
use App\Models\Question;
use App\Repositories\QuestionRepositoryInterface;
use App\Services\ExamAttemptFormatter;
use Illuminate\Contracts\Session\Session;
use Illuminate\Support\Facades\Cache;

/**
 * Lite L1: picks a full mock on the server and sends only those items.
 *
 * Answer keys stay withheld (ExamQuestionResource without key). The chosen
 * question IDs are stored in `exam_sessions` so submit can be checked against
 * exactly what the server served.
 *
 * The selection policy comes from the mode (ADR-0002): Study is adaptive and
 * keeps Reveal per item; Strict is representative (uniform within the Civio
 * blueprint), timed, and its keys stay locked until submit (StrictMockLock).
 */
class MockSessionService
{
    public const MAX_GUEST_SESSIONS = 20;

    public function __construct(
        protected QuestionRepositoryInterface $questionRepository,
        protected ExamAttemptFormatter $formatter,
        protected MockPoolSelector $selector,
    ) {}

    /**
     * @param  array{wrong_ids?: array<int, int>, weak_subcategories?: array<int, string>, weak_categories?: array<int, string>}  $clientBias
     * @return array{session_id: string, track: string, mode: string, time_limit_secs: int, target: int, short: bool, notice: string|null, questions: array<int, array<string, mixed>>}
     */
    public function start(?int $userId, string $track, array $clientBias, ?Session $session = null, ExamMode $mode = ExamMode::Study): array
    {
        $identity = $userId !== null ? 'user:'.$userId : 'browser:'.($session?->getId() ?? '');
        $lock = Cache::lock('mock-start:'.hash('sha256', $identity), 30);
        abort_unless($lock->get(), 429, 'A mock is already being started.');
        try {
            abort_if($mode === ExamMode::Strict
                && app(StrictMockLock::class)->lockedQuestionIds($userId, $session) !== [],
                409, 'Submit your current Strict Mock before starting another.');

            return $this->startUnlocked($userId, $track, $clientBias, $session, $mode);
        } finally {
            $lock->release();
        }
    }

    private function startUnlocked(?int $userId, string $track, array $clientBias, ?Session $session, ExamMode $mode): array
    {
        $level = MockPoolSelector::levelFor($track);
        $pool = $this->questionRepository->getActivePool();

        /** @var array<int, Question> $byId */
        $byId = [];
        $rows = [];

        foreach ($pool as $question) {
            $byId[(int) $question->id] = $question;
            $rows[] = self::selectorRow($question);
        }

        $policy = SelectionPolicy::forMode($mode);
        // Representative (Strict) never reads history or client personalisation.
        $bias = $policy === SelectionPolicy::Representative ? [] : [
            'seenIds' => $this->formatter->seenQuestionIdsByTrack($userId)[$level] ?? [],
            'wrongIds' => array_values(array_unique([...($this->formatter->wrongQuestionIdsByTrack($userId)[$level] ?? []), ...($clientBias['wrong_ids'] ?? [])])),
            'weakSubcategories' => $clientBias['weak_subcategories'] ?? [],
            'weakCategories' => $clientBias['weak_categories'] ?? [],
        ];

        $result = $this->selector->select($rows, $level, $bias, $policy);

        $ids = array_map(fn ($row) => (int) $row['id'], $result['items']);

        $startedAt = now();
        $examSession = ExamSession::create([
            'user_id' => $userId,
            'track' => $level,
            'mode' => $mode,
            'selection_policy' => $policy,
            'selection_policy_version' => MockPoolSelector::POLICY_VERSION,
            'question_ids' => $ids,
            'owner_session_hash' => $userId === null && $session !== null ? hash('sha256', $session->getId()) : null,
            'started_at' => $startedAt,
            'deadline_at' => $mode === ExamMode::Strict
                ? $startedAt->copy()->addSeconds(MockPoolSelector::timeLimitFor($level))
                : null,
        ]);

        if ($userId === null && $session !== null) {
            $owned = (array) $session->get(ExamSession::GUEST_SESSION_KEY, []);
            // Preserve protected guest IDs through login/session-ID regeneration.
            $protected = ExamSession::whereIn('id', $owned)->where('mode', 'strict')
                ->whereNull('exam_attempt_id')
                ->where('created_at', '>=', now()->subSeconds(max(MockPoolSelector::TIME_LIMIT_SECS) + StrictMockLock::GRACE_SECS))
                ->pluck('id')->all();
            $owned[] = $examSession->id;
            $owned = array_values(array_unique([...array_slice($owned, -self::MAX_GUEST_SESSIONS), ...$protected]));
            $session->put(ExamSession::GUEST_SESSION_KEY, $owned);
        }

        $questions = ExamQuestionResource::collectionForExam(
            array_map(fn (int $id) => $byId[$id], $ids),
            false
        );

        return [
            'session_id' => $examSession->id,
            'started_at' => $examSession->started_at?->toISOString(),
            'deadline_at' => $examSession->deadline()?->toISOString(),
            'server_now' => now()->toISOString(),
            'track' => $level,
            'mode' => $mode->value,
            'selection_policy' => $policy->value,
            'selection_policy_version' => MockPoolSelector::POLICY_VERSION,
            'time_limit_secs' => MockPoolSelector::timeLimitFor($level),
            'target' => $result['target'],
            'short' => $result['short'],
            'notice' => MockPoolSelector::shortNotice($level, count($ids)),
            'questions' => $questions,
        ];
    }

    /** Whether the current user (or guest browser session) owns this exam session. */
    public function owns(ExamSession $examSession, ?int $userId, ?Session $session): bool
    {
        if ($examSession->user_id !== null) {
            return $userId !== null && $examSession->user_id === $userId;
        }

        return $session !== null
            && (
                in_array($examSession->id, (array) $session->get(ExamSession::GUEST_SESSION_KEY, []), true)
                || ($examSession->owner_session_hash !== null
                    && hash_equals($examSession->owner_session_hash, hash('sha256', $session->getId())))
            );
    }

    /**
     * Selector input. Includes the explanation for the difficulty heuristic
     * only; it never leaves the server.
     *
     * @return array<string, mixed>
     */
    public static function selectorRow(Question $question): array
    {
        $rawLang = $question->language instanceof QuestionLanguage
            ? $question->language->value
            : (string) ($question->language ?? '');

        return [
            'id' => (int) $question->id,
            'stem' => (string) $question->stem,
            'options' => array_values((array) ($question->options ?? [])),
            // Server-only: lets MockPoolState keep a key and the same word used as a trap apart.
            'correct' => (int) ($question->correct_option ?? -1),
            'category' => $question->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $question->subcategory?->name ?? '',
            'language' => QuestionLanguage::fromRaw($rawLang)->value,
            'isDemographic' => (bool) ($question->subcategory?->category?->is_demographic ?? false),
            'offlineEligible' => (bool) ($question->offline_eligible ?? false),
            'explanation' => (string) ($question->explanation ?? ''),
        ];
    }
}
