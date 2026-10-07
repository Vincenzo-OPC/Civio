<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Enums\QuestionLanguage;
use App\Http\Resources\ExamQuestionResource;
use App\Models\ExamSession;
use App\Models\Question;
use App\Repositories\QuestionRepositoryInterface;
use App\Services\ExamAttemptFormatter;
use Illuminate\Contracts\Session\Session;

/**
 * Lite L1: picks a full mock on the server and sends only those items.
 *
 * Answer keys stay withheld (ExamQuestionResource without key). The chosen
 * question IDs are stored in `exam_sessions` so submit can be checked against
 * exactly what the server served.
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
     * @return array{session_id: string, track: string, target: int, short: bool, notice: string|null, questions: array<int, array<string, mixed>>}
     */
    public function start(?int $userId, string $track, array $clientBias, ?Session $session = null): array
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

        $serverSeen = $this->formatter->seenQuestionIdsByTrack($userId)[$level] ?? [];
        $serverWrong = $this->formatter->wrongQuestionIdsByTrack($userId)[$level] ?? [];

        $result = $this->selector->select($rows, $level, [
            'seenIds' => $serverSeen,
            'wrongIds' => array_values(array_unique([...$serverWrong, ...($clientBias['wrong_ids'] ?? [])])),
            'weakSubcategories' => $clientBias['weak_subcategories'] ?? [],
            'weakCategories' => $clientBias['weak_categories'] ?? [],
        ]);

        $ids = array_map(fn ($row) => (int) $row['id'], $result['items']);

        $examSession = ExamSession::create([
            'user_id' => $userId,
            'track' => $level,
            'question_ids' => $ids,
        ]);

        if ($userId === null && $session !== null) {
            $owned = (array) $session->get(ExamSession::GUEST_SESSION_KEY, []);
            $owned[] = $examSession->id;
            $session->put(ExamSession::GUEST_SESSION_KEY, array_slice($owned, -self::MAX_GUEST_SESSIONS));
        }

        $questions = ExamQuestionResource::collectionForExam(
            array_map(fn (int $id) => $byId[$id], $ids),
            false
        );

        return [
            'session_id' => $examSession->id,
            'track' => $level,
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
            && in_array($examSession->id, (array) $session->get(ExamSession::GUEST_SESSION_KEY, []), true);
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
            'category' => $question->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $question->subcategory?->name ?? '',
            'language' => QuestionLanguage::fromRaw($rawLang)->value,
            'isDemographic' => (bool) ($question->subcategory?->category?->is_demographic ?? false),
            'offlineEligible' => (bool) ($question->offline_eligible ?? false),
            'explanation' => (string) ($question->explanation ?? ''),
        ];
    }
}
