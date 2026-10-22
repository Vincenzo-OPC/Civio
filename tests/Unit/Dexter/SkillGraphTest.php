<?php

use App\Services\Dexter\SkillGraph;
use Tests\TestCase;

uses(TestCase::class);

test('the shipped graph is acyclic and has no dangling prerequisites', function () {
    expect((new SkillGraph)->problems())->toBe([])
        ->and(config('dexter_skill_graph.version'))->toMatch('/^\d{4}-\d{2}-\d{2}\.\d+$/');
});

test('every misconception remedial skill exists in the graph', function () {
    $graph = new SkillGraph;
    foreach (config('dexter_misconceptions.codes') as $code => $entry) {
        if ($entry['remedial_skill'] !== null) {
            expect($graph->has($entry['remedial_skill']))->toBeTrue("{$code} -> {$entry['remedial_skill']}");
        }
    }
});

test('foundations come out deepest first', function () {
    expect((new SkillGraph)->foundationsOf('NUM-WP-PCT-CHANGE'))
        ->toBe(['NUM-OPS-ORDER', 'NUM-FRAC-DEC', 'NUM-PCT-BASIC']);
});

test('a diamond lists each foundation once', function () {
    $f = (new SkillGraph)->foundationsOf('NUM-WP-RATE');
    expect($f)->toBe(array_values(array_unique($f)))
        ->and(array_search('NUM-OPS-ORDER', $f))->toBeLessThan(array_search('NUM-WP-ALGEBRA', $f));
});

test('cycles, self-loops and unknown skills are reported', function () {
    $graph = new SkillGraph([
        'A' => ['label' => 'A', 'domain' => 'x', 'prerequisites' => ['B']],
        'B' => ['label' => 'B', 'domain' => 'x', 'prerequisites' => ['A', 'B', 'Z']],
    ]);
    $p = implode("\n", $graph->problems());

    expect($p)->toContain('cycle')->toContain('B lists itself')->toContain('unknown skill Z');
});
