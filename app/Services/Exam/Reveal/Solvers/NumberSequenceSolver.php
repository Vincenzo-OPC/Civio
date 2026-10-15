<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * A next-term sequence with one checkable rule: consecutive squares, a
 * constant gap, or a constant multiplier. Fibonacci-type lists are left to
 * that solver. Anything else keeps its stored explanation.
 */
final class NumberSequenceSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->pattern($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $pattern = $this->pattern((string) $question->stem);
        if ($pattern === null) {
            return null;
        }

        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, (float) $pattern['next'])) {
            return null;
        }

        $pattern['commonMistakes'] = $pattern['miss'] === $pattern['next']
            ? []
            : $this->mistakes($options, (int) $question->correct_option, $pattern['miss'], $pattern['missWhy']);
        unset($pattern['next'], $pattern['miss'], $pattern['missWhy']);

        return $pattern;
    }

    /**
     * @return array{
     *     concept: string,
     *     simpler: string,
     *     steps: list<string>,
     *     shortcut: null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null,
     *     next: int,
     *     miss: int,
     *     missWhy: string
     * }|null
     */
    private function pattern(string $stem): ?array
    {
        $terms = $this->terms($stem);
        if ($terms === null || $this->fibonacci($terms)) {
            return null;
        }

        $squares = $this->squares($terms);
        if ($squares !== null) {
            return $squares;
        }

        if (count($terms) >= 4) {
            return $this->arithmetic($terms) ?? $this->geometric($terms);
        }

        return null;
    }

    /**
     * @return list<int>|null
     */
    private function terms(string $stem): ?array
    {
        if (in_array(preg_match('/(\d+(?:\s*,\s*\d+){2,})\s*,?\s*(?:_{2,}|\.{3}|__)/', $stem, $match), [0, false], true)) {
            return null;
        }

        $terms = array_map(intval(...), preg_split('/\s*,\s*/', $match[1]) ?: []);

        return count($terms) >= 3 ? $terms : null;
    }

    /**
     * @param  list<int>  $terms
     */
    private function fibonacci(array $terms): bool
    {
        if (count($terms) < 4) {
            return false;
        }

        for ($index = 2; $index < count($terms); $index++) {
            if ($terms[$index] !== $terms[$index - 2] + $terms[$index - 1]) {
                return false;
            }
        }

        return true;
    }

    /**
     * @param  list<int>  $terms
     * @return array{
     *     concept: string,
     *     simpler: string,
     *     steps: list<string>,
     *     shortcut: null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null,
     *     next: int,
     *     miss: int,
     *     missWhy: string
     * }|null
     */
    private function squares(array $terms): ?array
    {
        $roots = [];
        foreach ($terms as $term) {
            $root = (int) round(sqrt($term));
            if ($root < 1 || ($root * $root) !== $term) {
                return null;
            }
            $roots[] = $root;
        }

        for ($index = 1; $index < count($roots); $index++) {
            if ($roots[$index] !== $roots[$index - 1] + 1) {
                return null;
            }
        }

        $nextRoot = $roots[array_key_last($roots)] + 1;
        $steps = [];
        foreach ($roots as $index => $root) {
            $steps[] = "{$root} × {$root} = {$terms[$index]}.";
        }
        $steps[] = "{$nextRoot} × {$nextRoot} = ".($nextRoot * $nextRoot).'.';

        return [
            'concept' => 'These are consecutive square numbers. Each one is a whole number multiplied by itself.',
            'simpler' => 'Sunod-sunod na parisukat. Hanapin ang susunod na numerong minultiply sa sarili.',
            'steps' => $steps,
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => null,
            'next' => $nextRoot * $nextRoot,
            'miss' => $terms[array_key_last($terms)] + ($terms[1] - $terms[0]),
            'missWhy' => 'That continues the first gap. The gaps between consecutive squares get wider.',
        ];
    }

    /**
     * @param  list<int>  $terms
     * @return array{
     *     concept: string,
     *     simpler: string,
     *     steps: list<string>,
     *     shortcut: null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null,
     *     next: int,
     *     miss: int,
     *     missWhy: string
     * }|null
     */
    private function arithmetic(array $terms): ?array
    {
        $gap = $terms[1] - $terms[0];
        if ($gap === 0) {
            return null;
        }

        for ($index = 2; $index < count($terms); $index++) {
            if ($gap !== $terms[$index] - $terms[$index - 1]) {
                return null;
            }
        }

        $last = $terms[array_key_last($terms)];
        $next = $last + $gap;
        $sign = $gap > 0 ? '+' : '−';
        $size = abs($gap);

        return [
            'concept' => 'The same number is added each time. This is an arithmetic sequence.',
            'simpler' => 'Pareho ang dinadagdag o binabawas sa bawat hakbang.',
            'steps' => [
                "{$terms[1]} − {$terms[0]} = {$gap}. The gap stays {$gap}.",
                "{$last} {$sign} {$size} = {$next}.",
            ],
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => null,
            'next' => $next,
            'miss' => $last * 2,
            'missWhy' => 'That doubles the last term. This list adds '.$gap.' each time.',
        ];
    }

    /**
     * @param  list<int>  $terms
     * @return array{
     *     concept: string,
     *     simpler: string,
     *     steps: list<string>,
     *     shortcut: null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null,
     *     next: int,
     *     miss: int,
     *     missWhy: string
     * }|null
     */
    private function geometric(array $terms): ?array
    {
        $growing = abs($terms[1]) > abs($terms[0]);
        if ($growing) {
            if ($terms[0] === 0 || ($terms[1] % $terms[0]) !== 0) {
                return null;
            }
            $factor = intdiv($terms[1], $terms[0]);
        } else {
            if ($terms[1] === 0 || ($terms[0] % $terms[1]) !== 0) {
                return null;
            }
            $factor = intdiv($terms[0], $terms[1]);
        }

        if ($factor <= 1) {
            return null;
        }

        for ($index = 2; $index < count($terms); $index++) {
            $expected = $growing ? $terms[$index - 1] * $factor : intdiv($terms[$index - 1], $factor);
            if (! $growing && ($terms[$index - 1] % $factor) !== 0) {
                return null;
            }
            if ($terms[$index] !== $expected) {
                return null;
            }
        }

        $last = $terms[array_key_last($terms)];
        $next = $growing ? $last * $factor : intdiv($last, $factor);
        if (! $growing && ($last % $factor) !== 0) {
            return null;
        }

        $step = $growing
            ? "{$terms[1]} ÷ {$terms[0]} = {$factor}. That multiplier stays {$factor}."
            : "{$terms[0]} ÷ {$terms[1]} = {$factor}. Each term is divided by {$factor}.";
        $move = $growing ? "{$last} × {$factor} = {$next}." : "{$last} ÷ {$factor} = {$next}.";

        return [
            'concept' => 'Each term is multiplied or divided by the same number. This is a geometric sequence.',
            'simpler' => 'Minumultiply o hinahati nang paulit-ulit sa parehong numero.',
            'steps' => [$step, $move],
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => null,
            'next' => $next,
            'miss' => $growing ? $last + $factor : $last * $factor,
            'missWhy' => $growing
                ? 'That adds the multiplier. This list multiplies by it.'
                : 'That multiplies again. This list keeps dividing.',
        ];
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function mistakes(array $options, int $key, int $miss, string $why): array
    {
        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }
            $value = RevealNumbers::first((string) $option);
            if ($value !== null && RevealNumbers::same($value, (float) $miss)) {
                $mistakes[] = ['choice' => (string) $option, 'why' => $why];
            }
        }

        return $mistakes;
    }
}
