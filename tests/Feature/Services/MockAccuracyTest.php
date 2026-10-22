<?php

use App\Enums\ExamMode;
use App\Enums\SelectionPolicy;
use App\Jobs\GenerateUserAnalysisJob;
use App\Models\ExamAttempt;
use App\Models\User;
use App\Services\DeterministicAnalysisService;

function mockAttempt(int $userId, int $correct, int $total, ?SelectionPolicy $policy, string $track = 'Professional'): ExamAttempt
{
    return ExamAttempt::create([
        'user_id' => $userId, 'category_id' => null,
        'mode' => $policy === SelectionPolicy::Representative ? ExamMode::Strict->value : ExamMode::Study->value,
        'selection_policy' => $policy?->value,
        'question_ids' => range(1, $total), 'answers' => [],
        'cat_scores' => ['categoryScoreMap' => [], 'metadata' => ['track' => $track, 'correct_count' => $correct, 'total_questions' => $total]],
    ]);
}

test('mock accuracy is correct over scored questions, split by selection policy', function () {
    $u = User::factory()->create();
    mockAttempt($u->id, 120, 150, SelectionPolicy::Representative);
    mockAttempt($u->id, 90, 150, SelectionPolicy::Adaptive);
    $last = mockAttempt($u->id, 75, 150, null); // legacy row, no stored policy

    $ma = (new DeterministicAnalysisService)->generate($u->id, $last->id)['mock_accuracy'];

    expect($ma['correct'])->toBe(285)->and($ma['total'])->toBe(450)->and($ma['mocks'])->toBe(3)
        ->and($ma['percent'])->toEqual(63.3)
        ->and($ma['tracks'])->toBe(['Professional'])
        ->and($ma['representative'])->toMatchArray(['correct' => 120, 'total' => 150, 'mocks' => 1])
        ->and($ma['representative']['percent'])->toEqual(80)
        ->and($ma['personalized'])->toMatchArray(['correct' => 165, 'total' => 300, 'mocks' => 2, 'legacy' => 1]);
});

test('analysis carries no pass prediction fields', function () {
    $u = User::factory()->create();
    $a = mockAttempt($u->id, 140, 150, SelectionPolicy::Representative);
    $r = (new DeterministicAnalysisService)->generate($u->id, $a->id);

    expect($r)->not->toHaveKey('pass_probability')
        ->and($r['predictive_metrics'])->not->toHaveKeys(['days_to_readiness', 'estimated_exam_score', 'mock_pass_confidence'])
        ->and(json_encode($r))->not->toMatch('/pass(ing)? probability|days to readiness/i');
});

test('legacy stored analysis is sanitized and gains mock accuracy', function () {
    $u = User::factory()->create();
    mockAttempt($u->id, 100, 150, SelectionPolicy::Representative);
    $legacy = ['pass_probability' => 91, 'verdict' => 'x', 'predictive_metrics' => ['days_to_readiness' => '3 days', 'completion_pace' => 'ok']];

    $out = (new DeterministicAnalysisService)->sanitizeStored($legacy, $u->id);

    expect($out)->not->toHaveKey('pass_probability')
        ->and($out['predictive_metrics'])->toBe(['completion_pace' => 'ok'])
        ->and($out['mock_accuracy']['correct'])->toBe(100)
        ->and((new DeterministicAnalysisService)->sanitizeStored('garbage', $u->id))->toBeNull();
});

test('model output cannot reinject a pass probability', function () {
    expect(GenerateUserAnalysisJob::coachingFields([
        'pass_probability' => 99, 'verdict' => 'v', 'mock_accuracy' => ['percent' => 100],
        'predictive_metrics' => ['days_to_readiness' => '1', 'estimated_exam_score' => '90%', 'completion_pace' => 'ok'],
    ]))->toBe(['verdict' => 'v', 'predictive_metrics' => ['completion_pace' => 'ok']]);
});
