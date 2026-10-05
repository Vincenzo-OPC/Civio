<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\Question;
use Illuminate\Support\Collection;

/**
 * Server-authoritative exam grading.
 *
 * Preferred answer payload (Phase 0+):
 *   answers: { "<questionId>": <originalOptionIndex>, ... }
 *
 * Legacy payloads (pre-Phase 0) keyed answers by list position into question_ids
 * with values that may be shuffled display indexes. Those are graded best-effort
 * against bank correct_option (may disagree with historical client-side scores).
 */
class ExamGradingService
{
    /**
     * @param  array<int, int|string>  $questionIds
     * @param  array<int|string, mixed>  $answers
     * @param  array<string, mixed>  $clientMeta  Client metadata to preserve (timing, track, etc.) — never trusted for score fields.
     * @return array{
     *     answers: array<string, int|null>,
     *     cat_scores: array{categoryScoreMap: array<string, mixed>, metadata: array<string, mixed>},
     *     correct_count: int,
     *     wrong_count: int,
     *     skipped_count: int,
     *     total_questions: int,
     *     score: int,
     *     wrong_question_ids: array<int, int>,
     *     answer_keys: array<int, array{id: int, correct_option: int, explanation: string}>
     * }
     */
    public function grade(array $questionIds, array $answers, array $clientMeta = []): array
    {
        $ids = array_values(array_map('intval', $questionIds));
        $questions = Question::query()
            ->with(['subcategory.category'])
            ->whereIn('id', $ids)
            ->get()
            ->keyBy('id');

        $normalizedAnswers = $this->normalizeAnswers($ids, $answers);
        $schema = $this->detectAnswerSchema($answers, $ids);

        $correctCount = 0;
        $wrongCount = 0;
        $skippedCount = 0;
        $wrongQuestionIds = [];
        $catMap = [];
        $answerKeys = [];

        foreach ($ids as $position => $qId) {
            /** @var Question|null $question */
            $question = $questions->get($qId);

            if ($question === null) {
                $skippedCount++;
                $normalizedAnswers[(string) $qId] = $normalizedAnswers[(string) $qId] ?? null;

                continue;
            }

            $isDemographic = (bool) ($question->subcategory?->category?->is_demographic ?? false);

            $answerKeys[] = [
                'id' => (int) $question->id,
                'correct_option' => (int) $question->correct_option,
                'explanation' => (string) ($question->explanation ?? ''),
            ];

            if ($isDemographic) {
                continue;
            }

            $catName = $question->subcategory?->category?->name ?? 'General Information';
            $subcatName = $question->subcategory?->name ?? 'General Concepts';

            if (! isset($catMap[$catName])) {
                $catMap[$catName] = ['correct' => 0, 'total' => 0, 'subcats' => []];
            }
            if (! isset($catMap[$catName]['subcats'][$subcatName])) {
                $catMap[$catName]['subcats'][$subcatName] = ['correct' => 0, 'total' => 0];
            }

            $catMap[$catName]['total']++;
            $catMap[$catName]['subcats'][$subcatName]['total']++;

            $chosen = $this->resolveChosenOption($normalizedAnswers, $answers, $qId, $position, $schema);

            if ($chosen === null) {
                $skippedCount++;
                $wrongQuestionIds[] = $qId;

                continue;
            }

            if ((int) $chosen === (int) $question->correct_option) {
                $correctCount++;
                $catMap[$catName]['correct']++;
                $catMap[$catName]['subcats'][$subcatName]['correct']++;
            } else {
                $wrongCount++;
                $wrongQuestionIds[] = $qId;
            }
        }

        $totalScored = $correctCount + $wrongCount + $skippedCount;
        $score = $totalScored > 0 ? (int) round(($correctCount / $totalScored) * 100) : 0;

        $metadata = array_merge($clientMeta, [
            'correct_count' => $correctCount,
            'wrong_count' => $wrongCount,
            'skipped_count' => $skippedCount,
            'total_questions' => $totalScored,
            'score' => $score,
            'wrong_question_ids' => array_values(array_unique($wrongQuestionIds)),
            'graded_by' => 'server',
            'answer_schema' => 'question_id',
        ]);

        // Drop any client-forged score fields we already overwrote; keep timing/track.
        unset($metadata['categoryScoreMap']);

        return [
            'answers' => $normalizedAnswers,
            'cat_scores' => [
                'categoryScoreMap' => $catMap,
                'metadata' => $metadata,
            ],
            'correct_count' => $correctCount,
            'wrong_count' => $wrongCount,
            'skipped_count' => $skippedCount,
            'total_questions' => $totalScored,
            'score' => $score,
            'wrong_question_ids' => array_values(array_unique($wrongQuestionIds)),
            'answer_keys' => $answerKeys,
        ];
    }

    /**
     * @param  array<int, int>  $questionIds
     * @param  array<int|string, mixed>  $answers
     * @return array<string, int|null>
     */
    public function normalizeAnswers(array $questionIds, array $answers): array
    {
        $schema = $this->detectAnswerSchema($answers, $questionIds);
        $out = [];

        foreach ($questionIds as $position => $qId) {
            $chosen = $this->resolveChosenOption([], $answers, $qId, $position, $schema);
            $out[(string) $qId] = $chosen;
        }

        return $out;
    }

    /**
     * Resolve a chosen original option index for grading / review.
     *
     * @param  array<string, int|null>  $normalized
     * @param  array<int|string, mixed>  $raw
     * @param  array<int, int>  $questionIds
     */
    public function resolveChosenOption(array $normalized, array $raw, int $qId, int $position, string $schema): ?int
    {
        if (array_key_exists((string) $qId, $normalized)) {
            $existing = $normalized[(string) $qId];

            return $existing === null ? null : (int) $existing;
        }

        // Legacy position-keyed payload must be read by list index first.
        // Question IDs like 1,2 would otherwise collide with position keys.
        if ($schema === 'position') {
            if (array_key_exists($position, $raw) && $raw[$position] !== null && $raw[$position] !== '') {
                return (int) $raw[$position];
            }
            if (array_key_exists((string) $position, $raw) && $raw[(string) $position] !== null && $raw[(string) $position] !== '') {
                return (int) $raw[(string) $position];
            }

            return null;
        }

        if (array_key_exists($qId, $raw) && $raw[$qId] !== null && $raw[$qId] !== '') {
            return (int) $raw[$qId];
        }

        if (array_key_exists((string) $qId, $raw) && $raw[(string) $qId] !== null && $raw[(string) $qId] !== '') {
            return (int) $raw[(string) $qId];
        }

        return null;
    }

    /**
     * @param  array<int|string, mixed>  $answers
     * @param  array<int, int>  $questionIds
     */
    public function detectAnswerSchema(array $answers, array $questionIds): string
    {
        if ($answers === []) {
            return 'question_id';
        }

        $n = count($questionIds);
        $keys = array_map('intval', array_keys($answers));
        $idSet = array_fill_keys(array_map('intval', $questionIds), true);

        $allIds = true;
        $allPositions = true;

        foreach ($keys as $key) {
            if (! isset($idSet[$key])) {
                $allIds = false;
            }
            if ($key < 0 || $key >= $n) {
                $allPositions = false;
            }
        }

        if ($allIds && ! $allPositions) {
            return 'question_id';
        }

        if ($allPositions && ! $allIds) {
            return 'position';
        }

        if ($allIds && $allPositions) {
            // Ambiguous overlap (e.g. ids 0..n-1). Prefer question_id when key set equals id set.
            sort($keys);
            $sortedIds = array_values(array_map('intval', $questionIds));
            sort($sortedIds);
            if ($keys === $sortedIds) {
                return 'question_id';
            }

            return 'position';
        }

        // Mixed or unknown — prefer question_id when any key matches an id outside the position range.
        foreach ($keys as $key) {
            if (isset($idSet[$key]) && ($key < 0 || $key >= $n)) {
                return 'question_id';
            }
        }

        return $allPositions ? 'position' : 'question_id';
    }

    /**
     * Lookup helper for analytics / formatters (ID-first, position fallback).
     *
     * @param  array<int|string, mixed>  $answers
     * @param  array<int, int>  $questionIds
     */
    public function chosenForQuestion(array $answers, array $questionIds, int $qId): ?int
    {
        $position = array_search($qId, array_values(array_map('intval', $questionIds)), true);
        $schema = $this->detectAnswerSchema($answers, array_values(array_map('intval', $questionIds)));

        if ($position === false) {
            $position = 0;
        }

        return $this->resolveChosenOption([], $answers, $qId, (int) $position, $schema);
    }
}
