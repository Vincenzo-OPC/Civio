<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;
use App\Services\Exam\Reveal\RevealNumbers;

/**
 * Numerical patterns whose result is recomputed and kept only when it matches
 * the stored key. A recognized stem with a different key is refused.
 */
final class CheckedPatternSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return $this->percent($stem) !== null
            || $this->root($stem) !== null
            || $this->fraction($stem) !== null
            || $this->speed($stem) !== null
            || $this->discount($stem) !== null
            || $this->lcm($stem) !== null;
    }

    public function solve(Question $question): ?array
    {
        $stem = (string) $question->stem;
        $options = array_values($question->options ?? []);
        $key = (int) $question->correct_option;
        $choice = (string) ($options[$key] ?? '');
        $keyed = RevealNumbers::first($choice);
        if ($keyed === null) {
            return null;
        }

        $percent = $this->percent($stem);
        if ($percent !== null) {
            [$rate, $whole] = $percent;
            $value = $whole * $rate / 100;
            if (! RevealNumbers::same($value, $keyed)) {
                return null;
            }

            return $this->percentReveal($rate, $whole, $value, $options, $key);
        }

        $root = $this->root($stem);
        if ($root !== null) {
            $value = (int) round(sqrt($root));
            if ($value < 0 || ($value * $value) !== (int) $root || ! RevealNumbers::same((float) $value, $keyed)) {
                return null;
            }

            return [
                'concept' => 'A square root is the number that multiplies by itself to make the given number.',
                'simpler' => 'Hanapin ang numerong kapag minultiply sa sarili, lumalabas ang given.',
                'steps' => [RevealNumbers::format((float) $value).' × '.RevealNumbers::format((float) $value).' = '.RevealNumbers::format($root).'.'],
                'shortcut' => null,
                'commonMistakes' => $this->nearbySquares($options, $key, $root),
                'visual' => null,
            ];
        }

        $fraction = $this->fraction($stem);
        if ($fraction !== null) {
            [$numerator, $denominator, $whole] = $fraction;
            if ($denominator == 0.0) {
                return null;
            }
            $part = $whole / $denominator;
            $value = $part * $numerator;
            if (! RevealNumbers::same($value, $keyed)) {
                return null;
            }

            return [
                'concept' => 'A fraction of a total is that many equal parts of it.',
                'simpler' => 'Hatiin sa pantay na bahagi, tapos kunin ang ilan sa mga bahaging iyon.',
                'steps' => [
                    RevealNumbers::format($whole).' ÷ '.RevealNumbers::format($denominator).' = '.RevealNumbers::format($part).'.',
                    RevealNumbers::format($part).' × '.RevealNumbers::format($numerator).' = '.RevealNumbers::format($value).'.',
                ],
                'shortcut' => null,
                'commonMistakes' => $this->onePartMistake($options, $key, $part, $numerator, $denominator),
                'visual' => null,
            ];
        }

        $speed = $this->speed($stem);
        if ($speed !== null) {
            [$distance, $hours] = $speed;
            if ($hours == 0.0) {
                return null;
            }
            $value = $distance / $hours;
            if (! RevealNumbers::same($value, $keyed)) {
                return null;
            }

            return [
                'concept' => 'Speed is distance divided by time.',
                'simpler' => 'Speed ay layo kada oras. Hatiin ang layo sa oras.',
                'steps' => [RevealNumbers::format($distance).' ÷ '.RevealNumbers::format($hours).' = '.RevealNumbers::format($value).'.'],
                'shortcut' => null,
                'commonMistakes' => $this->speedMistakes($options, $key, $distance, $hours),
                'visual' => null,
            ];
        }

        $discount = $this->discount($stem);
        if ($discount !== null) {
            [$amount, $rate] = $discount;
            $off = $amount * $rate / 100;
            $due = $amount - $off;
            if (! RevealNumbers::same($due, $keyed)) {
                return null;
            }

            $shortcut = null;
            if (RevealNumbers::same($rate, 50)) {
                $shortcut = 'Half off. '.RevealNumbers::format($amount).' ÷ 2 = '.RevealNumbers::format($due).'.';
            } elseif (RevealNumbers::same($rate, 25)) {
                $shortcut = 'A quarter off. '.RevealNumbers::format($amount).' − '.RevealNumbers::format($amount).' ÷ 4 = '.RevealNumbers::format($due).'.';
            } elseif (RevealNumbers::same($rate, 10)) {
                $shortcut = 'Move the decimal one place, then subtract. '.RevealNumbers::format($off).' off '.RevealNumbers::format($amount).' leaves '.RevealNumbers::format($due).'.';
            }

            return [
                'concept' => 'A percent reduction is taken off the price. The amount due is what remains.',
                'simpler' => 'Bawasan ang presyo. Ang sagot ay ang natira, hindi ang nabawas.',
                'steps' => [
                    RevealNumbers::format($rate).' percent of '.RevealNumbers::format($amount).' is '.RevealNumbers::format($off).'.',
                    RevealNumbers::format($amount).' − '.RevealNumbers::format($off).' = '.RevealNumbers::format($due).'.',
                ],
                'shortcut' => $shortcut,
                'commonMistakes' => $this->discountMistakes($options, $key, $amount, $off),
                'visual' => null,
            ];
        }

        $lcm = $this->lcm($stem);
        if ($lcm !== null) {
            [$left, $right] = $lcm;
            $value = $this->leastCommonMultiple((int) $left, (int) $right);
            if (! RevealNumbers::same((float) $value, $keyed)) {
                return null;
            }

            $shortcut = null;
            if ($right != 0.0 && fmod($left, $right) == 0.0) {
                $shortcut = RevealNumbers::format($right).' already divides '.RevealNumbers::format($left).', so the least common multiple is '.RevealNumbers::format($left).'.';
            } elseif ($left != 0.0 && fmod($right, $left) == 0.0) {
                $shortcut = RevealNumbers::format($left).' already divides '.RevealNumbers::format($right).', so the least common multiple is '.RevealNumbers::format($right).'.';
            }

            $divisor = $this->greatestCommonDivisor((int) $left, (int) $right);

            return [
                'concept' => 'The least common multiple is the smallest whole number both values divide.',
                'simpler' => 'Hanapin ang pinakamaliit na numerong nahahati ng pareho.',
                'steps' => [
                    RevealNumbers::format($left).' × '.RevealNumbers::format($right).' ÷ '.RevealNumbers::format((float) $divisor).' = '.RevealNumbers::format((float) $value).'.',
                ],
                'shortcut' => $shortcut,
                'commonMistakes' => [],
                'visual' => null,
            ];
        }

        return null;
    }

    /**
     * @param  list<string>  $options
     * @return array{concept: string, simpler: string, steps: list<string>, shortcut: string|null, commonMistakes: list<array{choice: string, why: string}>, visual: null}
     */
    private function percentReveal(float $rate, float $whole, float $value, array $options, int $key): array
    {
        $shortcut = null;
        if (RevealNumbers::same($rate, 50)) {
            $shortcut = 'Half of '.RevealNumbers::format($whole).' is '.RevealNumbers::format($value).'.';
        } elseif (RevealNumbers::same($rate, 25)) {
            $shortcut = 'A quarter of '.RevealNumbers::format($whole).' is '.RevealNumbers::format($value).'.';
        } elseif (RevealNumbers::same($rate, 10)) {
            $shortcut = 'Move the decimal one place. 10 percent of '.RevealNumbers::format($whole).' is '.RevealNumbers::format($value).'.';
        }

        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }
            $choice = RevealNumbers::first((string) $option);
            if ($choice === null) {
                continue;
            }
            if (RevealNumbers::same($choice, $rate) && ! RevealNumbers::same($rate, $value)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'That is the percent rate, not the part of '.RevealNumbers::format($whole).'.',
                ];
            } elseif (RevealNumbers::same($choice, $whole * $rate)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'The percent was not divided by 100.',
                ];
            }
        }

        return [
            'concept' => 'Percent means out of 100.',
            'simpler' => 'Percent ay bahagi ng 100. '.RevealNumbers::format($rate).' percent ay '.RevealNumbers::format($rate).' sa bawat 100.',
            'steps' => [RevealNumbers::format($whole).' × '.RevealNumbers::format($rate).' ÷ 100 = '.RevealNumbers::format($value).'.'],
            'shortcut' => $shortcut,
            'commonMistakes' => $mistakes,
            'visual' => null,
        ];
    }

    /**
     * @return array{0: float, 1: float}|null
     */
    private function percent(string $stem): ?array
    {
        if (in_array(preg_match('/(\d+(?:\.\d+)?)\s*percent of\s+(\d+(?:,\d{3})*(?:\.\d+)?)/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) $match[1], (float) str_replace(',', '', $match[2])];
    }

    private function root(string $stem): ?float
    {
        if (in_array(preg_match('/square root of\s+(\d+(?:,\d{3})*)/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return (float) str_replace(',', '', $match[1]);
    }

    /**
     * @return array{0: float, 1: float, 2: float}|null
     */
    private function fraction(string $stem): ?array
    {
        if (in_array(preg_match('/(\d+)\s*\/\s*(\d+)\s+of\s+(\d+(?:,\d{3})*)/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) $match[1], (float) $match[2], (float) str_replace(',', '', $match[3])];
    }

    /**
     * @return array{0: float, 1: float}|null
     */
    private function speed(string $stem): ?array
    {
        if (in_array(preg_match('/speed/i', $stem), [0, false], true)) {
            return null;
        }
        if (in_array(preg_match('/(\d+(?:,\d{3})*)\s+kilometers in (\d+(?:\.\d+)?)\s+hours/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) str_replace(',', '', $match[1]), (float) $match[2]];
    }

    /**
     * @return array{0: float, 1: float}|null
     */
    private function discount(string $stem): ?array
    {
        if (in_array(preg_match('/(\d+(?:,\d{3})*)\s+pesos is reduced by (\d+(?:\.\d+)?)\s*percent/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) str_replace(',', '', $match[1]), (float) $match[2]];
    }

    /**
     * @return array{0: float, 1: float}|null
     */
    private function lcm(string $stem): ?array
    {
        if (in_array(preg_match('/least common multiple of (\d+) and (\d+)/i', $stem, $match), [0, false], true)) {
            return null;
        }

        return [(float) $match[1], (float) $match[2]];
    }

    private function greatestCommonDivisor(int $left, int $right): int
    {
        $left = abs($left);
        $right = abs($right);
        while ($right !== 0) {
            [$left, $right] = [$right, $left % $right];
        }

        return $left === 0 ? 1 : $left;
    }

    private function leastCommonMultiple(int $left, int $right): int
    {
        if ($left === 0 || $right === 0) {
            return 0;
        }

        return intdiv(abs($left * $right), $this->greatestCommonDivisor($left, $right));
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function nearbySquares(array $options, int $key, float $target): array
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
            $square = $choice * $choice;
            if (! RevealNumbers::same($square, $target)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => RevealNumbers::format($choice).' × '.RevealNumbers::format($choice).' is '.RevealNumbers::format($square).', not '.RevealNumbers::format($target).'.',
                ];
            }
        }

        return array_slice($mistakes, 0, 2);
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function onePartMistake(array $options, int $key, float $part, float $numerator, float $denominator): array
    {
        if (RevealNumbers::same($numerator, 1)) {
            return [];
        }

        $mistakes = [];
        foreach ($options as $index => $option) {
            if ($index === $key) {
                continue;
            }
            $choice = RevealNumbers::first((string) $option);
            if ($choice !== null && RevealNumbers::same($choice, $part)) {
                $mistakes[] = [
                    'choice' => (string) $option,
                    'why' => 'That is one of the '.RevealNumbers::format($denominator).' parts, not '.RevealNumbers::format($numerator).' of them.',
                ];
            }
        }

        return $mistakes;
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function speedMistakes(array $options, int $key, float $distance, float $hours): array
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
            if (RevealNumbers::same($choice, $distance)) {
                $mistakes[] = ['choice' => (string) $option, 'why' => 'That is the distance, not the speed.'];
            } elseif (RevealNumbers::same($choice, $hours)) {
                $mistakes[] = ['choice' => (string) $option, 'why' => 'That is the time, not the speed.'];
            }
        }

        return $mistakes;
    }

    /**
     * @param  list<string>  $options
     * @return list<array{choice: string, why: string}>
     */
    private function discountMistakes(array $options, int $key, float $amount, float $off): array
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
            if (RevealNumbers::same($choice, $amount)) {
                $mistakes[] = ['choice' => (string) $option, 'why' => 'That is the price before the reduction.'];
            } elseif (RevealNumbers::same($choice, $off)) {
                $mistakes[] = ['choice' => (string) $option, 'why' => 'That is the amount taken off, not the amount due.'];
            }
        }

        return $mistakes;
    }
}
