<?php

use App\Jobs\GenerateLearnModuleJob;
use App\Jobs\GenerateQuestionsJob;
use App\Jobs\GenerateUserAnalysisJob;
use App\Models\Category;
use App\Models\ExamAttempt;
use App\Models\User;
use App\Models\UserAiAnalysis;
use App\Rules\NoProfanity;
use App\Services\Ai\AiGatewayService;
use App\Services\Ai\OwnerAiSpendLock;
use App\Services\AiAnalysisOrchestrator;
use App\Services\UserPreferenceService;
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Validator;

/*
 * Issue #18: with fake but valid-looking owner credentials for every provider,
 * nothing may send an external AI request while the lock is closed (default).
 */

function setDummyOwnerAiKeys(): void
{
    config([
        'services.gemini.key' => 'AIzaFAKE-not-a-real-key-000000000000000',
        'services.cloudflare.account_id' => 'fake-account-0000',
        'services.cloudflare.api_token' => 'fake-cf-token-0000',
        'services.cloudflare.ai_gateway_id' => 'fake-gateway',
        'services.groq.key' => 'gsk_FAKE_not_real_0000',
        'ai.tutor_provider' => 'gemini',
        'ai.prism_default_provider' => 'gemini',
    ]);
}

function makeAttemptsFor(User $user): ExamAttempt
{
    $category = Category::create(['name' => 'Numerical Ability', 'slug' => 'numerical-ability-'.$user->id]);
    $mock = ExamAttempt::create(['user_id' => $user->id, 'category_id' => null, 'question_ids' => [], 'answers' => [], 'cat_scores' => []]);
    ExamAttempt::create(['user_id' => $user->id, 'category_id' => $category->id, 'question_ids' => [], 'answers' => [], 'cat_scores' => []]);

    return $mock;
}

beforeEach(function () {
    setDummyOwnerAiKeys();
    Http::preventStrayRequests();
    Http::fake();
});

afterEach(function () {
    Http::assertNothingSent();
});

test('the lock is closed by default even with every owner key present', function () {
    expect(config('ai.owner_funded_inference_enabled'))->toBeFalse()
        ->and(OwnerAiSpendLock::enabled())->toBeFalse();
});

test('only the exact raw string "true" parses as enabled', function (mixed $raw, bool $expected) {
    expect(OwnerAiSpendLock::parseFlag($raw))->toBe($expected);
})->with([
    ['true', true],
    ['1', false], ['yes', false], ['on', false], ['TRUE', false], ['True', false],
    ['TRUE ', false], [' true', false], ['true ', false], ['(true)', false],
    ['false', false], ['0', false], ['', false], [null, false], [1, false],
]);

test('config/ai.php reads the raw env value strictly', function (?string $raw, bool $expected) {
    $key = 'CIVIO_OWNER_FUNDED_AI';
    $old = [$_ENV[$key] ?? null, $_SERVER[$key] ?? null];
    if ($raw === null) {
        unset($_ENV[$key], $_SERVER[$key]);
    } else {
        $_ENV[$key] = $raw;
        $_SERVER[$key] = $raw;
    }

    try {
        $config = require base_path('config/ai.php');
        expect($config['owner_funded_inference_enabled'])->toBe($expected);
    } finally {
        [$e, $s] = $old;
        if ($e === null) {
            unset($_ENV[$key]);
        } else {
            $_ENV[$key] = $e;
        }
        if ($s === null) {
            unset($_SERVER[$key]);
        } else {
            $_SERVER[$key] = $s;
        }
    }
})->with([
    [null, false], ['1', false], ['yes', false], ['TRUE', false], ['TRUE ', false], ['on', false], ['true', true],
]);

test('production stays locked even when the flag is exactly true', function () {
    config(['ai.owner_funded_inference_enabled' => true]);
    app()->detectEnvironment(fn () => 'production');

    try {
        expect(OwnerAiSpendLock::enabled())->toBeFalse()
            ->and(app(AiGatewayService::class)->isAiConfigured())->toBeFalse();
    } finally {
        app()->detectEnvironment(fn () => 'testing');
    }
});

test('a non-boolean cached config value never opens the lock', function (mixed $value) {
    config(['ai.owner_funded_inference_enabled' => $value]);
    expect(OwnerAiSpendLock::enabled())->toBeFalse();
})->with(['true', 1, '1', 'yes', null]);

test('the gateway reports nothing configured and returns a disabled result before any HTTP', function () {
    $gateway = app(AiGatewayService::class);

    expect($gateway->isGeminiConfigured())->toBeFalse()
        ->and($gateway->isWorkersAiConfigured())->toBeFalse()
        ->and($gateway->isAiGatewayConfigured())->toBeFalse()
        ->and($gateway->isAiConfigured())->toBeFalse()
        ->and($gateway->isGroqConfigured())->toBeFalse();

    $results = [
        $gateway->runGemini(AiGatewayService::DEFAULT_GEMINI_MODEL, ['contents' => []]),
        $gateway->runGemini(AiGatewayService::FALLBACK_GEMINI_MODEL, ['contents' => []]),
        $gateway->runWorkersAi(AiGatewayService::DEFAULT_WORKERS_AI_MODEL, ['messages' => []]),
        $gateway->runGroqChat(['messages' => []]),
        $gateway->generateStructuredJson(AiGatewayService::DEFAULT_GEMINI_MODEL, 'sys', 'user'),
        $gateway->generateStructuredJson(AiGatewayService::DEFAULT_WORKERS_AI_MODEL, 'sys', 'user'),
    ];

    foreach ($results as $result) {
        expect($result['success'])->toBeFalse()
            ->and($result['disabled'])->toBeTrue()
            ->and($result['error'])->not->toContain('FAKE');
    }
});

test('stale queued generation jobs no-op on handle', function () {
    $admin = User::factory()->create(['role' => 'admin', 'is_active' => true]);
    $input = ['category' => 'Numerical Ability', 'subcategory' => 'Word problems', 'count' => 5, 'language' => 'English', 'topic' => 'Percent'];

    foreach ([AiGatewayService::DEFAULT_GEMINI_MODEL, AiGatewayService::DEFAULT_WORKERS_AI_MODEL] as $model) {
        (new GenerateQuestionsJob($input, $admin->id, $model, null))->handle();
        (new GenerateLearnModuleJob($input, $admin->id, $model, null))->handle();
    }
});

test('a stale queued analysis job saves deterministic analysis with no Cloudflare or Gemini fallback', function (string $model) {
    $user = User::factory()->create();
    $mock = makeAttemptsFor($user);

    (new GenerateUserAnalysisJob($user->id, $mock->id, $model))->handle();

    $analysis = UserAiAnalysis::where('user_id', $user->id)->first();
    expect($analysis)->not->toBeNull()
        ->and($analysis->last_exam_attempt_id)->toBe($mock->id);
})->with([AiGatewayService::DEFAULT_WORKERS_AI_MODEL, AiGatewayService::DEFAULT_GEMINI_MODEL]);

test('admin generation endpoints refuse clearly and queue nothing', function (string $route, array $payload) {
    Bus::fake();
    $admin = User::factory()->create(['role' => 'admin', 'is_active' => true]);

    $this->actingAs($admin)->postJson(route($route), $payload)
        ->assertStatus(503)
        ->assertJson(['success' => false, 'queued' => false, 'disabled' => true]);

    Bus::assertNotDispatched(GenerateQuestionsJob::class);
    Bus::assertNotDispatched(GenerateLearnModuleJob::class);
    Bus::assertNotDispatchedAfterResponse(GenerateQuestionsJob::class);
    Bus::assertNotDispatchedAfterResponse(GenerateLearnModuleJob::class);
})->with([
    ['questions.generate', ['category' => 'Numerical Ability', 'subcategory' => 'Word problems', 'count' => 5, 'language' => 'English']],
    ['admin.learn.generate', ['category' => 'Numerical Ability', 'subcategory' => 'Word problems', 'topic' => 'Percent']],
]);

test('analytics stays deterministic with a cached ai mode, a stored AI analysis and owner keys', function () {
    Bus::fake();
    $user = User::factory()->create();
    $mock = makeAttemptsFor($user);
    Cache::forever("user-analysis-mode-{$user->id}", 'ai');
    UserAiAnalysis::create(['user_id' => $user->id, 'last_exam_attempt_id' => $mock->id, 'analysis_json' => ['summary' => 'STALE GENERATED TEXT']]);

    $orchestrator = app(AiAnalysisOrchestrator::class);
    $strict = $orchestrator->resolveStrictStatusAndData($user->id);
    $loose = $orchestrator->resolveAnalysis($user->id);
    $orchestrator->retryAnalysis($user->id);

    expect($strict['status'])->toBe('ready')
        ->and(json_encode($strict['data']))->not->toContain('STALE GENERATED TEXT')
        ->and($loose['status'])->toBe('ready')
        ->and(json_encode($loose['data']))->not->toContain('STALE GENERATED TEXT');

    Bus::assertNotDispatched(GenerateUserAnalysisJob::class);
    Bus::assertNotDispatchedAfterResponse(GenerateUserAnalysisJob::class);
});

test('analysis mode defaults to instant and switching to ai dispatches nothing', function () {
    Bus::fake();
    $user = User::factory()->create();
    makeAttemptsFor($user);
    $prefs = app(UserPreferenceService::class);

    expect($prefs->isAiAvailable())->toBeFalse()
        ->and($prefs->getAnalysisMode($user->id))->toBe('instant');

    $prefs->switchAnalysisMode($user->id, 'ai');

    Bus::assertNotDispatchedAfterResponse(GenerateUserAnalysisJob::class);
});

test('the profanity rule never calls Groq or Workers AI', function () {
    $v = Validator::make(['name' => 'Juan dela Cruz unusual phrase'], ['name' => [new NoProfanity]]);
    expect($v->passes())->toBeTrue();
});
