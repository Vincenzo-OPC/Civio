<?php

declare(strict_types=1);

namespace App\Ai\Contracts;

/**
 * Server-side Dexter / tutor capabilities.
 * Implementations must never expose API keys to the client.
 */
interface TutorProvider
{
    /**
     * @param  array{stem: string, options: array<int, string>, correct_option: int, explanation?: string|null, chosen_option?: int|null}  $question
     * @return array{explanation: string, provider: string}
     */
    public function explainAnswer(array $question): array;

    /**
     * @param  array{stem: string, options: array<int, string>, correct_option?: int|null}  $question
     * @return array{hint: string, provider: string}
     */
    public function generateHint(array $question): array;

    /**
     * @param  array{stem: string, options: array<int, string>, correct_option: int, chosen_option: int, explanation?: string|null}  $question
     * @return array{classification: string, notes: string, provider: string}
     */
    public function classifyMistake(array $question): array;

    public function name(): string;
}
