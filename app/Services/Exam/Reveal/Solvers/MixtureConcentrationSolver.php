<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * Two-solution mixture. Published only when the weighted concentration
 * matches the stored key. An equal-parts average is named only as a miss
 * when the volumes are not equal.
 */
final class MixtureConcentrationSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->parts($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $parts = $this->parts((string) $question->stem);
        if ($parts === null) {
            return null;
        }

        [$leftAmount, $leftPercent, $rightAmount, $rightPercent] = $parts;
        $solute = ($leftAmount * $leftPercent / 100) + ($rightAmount * $rightPercent / 100);
        $total = $leftAmount + $rightAmount;
        if ($total <= 0) {
            return null;
        }

        $concentration = $solute / $total * 100;
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, $concentration)) {
            return null;
        }

        $leftSolute = $leftAmount * $leftPercent / 100;
        $rightSolute = $rightAmount * $rightPercent / 100;
        $leftText = RevealNumbers::format($leftAmount);
        $rightText = RevealNumbers::format($rightAmount);
        $result = RevealNumbers::format($concentration);

        return [
            'concept' => 'Concentration is the amount of substance divided by the whole mixture. The stronger solution pulls the result toward itself when there is more of it.',
            'simpler' => 'Kung mas marami ang mas matapang na solusyon, mas malapit doon ang sagot. Hindi ito simpleng average kapag hindi pantay ang dami.',
            'steps' => [
                "{$leftText} × {$leftPercent}% = ".RevealNumbers::format($leftSolute).' liter of substance.',
                "{$rightText} × {$rightPercent}% = ".RevealNumbers::format($rightSolute).' liter of substance.',
                RevealNumbers::format($leftSolute).' + '.RevealNumbers::format($rightSolute).' = '.RevealNumbers::format($solute).' liter.',
                "{$leftText} + {$rightText} = ".RevealNumbers::format($total).' liters.',
                RevealNumbers::format($solute).' ÷ '.RevealNumbers::format($total).' × 100 = '.$result.'%.',
            ],
            'shortcut' => $this->shortcut($leftAmount, $leftPercent, $rightAmount, $rightPercent, $result),
            'commonMistakes' => $this->mistakes($options, (int) $question->correct_option, $leftPercent, $rightPercent),
            'visual' => [
                'kind' => 'mixture',
                'groups' => [
                    "{$leftText} L at {$leftPercent}%",
                    "{$rightText} L at {$rightPercent}%",
                    "{$result}%",
                ],
            ],
        ];
    }

    /**
     * @return array{0: float, 1: float, 2: float, 3: float}|null
     */
    private function parts(string $stem): ?array
    {
        $patterns = [
            '/(\d+(?:\.\d+)?)\s*liters?\s+of\s+(?:a\s+)?(\d+(?:\.\d+)?)%\s+solution\s*(?:\+|with|and)\s*(\d+(?:\.\d+)?)\s*liters?\s+of\s+(?:a\s+)?(\d+(?:\.\d+)?)%/i',
            '/mix\s+(\d+(?:\.\d+)?)\s*liters?\s+of\s+(?:a\s+)?(\d+(?:\.\d+)?)%\s+solution\s+with\s+(\d+(?:\.\d+)?)\s*liters?\s+of\s+(?:a\s+)?(\d+(?:\.\d+)?)%/i',
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $stem, $match) === 1) {
                return [(float) $match[1], (float) $match[2], (float) $match[3], (float) $match[4]];
            }
        }

        return null;
    }

    private function shortcut(float $leftAmount, float $leftPercent, float $rightAmount, float $rightPercent, string $result): ?string
    {
        if (RevealNumbers::same($leftAmount, $rightAmount)) {
            return null;
        }

        $weaker = min($leftPercent, $rightPercent);
        $gap = abs($rightPercent - $leftPercent);
        $strongerAmount = $leftPercent >= $rightPercent ? $leftAmount : $rightAmount;

        return RevealNumbers::format($weaker).'% + ('.RevealNumbers::format($strongerAmount).'/'.RevealNumbers::format($leftAmount + $rightAmount).' × '.RevealNumbers::format($gap).'%) = '.$result.'%.';
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function mistakes(array $options, int $key, float $leftPercent, float $rightPercent): array
    {
        $average = ($leftPercent + $rightPercent) / 2;
        $mistakes = [];

        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }

            $value = RevealNumbers::first((string) $option);
            if ($value !== null && RevealNumbers::same($value, $average) && ! RevealNumbers::same($leftPercent, $rightPercent)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'That averages the two percentages and ignores which solution there is more of.',
                ];
            }
        }

        return $mistakes;
    }
}
