<?php

use App\Services\Dexter\SkillEvidenceBuilder;
use App\Services\Dexter\SkillMasteryEstimator;

function ev(int $qid, ?bool $correct, int $seq, ?int $at = null, bool $assisted = false, string $skill = 'S'): array
{
    return ['skill' => $skill, 'questionId' => $qid, 'answered' => $correct !== null, 'correct' => (bool) $correct,
        'assisted' => $assisted, 'at' => $at, 'seq' => $seq];
}

test('a blank is its own state, never wrong evidence, and does not use up the question', function () {
    $out = (new SkillEvidenceBuilder)->build([ev(1, null, 1, 100), ev(1, true, 2, 200)]);

    expect($out['unanswered'])->toBe(['S' => 1])
        ->and($out['knowledge'])->toBe([['skill' => 'S', 'correct' => true]])
        ->and($out['retention'])->toBe([]);
});

test('repeats of the same question feed retention only, whatever the gap', function () {
    $events = [];
    for ($i = 0; $i < 6; $i++) {
        $events[] = ev(7, true, $i, 100 + $i * 86400 * 30);
    }
    $out = (new SkillEvidenceBuilder)->build($events);

    expect($out['knowledge'])->toHaveCount(1)
        ->and($out['retention'])->toHaveCount(5);

    $est = (new SkillMasteryEstimator)->estimate($out['knowledge'])['S'];
    expect($est['answers'])->toBe(1)->and($est['status'])->toBe('insufficient')->and($est['calibrated'])->toBeFalse();
});

test('assisted answers are never knowledge evidence and use up the question', function () {
    $out = (new SkillEvidenceBuilder)->build([ev(3, true, 1, 100, true), ev(3, true, 2, 200)]);

    expect($out['knowledge'])->toBe([])
        ->and($out['assisted'])->toBe(['S' => 1])
        ->and($out['retention'])->toHaveCount(1);
});

test('events are ordered by timestamp, then sequence; out-of-order ids do not matter', function () {
    // Offline answer (higher seq) happened first in real time.
    $out = (new SkillEvidenceBuilder)->build([ev(5, false, 10, 500), ev(5, true, 99, 100)]);

    expect($out['knowledge'])->toBe([['skill' => 'S', 'correct' => true]])
        ->and($out['retention'][0]['correct'])->toBeFalse();
});

test('events without a timestamp sort after timed ones by sequence; no time is invented', function () {
    $out = (new SkillEvidenceBuilder)->build([ev(9, false, 1, null), ev(9, true, 2, 50)]);

    expect($out['knowledge'])->toBe([['skill' => 'S', 'correct' => true]]);
});

test('five distinct independent answers are needed before an estimate status', function () {
    $est = new SkillMasteryEstimator;
    $four = (new SkillEvidenceBuilder)->build([ev(1, true, 1, 1), ev(2, true, 2, 2), ev(3, true, 3, 3), ev(4, true, 4, 4), ev(4, true, 5, 5)]);
    $five = (new SkillEvidenceBuilder)->build([ev(1, true, 1, 1), ev(2, true, 2, 2), ev(3, true, 3, 3), ev(4, true, 4, 4), ev(5, true, 5, 5)]);

    expect($est->estimate($four['knowledge'])['S']['status'])->toBe('insufficient')
        ->and($est->estimate($five['knowledge'])['S']['status'])->toBe('estimate');
});
