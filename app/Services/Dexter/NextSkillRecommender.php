<?php

declare(strict_types=1);

namespace App\Services\Dexter;

/**
 * Picks the next skill to practice and explains why, from independent-answer
 * estimates and the prerequisite graph. Deterministic and explainable.
 */
final class NextSkillRecommender
{
    public const WEAK_BELOW = 0.6;

    public const FOUNDATION_MIN_ANSWERS = 3;

    public function __construct(private readonly SkillGraph $graph) {}

    /**
     * @param  array<string, array{answers: int, correct: int, estimate: float, enough: bool}>  $estimates
     * @return array{skill: string, label: string, kind: string, reason: string, basedOn: string, model: string, graphVersion: string}|null
     */
    public function recommend(array $estimates): ?array
    {
        $weak = array_filter(
            $estimates,
            fn (array $e, string $s) => $this->graph->has($s) && $e['enough'] && $e['estimate'] < self::WEAK_BELOW,
            ARRAY_FILTER_USE_BOTH,
        );
        if ($weak === []) {
            return null;
        }

        uasort($weak, fn ($a, $b) => [$a['estimate'], -$a['answers']] <=> [$b['estimate'], -$b['answers']]);
        $target = (string) array_key_first($weak);
        $t = $weak[$target];
        $targetLabel = $this->graph->label($target);
        $evidence = "{$t['correct']} of {$t['answers']} independent answers correct in {$targetLabel}";

        foreach ($this->graph->foundationsOf($target) as $f) {
            $fe = $estimates[$f] ?? null;
            $fLabel = $this->graph->label($f);

            if ($fe === null || $fe['answers'] < self::FOUNDATION_MIN_ANSWERS) {
                return $this->result($f, 'check_foundation', "{$targetLabel} builds on {$fLabel}, and you have too few independent answers in {$fLabel} to tell whether it is solid. A few {$fLabel} questions will show whether the gap starts there.", $evidence);
            }

            if ($fe['estimate'] < self::WEAK_BELOW) {
                return $this->result($f, 'repair_foundation', "{$targetLabel} builds on {$fLabel}, which also looks shaky ({$fe['correct']} of {$fe['answers']} correct). Fixing {$fLabel} first should make {$targetLabel} easier.", $evidence);
            }
        }

        return $this->result($target, 'practice_skill', "{$targetLabel} is your weakest skill with enough independent answers, and its foundations look solid. Practice it with new questions, without hints.", $evidence);
    }

    /** @return array{skill: string, label: string, kind: string, reason: string, basedOn: string, model: string, graphVersion: string} */
    private function result(string $skill, string $kind, string $reason, string $basedOn): array
    {
        return [
            'skill' => $skill,
            'label' => $this->graph->label($skill),
            'kind' => $kind,
            'reason' => $reason,
            'basedOn' => $basedOn,
            'model' => SkillMasteryEstimator::MODEL,
            'graphVersion' => $this->graph->version(),
        ];
    }
}
