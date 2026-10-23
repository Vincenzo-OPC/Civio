<?php

use App\Console\Commands\LaunchCheckCommand;
use App\Http\Middleware\VerifyTurnstile;
use Illuminate\Http\Request;
use Illuminate\Routing\Route;

/** A configuration that should pass every production check. */
function safeLaunchConfig(): void
{
    config()->set([
        'app.debug' => false,
        'session.secure' => true,
        'services.turnstile.site_key' => 'site',
        'services.turnstile.secret_key' => 'secret',
        'civio.turnstile_required' => true,
        'civio.trusted_proxies' => ['10.0.0.0/8'],
        'civio.trusted_proxies_allow_wildcard' => false,
        'ai.owner_funded_inference_enabled' => false,
        'civio.guest_unlimited' => false,
    ]);
}

function launchStatus(string $check, bool $production = true): string
{
    foreach (LaunchCheckCommand::results($production) as [$name, $status]) {
        if ($name === $check) {
            return $status;
        }
    }

    throw new RuntimeException("no check {$check}");
}

it('passes a fully safe production configuration', function () {
    safeLaunchConfig();

    $this->artisan('civio:launch-check', ['--production' => true])
        ->expectsOutputToContain('Launch check passed with 0 warning(s).')
        ->assertSuccessful();
});

it('fails each unsafe production setting', function (array $override, string $check) {
    safeLaunchConfig();
    config()->set($override);

    expect(launchStatus($check))->toBe('fail');
    $this->artisan('civio:launch-check', ['--production' => true])->assertFailed();
})->with([
    'debug on' => [['app.debug' => true], 'APP_DEBUG'],
    'secure cookie unset' => [['session.secure' => null], 'SESSION_SECURE_COOKIE'],
    'secure cookie false' => [['session.secure' => false], 'SESSION_SECURE_COOKIE'],
    'turnstile site key missing' => [['services.turnstile.site_key' => null], 'Turnstile keys'],
    'turnstile secret missing' => [['services.turnstile.secret_key' => ''], 'Turnstile keys'],
    'wildcard proxy' => [['civio.trusted_proxies' => ['*']], 'Trusted proxies'],
    'double wildcard proxy' => [['civio.trusted_proxies' => ['**']], 'Trusted proxies'],
    'AI kill switch open' => [['ai.owner_funded_inference_enabled' => true], 'AI kill switch'],
    'guest unlimited' => [['civio.guest_unlimited' => true], 'Guest unlimited'],
]);

it('downgrades an acknowledged wildcard proxy to a warning', function () {
    safeLaunchConfig();
    config()->set(['civio.trusted_proxies' => ['*'], 'civio.trusted_proxies_allow_wildcard' => true]);

    expect(launchStatus('Trusted proxies'))->toBe('warn');
    $this->artisan('civio:launch-check', ['--production' => true])->assertSuccessful();
});

it('warns, not fails, when no proxies are configured or fail-closed is off', function () {
    safeLaunchConfig();
    config()->set(['civio.trusted_proxies' => [], 'civio.turnstile_required' => false]);

    expect(launchStatus('Trusted proxies'))->toBe('warn')
        ->and(launchStatus('Turnstile fail-closed'))->toBe('warn');
    $this->artisan('civio:launch-check', ['--production' => true])
        ->expectsOutputToContain('2 warning(s)')
        ->assertSuccessful();
});

it('reports problems as warnings outside production', function () {
    safeLaunchConfig();
    config()->set(['app.debug' => true, 'civio.guest_unlimited' => true]);

    expect(launchStatus('APP_DEBUG', production: false))->toBe('warn');
    $this->artisan('civio:launch-check')->assertSuccessful();
});

it('evaluates as production when APP_ENV is production', function () {
    safeLaunchConfig();
    config()->set('app.debug', true);
    app()->detectEnvironment(fn () => 'production');

    $this->withoutMiddleware([VerifyCsrfToken::class, ValidateCsrfToken::class])->artisan('civio:launch-check')->assertFailed();
});

it('reads the trusted proxy list from config without trusting anyone by default', function () {
    expect(config('civio.trusted_proxies'))->toBe([]);
});

/** Run VerifyTurnstile on a login POST; true when the request got through. */
function turnstilePasses(): bool
{
    $request = Request::create('/login', 'POST', ['email' => 'a@b.test']);
    $request->setLaravelSession(app('session.store'));
    $route = (new Route('POST', '/login', []))->name('login.store');
    $request->setRouteResolver(fn () => $route);

    $response = app(VerifyTurnstile::class)->handle($request, fn () => response('next'));

    return $response->getContent() === 'next';
}

it('fails closed on login when Turnstile is required in production but keys are missing', function () {
    config()->set(['services.turnstile.site_key' => null, 'services.turnstile.secret_key' => null, 'civio.turnstile_required' => true]);
    app()->detectEnvironment(fn () => 'production');

    expect(turnstilePasses())->toBeFalse()
        ->and(session('errors')?->has('turnstile'))->toBeTrue();
});

it('keeps the old skip behaviour when fail-closed is not requested', function () {
    config()->set(['services.turnstile.site_key' => null, 'services.turnstile.secret_key' => null, 'civio.turnstile_required' => false]);
    app()->detectEnvironment(fn () => 'production');

    expect(turnstilePasses())->toBeTrue();
});

it('does not fail closed outside production', function () {
    config()->set(['services.turnstile.site_key' => null, 'services.turnstile.secret_key' => null, 'civio.turnstile_required' => true]);

    expect(turnstilePasses())->toBeTrue();
});
