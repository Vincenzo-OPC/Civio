<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;

/**
 * Alphabetical filing by the written name. A lesson is published only when
 * the stored key is the name, or the sequence, that sorts into that place.
 */
final class AlphabeticalFilingSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->place($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $place = $this->place((string) $question->stem);
        if ($place === null) {
            return null;
        }

        $options = array_values(array_map(strval(...), $question->options ?? []));
        $key = (int) $question->correct_option;
        $choice = $options[$key] ?? '';

        if ($place === 'sequence') {
            return $this->sequence($options, $key, $choice);
        }

        $names = $this->names($options);
        if ($names === null) {
            return null;
        }

        $ordered = $names;
        usort($ordered, strcasecmp(...));
        $expected = $place === 'first' ? $ordered[0] : $ordered[array_key_last($ordered)];
        if (strcasecmp($choice, $expected) !== 0) {
            return null;
        }

        $shown = implode(', ', $ordered);

        return [
            'concept' => 'Alphabetical filing compares names from the left. When the surname is the same, the given name decides the order.',
            'simpler' => 'Kung pareho ang apelyido, tingnan ang pangalan. A una kaysa B.',
            'steps' => ["In order: {$shown}."],
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => [
                'kind' => 'order',
                'groups' => $ordered,
                'mark' => $expected,
            ],
        ];
    }

    /**
     * @param  list<string>  $options
     */
    private function sequence(array $options, int $key, string $choice): ?array
    {
        $sorted = [];
        foreach ($options as $index => $option) {
            $parts = $this->names(array_map(trim(...), explode(';', $option)));
            if ($parts === null) {
                return null;
            }

            $ordered = $parts;
            usort($ordered, strcasecmp(...));
            $sorted[$index] = $parts === $ordered ? $ordered : null;
        }

        $matches = array_keys(array_filter($sorted, fn (?array $row): bool => $row !== null));
        if ($matches !== [$key]) {
            return null;
        }

        $shown = implode('; ', $sorted[$key] ?? []);

        return [
            'concept' => 'When the surname is the same, file by the given name from A onward.',
            'simpler' => 'Parehong apelyido, kaya ang pangalan ang magpapasya. A, saka B, saka C.',
            'steps' => ["The names in order are {$shown}."],
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => [
                'kind' => 'order',
                'groups' => $sorted[$key] ?? [],
                'mark' => ($sorted[$key] ?? [])[0] ?? $choice,
            ],
        ];
    }

    private function place(string $stem): ?string
    {
        if (in_array(preg_match('/alphabet/i', $stem), [0, false], true)) {
            return null;
        }

        if (preg_match('/comes first/i', $stem) === 1) {
            return 'first';
        }

        if (preg_match('/comes last/i', $stem) === 1) {
            return 'last';
        }

        if (preg_match('/file order|arranging surnames/i', $stem) === 1) {
            return 'sequence';
        }

        return null;
    }

    /**
     * @param  list<string>  $options
     * @return list<string>|null
     */
    private function names(array $options): ?array
    {
        if (count($options) < 2) {
            return null;
        }

        foreach ($options as $option) {
            if (preg_match('/^[\p{L}][\p{L}\s\'.-]*,\s*[\p{L}][\p{L}\s\'.-]*$/u', $option) !== 1) {
                return null;
            }
        }

        return $options;
    }
}
