<?php

namespace App\Rules;

use App\Services\Ai\AiGatewayService;
use Closure;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Translation\PotentiallyTranslatedString;

class NoProfanity implements ValidationRule
{
    /**
     * Common vulgar / inappropriate terms for zero-latency local checks.
     *
     * @var array<int, string>
     */
    protected array $badWords = [
        'fuck', 'shit', 'asshole', 'bitch', 'bastard', 'cunt', 'dick', 'pussy', 'whore',
        'puta', 'gago', 'tanga', 'bobo', 'pakshet', 'tangina', 'putangina', 'hudas', 'ulol', 'siraulo',
        'tite', 'puke', 'kantot', 'jakol', 'pekpek', 'suso',
    ];

    /**
     * Run the validation rule.
     *
     * @param  Closure(string): PotentiallyTranslatedString  $fail
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! is_string($value)) {
            return;
        }

        $trimmedValue = trim($value);
        if ($trimmedValue === '') {
            return;
        }

        $lowerValue = strtolower($trimmedValue);

        // 1. Fast local dictionary check (Zero neurons burned)
        foreach ($this->badWords as $word) {
            if (preg_match('/\b'.preg_quote($word, '/').'\b/i', $lowerValue)) {
                Log::info("NoProfanity: Input '{$trimmedValue}' was FLAGGED by local dictionary word: '{$word}'.");
                $fail('The :attribute field contains inappropriate language.');

                return;
            }
        }

        // 2. Cache check for verified clean inputs (Zero neurons burned across repeating inputs)
        $cacheKey = 'profanity_clean:'.md5($lowerValue);
        if (Cache::get($cacheKey) === true) {
            return;
        }

        // 3. Try checking using Cloudflare Workers AI (Llama 3.2 1B via AI Gateway or direct)
        $aiGateway = app(AiGatewayService::class);
        if ($aiGateway->isWorkersAiConfigured()) {
            $ip = request()->ip() ?: 'unknown';
            $limiterKey = 'cf-profanity-check:'.$ip;

            if (! RateLimiter::tooManyAttempts($limiterKey, 30)) {
                RateLimiter::hit($limiterKey, 60);
                try {
                    $systemPrompt = 'You are a strict content moderator for a Philippine civil service exam platform. Analyze the input text for any profanity, vulgarity, offensive language, hate speech, inappropriate slurs, sexual/anatomical slang, and crude colloquial terms in English or Tagalog/Filipino. Respond strictly in JSON format matching this schema: {"inappropriate": boolean}';

                    $res = $aiGateway->runWorkersAi(AiGatewayService::FAST_WORKERS_AI_MODEL, [
                        'messages' => [
                            ['role' => 'system', 'content' => $systemPrompt],
                            ['role' => 'user', 'content' => $trimmedValue],
                        ],
                        'max_tokens' => 50,
                        'temperature' => 0.0,
                    ], 3);

                    if ($res['success']) {
                        $cleaned = trim($res['text'] ?? '');
                        if (str_starts_with($cleaned, '```')) {
                            $cleaned = (string) preg_replace('/^```(?:json)?\n?|```$/', '', $cleaned);
                        }
                        $parsed = json_decode(trim($cleaned), true);
                        if (isset($parsed['inappropriate']) && $parsed['inappropriate'] === true) {
                            Log::info("NoProfanity: Input '{$trimmedValue}' was FLAGGED as inappropriate by Cloudflare AI.");
                            $fail('The :attribute field contains inappropriate language.');

                            return;
                        }

                        if (isset($parsed['inappropriate']) && $parsed['inappropriate'] === false) {
                            Log::info("NoProfanity: Input '{$trimmedValue}' was CLEANED by Cloudflare AI.");
                            Cache::put($cacheKey, true, now()->addHours(24));

                            return;
                        }
                    }
                } catch (\Throwable $e) {
                    Log::warning('NoProfanity Cloudflare AI check failed: '.$e->getMessage());
                }
            }
        }

        // 4. Fallback to Groq API (NLP) - Direct API
        $groqKey = config('services.groq.key') ?: env('GROQ_API_KEY');
        if ($groqKey) {
            $ip = request()->ip() ?: 'unknown';
            $limiterKey = 'nlp-profanity-check:'.$ip;

            if (RateLimiter::tooManyAttempts($limiterKey, 10)) {
                Log::info("NoProfanity: NLP rate limit exceeded for IP {$ip}. Cleaned by local dictionary.");
                Cache::put($cacheKey, true, now()->addHours(24));

                return;
            }

            RateLimiter::hit($limiterKey, 60);
            Log::info("NoProfanity: Checking input '{$trimmedValue}' with Groq NLP for IP {$ip}");

            try {
                $model = 'llama-3.3-70b-versatile';
                $response = Http::withToken($groqKey)
                    ->timeout(3)
                    ->post('https://api.groq.com/openai/v1/chat/completions', [
                        'model' => $model,
                        'messages' => [
                            [
                                'role' => 'system',
                                'content' => 'You are a strict content moderator for a Philippine civil service exam platform. Analyze the input text for any profanity, vulgarity, offensive language, hate speech, inappropriate slurs, sexual/anatomical slang, and crude colloquial terms in English or Tagalog/Filipino. Respond strictly in JSON format matching this schema: {"inappropriate": boolean}',
                            ],
                            [
                                'role' => 'user',
                                'content' => $trimmedValue,
                            ],
                        ],
                        'temperature' => 0.0,
                        'response_format' => ['type' => 'json_object'],
                    ]);

                if ($response->successful()) {
                    $json = $response->json();
                    $text = $json['choices'][0]['message']['content'] ?? '';
                    $parsed = json_decode($text, true);

                    if (isset($parsed['inappropriate']) && $parsed['inappropriate'] === true) {
                        Log::info("NoProfanity: Input '{$trimmedValue}' was FLAGGED as inappropriate by Groq NLP.");
                        $fail('The :attribute field contains inappropriate language.');

                        return;
                    }

                    Log::info("NoProfanity: Input '{$trimmedValue}' was CLEANED by Groq NLP.");
                    Cache::put($cacheKey, true, now()->addHours(24));

                    return;
                }
            } catch (\Exception $e) {
                Log::warning('NoProfanity rule Groq NLP check failed: '.$e->getMessage());
            }
        }

        // Passed all checks - cache clean status
        Cache::put($cacheKey, true, now()->addHours(24));
    }
}
