<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionSourceGroup;
use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * Imports an approved Civio item batch (docs/batches/batch-NNN.json) as active
 * questions with source_group "civio". Idempotent: an item whose stem already
 * exists in the civio group is updated, never duplicated. New items are never
 * offline_eligible (only civio:mark-offline-eligible marks items), so they only
 * add to the mock pool and cannot break the offline caps.
 */
class ImportBatchCommand extends Command
{
    protected $signature = 'civio:import-batch
        {path : Path to the batch JSON file}
        {--dry-run : Validate and report without saving}';

    protected $description = 'Import an approved Civio item batch as active questions (idempotent)';

    /** Spec domain to bank category. */
    public const CATEGORIES = [
        'numerical' => 'Numerical Ability',
        'verbal_en' => 'Verbal Ability',
        'verbal_fil' => 'Verbal Ability',
        'analytical' => 'Analytical Ability',
        'clerical' => 'Clerical Ability',
        'general_information' => 'General Information',
    ];

    public function handle(): int
    {
        $path = (string) $this->argument('path');

        if (! is_file($path)) {
            $this->error("File not found: {$path}");

            return self::FAILURE;
        }

        $batch = json_decode((string) file_get_contents($path), true);
        $items = is_array($batch) ? ($batch['items'] ?? null) : null;

        if (! is_array($items) || $items === []) {
            $this->error('No items in the batch file.');

            return self::FAILURE;
        }

        foreach ($items as $i => $item) {
            if ($problem = self::problem($item)) {
                $this->error('Item '.($i + 1)." ({$item['id']}): {$problem}");

                return self::FAILURE;
            }
        }

        $created = 0;
        $updated = 0;

        if (! $this->option('dry-run')) {
            DB::transaction(function () use ($items, &$created, &$updated): void {
                foreach ($items as $item) {
                    $question = $this->upsert($item);
                    $question->wasRecentlyCreated ? $created++ : $updated++;
                }
            });
            Cache::forget('questions.active');
        }

        $verb = $this->option('dry-run') ? 'Validated' : 'Imported';
        $this->info("{$verb} ".count($items)." item(s): {$created} created, {$updated} updated.");

        return self::SUCCESS;
    }

    /** @param array<string, mixed> $item */
    public static function problem(array $item): ?string
    {
        foreach (['id', 'domain', 'competency', 'stem', 'options', 'answer_option_id', 'reveal'] as $key) {
            if (empty($item[$key])) {
                return "missing {$key}";
            }
        }

        if (! isset(self::CATEGORIES[$item['domain']])) {
            return "unknown domain {$item['domain']}";
        }

        if (count($item['options']) !== 4) {
            return 'needs exactly 4 options';
        }

        if (! in_array($item['answer_option_id'], array_column($item['options'], 'option_id'), true)) {
            return 'answer_option_id is not one of the options';
        }

        return null;
    }

    /** @param array<string, mixed> $item */
    private function upsert(array $item): Question
    {
        $category = Category::firstOrCreate(
            ['name' => self::CATEGORIES[$item['domain']]],
            ['slug' => Str::slug(self::CATEGORIES[$item['domain']]), 'is_demographic' => false],
        );
        $subName = trim((string) preg_replace('/\s*\(.*\)\s*$/', '', (string) $item['competency']));
        $slug = Str::slug($subName);
        $slug = Subcategory::query()->where('slug', $slug)->where('category_id', '!=', $category->id)->exists()
            ? Str::slug($category->name.' '.$subName)
            : $slug;
        $subcategory = Subcategory::firstOrCreate(
            ['category_id' => $category->id, 'name' => $subName],
            ['slug' => $slug],
        );

        $texts = array_column($item['options'], 'text', 'option_id');
        $correct = array_search($item['answer_option_id'], array_keys($texts), true);

        return Question::updateOrCreate(
            ['source_group' => QuestionSourceGroup::Civio->value, 'stem' => $item['stem']],
            [
                'subcategory_id' => $subcategory->id,
                'language' => ($item['language'] ?? 'en') === 'fil' ? 'Filipino' : 'English',
                'options' => array_values($texts),
                'correct_option' => (int) $correct,
                'explanation' => self::explanation($item, $texts),
                'status' => 'active',
            ],
        );
    }

    /**
     * Reveal text in spec order. Choices are named by content, never by letter.
     *
     * @param  array<string, mixed>  $item
     * @param  array<string, string>  $texts
     */
    public static function explanation(array $item, array $texts): string
    {
        $r = $item['reveal'];
        $lines = [];

        if (! empty($r['terms'])) {
            $lines[] = 'Meaning: '.$r['terms'];
        }

        $lines[] = 'Shortcut: '.$r['shortcut'];
        $lines[] = 'Why it is right: '.$r['why_correct'];
        $lines[] = 'Why the others are wrong:';

        foreach ((array) $r['why_wrong'] as $optionId => $why) {
            $lines[] = '- '.($texts[$optionId] ?? $optionId).': '.$why;
        }

        $lines[] = 'Source: '.($item['source'] ?? 'Original, Civio').(! empty($item['source_url']) ? ' ('.$item['source_url'].')' : '');

        return implode("\n", $lines);
    }
}
