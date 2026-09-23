<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use App\Support\QuestionStem;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;

class ImportQuestionsCommand extends Command
{
    protected $signature = 'questions:import
        {path : JSON array or CSV file of practice questions}
        {--user= : User id or email stored in questions.created_by}
        {--status=active : active or draft}';

    protected $description = 'Import paraphrased practice questions into the existing questions table';

    public function handle(): int
    {
        $path = (string) $this->argument('path');
        if (! is_file($path)) {
            $this->error("File not found: {$path}");

            return self::FAILURE;
        }

        $status = (string) $this->option('status');
        if (! in_array($status, ['active', 'draft'], true)) {
            $this->error('Status must be active or draft.');

            return self::FAILURE;
        }

        $user = $this->resolveUser();
        if (! $user) {
            $this->error('No user found for created_by. Pass --user= or create a user first.');

            return self::FAILURE;
        }

        $rows = $this->readRows($path);
        $seen = [];
        foreach (Question::query()->pluck('stem') as $existing) {
            $seen[QuestionStem::normalize((string) $existing)] = true;
        }

        $created = 0;
        $skipped = 0;

        foreach ($rows as $index => $row) {
            $stem = QuestionStem::withoutVariantSuffix((string) ($row['stem'] ?? ''));
            $normalized = QuestionStem::normalize($stem);
            $subcategoryName = trim((string) ($row['subcategory'] ?? $row['subcategory_name'] ?? ''));

            if ($stem === '' || $normalized === '' || $subcategoryName === '') {
                $this->warn('Row '.($index + 1).' skipped: stem and subcategory are required.');
                $skipped++;

                continue;
            }

            if (isset($seen[$normalized])) {
                $skipped++;

                continue;
            }

            $subcategory = Subcategory::query()->where('name', $subcategoryName)->first();
            if (! $subcategory && isset($row['subcategory_id'])) {
                $subcategory = Subcategory::query()->find($row['subcategory_id']);
            }

            if (! $subcategory) {
                $this->warn('Row '.($index + 1)." skipped: unknown subcategory \"{$subcategoryName}\".");
                $skipped++;

                continue;
            }

            $options = $this->optionsFor($row);
            if (count($options) < 2) {
                $this->warn('Row '.($index + 1).' skipped: at least two options are required.');
                $skipped++;

                continue;
            }

            $correct = $this->correctIndex($row, count($options));
            if ($correct === null) {
                $this->warn('Row '.($index + 1).' skipped: correct_option is missing or out of range.');
                $skipped++;

                continue;
            }

            Question::query()->create([
                'subcategory_id' => $subcategory->id,
                'language' => (string) ($row['language'] ?? 'English'),
                'stem' => $stem,
                'options' => $options,
                'correct_option' => $correct,
                'explanation' => (string) ($row['explanation'] ?? 'Practice paraphrase. Not an official CSC item.'),
                'status' => (string) ($row['status'] ?? $status),
                'created_by' => $user->id,
            ]);

            $seen[$normalized] = true;
            $created++;
        }

        Cache::forget('questions.active');
        Cache::forget('categories.tree');

        $this->info("Imported {$created} unique question(s). Skipped {$skipped}.");

        return self::SUCCESS;
    }

    private function resolveUser(): ?User
    {
        $needle = $this->option('user');
        if (is_string($needle) && $needle !== '') {
            if (ctype_digit($needle)) {
                return User::query()->find((int) $needle);
            }

            return User::query()->where('email', $needle)->first();
        }

        return User::query()->orderBy('id')->first();
    }

    /**
     * @return array<int, array<string, mixed>>
     */
    private function readRows(string $path): array
    {
        $extension = strtolower(pathinfo($path, PATHINFO_EXTENSION));
        if ($extension === 'json') {
            $decoded = json_decode((string) file_get_contents($path), true);
            if (! is_array($decoded)) {
                return [];
            }

            return array_is_list($decoded) ? $decoded : [$decoded];
        }

        $handle = fopen($path, 'rb');
        if ($handle === false) {
            return [];
        }

        $header = fgetcsv($handle);
        if (! is_array($header)) {
            fclose($handle);

            return [];
        }

        $header = array_map(fn ($column) => strtolower(trim((string) $column)), $header);
        $rows = [];
        while (($line = fgetcsv($handle)) !== false) {
            $row = [];
            foreach ($header as $i => $column) {
                $row[$column] = $line[$i] ?? null;
            }
            $rows[] = $row;
        }
        fclose($handle);

        return $rows;
    }

    /**
     * @param  array<string, mixed>  $row
     * @return array<int, string>
     */
    private function optionsFor(array $row): array
    {
        $raw = $row['options'] ?? null;
        if (is_string($raw) && $raw !== '') {
            $decoded = json_decode($raw, true);
            $raw = is_array($decoded) ? $decoded : null;
        }

        if (is_array($raw)) {
            return array_values(array_filter(array_map(
                fn ($option) => trim((string) $option),
                $raw
            ), fn ($option) => $option !== ''));
        }

        $options = [];
        foreach (['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'a', 'b', 'c', 'd', 'e'] as $key) {
            if (! array_key_exists($key, $row) || trim((string) $row[$key]) === '') {
                continue;
            }
            $options[] = trim((string) $row[$key]);
        }

        return $options;
    }

    /**
     * @param  array<string, mixed>  $row
     */
    private function correctIndex(array $row, int $count): ?int
    {
        $raw = $row['correct_option'] ?? $row['correct'] ?? $row['answer'] ?? null;
        if ($raw === null || $raw === '') {
            return null;
        }

        if (is_numeric($raw)) {
            $index = (int) $raw;

            return $index >= 0 && $index < $count ? $index : null;
        }

        $letter = strtoupper(trim((string) $raw));
        if (preg_match('/^[A-E]$/', $letter) === 1) {
            $index = ord($letter) - 65;

            return $index < $count ? $index : null;
        }

        return null;
    }
}
