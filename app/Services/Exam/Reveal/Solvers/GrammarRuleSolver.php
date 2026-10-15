<?php

declare(strict_types=1);

namespace App\Services\Exam\Reveal\Solvers;

use App\Models\Question;

/**
 * A few grammar errors with a checkable rule. The lesson is published only
 * when the stored key is the option that contains that error. Other pronoun
 * and agreement items keep their stored explanation.
 */
final class GrammarRuleSolver implements RevealSolver
{
    public function recognizes(string $stem): bool
    {
        return false;
    }

    public function solve(Question $question): ?array
    {
        $options = array_values(array_map(strval(...), $question->options ?? []));
        $choice = $options[(int) $question->correct_option] ?? '';
        $rule = $this->rule($choice);
        if ($rule === null) {
            return null;
        }

        $rule['commonMistakes'] = [];
        unset($rule['others']);

        return $rule;
    }

    /**
     * recognizes() stays false so an unmatched pronoun item is not flagged as
     * a bad key. Ownership is the keyed sentence itself.
     *
     * @return array{
     *     concept: string,
     *     simpler: string|null,
     *     steps: list<string>,
     *     shortcut: string|null,
     *     others: list<array{choice: string, why: string}>,
     *     commonMistakes: list<array{choice: string, why: string}>,
     *     visual: null
     * }|null
     */
    private function rule(string $choice): ?array
    {
        if (preg_match('/between you and I\b/i', $choice) === 1) {
            return [
                'concept' => 'A preposition such as between takes the object form. "Between you and I" should be "between you and me."',
                'simpler' => 'Alisin muna ang "you and." "Between I" ay mali. "Between me" ang tama.',
                'steps' => [
                    'Between is a preposition.',
                    'The pronoun after it has to be me, not I.',
                    'Drop the other person: "between me" is the form that remains.',
                ],
                'shortcut' => 'Drop the other person. If "I" sounds wrong alone, it is wrong in the pair.',
                'others' => [],
                'commonMistakes' => [],
                'visual' => null,
            ];
        }

        if (preg_match('/\bMe and him\b/i', $choice) === 1) {
            return [
                'concept' => 'The subject of the sentence needs the subject form. "Me and him will attend" should be "He and I will attend."',
                'simpler' => 'Kung ikaw ang gumagawa, "I" at "he," hindi "me" at "him."',
                'steps' => [
                    'The people are doing the action, so they are the subject.',
                    'Me and him are object forms.',
                    'The subject forms are he and I.',
                ],
                'shortcut' => 'Try each person alone. "Me will attend" is already wrong.',
                'others' => [],
                'commonMistakes' => [],
                'visual' => null,
            ];
        }

        if (preg_match('/\bEach of the\b.+\bneed\b/i', $choice) === 1 && preg_match('/\bneeds\b/i', $choice) !== 1) {
            return [
                'concept' => 'Each is singular. Words that follow "of" do not become the subject.',
                'simpler' => 'Ang "each" ay isa. Kaya "needs," hindi "need."',
                'steps' => [
                    'The subject is each.',
                    'Each takes a singular verb.',
                    'The sentence should say "needs," not "need."',
                ],
                'shortcut' => 'Cover the phrase after of. "Each need" is the error.',
                'others' => [],
                'commonMistakes' => [],
                'visual' => null,
            ];
        }

        if (preg_match('/\bThe set of\b.+\bwere\b/i', $choice) === 1) {
            return [
                'concept' => 'The subject is set, which is singular. "Of keys" describes the set. It does not make the verb plural.',
                'simpler' => 'Ang subject ay "set," isa lang. Kaya "was," hindi "were."',
                'steps' => [
                    'Find the subject before of.',
                    'Set is singular.',
                    'The verb should be was, not were.',
                ],
                'shortcut' => 'Cover the words after of. "The set were" is the error.',
                'others' => [],
                'commonMistakes' => [],
                'visual' => null,
            ];
        }

        return null;
    }
}
