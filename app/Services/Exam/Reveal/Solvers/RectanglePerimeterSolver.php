<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

final class RectanglePerimeterSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->sides($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $sides = $this->sides((string) $question->stem);
        if ($sides === null) {
            return null;
        }

        [$length, $width] = $sides;
        $perimeter = 2 * ($length + $width);
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, $perimeter)) {
            return null;
        }

        $lengthText = RevealNumbers::format($length);
        $widthText = RevealNumbers::format($width);
        $perimeterText = RevealNumbers::format($perimeter);
        $unit = 'm';

        return [
            'concept' => 'Perimeter is the distance around the outside. It is not the space inside.',
            'simpler' => 'Perimeter ay ang layo sa paligid. Lakarin ang apat na gilid. Hindi ito ang loob, na area.',
            'steps' => [
                "{$lengthText} + {$widthText} + {$lengthText} + {$widthText} = {$perimeterText} {$unit}.",
            ],
            'shortcut' => "2 × ({$lengthText} + {$widthText}) = {$perimeterText} {$unit}.",
            'commonMistakes' => $this->mistakes($options, (int) $question->correct_option, $length, $width),
            'visual' => [
                'kind' => 'rectangle',
                'length' => $length,
                'width' => $width,
                'unit' => $unit,
            ],
        ];
    }

    /**
     * @return array{0: float, 1: float}|null
     */
    private function sides(string $stem): ?array
    {
        if (in_array(preg_match('/perimeter/i', $stem), [0, false], true)) {
            return null;
        }

        if (in_array(preg_match('/rectangle\D+(\d+(?:\.\d+)?)\s*(?:meters?|m)\s+by\s+(\d+(?:\.\d+)?)\s*(?:meters?|m)/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) $match[1], (float) $match[2]];
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function mistakes(array $options, int $key, float $length, float $width): array
    {
        $area = $length * $width;
        $twoSides = $length + $width;
        $mistakes = [];

        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }

            $value = RevealNumbers::first((string) $option);
            if ($value === null) {
                continue;
            }

            if (RevealNumbers::same($value, $area)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => RevealNumbers::format($length).' × '.RevealNumbers::format($width).' is the area, the space inside. The question asks for the distance around.',
                ];
            } elseif (RevealNumbers::same($value, $twoSides)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'That adds only the length and the width. A rectangle has four sides.',
                ];
            }
        }

        return $mistakes;
    }
}
