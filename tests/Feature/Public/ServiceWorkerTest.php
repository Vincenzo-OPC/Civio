<?php

use Illuminate\Support\Facades\File;

test('the service worker is served from the site root with root scope and no long cache', function () {
    $path = public_path('build/sw.js');
    $existed = is_file($path);
    $original = $existed ? File::get($path) : null;

    File::ensureDirectoryExists(dirname($path));
    File::put($path, 'self.addEventListener("fetch", () => {});');

    try {
        $response = $this->get('/sw.js')->assertOk();

        expect($response->headers->get('Service-Worker-Allowed'))->toBe('/')
            ->and($response->headers->get('Content-Type'))->toContain('javascript')
            ->and($response->headers->get('Cache-Control'))->toContain('no-cache')
            ->and($response->headers->get('Cache-Control'))->not->toContain('immutable');
    } finally {
        $existed ? File::put($path, (string) $original) : File::delete($path);
    }
});
