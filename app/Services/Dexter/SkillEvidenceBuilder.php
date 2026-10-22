<?php

declare(strict_types=1);

namespace App\Services\Dexter;

/**
 * Splits raw answer events into evidence streams (ADR-0001, as decided by GT):
 *
 * - knowledge: the FIRST independent answer to each distinct question. Only
 *   this stream feeds SkillMasteryEstimator.
 * - retention: later answers to a question already answered (or already seen
 *   with help). These belong to retention/FSRS only and never raise or lower
 *   the knowledge estimate.
 * - unanswered: blanks are their own state. A blank is not a wrong answer and
 *   does not use up the question's first independent answer.
 * - assisted: answers given after Reveal/Expound. Never knowledge evidence;
 *   they do use up the question (the learner has seen the explanation).
 *
 * Ordering is by the event timestamp, then by a stable sequence (attempt id
 * and position). Events with no timestamp sort after timed ones, by sequence
 * only; no time is invented.
 */
final class SkillEvidenceBuilder
{
    /**
     * @param  list<array{skill: string, questionId: int, answered: bool, correct: bool, assisted: bool, at: int|null, seq: int}>  $events
     * @return array{knowledge: list<array{skill: string, correct: bool}>, retention: list<array{skill: string, questionId: int, correct: bool}>, unanswered: array<string, int>, assisted: array<string, int>}
     */
    public function build(array $events): array
    {
        usort($events, fn ($a, $b) => [$a['at'] === null ? 1 : 0, $a['at'] ?? 0, $a['seq']]
            <=> [$b['at'] === null ? 1 : 0, $b['at'] ?? 0, $b['seq']]);

        $used = [];
        $out = ['knowledge' => [], 'retention' => [], 'unanswered' => [], 'assisted' => []];

        foreach ($events as $e) {
            $skill = $e['skill'];
            $qid = $e['questionId'];

            if (! $e['answered']) {
                $out['unanswered'][$skill] = ($out['unanswered'][$skill] ?? 0) + 1;

                continue;
            }

            if ($e['assisted']) {
                $out['assisted'][$skill] = ($out['assisted'][$skill] ?? 0) + 1;
                $used[$qid] = true;

                continue;
            }

            if (isset($used[$qid])) {
                $out['retention'][] = ['skill' => $skill, 'questionId' => $qid, 'correct' => $e['correct']];

                continue;
            }

            $used[$qid] = true;
            $out['knowledge'][] = ['skill' => $skill, 'correct' => $e['correct']];
        }

        return $out;
    }
}
