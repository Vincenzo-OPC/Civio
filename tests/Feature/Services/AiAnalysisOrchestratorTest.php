<?php

use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\User;
use App\Models\UserAiAnalysis;
use App\Services\Ai\AiGatewayService;
use App\Services\AiAnalysisOrchestrator;
use App\Services\DeterministicAnalysisService;
use Illuminate\Support\Facades\DB;

/**
 * Upstream fix 7b9f6bb (cherry-picked as c6a173f): a stored AI analysis with missing keys (or a
 * non-array payload) must not throw when fresh drill results are merged in.
 */
function orchestratorWithDrillAfterMock(User $user): AiAnalysisOrchestrator
{
    $category = Category::create(['name' => 'Numerical Ability', 'slug' => 'numerical-ability']);

    $mock = ExamAttempt::create(['user_id' => $user->id, 'category_id' => null, 'question_ids' => [], 'answers' => [], 'cat_scores' => []]);
    $mock->forceFill(['created_at' => now()->subHour()])->save();
    ExamAttempt::create(['user_id' => $user->id, 'category_id' => $category->id, 'question_ids' => [], 'answers' => [], 'cat_scores' => []]);

    $gateway = Mockery::mock(AiGatewayService::class);
    $gateway->shouldReceive('isAiConfigured')->andReturn(true);

    // Deterministic drill analysis that is missing every merged key.
    $deterministic = Mockery::mock(DeterministicAnalysisService::class);
    $deterministic->shouldReceive('generate')->andReturn([]);
    $deterministic->shouldReceive('sanitizeStored')->andReturnUsing(fn ($d) => is_array($d) ? $d : null);

    UserAiAnalysis::create([
        'user_id' => $user->id,
        'last_exam_attempt_id' => $mock->id,
        'analysis_json' => ['summary' => 'Partial analysis'],
    ]);

    return new AiAnalysisOrchestrator($deterministic, $gateway);
}

// These tests exercise the legacy AI code paths, so they open the Issue #18
// owner-funded AI lock explicitly. HTTP stays faked; no real request is made.
beforeEach(function () {
    config(['ai.owner_funded_inference_enabled' => true]);
});

test('merging drill results into an analysis with missing keys falls back to safe defaults', function () {
    $user = User::factory()->create();
    $result = orchestratorWithDrillAfterMock($user)->resolveAnalysis($user->id);

    expect($result['status'])->toBe('ready')
        ->and($result['data']['summary'])->toBe('Partial analysis')
        ->and($result['data']['subject_breakdowns'])->toBe([])
        ->and($result['data']['critical_weaknesses'])->toBe([])
        ->and($result['data']['top_strengths'])->toBe([])
        ->and($result['data']['readiness_index'])->toBe(0);
});

test('a non-array stored analysis is treated as empty instead of throwing', function () {
    $user = User::factory()->create();
    $orchestrator = orchestratorWithDrillAfterMock($user);
    DB::table('user_ai_analyses')->where('user_id', $user->id)->update(['analysis_json' => json_encode('not an object')]);

    $result = $orchestrator->resolveAnalysis($user->id);

    expect($result['status'])->toBe('ready')
        ->and($result['data'])->toBe([
            'subject_breakdowns' => [],
            'critical_weaknesses' => [],
            'top_strengths' => [],
            'readiness_index' => 0,
        ]);
});
