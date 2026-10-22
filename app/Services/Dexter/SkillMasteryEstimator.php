<?php

declare(strict_types=1);

namespace App\Services\Dexter;

/**
 * Bayesian Knowledge Tracing over INDEPENDENT answers only (callers must drop
 * assisted answers). Fixed, conservative parameters; guess = 0.25 for 4-option
 * MCQ. The estimate is a probability the method is known, never a "mastered" flag.
 */
final class SkillMasteryEstimator
{
    public const MODEL = 'bkt-v1';

    public const P_INIT = 0.2;

    public const P_LEARN = 0.1;

    public const P_SLIP = 0.1;

    public const P_GUESS = 0.25;

    /** Below this many independent answers the estimate is not reported as evidence. */
    public const MIN_ANSWERS = 5;

    /**
     * @param  list<array{skill: string, correct: bool}>  $events  oldest first
     * @return array<string, array{answers: int, correct: int, estimate: float, enough: bool}>
     */
    public function estimate(array $events): array
    {
        $out = [];
        foreach ($events as $e) {
            $s = $e['skill'];
            $p = $out[$s]['estimate'] ?? self::P_INIT;

            if ($e['correct']) {
                $num = $p * (1 - self::P_SLIP);
                $post = $num / ($num + (1 - $p) * self::P_GUESS);
            } else {
                $num = $p * self::P_SLIP;
                $post = $num / ($num + (1 - $p) * (1 - self::P_GUESS));
            }
            $p = $post + (1 - $post) * self::P_LEARN;

            $answers = ($out[$s]['answers'] ?? 0) + 1;
            $out[$s] = [
                'answers' => $answers,
                'correct' => ($out[$s]['correct'] ?? 0) + ($e['correct'] ? 1 : 0),
                'estimate' => round($p, 3),
                'enough' => $answers >= self::MIN_ANSWERS,
            ];
        }

        return $out;
    }
}
