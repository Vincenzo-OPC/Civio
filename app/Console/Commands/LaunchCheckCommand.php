<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Services\TurnstileService;
use Illuminate\Console\Command;

/**
 * Host-independent production readiness check. Reads configuration only;
 * makes no network calls and changes nothing. Exits non-zero when any
 * check fails so a deploy pipeline can stop on it.
 */
class LaunchCheckCommand extends Command
{
    protected $signature = 'civio:launch-check
        {--production : Evaluate as production even if APP_ENV is not production}';

    protected $description = 'Check production safety settings (Turnstile, cookies, debug, proxies, AI lock, guest access)';

    /** @return list<array{0: string, 1: 'pass'|'warn'|'fail', 2: string}> */
    public static function results(bool $production): array
    {
        $fail = $production ? 'fail' : 'warn';
        $r = [];

        $r[] = ['APP_ENV', $production ? 'pass' : 'warn', $production ? 'production' : 'not production; failures are reported as warnings'];
        $r[] = ['APP_DEBUG', config('app.debug') ? $fail : 'pass', config('app.debug') ? 'debug is on; stack traces and env can leak' : 'off'];
        $r[] = ['SESSION_SECURE_COOKIE', config('session.secure') === true ? 'pass' : $fail, config('session.secure') === true ? 'true' : 'not true; session cookies can travel over HTTP'];

        $turnstile = app(TurnstileService::class)->isConfigured();
        $r[] = ['Turnstile keys', $turnstile ? 'pass' : $fail, $turnstile ? 'site and secret key set' : 'missing; login and register run without CAPTCHA'];
        $r[] = ['Turnstile fail-closed', config('civio.turnstile_required') === true ? 'pass' : 'warn', config('civio.turnstile_required') === true ? 'CIVIO_TURNSTILE_REQUIRED=true' : 'off; missing keys skip the CAPTCHA'];

        $proxies = (array) config('civio.trusted_proxies', []);
        if (in_array('*', $proxies, true) || in_array('**', $proxies, true)) {
            $ack = config('civio.trusted_proxies_allow_wildcard') === true;
            $r[] = ['Trusted proxies', $ack ? 'warn' : $fail, $ack ? 'wildcard acknowledged; origin must be reachable only through the edge' : "wildcard '*' lets any client spoof its IP"];
        } else {
            $r[] = ['Trusted proxies', $proxies === [] ? 'warn' : 'pass', $proxies === [] ? 'none; behind a CDN every client shares the edge IP for rate limits' : count($proxies).' range(s) configured'];
        }

        $ai = config('ai.owner_funded_inference_enabled') === true;
        $r[] = ['AI kill switch', $ai ? $fail : 'pass', $ai ? 'CIVIO_OWNER_FUNDED_AI=true; must stay closed' : 'closed'];

        $guest = config('civio.guest_unlimited') === true;
        $r[] = ['Guest unlimited', $guest ? $fail : 'pass', $guest ? 'CIVIO_GUEST_UNLIMITED=true removes the free-attempt wall' : 'off'];

        return $r;
    }

    public function handle(): int
    {
        $production = app()->isProduction() || (bool) $this->option('production');
        $results = self::results($production);

        $this->table(['Check', 'Status', 'Detail'], array_map(fn (array $row): array => [$row[0], strtoupper($row[1]), $row[2]], $results));

        $failed = count(array_filter($results, fn (array $row): bool => $row[1] === 'fail'));
        $warned = count(array_filter($results, fn (array $row): bool => $row[1] === 'warn'));

        if ($failed > 0) {
            $this->error("Launch check failed: {$failed} failure(s), {$warned} warning(s).");

            return self::FAILURE;
        }

        $this->info("Launch check passed with {$warned} warning(s).");

        return self::SUCCESS;
    }
}
