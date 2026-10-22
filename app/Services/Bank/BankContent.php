<?php

declare(strict_types=1);

namespace App\Services\Bank;

use App\Models\Question;
use RuntimeException;

final class BankContent
{
    public static function digest(array $value): string
    {
        $sort = function (array $data) use (&$sort): array {
            if (! array_is_list($data)) {
                ksort($data);
            }
            foreach ($data as &$entry) {
                if (is_array($entry)) {
                    $entry = $sort($entry);
                }
            }

            return $data;
        };

        return hash('sha256', json_encode($sort($value), JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    }

    public static function itemDigest(array $item): string
    {
        // Editorial labels and spec tags (fact_id, theme) may change after review;
        // content never changes in place. The question fingerprint excludes the tags too.
        return self::digest(array_diff_key($item, array_flip([
            'status', 'review_status', 'reviewer', 'reviewed_at', 'approved_by', 'approved_at',
            'fact_id', 'theme',
        ])));
    }

    public static function fingerprint(Question $question): string
    {
        $question->load('subcategory.category');

        return self::digest([
            'category' => $question->subcategory->category->name,
            'subcategory' => $question->subcategory->name,
            'language' => $question->language,
            'stem' => $question->stem,
            'options' => $question->options,
            'correct_option' => $question->correct_option,
            'explanation' => $question->explanation,
            'source_group' => $question->source_group->value,
        ]);
    }

    public static function text(mixed $value): bool
    {
        return is_string($value) && trim($value) !== '' && mb_check_encoding($value, 'UTF-8');
    }

    public static function validate(array $item): void
    {
        foreach (['id', 'stem', 'explanation', 'language'] as $field) {
            if (! self::text($item[$field] ?? null)) {
                throw new RuntimeException("Invalid {$field}.");
            }
        }
        if (! preg_match('/\A[A-Za-z0-9][A-Za-z0-9._:-]{0,190}\z/D', $item['id'])) {
            throw new RuntimeException('Invalid stable item identity.');
        }
        if (! in_array($item['language'], ['English', 'Filipino'], true)) {
            throw new RuntimeException('Invalid language.');
        }
        $options = $item['options'] ?? null;
        if (! is_array($options) || ! array_is_list($options) || count($options) !== 4) {
            throw new RuntimeException('Exactly four ordered options are required.');
        }
        $normalized = [];
        foreach ($options as $option) {
            if (! self::text($option)) {
                throw new RuntimeException('Options must be nonempty UTF-8 text.');
            }
            $normalized[] = mb_strtolower(trim((string) preg_replace('/\s+/u', ' ', $option)));
        }
        if (count(array_unique($normalized)) !== count($options)) {
            throw new RuntimeException('Options must be distinct after case/whitespace normalization.');
        }
        if (! is_int($item['correct_option'] ?? null) || $item['correct_option'] < 0 || $item['correct_option'] >= count($options)) {
            throw new RuntimeException('Invalid integer answer index.');
        }
    }
}
