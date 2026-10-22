<?php

/*
 * Pest must never touch a real database or the browser E2E's throwaway file,
 * even when the shell exports DB_* variables. phpunit.xml forces these values.
 */
test('tests always run on in-memory SQLite, whatever the shell exports', function () {
    expect(config('database.default'))->toBe('sqlite')
        ->and(config('database.connections.sqlite.database'))->toBe(':memory:')
        ->and(config('database.connections.sqlite.url'))->toBeEmpty()
        ->and(config('session.driver'))->toBe('array')
        ->and(config('cache.default'))->toBe('array')
        ->and(app()->environment())->toBe('testing');
});
