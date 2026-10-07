<?php

use Symfony\Component\Process\ExecutableFinder;
use Symfony\Component\Process\Process;

/**
 * The inline <script> blocks in resources/views/app.blade.php are sent to the
 * browser as-is (no TypeScript build step). TypeScript-only syntax there makes
 * the whole block fail to parse, which used to break system dark-mode detection.
 */

/** @return list<string> inline (non-src, non-JSON) script bodies of the rendered page */
function inlineScripts(string $html): array
{
    preg_match_all('#<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>#s', $html, $matches, PREG_SET_ORDER);

    return array_values(array_map(
        fn (array $m): string => $m['body'],
        array_filter($matches, fn (array $m): bool => ! str_contains($m['attrs'], 'src=')
            && ! str_contains($m['attrs'], 'application/json')
            && trim($m['body']) !== ''),
    ));
}

function nodeBinary(): ?string
{
    return (new ExecutableFinder)->find('node');
}

/** Runs $code with node and returns trimmed stdout; fails the test on a non-zero exit. */
function runNode(string $code): string
{
    $file = tempnam(sys_get_temp_dir(), 'civio-inline-').'.js';
    file_put_contents($file, $code);

    try {
        $process = new Process([nodeBinary(), $file]);
        $process->run();
        expect($process->getExitCode())->toBe(0, $process->getErrorOutput());

        return trim($process->getOutput());
    } finally {
        @unlink($file);
    }
}

function darkModeHarness(string $script, bool $prefersDark): string
{
    $prefers = $prefersDark ? 'true' : 'false';

    return <<<JS
        const classes = new Set();
        globalThis.window = { matchMedia: () => ({ matches: {$prefers} }) };
        globalThis.document = { documentElement: { classList: { add: (c) => classes.add(c) } } };
        {$script}
        console.log(JSON.stringify([...classes]));
        JS;
}

test('rendered inline scripts contain no TypeScript-only syntax', function () {
    $scripts = inlineScripts($this->withoutVite()->get('/')->assertOk()->getContent());

    expect($scripts)->not->toBeEmpty();

    foreach ($scripts as $script) {
        // `x as Type`, `(e: Event)`, `foo!.bar`, `<Type>value` casts and type annotations on declarations.
        expect($script)
            ->not->toMatch('/\)\s+as\s+[A-Z]\w*/')
            ->not->toMatch('/\bas\s+(HTMLElement|KeyboardEvent|Event|MouseEvent|Element|any|unknown)\b/')
            ->not->toMatch('/\b(const|let|var)\s+\w+\s*:\s*[A-Za-z]/')
            ->not->toMatch('/\(\s*\w+\s*:\s*[A-Z]\w*\s*\)\s*=>/');
    }
});

test('rendered inline scripts pass node --check', function () {
    if (nodeBinary() === null) {
        $this->markTestSkipped('node is not installed.');
    }

    // Guard: the checker really rejects TypeScript casts.
    $bad = tempnam(sys_get_temp_dir(), 'civio-ts-').'.js';
    file_put_contents($bad, 'document.addEventListener("keydown", (e) => { (e as KeyboardEvent).key; });');
    $badCheck = new Process([nodeBinary(), '--check', $bad]);
    $badCheck->run();
    @unlink($bad);
    expect($badCheck->getExitCode())->not->toBe(0);

    foreach (inlineScripts($this->withoutVite()->get('/')->assertOk()->getContent()) as $script) {
        $file = tempnam(sys_get_temp_dir(), 'civio-inline-').'.js';
        file_put_contents($file, $script);
        $check = new Process([nodeBinary(), '--check', $file]);
        $check->run();
        @unlink($file);

        expect($check->getExitCode())->toBe(0, $check->getErrorOutput());
    }
});

test('system appearance follows prefers-color-scheme', function () {
    if (nodeBinary() === null) {
        $this->markTestSkipped('node is not installed.');
    }

    $scripts = inlineScripts($this->withoutVite()->get('/')->assertOk()->getContent());
    $darkScript = collect($scripts)->first(fn (string $s): bool => str_contains($s, 'prefers-color-scheme'));

    expect($darkScript)->not->toBeNull()
        ->and($darkScript)->toContain("var appearance = 'system'");

    expect(runNode(darkModeHarness($darkScript, true)))->toBe('["dark"]')
        ->and(runNode(darkModeHarness($darkScript, false)))->toBe('[]');
});

test('explicit appearance cookies set the html class on the server', function () {
    $dark = $this->withoutVite()->withUnencryptedCookie('appearance', 'dark')->get('/')->assertOk()->getContent();
    $light = $this->withoutVite()->withUnencryptedCookie('appearance', 'light')->get('/')->assertOk()->getContent();

    expect($dark)->toMatch('/<html[^>]*class="[^"]*\bdark\b/')
        ->and($light)->not->toMatch('/<html[^>]*class="[^"]*\bdark\b/');

    $lightScript = collect(inlineScripts($light))->first(fn (string $s): bool => str_contains($s, 'prefers-color-scheme'));
    expect($lightScript)->toContain("var appearance = 'light'");

    if (nodeBinary() !== null) {
        // An explicit light choice ignores a dark OS preference.
        expect(runNode(darkModeHarness($lightScript, true)))->toBe('[]');
    }
});

test('the exam copy override leaves keyboard events alone', function () {
    if (nodeBinary() === null) {
        $this->markTestSkipped('node is not installed.');
    }

    $scripts = inlineScripts($this->withoutVite()->get('/')->assertOk()->getContent());
    $override = collect($scripts)->first(fn (string $s): bool => str_contains($s, 'gt-selectable-override'));

    expect($override)->not->toBeNull();

    $harness = <<<JS
        const listened = [];
        const head = { appendChild: () => {} };
        globalThis.location = { pathname: '/exams/1', hostname: 'civio.example' };
        globalThis.setInterval = () => 0;
        globalThis.document = {
            head,
            getElementById: () => null,
            createElement: () => ({}),
            addEventListener: (type) => listened.push(type),
        };
        {$override}
        console.log(JSON.stringify(listened));
        JS;

    expect(json_decode(runNode($harness), true))->toBe(['copy', 'cut', 'contextmenu', 'selectstart']);
});
