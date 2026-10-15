<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * Mean, median, percent change, simple interest, and a greatest common
 * factor. Each lesson is published only when the recomputed value matches
 * the stored key.
 */
final class CheckedQuantitySolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->work($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $work = $this->work((string) $question->stem);
        if ($work === null) {
            return null;
        }

        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null || ! RevealNumbers::same($keyed, $work['value'])) {
            return null;
        }

        $work['commonMistakes'] = $this->named($options, (int) $question->correct_option, $work['misses']);
        unset($work['value'], $work['misses']);

        return $work;
    }

    /**
     * @return array{
     *     concept: string,
     *     simpler: string,
     *     steps: list<string>,
     *     shortcut: null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null,
     *     value: float,
     *     misses: list<array{value: float, why: string}>
     * }|null
     */
    private function work(string $stem): ?array
    {
        return $this->interest($stem)
            ?? $this->percentChange($stem)
            ?? $this->gcf($stem)
            ?? $this->average($stem)
            ?? $this->median($stem);
    }

    /**
     * @return array<string, mixed>|null
     */
    private function average(string $stem): ?array
    {
        if (preg_match('/\b(mean|average)\b/i', $stem) !== 1 || preg_match('/speed|km|kilometer/i', $stem) === 1) {
            return null;
        }

        $numbers = $this->numbers($stem);
        if (count($numbers) < 3) {
            return null;
        }

        $total = array_sum($numbers);
        $value = $total / count($numbers);

        return $this->lesson(
            'The mean is the total divided by how many numbers there are.',
            'I-add lahat, saka hatiin sa bilang ng numero.',
            [
                implode(' + ', array_map(fn (float $number): string => RevealNumbers::format($number), $numbers)).' = '.RevealNumbers::format($total).'.',
                RevealNumbers::format($total).' ÷ '.count($numbers).' = '.RevealNumbers::format($value).'.',
            ],
            $value,
            [['value' => $total, 'why' => 'That is the total. The mean still has to be divided by how many numbers there are.']],
        );
    }

    /**
     * @return array<string, mixed>|null
     */
    private function median(string $stem): ?array
    {
        if (preg_match('/\bmedian\b/i', $stem) !== 1) {
            return null;
        }

        $numbers = $this->numbers($stem);
        if (count($numbers) < 3) {
            return null;
        }

        $ordered = $numbers;
        sort($ordered);
        $count = count($ordered);
        $mid = intdiv($count, 2);
        $value = $count % 2 === 1 ? $ordered[$mid] : ($ordered[$mid - 1] + $ordered[$mid]) / 2;
        $shown = implode(', ', array_map(fn (float $number): string => RevealNumbers::format($number), $ordered));

        return $this->lesson(
            'The median is the middle value after the numbers are put in order.',
            'Ayusin muna mula sa pinakamaliit. Ang nasa gitna ang median.',
            ["In order: {$shown}.", 'The middle value is '.RevealNumbers::format($value).'.'],
            $value,
            [],
        );
    }

    /**
     * @return array<string, mixed>|null
     */
    private function percentChange(string $stem): ?array
    {
        if (preg_match('/percent/i', $stem) !== 1 || preg_match('/from\s+(\d+(?:,\d{3})*(?:\.\d+)?)\s+to\s+(\d+(?:,\d{3})*(?:\.\d+)?)/i', $stem, $match) !== 1) {
            return null;
        }

        $start = (float) str_replace(',', '', $match[1]);
        $end = (float) str_replace(',', '', $match[2]);
        if ($start == 0.0) {
            return null;
        }

        $change = $end - $start;
        $value = abs($change) / $start * 100;
        $down = preg_match('/decrease|falling|fell|drop/i', $stem) === 1;

        return $this->lesson(
            'Percent change is the change divided by the starting amount, then turned into a percent.',
            'Kunin ang diperensiya, hatiin sa unang numero, saka gawing percent.',
            [
                RevealNumbers::format($end).' − '.RevealNumbers::format($start).' = '.RevealNumbers::format($change).'.',
                RevealNumbers::format(abs($change)).' ÷ '.RevealNumbers::format($start).' × 100 = '.RevealNumbers::format($value).'%.',
            ],
            $value,
            $down ? [] : [[
                'value' => abs($change) / $end * 100,
                'why' => 'That divides by the new amount. Percent change uses the starting amount.',
            ]],
        );
    }

    /**
     * @return array<string, mixed>|null
     */
    private function interest(string $stem): ?array
    {
        if (preg_match('/simple interest on\s+(\d+(?:,\d{3})*)\s+pesos at\s+(\d+(?:\.\d+)?)%\s+per year for\s+(\d+(?:\.\d+)?)\s+years/i', $stem, $match) !== 1) {
            return null;
        }

        $principal = (float) str_replace(',', '', $match[1]);
        $rate = (float) $match[2];
        $years = (float) $match[3];
        $value = $principal * $rate * $years / 100;

        return $this->lesson(
            'Simple interest is the principal times the yearly rate times the number of years. It does not add interest onto interest.',
            'Principal × rate × taon. Hindi ito pinapataas nang pataas.',
            [RevealNumbers::format($principal).' × '.RevealNumbers::format($rate).'% × '.RevealNumbers::format($years).' = '.RevealNumbers::format($value).'.'],
            $value,
            [[
                'value' => $principal * $rate / 100,
                'why' => 'That is the interest for one year. The question asks for '.RevealNumbers::format($years).' years.',
            ]],
        );
    }

    /**
     * @return array<string, mixed>|null
     */
    private function gcf(string $stem): ?array
    {
        if (preg_match('/\b(?:GCF|greatest common factor)\s+of\s+(\d+)\s+and\s+(\d+)/i', $stem, $match) !== 1) {
            return null;
        }

        $left = (int) $match[1];
        $right = (int) $match[2];
        $value = $this->divisor($left, $right);

        return $this->lesson(
            'The greatest common factor is the largest whole number that divides both numbers with nothing left over.',
            'Hanapin ang pinakamalaking numerong pantay na humahati sa dalawa.',
            ["The greatest common factor of {$left} and {$right} is {$value}."],
            (float) $value,
            [],
        );
    }

    private function divisor(int $left, int $right): int
    {
        $left = abs($left);
        $right = abs($right);
        while ($right !== 0) {
            [$left, $right] = [$right, $left % $right];
        }

        return $left === 0 ? 1 : $left;
    }

    /**
     * @return list<float>
     */
    private function numbers(string $stem): array
    {
        preg_match_all('/\d+(?:,\d{3})*(?:\.\d+)?/', $stem, $matches);

        return array_map(fn (string $number): float => (float) str_replace(',', '', $number), $matches[0]);
    }

    /**
     * @param  list<string>  $steps
     * @param  list<array{value: float, why: string}>  $misses
     * @return array<string, mixed>
     */
    private function lesson(string $concept, string $simpler, array $steps, float $value, array $misses): array
    {
        return [
            'concept' => $concept,
            'simpler' => $simpler,
            'steps' => $steps,
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => null,
            'value' => $value,
            'misses' => $misses,
        ];
    }

    /**
     * @param  list<string>  $options
     * @param  list<array{value: float, why: string}>  $misses
     * @return list<array{choice: string, why: string}>
     */
    private function named(array $options, int $key, array $misses): array
    {
        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }
            $choice = RevealNumbers::first((string) $option);
            if ($choice === null) {
                continue;
            }
            foreach ($misses as $miss) {
                if (RevealNumbers::same($choice, $miss['value'])) {
                    $mistakes[] = ['choice' => (string) $option, 'why' => $miss['why']];
                    break;
                }
            }
        }

        return $mistakes;
    }
}
