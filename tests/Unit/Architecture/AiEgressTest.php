<?php

/*
 * Issue #18 architecture guard: app code may reach an AI host or an HTTP client
 * only through AiGatewayService, whose network methods must check the
 * owner-funded AI lock first. TurnstileService is the one non-AI HTTP user.
 */

const AI_GATEWAY_FILE = 'app/Services/Ai/AiGatewayService.php';

/** @return array<string, string> relative path => source */
function civioPhpSources(): array
{
    $root = dirname(__DIR__, 3);
    $out = [];
    foreach (['app', 'routes', 'bootstrap'] as $dir) {
        $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator("{$root}/{$dir}", FilesystemIterator::SKIP_DOTS));
        foreach ($it as $file) {
            if ($file->getExtension() === 'php' && ! str_contains($file->getPathname(), '/bootstrap/cache/')) {
                $out[substr($file->getPathname(), strlen($root) + 1)] = (string) file_get_contents($file->getPathname());
            }
        }
    }

    return $out;
}

test('no app code outside the gateway names a known AI host', function () {
    $hosts = '/(generativelanguage\.googleapis\.com|aiplatform\.googleapis\.com|api\.cloudflare\.com|\/ai\/run\/|gateway\.ai\.cloudflare\.com|api\.groq\.com|openrouter\.ai|api\.openai\.com|chatgpt\.com\/backend|api\.anthropic\.com|api\.x\.ai|api\.mistral\.ai|api-inference\.huggingface\.co|router\.huggingface\.co|api\.together\.xyz|api\.deepseek\.com|api\.cohere\.)/i';
    $offenders = [];
    foreach (civioPhpSources() as $path => $src) {
        if ($path !== AI_GATEWAY_FILE && preg_match($hosts, $src, $m)) {
            $offenders[] = "{$path}: {$m[0]}";
        }
    }

    expect($offenders)->toBe([]);
});

test('only the gateway and Turnstile use an HTTP client', function () {
    $client = '/(Facades\\\\Http\b|\bHttp::|GuzzleHttp|\bcurl_init\s*\(|\bcurl_exec\s*\(|\bfsockopen\s*\(|stream_socket_client\s*\(|file_get_contents\s*\(\s*[\'"]https?:|\bPrism\\\\|use\s+Prism\b|OpenAI\\\\Client|Gemini\\\\Client)/';
    $allowed = [AI_GATEWAY_FILE, 'app/Services/TurnstileService.php'];
    $offenders = [];
    foreach (civioPhpSources() as $path => $src) {
        $code = preg_replace('#^\s*(//|\*|/\*).*$#m', '', $src);
        if (! in_array($path, $allowed, true) && preg_match($client, (string) $code, $m)) {
            $offenders[] = "{$path}: {$m[0]}";
        }
    }

    expect($offenders)->toBe([]);
});

test('Turnstile only talks to the Turnstile verify endpoint', function () {
    $src = (string) file_get_contents(dirname(__DIR__, 3).'/app/Services/TurnstileService.php');
    preg_match_all('#https?://[^\'"\s]+#', $src, $m);

    expect(array_unique($m[0]))->toBe(['https://challenges.cloudflare.com/turnstile/v0/siteverify']);
});

test('every gateway method that sends HTTP checks the lock first', function () {
    $src = (string) file_get_contents(dirname(__DIR__, 3).'/'.AI_GATEWAY_FILE);
    preg_match_all('/public function (\w+)\([^)]*\)[^{]*\{(.*?)\n    \}/s', $src, $methods, PREG_SET_ORDER);

    $networkMethods = 0;
    foreach ($methods as [, $name, $body]) {
        if (! str_contains($body, 'Http::') && ! preg_match('/\$this->(run\w+)\(/', $body)) {
            continue;
        }
        $networkMethods++;
        $first = trim(strtok(ltrim($body), "\n"));
        expect($first)->toBe('if (OwnerAiSpendLock::disabled()) {', "{$name} must check the lock first");
    }

    expect($networkMethods)->toBeGreaterThanOrEqual(4);
});

test('no app code reads AI credentials straight from env()', function () {
    $offenders = [];
    foreach (civioPhpSources() as $path => $src) {
        if (preg_match('/env\(\s*[\'"](GEMINI|GROQ|CLOUDFLARE|OPENAI|XAI|OPENROUTER|ANTHROPIC|MISTRAL)[A-Z_]*[\'"]/', $src, $m)) {
            $offenders[] = "{$path}: {$m[0]}";
        }
    }

    expect($offenders)->toBe([]);
});
