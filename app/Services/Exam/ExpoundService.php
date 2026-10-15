<?php

declare(strict_types=1);

namespace App\Services\Exam;

use App\Models\Question;

/**
 * A longer walkthrough for Expound. Order-of-operations stems are solved
 * with PEMDAS. Everything else is the stored explanation, split into steps.
 */
final class ExpoundService
{
    /**
     * @return array{rule: string|null, steps: list<string>, explanation: string}
     */
    public function forQuestion(Question $question): array
    {
        $options = array_values($question->options ?? []);
        $choice = (string) ($options[(int) $question->correct_option] ?? '');
        $arithmetic = $this->arithmeticSteps(trim((string) $question->stem), $choice);

        if ($arithmetic !== null) {
            return [
                'rule' => 'PEMDAS: parentheses, exponents, multiplication and division, then addition and subtraction. Multiplication and division go left to right. Addition and subtraction go left to right.',
                'steps' => $arithmetic,
                'explanation' => implode(' ', $arithmetic),
            ];
        }

        $steps = $this->workSteps((string) ($question->explanation ?? ''));
        if ($steps === []) {
            $steps = ['No further explanation is stored for this item yet.'];
        }

        return [
            'rule' => null,
            'steps' => $steps,
            'explanation' => implode(' ', $steps),
        ];
    }

    /**
     * @return list<string>|null
     */
    public function arithmeticSteps(string $stem, string $choice): ?array
    {
        return $this->orderOfOperations($stem, $choice);
    }

    public function isArithmeticExpression(string $stem): bool
    {
        return $this->expressionTokens($stem) !== null;
    }

    /**
     * @return list<string>
     */
    public function storedSteps(string $explanation): array
    {
        return $this->workSteps($explanation);
    }

    /**
     * Value of an order-of-operations stem, or null when it is not one.
     */
    public function arithmeticValue(string $stem): ?float
    {
        $tokens = $this->expressionTokens($stem);
        if ($tokens === null) {
            return null;
        }

        $reduced = $this->reduce($tokens);

        return count($reduced) === 1 ? (float) $reduced[0] : null;
    }

    /**
     * @return list<string>|null
     */
    public function expressionTokens(string $stem): ?array
    {
        if (in_array(preg_match('/^evaluate\b[:\s]*/i', $stem), [0, false], true)) {
            return null;
        }

        $body = preg_replace('/^evaluate\b[:\s]*/i', '', $stem) ?? $stem;
        $body = str_ireplace(
            ['multiplied by', 'divided by', 'times', 'then add', 'then subtract', 'plus', 'minus'],
            ['*', '/', '*', '+', '-', '+', '-'],
            $body,
        );
        $body = str_replace(['−', '–', '—', '×', '÷', ',', '.'], ['-', '-', '-', '*', '/', ' ', ' '], $body);
        $body = trim($body);

        if (in_array(preg_match('/^\d+(?:\s*[+\-*\/]\s*\d+)+$/', $body), [0, false], true)) {
            return null;
        }

        preg_match_all('/\d+|[+\-*\/]/', $body, $matches);
        $tokens = $matches[0];

        return count($tokens) >= 3 ? $tokens : null;
    }

    /**
     * @param  list<string>  $tokens
     * @return list<string>
     */
    private function reduce(array $tokens): array
    {
        $ignored = [];
        if ($this->hasOperator($tokens, ['*', '/'])) {
            $tokens = $this->collapse($tokens, ['*', '/'], $ignored);
        }
        if ($this->hasOperator($tokens, ['+', '-']) && count($tokens) > 1) {
            $tokens = $this->collapse($tokens, ['+', '-'], $ignored);
        }

        return $tokens;
    }

    /**
     * @return list<string>|null
     */
    private function orderOfOperations(string $stem, string $choice): ?array
    {
        $tokens = $this->expressionTokens($stem);
        if ($tokens === null) {
            return null;
        }

        $steps = [];
        $hasMultiplication = $this->hasOperator($tokens, ['*', '/']);
        $hasAddition = $this->hasOperator($tokens, ['+', '-']);
        $steps[] = 'Write it as '.$this->pretty($tokens).'.';

        if ($hasMultiplication) {
            $steps[] = 'There are no parentheses or exponents, so multiplication and division come next. They go left to right.';
            $tokens = $this->collapse($tokens, ['*', '/'], $steps);
        }

        if ($hasAddition && count($tokens) > 1) {
            $steps[] = $hasMultiplication
                ? 'That leaves '.$this->pretty($tokens).'. Addition and subtraction go left to right.'
                : 'There are no parentheses, exponents, multiplication, or division. Addition and subtraction go left to right.';
            $tokens = $this->collapse($tokens, ['+', '-'], $steps);
        }

        if (count($tokens) !== 1 || ! $this->matchesChoice((float) $tokens[0], $choice)) {
            return null;
        }

        return $steps;
    }

    /**
     * @param  list<string>  $tokens
     * @param  list<string>  $operators
     * @param  list<string>  $steps
     * @return list<string>
     */
    private function collapse(array $tokens, array $operators, array &$steps): array
    {
        while (true) {
            $index = null;
            foreach ($tokens as $position => $token) {
                if (in_array($token, $operators, true)) {
                    $index = $position;
                    break;
                }
            }

            if ($index === null || $index === 0 || ! isset($tokens[$index + 1])) {
                return $tokens;
            }

            $value = $this->apply($tokens[$index], (float) $tokens[$index - 1], (float) $tokens[$index + 1]);
            if ($value === null) {
                return $tokens;
            }

            $shown = $this->formatNumber($value);
            $steps[] = $this->formatNumber((float) $tokens[$index - 1]).' '.$this->symbol($tokens[$index]).' '.$this->formatNumber((float) $tokens[$index + 1]).' = '.$shown.'.';
            array_splice($tokens, $index - 1, 3, [$shown]);
        }
    }

    private function apply(string $operator, float $left, float $right): ?float
    {
        return match ($operator) {
            '*' => $left * $right,
            '/' => $right == 0.0 ? null : $left / $right,
            '+' => $left + $right,
            '-' => $left - $right,
            default => null,
        };
    }

    /**
     * @param  list<string>  $tokens
     * @param  list<string>  $operators
     */
    private function hasOperator(array $tokens, array $operators): bool
    {
        foreach ($tokens as $token) {
            if (in_array($token, $operators, true)) {
                return true;
            }
        }

        return false;
    }

    /**
     * @param  list<string>  $tokens
     */
    private function pretty(array $tokens): string
    {
        return implode(' ', array_map(fn (string $token): string => $this->symbol($token), $tokens));
    }

    private function symbol(string $token): string
    {
        return match ($token) {
            '*' => '×',
            '/' => '÷',
            '-' => '−',
            default => $token,
        };
    }

    private function formatNumber(float $value): string
    {
        if (abs($value - round($value)) < 0.00001) {
            return (string) (int) round($value);
        }

        return rtrim(rtrim(number_format($value, 2, '.', ''), '0'), '.');
    }

    private function matchesChoice(float $value, string $choice): bool
    {
        $choice = trim($choice);

        return $choice !== '' && is_numeric($choice) && abs((float) $choice - $value) < 0.001;
    }

    /**
     * @return list<string>
     */
    private function workSteps(string $explanation): array
    {
        $text = trim($explanation);
        if ($text === '') {
            return [];
        }

        $text = preg_replace('/The matching choice is “[^”]+”?\.?/u', '', $text) ?? $text;
        $text = preg_replace('/(?:“[^”]+”(?:,\s*)?)+(?:\s*do not follow the same steps)\.?/u', '', $text) ?? $text;
        $text = preg_replace_callback('/\b(?:[A-Z]\.)+/u', fn (array $match): string => str_replace('.', '∯', $match[0]), trim($text)) ?? trim($text);
        $parts = preg_split('/(?<=[.!?])\s+/u', $text) ?: [];
        $steps = [];

        foreach ($parts as $part) {
            $part = trim(str_replace('∯', '.', (string) $part));
            if ($part !== '') {
                $steps[] = $part;
            }
        }

        return $steps;
    }
}
