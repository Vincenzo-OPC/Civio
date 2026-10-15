<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\ExpoundService;
use App\Services\Exam\Reveal\RevealNumbers;

final class OrderOfOperationsSolver implements RevealSolver
{
    public function __construct(private readonly ExpoundService $expound) {}

    public function recognizes(string $stem): bool
    {
        return $this->expound->isArithmeticExpression($stem);
    }

    public function solve(Question $question): ?array
    {
        $stem = trim((string) $question->stem);
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $steps = $this->expound->arithmeticSteps($stem, $choice);
        if ($steps === null) {
            return null;
        }

        return [
            'concept' => 'Multiply and divide before you add or subtract. Within each pair, go left to right.',
            'simpler' => 'Unahin ang multiply at divide, kaliwa pakanan. Saka lang ang plus at minus.',
            'steps' => $steps,
            'shortcut' => null,
            'commonMistakes' => $this->leftToRightMistake($stem, $options, (int) $question->correct_option),
            'visual' => null,
        ];
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function leftToRightMistake(string $stem, array $options, int $key): array
    {
        $tokens = $this->expound->expressionTokens($stem);
        $correct = $this->expound->arithmeticValue($stem);
        if ($tokens === null || $correct === null) {
            return [];
        }

        $value = (float) $tokens[0];
        for ($index = 1; $index < count($tokens); $index += 2) {
            $operator = $tokens[$index];
            $right = (float) ($tokens[$index + 1] ?? 0);
            $value = match ($operator) {
                '*' => $value * $right,
                '/' => $right == 0.0 ? $value : $value / $right,
                '+' => $value + $right,
                '-' => $value - $right,
                default => $value,
            };
        }

        if (RevealNumbers::same($value, $correct)) {
            return [];
        }

        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }
            $choice = RevealNumbers::first((string) $option);
            if ($choice !== null && RevealNumbers::same($choice, $value)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'That goes straight from the left, so the multiplication happens too late.',
                ];
            }
        }

        return $mistakes;
    }
}
