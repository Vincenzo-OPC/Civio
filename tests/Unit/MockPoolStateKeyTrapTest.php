<?php

use App\Services\Exam\MockPoolState;

function filRow(int $id, array $options, int $correct, string $stem): array
{
    return ['id' => $id, 'stem' => $stem, 'options' => $options, 'correct' => $correct, 'language' => 'Filipino', 'category' => 'Verbal Ability', 'subcategory' => 'Filipino'];
}

test('a Filipino item whose key is another taken item\'s distractor is not free, both ways', function () {
    $syn = filRow(1, ['tuyo', 'napakalaki', 'malago', 'mabango'], 2, 'Kahulugan ng MAYABONG?');
    $ant = filRow(2, ['kalbo', 'mabango', 'malago', 'lubos na patay'], 0, 'Kasalungat ng MALABAY?');

    $state = new MockPoolState;
    $state->take($syn);
    expect($state->isFree($ant))->toBeFalse();

    $state = new MockPoolState;
    $state->take($ant);
    expect($state->isFree($syn))->toBeFalse();
});

test('marker pairs, order codes and English items never block each other', function () {
    $state = new MockPoolState;
    $state->take(filRow(1, ['ng / ng', 'nang / nang', 'nang / ng', 'ng / nang'], 3, 'A ___ B ___'));
    expect($state->isFree(filRow(2, ['nang / ng', 'ng / ng', 'nang / nang', 'ng / nang'], 0, 'C ___ D ___')))->toBeTrue();

    $state->take(['id' => 3, 'stem' => 'Pick', 'options' => ['quiet', 'noisy', 'loud', 'calm'], 'correct' => 0, 'language' => 'English']);
    expect($state->isFree(['id' => 4, 'stem' => 'Opposite', 'options' => ['quiet', 'noisy', 'loud', 'calm'], 'correct' => 1, 'language' => 'English']))->toBeTrue();
});

test('rows without a known key (old callers) behave exactly as before', function () {
    $state = new MockPoolState;
    $state->take(['id' => 1, 'stem' => 'x', 'options' => ['malago', 'b', 'c', 'd'], 'language' => 'Filipino']);
    expect($state->isFree(['id' => 2, 'stem' => 'y', 'options' => ['e', 'malago', 'g', 'h'], 'language' => 'Filipino', 'correct' => 0]))->toBeTrue()
        ->and($state->isFree(['id' => 1, 'stem' => 'x', 'options' => [], 'language' => 'Filipino']))->toBeFalse();
});
