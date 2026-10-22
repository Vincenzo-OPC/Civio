<?php

use App\Services\Dexter\NextSkillRecommender;
use App\Services\Dexter\SkillGraph;
use App\Services\Dexter\SkillMasteryEstimator;
use Tests\TestCase;

uses(TestCase::class);

function events(string $skill, string $pattern): array
{
    return array_map(fn ($c) => ['skill' => $skill, 'correct' => $c === '1'], str_split($pattern));
}

test('BKT rises with correct answers, falls with wrong ones and stays a probability', function () {
    $est = new SkillMasteryEstimator;
    $up = $est->estimate(events('NUM-PCT-BASIC', '11111111'))['NUM-PCT-BASIC'];
    $down = $est->estimate(events('NUM-PCT-BASIC', '00000000'))['NUM-PCT-BASIC'];

    expect($up['estimate'])->toBeGreaterThan(0.9)->toBeLessThanOrEqual(1.0)
        ->and($down['estimate'])->toBeLessThan(0.2)->toBeGreaterThan(0.0)
        ->and($up['answers'])->toBe(8)->and($up['correct'])->toBe(8);
});

test('a lucky guess or two is not enough evidence', function () {
    $e = (new SkillMasteryEstimator)->estimate(events('NUM-FRAC-DEC', '11'))['NUM-FRAC-DEC'];

    expect($e['enough'])->toBeFalse()->and($e['answers'])->toBeLessThan(SkillMasteryEstimator::MIN_ANSWERS);
});

test('recent answers outweigh old ones', function () {
    $est = new SkillMasteryEstimator;
    expect($est->estimate(events('S', '00001111'))['S']['estimate'])
        ->toBeGreaterThan($est->estimate(events('S', '11110000'))['S']['estimate']);
});

test('no weak skill with enough evidence means no recommendation', function () {
    $est = (new SkillMasteryEstimator)->estimate([...events('NUM-PCT-BASIC', '0000'), ...events('NUM-FRAC-DEC', '11111')]);

    expect((new NextSkillRecommender(new SkillGraph))->recommend($est))->toBeNull();
});

test('an untested foundation is checked first', function () {
    $est = (new SkillMasteryEstimator)->estimate(events('NUM-WP-PCT-CHANGE', '000010'));
    $r = (new NextSkillRecommender(new SkillGraph))->recommend($est);

    expect($r['skill'])->toBe('NUM-OPS-ORDER')
        ->and($r['kind'])->toBe('check_foundation')
        ->and($r['basedOn'])->toBe('1 of 6 independent answers correct in Percent change, discounts and markups')
        ->and($r['reason'])->toContain('builds on Order of operations');
});

test('a shaky foundation is repaired before the target', function () {
    $est = (new SkillMasteryEstimator)->estimate([
        ...events('NUM-OPS-ORDER', '11111'),
        ...events('NUM-FRAC-DEC', '11111'),
        ...events('NUM-PCT-BASIC', '00100'),
        ...events('NUM-WP-PCT-CHANGE', '000000'),
    ]);
    $r = (new NextSkillRecommender(new SkillGraph))->recommend($est);

    expect($r['skill'])->toBe('NUM-PCT-BASIC')->and($r['kind'])->toBe('repair_foundation');
});

test('with solid foundations the weak skill itself is recommended, never called mastered', function () {
    $est = (new SkillMasteryEstimator)->estimate([
        ...events('NUM-OPS-ORDER', '11111'),
        ...events('NUM-FRAC-DEC', '11111'),
        ...events('NUM-PCT-BASIC', '11111'),
        ...events('NUM-WP-PCT-CHANGE', '010000'),
    ]);
    $r = (new NextSkillRecommender(new SkillGraph))->recommend($est);

    expect($r['skill'])->toBe('NUM-WP-PCT-CHANGE')
        ->and($r['kind'])->toBe('practice_skill')
        ->and($r['model'])->toBe('bkt-v2-fixed')
        ->and(strtolower(json_encode($r)))->not->toContain('master');
});

test('skills outside the graph are ignored', function () {
    $est = (new SkillMasteryEstimator)->estimate(events('Word problems', '000000'));

    expect((new NextSkillRecommender(new SkillGraph))->recommend($est))->toBeNull();
});
