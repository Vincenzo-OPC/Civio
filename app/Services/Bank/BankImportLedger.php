<?php

declare(strict_types=1);

namespace App\Services\Bank;

use App\Models\Question;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use RuntimeException;

final class BankImportLedger
{
    private static bool $importing = false;

    public static function importing(): bool
    {
        return self::$importing;
    }

    public static function transaction(callable $apply): mixed
    {
        return DB::transaction(function () use ($apply): mixed {
            self::$importing = true;
            try {
                return $apply();
            } finally {
                self::$importing = false;
            }
        });
    }

    public static function lock(): void
    {
        if (DB::table('bank_import_locks')->where('id', 1)->lockForUpdate()->first() === null) {
            throw new RuntimeException('Bank import lock is unavailable.');
        }
    }

    public static function existing(array $item, string $operation, string $status, bool $allowPromotion = false): ?Question
    {
        $entry = DB::table('bank_import_entries')->where('id', $item['id'])->first();
        if ($entry === null) {
            return null;
        }
        $question = Question::query()->lockForUpdate()->find($entry->question_id);
        $promotion = $allowPromotion && $entry->status === 'draft' && $status === 'active';
        if ($entry->operation !== $operation || $entry->digest !== BankContent::itemDigest($item)
            || (! $promotion && $entry->status !== $status) || $question === null
            || $question->status->value !== $entry->status
            || $entry->question_fingerprint !== BankContent::fingerprint($question)) {
            throw new RuntimeException('Existing revisions are immutable or have drifted; a separately reviewed revision is required.');
        }

        return $question;
    }

    public static function record(array $item, string $operation, string $status, string $manifest, Question $question, array $evidence = []): void
    {
        $values = [
            'id' => $item['id'], 'operation' => $operation, 'digest' => BankContent::itemDigest($item),
            'question_id' => $question->id, 'question_fingerprint' => BankContent::fingerprint($question),
            'manifest_sha256' => hash('sha256', $manifest), 'status' => $status, 'created_at' => now(), ...$evidence,
        ];
        $draft = DB::table('bank_import_entries')->where('id', $item['id'])->where('question_id', $question->id)->where('status', 'draft');
        if ($status === 'active' && $draft->exists()) {
            unset($values['created_at']);
            $draft->update($values);
        } else {
            DB::table('bank_import_entries')->insert($values);
        }
    }

    public static function invalidate(): void
    {
        DB::afterCommit(function (): void {
            foreach (['questions.all', 'questions.active', 'categories.tree'] as $key) {
                Cache::forget($key);
            }
        });
    }

    public static function collision(string $stem): bool
    {
        $normalize = fn (string $value): string => mb_strtolower(trim((string) preg_replace('/\\s+/u', ' ', $value)));
        $target = $normalize($stem);

        return Question::query()->pluck('stem')->contains(fn (string $existing): bool => $normalize($existing) === $target);
    }

    public static function unique(array $items): void
    {
        foreach (['id', 'stem'] as $field) {
            $values = array_map(fn (array $item): string => mb_strtolower(trim((string) preg_replace('/\s+/u', ' ', $item[$field]))), $items);
            if (count(array_unique($values)) !== count($values)) {
                throw new RuntimeException("Duplicate {$field} in manifest.");
            }
        }
    }
}
