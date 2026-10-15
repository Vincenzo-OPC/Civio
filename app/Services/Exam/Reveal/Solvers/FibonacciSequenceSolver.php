<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * A Fibonacci-type sequence: each shown term is the sum of the two before it.
 * Published only when the next term matches the stored key. Other sequences
 * are left alone.
 */
final class FibonacciSequenceSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->terms($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $terms = $this->terms((string) $question->stem);
        if ($terms === null) {
            return null;
        }

        $count = count($terms);
        $next = $terms[$count - 2] + $terms[$count - 1];
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, (float) $next)) {
            return null;
        }

        $steps = [];
        for ($index = 2; $index < $count; $index++) {
            $steps[] = "{$terms[$index - 2]} + {$terms[$index - 1]} = {$terms[$index]}.";
        }
        $steps[] = "{$terms[$count - 2]} + {$terms[$count - 1]} = {$next}.";

        return [
            'concept' => 'Each number is the sum of the two numbers just before it. This is a Fibonacci-type sequence, not every irregular list.',
            'simpler' => 'Dagdagan ang dalawang huling numero. Iyon ang susunod.',
            'steps' => $steps,
            'shortcut' => 'If the gap is not constant, add the previous two terms.',
            'commonMistakes' => [],
            'visual' => null,
        ];
    }

    /**
     * @return list<int>|null
     */
    private function terms(string $stem): ?array
    {
        if (in_array(preg_match('/(\d+(?:\s*,\s*\d+){3,})\s*,?\s*(?:_{2,}|\.{3}|\?)/', $stem, $match), [0, false], true)
            && in_array(preg_match('/next number:\s*(\d+(?:\s*,\s*\d+){3,})/i', $stem, $match), [0, false], true)) {
            return null;
        }

        $terms = array_map(intval(...), preg_split('/\s*,\s*/', $match[1]) ?: []);
        if (count($terms) < 4) {
            return null;
        }

        for ($index = 2; $index < count($terms); $index++) {
            if ($terms[$index] !== $terms[$index - 2] + $terms[$index - 1]) {
                return null;
            }
        }

        return $terms;
    }
}
