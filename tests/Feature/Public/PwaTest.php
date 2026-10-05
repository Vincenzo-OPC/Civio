<?php

use Illuminate\Support\Facades\File;

test('pwa manifest exists and is branded Civio', function () {
    $manifestPath = public_path('manifest.json');

    expect(File::exists($manifestPath))->toBeTrue();

    $manifestJson = json_decode(File::get($manifestPath), true);

    expect($manifestJson)->toBeArray();
    expect($manifestJson['name'])->toBe('Civio');
    expect($manifestJson['short_name'])->toBe('Civio');
    expect($manifestJson['display'])->toBe('standalone');
    expect($manifestJson)->toHaveKey('id');
});

test('service worker source excludes exam and auth routes from caching', function () {
    $swSource = File::get(resource_path('js/sw.ts'));

    expect($swSource)->toContain('/exams');
    expect($swSource)->toContain('/dashboard');
    expect($swSource)->toContain('/settings');
    expect($swSource)->toContain('/admin');
    expect($swSource)->toContain('/sanctum');
    expect($swSource)->toContain('NetworkOnly');
    expect($swSource)->toContain('NetworkFirst');
});

test('pwa meta tags are present in the app layout html', function () {
    $response = $this->withoutVite()->get(route('home'));

    $response->assertOk();
    $response->assertSee('link rel="manifest" href="/manifest.json"', false);
    $response->assertSee('meta name="theme-color" content="#0f172a"', false);
    $response->assertSee('meta name="apple-mobile-web-app-capable" content="yes"', false);
});
