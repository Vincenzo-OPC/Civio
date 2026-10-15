<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * Terminal-digit filing is read by groups, not by reversing the whole number.
 * The lesson is published only when the stored key is the last group.
 */
final class TerminalDigitFilingSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->groups($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $groups = $this->groups((string) $question->stem);
        if ($groups === null) {
            return null;
        }

        [$tertiary, $secondary, $primary] = $groups;
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, (float) $primary)) {
            return null;
        }

        return [
            'concept' => 'Terminal-digit filing uses the last group of digits as the primary filing group. Terminal means the end. The groups are not a reversed number.',
            'simpler' => 'Ang terminal ay ang dulo. Unahin ang huling pares, hindi ang una.',
            'steps' => [
                "{$primary} is the primary group. Read it first.",
                "{$secondary} is the secondary group. Read it second.",
                "{$tertiary} is the tertiary group. Read it third.",
                "Reading order: {$primary} → {$secondary} → {$tertiary}.",
            ],
            'shortcut' => 'Terminal = End. Read the rightmost group first.',
            'commonMistakes' => $this->mistakes($options, (int) $question->correct_option, $tertiary, $secondary),
            'visual' => [
                'kind' => 'filing',
                'groups' => [$tertiary, $secondary, $primary],
            ],
        ];
    }

    /**
     * @return array{0: string, 1: string, 2: string}|null
     */
    private function groups(string $stem): ?array
    {
        if (in_array(preg_match('/terminal[-\s]?digit/i', $stem), [0, false], true)) {
            return null;
        }

        if (in_array(preg_match('/(\d{2})-(\d{2})-(\d{2})/', $stem, $match), [0, false], true)) {
            return null;
        }

        return [$match[1], $match[2], $match[3]];
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function mistakes(array $options, int $key, string $tertiary, string $secondary): array
    {
        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }

            $value = RevealNumbers::first((string) $option);
            if ($value === null) {
                continue;
            }

            $text = (string) $option;
            if (RevealNumbers::same($value, (float) $tertiary)) {
                $mistakes[] = [
                    'choice' => $text,
                    'why' => "{$tertiary} is the first group written, but it is read last.",
                ];
            } elseif (RevealNumbers::same($value, (float) $secondary)) {
                $mistakes[] = [
                    'choice' => $text,
                    'why' => "{$secondary} is the middle group. It is read second, not first.",
                ];
            }
        }

        return $mistakes;
    }
}
