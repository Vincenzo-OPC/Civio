<?php

declare(strict_types=1);

namespace App\Services\Ai;

use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

class AiGatewayService
{
    public const DEFAULT_WORKERS_AI_MODEL = '@cf/meta/llama-3.2-3b-instruct';

    public const FAST_WORKERS_AI_MODEL = '@cf/meta/llama-3.2-1b-instruct';

    public const DEFAULT_GEMINI_MODEL = 'gemini-3.7-flash';

    public const FALLBACK_GEMINI_MODEL = 'gemini-3.5-flash';

    /**
     * Determine if a given model identifier belongs to Cloudflare Workers AI.
     */
    public function isWorkersAiModel(string $model): bool
    {
        return str_starts_with($model, '@cf/')
            || str_starts_with($model, 'cf/')
            || str_contains($model, 'llama-3.2')
            || str_contains($model, 'deepseek');
    }

    /**
     * Resolve the REST endpoint for Cloudflare Workers AI.
     */
    public function resolveWorkersAiUrl(string $model): string
    {
        $accountId = (string) config('services.cloudflare.account_id');
        $normalizedModel = ltrim($model, '/');

        return "https://api.cloudflare.com/client/v4/accounts/{$accountId}/ai/run/{$normalizedModel}";
    }

    /**
     * Check whether Cloudflare AI Gateway is configured.
     */
    public function isAiGatewayConfigured(): bool
    {
        return ! empty(config('services.cloudflare.account_id'))
            && (! empty(config('services.cloudflare.ai_gateway_id')) || ! empty(config('services.cloudflare.ai_gateway.id')));
    }

    /**
     * Resolve the direct Google Generative Language endpoint for Gemini models.
     */
    public function resolveGeminiUrl(string $model): string
    {
        return "https://generativelanguage.googleapis.com/v1beta/models/{$model}:generateContent";
    }

    /**
     * Resolve the direct Groq API endpoint.
     */
    public function resolveGroqUrl(): string
    {
        return 'https://api.groq.com/openai/v1/chat/completions';
    }

    /**
     * Check whether Cloudflare Workers AI credentials are configured.
     */
    public function isWorkersAiConfigured(): bool
    {
        return (bool) (config('services.cloudflare.account_id') && config('services.cloudflare.api_token'));
    }

    /**
     * Check whether Google Gemini credentials are configured.
     */
    public function isGeminiConfigured(): bool
    {
        return (bool) config('services.gemini.key');
    }

    /**
     * Check whether any AI provider (Cloudflare Workers AI or Google Gemini) is configured.
     */
    public function isAiConfigured(): bool
    {
        return $this->isWorkersAiConfigured() || $this->isGeminiConfigured();
    }

    /**
     * Execute a text generation run against Cloudflare Workers AI.
     *
     * @param  array<string, mixed>  $payload
     * @return array{success: bool, text?: string, error?: string, status?: int}
     */
    public function runWorkersAi(string $model, array $payload, int $timeout = 180): array
    {
        $token = (string) config('services.cloudflare.api_token');
        if ($token === '') {
            return ['success' => false, 'error' => 'CLOUDFLARE_API_TOKEN is missing.'];
        }

        $url = $this->resolveWorkersAiUrl($model);
        $headers = [
            'Authorization' => "Bearer {$token}",
        ];

        $gatewayId = (string) (config('services.cloudflare.ai_gateway_id') ?: config('services.cloudflare.ai_gateway.id'));
        if ($gatewayId !== '') {
            $headers['cf-aig-gateway-id'] = $gatewayId;
        }

        try {
            /** @var Response $response */
            $response = Http::withHeaders($headers)
                ->timeout($timeout)
                ->post($url, $payload);

            if ($response->successful()) {
                $data = $response->json();
                $text = $data['result']['response'] ?? '';

                return [
                    'success' => true,
                    'text' => is_string($text) ? $text : json_encode($text),
                    'status' => $response->status(),
                ];
            }

            $errorBody = $response->json();
            $errorMessage = $errorBody['errors'][0]['message'] ?? $response->body();

            return [
                'success' => false,
                'error' => "Workers AI request failed with status {$response->status()}: {$errorMessage}",
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            return [
                'success' => false,
                'error' => "Workers AI Exception: {$e->getMessage()}",
            ];
        }
    }

    /**
     * Execute a generation run against Google Gemini API.
     *
     * @param  array<string, mixed>  $payload
     * @return array{success: bool, text?: string, error?: string, status?: int}
     */
    public function runGemini(string $model, array $payload, int $timeout = 300): array
    {
        $geminiKey = (string) config('services.gemini.key');
        if ($geminiKey === '') {
            return ['success' => false, 'error' => 'GEMINI_API_KEY is missing.'];
        }

        $url = $this->resolveGeminiUrl($model);

        try {
            /** @var Response $response */
            $response = Http::withHeaders([
                'x-goog-api-key' => $geminiKey,
                'Content-Type' => 'application/json',
            ])->timeout($timeout)->post($url, $payload);

            if ($response->successful()) {
                $data = $response->json();
                $text = $data['candidates'][0]['content']['parts'][0]['text'] ?? '';

                return [
                    'success' => true,
                    'text' => (string) $text,
                    'status' => $response->status(),
                ];
            }

            $errorBody = $response->json();
            $errorMessage = $errorBody['error']['message'] ?? $response->body();

            return [
                'success' => false,
                'error' => "Gemini API failed with status {$response->status()}: {$errorMessage}",
                'status' => $response->status(),
            ];
        } catch (\Throwable $e) {
            return [
                'success' => false,
                'error' => "Gemini Exception: {$e->getMessage()}",
            ];
        }
    }

    /**
     * Execute structured JSON generation using the appropriate provider driver.
     *
     * @param  array<string, mixed>|null  $responseSchema  Optional schema for Gemini native responseSchema
     * @return array{success: bool, data?: array<string, mixed>|list<mixed>, text?: string, error?: string}
     */
    public function generateStructuredJson(
        string $model,
        string $systemPrompt,
        string $userPrompt,
        ?array $responseSchema = null,
        int $timeout = 240
    ): array {
        $cleanJson = static function (string $text): ?array {
            $cleaned = trim($text);
            if (str_starts_with($cleaned, '```')) {
                $cleaned = (string) preg_replace('/^```(?:json)?\n?|```$/', '', $cleaned);
            }
            $cleaned = trim($cleaned);

            $decoded = json_decode($cleaned, true);

            return is_array($decoded) ? $decoded : null;
        };

        if ($this->isWorkersAiModel($model)) {
            $systemDirective = $systemPrompt."\n\nCRITICAL: You MUST reply ONLY with a valid JSON object or array. Do NOT wrap output in markdown code blocks, backticks, or any additional text.";

            $payload = [
                'messages' => [
                    ['role' => 'system', 'content' => $systemDirective],
                    ['role' => 'user', 'content' => $userPrompt],
                ],
                'max_tokens' => 4096,
                'temperature' => 0.7,
            ];

            $result = $this->runWorkersAi($model, $payload, $timeout);
            if (! $result['success']) {
                return $result;
            }

            $decoded = $cleanJson($result['text'] ?? '');
            if ($decoded === null) {
                return [
                    'success' => false,
                    'error' => 'Workers AI returned invalid JSON structure.',
                    'text' => $result['text'] ?? '',
                ];
            }

            return ['success' => true, 'data' => $decoded, 'text' => $result['text'] ?? ''];
        }

        // Gemini payload
        $payload = [
            'system_instruction' => [
                'parts' => [['text' => $systemPrompt]],
            ],
            'contents' => [
                [
                    'parts' => [['text' => $userPrompt]],
                ],
            ],
            'generationConfig' => [
                'temperature' => 0.7,
                'topP' => 0.9,
                'responseMimeType' => 'application/json',
            ],
        ];

        if ($responseSchema !== null) {
            $payload['generationConfig']['responseSchema'] = $responseSchema;
        }

        if (str_contains($model, 'thinking')) {
            $payload['generationConfig']['thinkingConfig'] = ['thinkingLevel' => 'high'];
        }

        $result = $this->runGemini($model, $payload, $timeout);
        if (! $result['success']) {
            return $result;
        }

        $decoded = $cleanJson($result['text'] ?? '');
        if ($decoded === null) {
            return [
                'success' => false,
                'error' => 'Gemini returned invalid JSON structure.',
                'text' => $result['text'] ?? '',
            ];
        }

        return ['success' => true, 'data' => $decoded, 'text' => $result['text'] ?? ''];
    }
}
