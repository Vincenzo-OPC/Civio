<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;

interface RevealSolver
{
    public function recognizes(string $stem): bool;

    /**
     * A checked explanation, or null when this solver does not own the item
     * or the recomputed value does not match the stored key.
     *
     * @return array{
     *     concept: string,
     *     simpler: string|null,
     *     steps: list<string>,
     *     shortcut: string|null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: array<string, mixed>|null
     * }|null
     */
    public function solve(Question $question): ?array;
}
