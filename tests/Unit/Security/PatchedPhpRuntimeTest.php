<?php

// Regression guard for CVE-2026-109618 / CVE-2026-109619.

function civioRepoFile(string $path): string
{
    return file_get_contents(dirname(__DIR__, 3).'/'.$path);
}

function civioPhpGuard(string $version): int
{
    $script = dirname(__DIR__, 3).'/scripts/security/assert-patched-php.php';
    exec(escapeshellarg(PHP_BINARY).' '.escapeshellarg($script).' '.escapeshellarg($version).' 2>&1', $out, $code);

    return $code;
}

it('runs the test suite on a patched PHP', function () {
    $min = (require dirname(__DIR__, 3).'/scripts/security/patched-php-minimums.php')[PHP_MAJOR_VERSION.'.'.PHP_MINOR_VERSION] ?? null;

    expect($min)->not->toBeNull()
        ->and(version_compare(PHP_VERSION, $min, '>='))->toBeTrue();
});

it('rejects vulnerable and unsupported versions and accepts patched ones', function (string $version, int $expected) {
    expect(civioPhpGuard($version))->toBe($expected);
})->with([
    ['8.4.26', 1], ['8.5.11', 1], ['8.3.35', 1], ['8.2.34', 1], ['8.1.99', 1], ['7.4.33', 1],
    ['8.4.27', 0], ['8.5.12', 0], ['8.3.36', 0], ['8.2.35', 0], ['8.4.30', 0],
]);

it('pins the Docker base image to a patched PHP tag and a digest', function () {
    $dockerfile = civioRepoFile('Dockerfile');

    preg_match('/^ARG PHP_BASE_IMAGE=serversideup\/php:(\d+\.\d+\.\d+)-fpm-nginx[^@\s]*@sha256:[0-9a-f]{64}$/m', $dockerfile, $m);
    expect($m)->not->toBeEmpty('Dockerfile must pin serversideup/php to an exact X.Y.Z tag and digest.')
        ->and(civioPhpGuard($m[1]))->toBe(0)
        ->and($dockerfile)->toContain('FROM ${PHP_BASE_IMAGE}')
        ->and($dockerfile)->toContain('RUN php /tmp/php-guard/assert-patched-php.php')
        ->and(preg_match('/^FROM serversideup\/php:\d+\.\d+-/m', $dockerfile))->toBe(0);
});

it('asserts the patched PHP in every CI job that sets up PHP', function (string $workflow) {
    $yaml = civioRepoFile('.github/workflows/'.$workflow);

    expect($yaml)->toContain('php scripts/security/assert-patched-php.php');
})->with(['tests.yml', 'lint.yml']);
