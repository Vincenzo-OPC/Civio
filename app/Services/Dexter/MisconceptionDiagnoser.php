<?php

declare(strict_types=1);

namespace App\Services\Dexter;

use App\Models\Question;

/**
 * Names the likely mistake behind a wrong choice from the item's reviewed
 * distractor codes. Deterministic, no AI. Call it only after the answer is
 * graded (never in an unsubmitted Strict Mock): the result implies the key.
 */
final class MisconceptionDiagnoser
{
    /**
     * @return array{code: string, label: string, method: string, remedialSkill: string|null, version: string}|null
     */
    public function diagnose(Question $question, ?int $chosenIndex): ?array
    {
        if ($chosenIndex === null || $chosenIndex === (int) $question->correct_option) {
            return null;
        }

        $code = $this->codes($question)[$chosenIndex] ?? null;
        $entry = $code !== null ? $this->taxonomy()[$code] ?? null : null;

        if ($entry === null) {
            return null;
        }

        return [
            'code' => $code,
            'label' => (string) $entry['label'],
            'method' => (string) $entry['method'],
            'remedialSkill' => $entry['remedial_skill'] ?? null,
            'version' => (string) config('dexter_misconceptions.version'),
        ];
    }

    /**
     * QA check for an item's distractor codes. Empty list means valid (or untagged).
     *
     * @return list<string>
     */
    public function problems(Question $question): array
    {
        $raw = $question->distractor_codes;
        if ($raw === null) {
            return [];
        }
        if (! is_array($raw)) {
            return ['distractor_codes must be an object of option index => code'];
        }

        $problems = [];
        $optionCount = count((array) $question->options);
        $taxonomy = $this->taxonomy();
        $correct = (int) $question->correct_option;

        foreach ($raw as $index => $code) {
            if (! is_numeric($index) || (int) $index < 0 || (int) $index >= $optionCount) {
                $problems[] = "option index {$index} is out of range";

                continue;
            }
            if ((int) $index === $correct) {
                $problems[] = "the correct option {$index} must not carry a distractor code";
            }
            if (! is_string($code) || ! isset($taxonomy[$code])) {
                $problems[] = 'unknown distractor code '.json_encode($code)." on option {$index}";
            }
        }

        return $problems;
    }

    /** @return array<int, string> */
    private function codes(Question $question): array
    {
        $out = [];
        foreach ((array) ($question->distractor_codes ?? []) as $index => $code) {
            if (is_numeric($index) && is_string($code)) {
                $out[(int) $index] = $code;
            }
        }

        return $out;
    }

    /** @return array<string, array<string, mixed>> */
    private function taxonomy(): array
    {
        return (array) config('dexter_misconceptions.codes', []);
    }
}
