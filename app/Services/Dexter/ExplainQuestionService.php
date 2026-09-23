<?php

declare(strict_types=1);

namespace App\Services\Dexter;

use Illuminate\Support\Facades\Http;
use Throwable;

class ExplainQuestionService
{
    /**
     * @param  array<string, mixed>  $payload
     * @return array{eli5: string, why_right: string, why_wrong: string, tip: string, citation: ?string, provider: string, notice?: string}
     */
    public function explain(array $payload): array
    {
        $provider = strtolower((string) config('civio.explain_provider', 'stub'));
        $key = trim((string) config('civio.explain_api_key', ''));

        if ($provider === '' || $provider === 'stub' || $key === '') {
            return $this->stub($payload);
        }

        try {
            $live = $this->fromProvider($provider, $key, $payload);
            if ($live !== null) {
                return $live;
            }
        } catch (Throwable) {
            // Fall through to the offline explainer.
        }

        $fallback = $this->stub($payload);
        $fallback['notice'] = 'Dexter used the offline explainer because the tutor provider did not respond.';

        return $fallback;
    }

    /**
     * @param  array<string, mixed>  $payload
     * @return array{eli5: string, why_right: string, why_wrong: string, tip: string, citation: ?string, provider: string}
     */
    public function stub(array $payload): array
    {
        $options = array_values(is_array($payload['options'] ?? null) ? $payload['options'] : []);
        $correctIndex = (int) ($payload['correct_index'] ?? 0);
        $chosenIndex = $payload['chosen_index'] ?? null;
        $correctText = (string) ($options[$correctIndex] ?? 'the keyed choice');
        $chosenText = is_numeric($chosenIndex) && isset($options[(int) $chosenIndex])
            ? (string) $options[(int) $chosenIndex]
            : null;
        $isRight = is_numeric($chosenIndex) && (int) $chosenIndex === $correctIndex;
        $bank = $this->plain((string) ($payload['explanation'] ?? ''));
        $citation = $this->citation($payload);

        $eli5 = $isRight
            ? "You picked the right one. In plain words, \"{$correctText}\" is the choice that fits."
            : "The question wants one best choice. The right pick is \"{$correctText}\".";

        if ($bank !== '') {
            $eli5 .= ' '.$bank;
        }

        $whyWrong = 'The other choices miss the idea the question is testing.';
        if (! $isRight && $chosenText !== null) {
            $whyWrong = "\"{$chosenText}\" does not fit as well as \"{$correctText}\".";
        }

        return [
            'eli5' => $eli5,
            'why_right' => $bank !== '' ? $bank : "\"{$correctText}\" matches what the question is asking.",
            'why_wrong' => $whyWrong,
            'tip' => 'Cover the choices, say the idea in your own words, then match one choice.',
            'citation' => $citation,
            'provider' => 'stub',
        ];
    }

    /**
     * @param  array<string, mixed>  $payload
     * @return array{eli5: string, why_right: string, why_wrong: string, tip: string, citation: ?string, provider: string}|null
     */
    private function fromProvider(string $provider, string $key, array $payload): ?array
    {
        $tutor = (string) config('civio.tutor_name', 'Dexter');
        $system = <<<PROMPT
You are {$tutor}, the study tutor inside CIVIO. Explain one practice question for a Philippine civil service examinee.
Return ONLY JSON with keys eli5, why_right, why_wrong, tip, citation.
eli5 is plain language. why_right says why the correct choice fits. why_wrong says why the chosen choice fails, or why the distractors fail if the chosen choice is correct.
tip is one short study move. citation is a Constitution article or Republic Act number only when the question is actually about that law, otherwise null.
Never claim this is an official CSC or CSDEx item. Never invent a statute.
PROMPT;

        $user = json_encode([
            'stem' => $payload['stem'] ?? '',
            'options' => $payload['options'] ?? [],
            'chosen_index' => $payload['chosen_index'] ?? null,
            'correct_index' => $payload['correct_index'] ?? null,
            'bank_explanation' => $payload['explanation'] ?? null,
            'category' => $payload['category'] ?? null,
            'subcategory' => $payload['subcategory'] ?? null,
        ], JSON_UNESCAPED_UNICODE);

        $text = $provider === 'gemini'
            ? $this->callGemini($key, $system, (string) $user)
            : $this->callChat($provider, $key, $system, (string) $user);

        if ($text === null || trim($text) === '') {
            return null;
        }

        $parsed = $this->decodeJson($text);
        if (! is_array($parsed) || ! isset($parsed['eli5'])) {
            return null;
        }

        return [
            'eli5' => $this->plain((string) $parsed['eli5']),
            'why_right' => $this->plain((string) ($parsed['why_right'] ?? '')),
            'why_wrong' => $this->plain((string) ($parsed['why_wrong'] ?? '')),
            'tip' => $this->plain((string) ($parsed['tip'] ?? '')),
            'citation' => $this->nullableString($parsed['citation'] ?? null),
            'provider' => $provider,
        ];
    }

    private function callChat(string $provider, string $key, string $system, string $user): ?string
    {
        $url = match ($provider) {
            'groq' => 'https://api.groq.com/openai/v1/chat/completions',
            'openai' => 'https://api.openai.com/v1/chat/completions',
            'xai' => 'https://api.x.ai/v1/chat/completions',
            default => (string) config('civio.explain_base_url', ''),
        };

        if ($url === '') {
            return null;
        }

        $model = (string) (config('civio.explain_model') ?: match ($provider) {
            'groq' => 'llama-3.3-70b-versatile',
            'xai' => 'grok-3-mini',
            default => 'gpt-4o-mini',
        });

        $response = Http::withToken($key)
            ->timeout(25)
            ->acceptJson()
            ->post($url, [
                'model' => $model,
                'temperature' => 0.2,
                'messages' => [
                    ['role' => 'system', 'content' => $system],
                    ['role' => 'user', 'content' => $user],
                ],
            ]);

        if (! $response->successful()) {
            return null;
        }

        return $response->json('choices.0.message.content');
    }

    private function callGemini(string $key, string $system, string $user): ?string
    {
        $model = (string) (config('civio.explain_model') ?: 'gemini-2.0-flash');
        $url = "https://generativelanguage.googleapis.com/v1beta/models/{$model}:generateContent";

        $response = Http::timeout(25)
            ->acceptJson()
            ->post($url.'?key='.urlencode($key), [
                'contents' => [
                    ['role' => 'user', 'parts' => [['text' => $system."\n\n".$user]]],
                ],
            ]);

        if (! $response->successful()) {
            return null;
        }

        return $response->json('candidates.0.content.parts.0.text');
    }

    /**
     * @return array<string, mixed>|null
     */
    private function decodeJson(string $text): ?array
    {
        $cleaned = trim($text);
        if (str_starts_with($cleaned, '```')) {
            $cleaned = (string) preg_replace('/^```(?:json)?\s*|\s*```$/', '', $cleaned);
        }

        $decoded = json_decode(trim($cleaned), true);

        return is_array($decoded) ? $decoded : null;
    }

    private function plain(string $text): string
    {
        $text = trim(strip_tags($text));
        $text = (string) preg_replace('/\s+/u', ' ', $text);

        return trim($text);
    }

    private function nullableString(mixed $value): ?string
    {
        if (! is_string($value)) {
            return null;
        }

        $value = trim($value);

        return $value === '' || strtolower($value) === 'null' ? null : $value;
    }

    /**
     * @param  array<string, mixed>  $payload
     */
    private function citation(array $payload): ?string
    {
        $haystack = implode(' ', [
            (string) ($payload['stem'] ?? ''),
            (string) ($payload['subcategory'] ?? ''),
            (string) ($payload['explanation'] ?? ''),
            implode(' ', is_array($payload['options'] ?? null) ? $payload['options'] : []),
        ]);

        if (preg_match('/\b(R\.?\s*A\.?\s*\d+|Republic Act\s+\d+)\b/i', $haystack, $match) === 1) {
            return trim((string) preg_replace('/\s+/', ' ', $match[1]));
        }

        if (preg_match('/\bArticle\s+([IVXLC]+|\d+)\b/i', $haystack, $match) === 1) {
            return 'Article '.strtoupper($match[1]).' of the 1987 Constitution';
        }

        if (preg_match('/\bConstitution\b/i', $haystack) === 1) {
            return '1987 Constitution of the Philippines';
        }

        return null;
    }
}
