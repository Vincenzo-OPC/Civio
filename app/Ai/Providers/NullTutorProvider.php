<?php

declare(strict_types=1);

namespace App\Ai\Providers;

use App\Ai\Contracts\TutorProvider;

/**
 * Default provider: works with zero API keys.
 */
class NullTutorProvider implements TutorProvider
{
    public function name(): string
    {
        return 'null';
    }

    public function explainAnswer(array $question): array
    {
        $explanation = trim((string) ($question['explanation'] ?? ''));

        if ($explanation === '') {
            $explanation = 'No AI explanation is configured. Review the answer key and try a similar drill.';
        }

        return [
            'explanation' => $explanation,
            'provider' => $this->name(),
        ];
    }

    public function generateHint(array $question): array
    {
        return [
            'hint' => 'Eliminate options that contradict the stem, then compare the remaining choices carefully.',
            'provider' => $this->name(),
        ];
    }

    public function classifyMistake(array $question): array
    {
        $correct = (int) ($question['correct_option'] ?? -1);
        $chosen = (int) ($question['chosen_option'] ?? -1);

        $classification = $chosen === $correct
            ? 'correct'
            : ($chosen < 0 ? 'skipped' : 'incorrect_selection');

        return [
            'classification' => $classification,
            'notes' => 'Stub classifier (no AI keys). Wire a live TutorProvider when ready.',
            'provider' => $this->name(),
        ];
    }
}
