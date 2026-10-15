<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal;

use App\Enums\QuestionStatus;
use App\Models\Question;
use App\Models\Subcategory;
use App\Services\Exam\ExpoundService;
use App\Services\Exam\MockPoolSelector;
use App\Services\Exam\Reveal\Solvers\CheckedPatternSolver;
use App\Services\Exam\Reveal\Solvers\OrderOfOperationsSolver;
use App\Services\Exam\Reveal\Solvers\RectanglePerimeterSolver;
use App\Services\Exam\Reveal\Solvers\RevealSolver;

/**
 * Structured reveal. A pattern explanation is published only when the
 * recomputed value matches the stored key. Otherwise the stored explanation
 * is split into a concept and steps, with no invented shortcut or mistake.
 */
final class RevealTutor
{
    /** @var list<RevealSolver> */
    private array $solvers;

    public function __construct(private readonly ExpoundService $expound)
    {
        $this->solvers = [
            new RectanglePerimeterSolver,
            new OrderOfOperationsSolver($expound),
            new CheckedPatternSolver,
        ];
    }

    /**
     * @param  list<string>  $weakSubcategories
     * @return array{
     *     concept: string|null,
     *     simpler: string|null,
     *     steps: list<string>,
     *     shortcut: string|null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: array{kind: string, length: float, width: float, unit: string}|null,
     *     followUp: array{questionId: int, stem: string, skill: string, direction: string}|null
     * }
     */
    public function forQuestion(Question $question, string $result = 'unanswered', array $weakSubcategories = []): array
    {
        $taught = $this->teach($question);
        $taught['followUp'] = $this->followUp($question, $result, $weakSubcategories);

        return $taught;
    }

    /**
     * @return array{checked: int, stored: int, empty: int, thin: int, conflicts: int}
     */
    public function audit(): array
    {
        $checked = 0;
        $stored = 0;
        $empty = 0;
        $thin = 0;
        $conflicts = 0;

        Question::query()->where('status', QuestionStatus::Active)->orderBy('id')->each(function (Question $question) use (&$checked, &$stored, &$empty, &$thin, &$conflicts): void {
            if ($this->conflict($question)) {
                $conflicts++;
            }

            $sentences = $this->expound->storedSteps((string) ($question->explanation ?? ''));
            if ($sentences === []) {
                $empty++;
            } elseif (mb_strlen($sentences[0]) < 12) {
                $thin++;
            }

            if ($this->checked($question) !== null) {
                $checked++;
            } else {
                $stored++;
            }
        });

        return compact('checked', 'stored', 'empty', 'thin', 'conflicts');
    }

    public function conflict(Question $question): bool
    {
        $stem = (string) $question->stem;
        foreach ($this->solvers as $solver) {
            if ($solver->recognizes($stem) && $solver->solve($question) === null) {
                return true;
            }
        }

        return false;
    }

    /**
     * @return array{
     *     concept: string|null,
     *     simpler: string|null,
     *     steps: list<string>,
     *     shortcut: string|null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: array{kind: string, length: float, width: float, unit: string}|null
     * }
     */
    private function teach(Question $question): array
    {
        $checked = $this->checked($question);
        if ($checked !== null) {
            $checked['simpler'] = $this->allowsSimpler($question) ? $checked['simpler'] : null;
            $checked['shortcut'] = $this->distinctShortcut($checked['shortcut'], $checked['steps']);

            return $checked;
        }

        $sentences = $this->expound->storedSteps((string) ($question->explanation ?? ''));

        return [
            'concept' => $sentences[0] ?? null,
            'simpler' => null,
            'steps' => array_values(array_slice($sentences, 1)),
            'shortcut' => null,
            'commonMistakes' => [],
            'visual' => null,
        ];
    }

    /**
     * @return array{
     *     concept: string,
     *     simpler: string|null,
     *     steps: list<string>,
     *     shortcut: string|null,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: array{kind: string, length: float, width: float, unit: string}|null
     * }|null
     */
    private function checked(Question $question): ?array
    {
        foreach ($this->solvers as $solver) {
            $solved = $solver->solve($question);
            if ($solved !== null) {
                return $solved;
            }
        }

        return null;
    }

    private function allowsSimpler(Question $question): bool
    {
        $language = strtolower((string) $question->language);

        return ! str_contains($language, 'fil') && ! str_contains($language, 'tagalog');
    }

    /**
     * @param  list<string>  $steps
     */
    private function distinctShortcut(?string $shortcut, array $steps): ?string
    {
        if ($shortcut === null) {
            return null;
        }

        $plain = $this->plain($shortcut);
        foreach ($steps as $step) {
            if ($this->plain($step) === $plain) {
                return null;
            }
        }

        return $shortcut;
    }

    private function plain(string $text): string
    {
        $text = str_replace(['×', '÷', '−'], ['x', '/', '-'], mb_strtolower($text));

        return preg_replace('/\s+/', '', $text) ?? $text;
    }

    /**
     * @param  list<string>  $weakSubcategories
     * @return array{questionId: int, stem: string, skill: string, direction: string}|null
     */
    private function followUp(Question $question, string $result, array $weakSubcategories): ?array
    {
        if (! $question->exists || $question->subcategory_id === null) {
            return null;
        }

        $question->loadMissing('subcategory.category');

        if ($result === 'correct') {
            $other = $this->otherSkill($question, $weakSubcategories);
            if ($other !== null) {
                return $other;
            }
        }

        $pool = Question::query()
            ->with('subcategory.category')
            ->where('status', QuestionStatus::Active)
            ->where('subcategory_id', $question->subcategory_id)
            ->whereKeyNot($question->id)
            ->get();

        if ($pool->isEmpty()) {
            return null;
        }

        $current = $this->score($question);
        $ranked = $pool->map(fn (Question $item): array => ['item' => $item, 'score' => $this->score($item)]);
        $pick = null;
        $direction = 'same';

        if ($result === 'incorrect') {
            $easier = $ranked->filter(fn (array $row): bool => $row['score'] < $current)->sortByDesc('score')->first();
            if (is_array($easier)) {
                $pick = $easier['item'];
                $direction = 'easier';
            }
        } elseif ($result === 'correct') {
            $harder = $ranked->filter(fn (array $row): bool => $row['score'] > $current)->sortBy('score')->first();
            if (is_array($harder)) {
                $pick = $harder['item'];
                $direction = 'harder';
            }
        }

        if (! $pick instanceof Question) {
            $first = $ranked->first();
            $pick = is_array($first) ? $first['item'] : null;
        }

        if (! $pick instanceof Question) {
            return null;
        }

        return $this->card($pick, (string) ($question->subcategory?->name ?? ''), $direction);
    }

    /**
     * @param  list<string>  $weakSubcategories
     * @return array{questionId: int, stem: string, skill: string, direction: string}|null
     */
    private function otherSkill(Question $question, array $weakSubcategories): ?array
    {
        $current = (string) ($question->subcategory?->name ?? '');

        foreach ($weakSubcategories as $name) {
            $name = trim((string) $name);
            if ($name === '' || strcasecmp($name, $current) === 0) {
                continue;
            }

            $subcategory = Subcategory::query()->where('name', $name)->first();
            if ($subcategory === null) {
                continue;
            }

            $easiest = Question::query()
                ->with('subcategory.category')
                ->where('status', QuestionStatus::Active)
                ->where('subcategory_id', $subcategory->id)
                ->whereKeyNot($question->id)
                ->get()
                ->sortBy(fn (Question $item): int => $this->score($item))
                ->first();

            if ($easiest instanceof Question) {
                return $this->card($easiest, (string) $subcategory->name, 'other-skill');
            }
        }

        return null;
    }

    /**
     * @return array{questionId: int, stem: string, skill: string, direction: string}
     */
    private function card(Question $question, string $skill, string $direction): array
    {
        return [
            'questionId' => (int) $question->id,
            'stem' => mb_substr(trim((string) $question->stem), 0, 160),
            'skill' => $skill,
            'direction' => $direction,
        ];
    }

    private function score(Question $question): int
    {
        return MockPoolSelector::estimateDifficulty([
            'stem' => (string) $question->stem,
            'explanation' => (string) ($question->explanation ?? ''),
            'options' => array_values($question->options ?? []),
            'category' => (string) ($question->subcategory?->category?->name ?? ''),
            'subcategory' => (string) ($question->subcategory?->name ?? ''),
        ]);
    }
}
