<?php

declare(strict_types=1);

namespace App\Services\Learning;

use App\Enums\ExamMode;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewEvent;

/**
 * Honest per-subject learning signals.
 *
 * - Mastery counts only independent answers: every Strict Mock item, plus
 *   practice items answered without help. An item whose explanation was shown
 *   (assisted) never counts, right or wrong.
 * - Timed practice is SUGGESTED once a subject has >= 30 independent items at
 *   >= 80% accuracy. It is a suggestion, never a "proficient" label.
 * - Pace is average seconds per answered item, by subject.
 */
final class LearningInsightsService
{
    public const SUGGEST_MIN_ITEMS = 30;

    public const SUGGEST_MIN_ACCURACY = 80;

    public const RECENT_ATTEMPTS = 50;

    /**
     * @return array{
     *     mastery: array<int, array{name: string, correct: int, total: int, percentage: int}>,
     *     timedSuggestions: array<int, string>,
     *     pace: array<int, array{name: string, secondsPerItem: float, items: int}>
     * }
     */
    public function forUser(int $userId): array
    {
        $attempts = ExamAttempt::query()->where('user_id', $userId)->latest('id')->limit(self::RECENT_ATTEMPTS)->get();
        $allIds = $attempts->flatMap(fn (ExamAttempt $a) => array_map('intval', (array) $a->question_ids))->unique()->values()->all();

        $questions = Question::query()->with('subcategory.category')->whereIn('id', $allIds)->get()->keyBy('id');

        $assisted = [];
        ReviewEvent::query()->where('user_id', $userId)->where('assisted', true)
            ->whereIn('source_attempt_id', $attempts->pluck('id'))
            ->get(['source_attempt_id', 'question_id'])
            ->each(function ($e) use (&$assisted) {
                $assisted[(int) $e->source_attempt_id.':'.(int) $e->question_id] = true;
            });

        $mastery = [];
        $pace = [];

        foreach ($attempts as $attempt) {
            $strict = $attempt->mode === ExamMode::Strict;
            $answers = (array) $attempt->answers;
            $times = (array) ($attempt->cat_scores['metadata']['question_times'] ?? []);

            foreach (array_values(array_map('intval', (array) $attempt->question_ids)) as $position => $qid) {
                /** @var Question|null $q */
                $q = $questions->get($qid);

                if ($q === null || (bool) ($q->subcategory?->category?->is_demographic ?? false)) {
                    continue;
                }

                $cat = $q->subcategory?->category?->name ?? 'General Information';
                $chosen = $answers[(string) $qid] ?? $answers[$qid] ?? null;

                $secs = $times[$position] ?? $times[(string) $position] ?? null;
                if (is_numeric($secs) && (float) $secs > 0 && $chosen !== null) {
                    $pace[$cat]['secs'] = ($pace[$cat]['secs'] ?? 0) + (float) $secs;
                    $pace[$cat]['items'] = ($pace[$cat]['items'] ?? 0) + 1;
                }

                if (! $strict && isset($assisted[$attempt->id.':'.$qid])) {
                    continue;
                }

                $mastery[$cat]['total'] = ($mastery[$cat]['total'] ?? 0) + 1;
                $isCorrect = $chosen !== null && $chosen !== '' && (int) $chosen === (int) $q->correct_option;
                $mastery[$cat]['correct'] = ($mastery[$cat]['correct'] ?? 0) + ($isCorrect ? 1 : 0);
            }
        }

        $masteryOut = [];
        $suggest = [];
        ksort($mastery);
        foreach ($mastery as $name => $m) {
            $pct = (int) round($m['correct'] / $m['total'] * 100);
            $masteryOut[] = ['name' => (string) $name, 'correct' => $m['correct'], 'total' => $m['total'], 'percentage' => $pct];
            if ($m['total'] >= self::SUGGEST_MIN_ITEMS && $pct >= self::SUGGEST_MIN_ACCURACY) {
                $suggest[] = (string) $name;
            }
        }

        $paceOut = [];
        ksort($pace);
        foreach ($pace as $name => $p) {
            $paceOut[] = ['name' => (string) $name, 'secondsPerItem' => round($p['secs'] / $p['items'], 1), 'items' => $p['items']];
        }

        return ['mastery' => $masteryOut, 'timedSuggestions' => $suggest, 'pace' => $paceOut];
    }
}
