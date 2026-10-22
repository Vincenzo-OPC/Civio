<?php

declare(strict_types=1);

namespace App\Services\Learning;

use App\Enums\ExamMode;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Models\ReviewEvent;
use App\Services\Dexter\NextSkillRecommender;
use App\Services\Dexter\SkillGraph;
use App\Services\Dexter\SkillMasteryEstimator;

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

    /** One idle item (tab left open) must not skew pace: cap per-item seconds. */
    public const MAX_ITEM_SECONDS = 300;

    public const SKILL_LIMIT = 5;

    public const RETENTION_MIN_SAMPLE = 10;

    /**
     * Weakest skills first, each with a stage and the next step. Stages are
     * descriptive (never "mastered" or "proficient"):
     *   start    (< 5 independent items)  -> learn the method, untimed
     *   building (< 70%)                  -> untimed practice on this skill
     *   steady   (>= 70%, >= 10 items)    -> mixed practice
     *   timed    (>= 80%, >= 20 items)    -> try it under time
     *
     * @param  array<string, array{total: int, correct: int, subcategoryId: int}>  $skills
     * @return array<int, array{subject: string, skill: string, subcategoryId: int, correct: int, total: int, percentage: int, stage: string, next: string}>
     */
    private function skillProgression(array $skills): array
    {
        $out = [];
        foreach ($skills as $key => $s) {
            [$subject, $skill] = explode('|', $key, 2);
            $pct = (int) round($s['correct'] / $s['total'] * 100);
            [$stage, $next] = match (true) {
                $s['total'] < 5 => ['start', 'Learn the method, then answer a few untimed items.'],
                $pct < 70 => ['building', 'Untimed practice on this skill; read each explanation after answering.'],
                $pct >= 80 && $s['total'] >= 20 => ['timed', 'Try this skill under time.'],
                $s['total'] >= 10 => ['steady', 'Mix it with other skills to check it holds.'],
                default => ['building', 'Untimed practice on this skill; read each explanation after answering.'],
            };
            $out[] = ['subject' => $subject, 'skill' => $skill, 'subcategoryId' => $s['subcategoryId'], 'correct' => $s['correct'], 'total' => $s['total'], 'percentage' => $pct, 'stage' => $stage, 'next' => $next];
        }

        $rank = ['building' => 0, 'start' => 1, 'steady' => 2, 'timed' => 3];
        usort($out, fn ($a, $b) => [$rank[$a['stage']], $a['percentage'], -$a['total']] <=> [$rank[$b['stage']], $b['percentage'], -$b['total']]);

        return array_slice($out, 0, self::SKILL_LIMIT);
    }

    /**
     * Retention: of items answered correctly on their own, how many were
     * still correct on a later independent attempt at least a day later.
     * Null until there are enough re-checks to say anything.
     *
     * @param  array<int, array<int, array{correct: bool, at: mixed}>>  $history
     * @return array{checked: int, kept: int, percentage: int}|null
     */
    private function retention(array $history): ?array
    {
        $checked = 0;
        $kept = 0;

        foreach ($history as $events) {
            for ($i = 0; $i < count($events) - 1; $i++) {
                if (! $events[$i]['correct']) {
                    continue;
                }
                for ($j = $i + 1; $j < count($events); $j++) {
                    if ($events[$i]['at']->diffInHours($events[$j]['at']) >= 24) {
                        $checked++;
                        $kept += $events[$j]['correct'] ? 1 : 0;
                        break;
                    }
                }
                break;
            }
        }

        return $checked >= self::RETENTION_MIN_SAMPLE
            ? ['checked' => $checked, 'kept' => $kept, 'percentage' => (int) round($kept / $checked * 100)]
            : null;
    }

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
        $skills = [];
        $history = [];
        $graph = new SkillGraph;
        $skillEvents = [];

        foreach ($attempts->sortBy('id') as $attempt) {
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
                    $pace[$cat]['secs'] = ($pace[$cat]['secs'] ?? 0) + min((float) $secs, self::MAX_ITEM_SECONDS);
                    $pace[$cat]['items'] = ($pace[$cat]['items'] ?? 0) + 1;
                }

                if (! $strict && isset($assisted[$attempt->id.':'.$qid])) {
                    continue;
                }

                $mastery[$cat]['total'] = ($mastery[$cat]['total'] ?? 0) + 1;
                $isCorrect = $chosen !== null && $chosen !== '' && (int) $chosen === (int) $q->correct_option;
                $mastery[$cat]['correct'] = ($mastery[$cat]['correct'] ?? 0) + ($isCorrect ? 1 : 0);

                $skill = $q->subcategory?->name ?? 'General';
                $skills[$cat.'|'.$skill]['total'] = ($skills[$cat.'|'.$skill]['total'] ?? 0) + 1;
                $skills[$cat.'|'.$skill]['correct'] = ($skills[$cat.'|'.$skill]['correct'] ?? 0) + ($isCorrect ? 1 : 0);
                $skills[$cat.'|'.$skill]['subcategoryId'] = (int) $q->subcategory_id;
                $history[$qid][] = ['correct' => $isCorrect, 'at' => $attempt->created_at];

                $graphSkill = $graph->skillFor($q);
                if ($graphSkill !== null) {
                    $skillEvents[] = ['skill' => $graphSkill, 'correct' => $isCorrect];
                }
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

        return [
            'mastery' => $masteryOut,
            'timedSuggestions' => $suggest,
            'pace' => $paceOut,
            // ADR-0002: Strict scores from before the representative policy are
            // not comparable with later ones, so they are counted apart.
            'strictMockPolicies' => [
                'representative' => $attempts->filter(fn (ExamAttempt $a) => $a->mode === ExamMode::Strict && $a->selection_policy_version !== null)->count(),
                'legacy' => $attempts->filter(fn (ExamAttempt $a) => $a->mode === ExamMode::Strict && $a->selection_policy_version === null)->count(),
            ],
            'skills' => $this->skillProgression($skills),
            'retention' => $this->retention($history),
            // Independent answers only; null until items carry a graph archetype.
            'nextFocus' => (new NextSkillRecommender($graph))->recommend((new SkillMasteryEstimator)->estimate($skillEvents)),
        ];
    }
}
