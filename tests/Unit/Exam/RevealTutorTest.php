<?php

declare(strict_types=1);

use App\Models\Question;
use App\Services\Exam\ExpoundService;
use App\Services\Exam\Reveal\RevealTutor;

function tutor(): RevealTutor
{
    return new RevealTutor(new ExpoundService);
}

function tutorQuestion(array $overrides): Question
{
    return new Question(array_merge([
        'language' => 'English',
        'options' => ['34 m', '60 m', '17 m', '24 m'],
        'correct_option' => 0,
        'explanation' => 'Stored work.',
    ], $overrides));
}

it('teaches a rectangle perimeter without hard-coding one example', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'A rectangle is 12 m by 5 m. Its perimeter is:',
    ]));

    expect($tutor['concept'])->toContain('distance around')
        ->and($tutor['steps'][0])->toBe('12 + 5 + 12 + 5 = 34 m.')
        ->and($tutor['shortcut'])->toBe('2 × (12 + 5) = 34 m.')
        ->and($tutor['simpler'])->toContain('paligid')
        ->and($tutor['visual']['kind'] ?? null)->toBe('rectangle')
        ->and($tutor['commonMistakes'][0]['choice'] ?? null)->toBe('60 m')
        ->and($tutor['commonMistakes'][0]['why'] ?? '')->toContain('area');
});

it('teaches the bank perimeter wording the same way', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Lot 9 is a rectangle 9 meters by 4 meters. What is its perimeter?',
        'options' => ['36 m', '26 m', '13 m', '28 m'],
        'correct_option' => 1,
    ]));

    expect($tutor['steps'][0])->toBe('9 + 4 + 9 + 4 = 26 m.')
        ->and($tutor['commonMistakes'])->toHaveCount(2);
});

it('refuses a perimeter explanation when the key is the area', function () {
    $question = tutorQuestion([
        'stem' => 'A rectangle is 12 m by 5 m. Its perimeter is:',
        'options' => ['60 m', '34 m', '17 m', '24 m'],
        'correct_option' => 0,
        'explanation' => 'Stored work stays. The matching choice is “60 m.”',
    ]);
    $tutor = tutor();

    expect($tutor->conflict($question))->toBeTrue()
        ->and($tutor->forQuestion($question)['concept'])->toBe('Stored work stays.')
        ->and($tutor->forQuestion($question)['visual'])->toBeNull()
        ->and($tutor->forQuestion($question)['shortcut'])->toBeNull();
});

it('names the left-to-right miss on an order-of-operations item', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Evaluate: 15 - 3 times 4 + 6',
        'options' => ['54', '9', '18', '3'],
        'correct_option' => 1,
    ]));

    expect($tutor['concept'])->toContain('Multiply and divide')
        ->and(implode(' ', $tutor['steps']))->toContain('3 × 4 = 12.')
        ->and($tutor['shortcut'])->toBeNull()
        ->and($tutor['commonMistakes'][0]['choice'] ?? null)->toBe('54');
});

it('checks a percent item and skips a shortcut that is not faster', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'What is 20 percent of 100 forms?',
        'options' => ['20', '40', '2000', '19'],
        'correct_option' => 0,
    ]));

    expect($tutor['steps'][0])->toBe('100 × 20 ÷ 100 = 20.')
        ->and($tutor['shortcut'])->toBeNull()
        ->and($tutor['commonMistakes'][0]['why'] ?? '')->toContain('divided by 100');
});

it('does not invent a shortcut for a stored verbal explanation', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'The word “benign” most nearly means:',
        'options' => ['Harmless', 'Dangerous', 'Hidden', 'Required'],
        'correct_option' => 0,
        'explanation' => 'Benign means not harmful. The matching choice is “Harmless.” “Dangerous”, “Hidden”, “Required” do not follow the same steps.',
    ]));

    expect($tutor['concept'])->toBe('Benign means not harmful.')
        ->and($tutor['steps'])->toBe([])
        ->and($tutor['shortcut'])->toBeNull()
        ->and($tutor['simpler'])->toBeNull()
        ->and($tutor['commonMistakes'])->toBe([]);
});

it('does not add Taglish to a Filipino item', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'language' => 'Filipino',
        'stem' => 'A rectangle is 12 m by 5 m. Its perimeter is:',
    ]));

    expect($tutor['simpler'])->toBeNull()
        ->and($tutor['steps'])->not->toBeEmpty();
});

it('teaches terminal-digit filing by groups when the key is the last pair', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'In terminal-digit filing of 12-34-56, which pair is read first?',
        'options' => ['12', '34', '56', '65'],
        'correct_option' => 2,
    ]));

    expect($tutor['concept'])->toContain('last group')
        ->and($tutor['steps'][0])->toBe('56 is the primary group. Read it first.')
        ->and($tutor['shortcut'])->toContain('rightmost')
        ->and($tutor['visual']['kind'] ?? null)->toBe('filing')
        ->and($tutor['commonMistakes'][0]['choice'] ?? null)->toBe('12');
});

it('refuses a terminal-digit item whose key is not the last group', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'In terminal-digit filing of 12-34-56, which pair is read first?',
        'options' => ['12', '34', '56', '65'],
        'correct_option' => 0,
    ]));

    expect($tutor['visual'])->toBeNull()
        ->and($tutor['shortcut'])->toBeNull();
});

it('teaches a Fibonacci-type sequence only when the next term matches the key', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Find the next number: 1, 1, 2, 3, 5, 8, ___',
        'options' => ['11', '12', '13', '16'],
        'correct_option' => 2,
    ]));

    expect($tutor['concept'])->toContain('Fibonacci-type')
        ->and(implode(' ', $tutor['steps']))->toContain('5 + 8 = 13.');
});

it('does not call an ordinary sequence Fibonacci', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Find the next number: 2, 4, 6, 8, ___',
        'options' => ['9', '10', '12', '16'],
        'correct_option' => 1,
    ]));

    expect($tutor['concept'])->not->toContain('Fibonacci');
});

it('teaches a two-solution mixture when the weighted result matches the key', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Mixture: 2 liters of 10% solution + 3 liters of 20% solution. Resulting concentration:',
        'options' => ['14%', '15%', '16%', '18%'],
        'correct_option' => 2,
    ]));

    expect($tutor['steps'][4] ?? null)->toBe('0.8 ÷ 5 × 100 = 16%.')
        ->and($tutor['shortcut'])->toContain('16%')
        ->and($tutor['commonMistakes'][0]['choice'] ?? null)->toBe('15%')
        ->and($tutor['visual']['kind'] ?? null)->toBe('mixture');
});

it('refuses a mixture whose key is the unweighted average', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Mix 2 liters of a 10% solution with 3 liters of a 20% solution. What is the resulting concentration?',
        'options' => ['14%', '15%', '16%', '18%'],
        'correct_option' => 1,
    ]));

    expect($tutor['visual'])->toBeNull()
        ->and($tutor['shortcut'])->toBeNull();
});

it('teaches alphabetical order when the key is the last name', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Which comes last alphabetically?',
        'options' => ['Lopez, Ana', 'Lopez, Beatriz', 'Lopez, Carla', 'Lopez, Diana'],
        'correct_option' => 3,
    ]));

    expect($tutor['steps'][0])->toContain('Lopez, Diana')
        ->and($tutor['visual']['mark'] ?? null)->toBe('Lopez, Diana');
});

it('teaches between you and I only when that sentence is the key', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Which sentence contains an incorrect pronoun case?',
        'options' => [
            'The supervisor spoke with Ana and me.',
            'He and I prepared the index.',
            'Between you and I, the file is incomplete.',
            'They submitted their reports.',
        ],
        'correct_option' => 2,
    ]));

    expect($tutor['concept'])->toContain('between you and me')
        ->and($tutor['shortcut'])->toContain('Drop the other person');
});

it('keeps a stored explanation when the pronoun error is not a checked rule', function () {
    $tutor = tutor()->forQuestion(tutorQuestion([
        'stem' => 'Which sentence contains an incorrect pronoun case?',
        'options' => ['Ana and me went.', 'Correct one.', 'Also fine.', 'Fine too.'],
        'correct_option' => 0,
        'explanation' => 'Stored pronoun note.',
    ]));

    expect($tutor['concept'])->toBe('Stored pronoun note.')
        ->and($tutor['shortcut'])->toBeNull();
});
