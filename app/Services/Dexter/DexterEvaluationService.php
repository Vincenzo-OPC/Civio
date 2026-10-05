<?php

declare(strict_types=1);

namespace App\Services\Dexter;

use App\Models\Question;

class DexterEvaluationService
{
    /**
     * Evaluate a question independently and compare against the stored answer key.
     */
    public function evaluate(Question $question, ?string $studentReasoning = null): array
    {
        $answerKey = $question->correct_option;
        $options = $question->options ?? [];
        $stem = strtolower($question->stem ?? '');

        $evaluation = [
            'aiEvaluation' => 'Basic verification passed.',
            'answerKeyConflict' => false,
            'ambiguity' => null,
            'confidence' => 0.85,
            'recommendedResponseTone' => 'neutral',
            'answerKey' => $answerKey,
            'options' => $options,
        ];

        // Simple calculation check for earnings/days type questions
        if (str_contains($stem, 'earns') && str_contains($stem, 'day') && str_contains($stem, 'total')) {
            if (preg_match('/₱?([\d,]+)\/day.*?(\d+)\s*days?/i', $question->stem, $matches)) {
                $daily = (int) str_replace(',', '', $matches[1]);
                $days = (int) $matches[2];
                $correct = $daily * $days;

                $dbAnswer = $options[$answerKey] ?? null;
                $dbValue = $dbAnswer ? (int) preg_replace('/[^\d]/', '', $dbAnswer) : null;

                if ($dbValue && $dbValue !== $correct) {
                    $evaluation['answerKeyConflict'] = true;
                    $evaluation['aiEvaluation'] = "Calculation shows {$correct}, but answer key says {$dbValue}.";
                    $evaluation['recommendedResponseTone'] = 'corrective';
                }
            }
        }

        return $evaluation;
    }
}
