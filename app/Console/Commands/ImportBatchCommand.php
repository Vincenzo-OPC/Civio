<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionSourceGroup;
use App\Models\Category;
use App\Models\Question;
use App\Models\Subcategory;
use App\Services\Bank\BankApproval;
use App\Services\Bank\BankContent;
use App\Services\Bank\BankImportLedger;
use Illuminate\Console\Command;
use Illuminate\Support\Str;
use JsonException;
use RuntimeException;

class ImportBatchCommand extends Command
{
    protected $signature = 'civio:import-batch
        {path : Path to the batch JSON file}
        {--dry-run : Validate and report without saving}
        {--status=active : Status to save the items with: active or draft}
        {--approval= : GT-signed approval JSON; signature at PATH.sig}
        {--review-report= : Independent review report bound by the approval}';

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

    public function handle(BankApproval $approval): int
    {
        try {
            $manifest = BankApproval::read((string) $this->argument('path'));
            $batch = json_decode($manifest, true, 512, JSON_THROW_ON_ERROR);
            $items = is_array($batch) ? ($batch['items'] ?? null) : null;
            if (! is_array($items) || ! array_is_list($items) || $items === []) {
                throw new RuntimeException('Batch must contain a nonempty list of items.');
            }
            $status = (string) $this->option('status');
            if (! in_array($status, ['active', 'draft'], true)) {
                throw new RuntimeException('Status must be active or draft.');
            }
            $rows = [];
            foreach ($items as $item) {
                if (! is_array($item) || ($problem = self::problem($item)) !== null) {
                    throw new RuntimeException($problem ?? 'Invalid item object.');
                }
                if ($status === 'active' && (($item['status'] ?? null) !== 'approved' || ($item['review_status'] ?? null) !== 'passed')) {
                    throw new RuntimeException('active import requires status=approved and review_status=passed plus independent signed approval.');
                }
                $texts = array_column($item['options'], 'text', 'option_id');
                $row = [
                    'id' => $item['id'], 'stem' => $item['stem'],
                    'language' => ($item['language'] ?? 'en') === 'fil' ? 'Filipino' : 'English',
                    'options' => array_values($texts),
                    'correct_option' => array_search($item['answer_option_id'], array_keys($texts), true),
                    'explanation' => self::explanation($item, $texts),
                ];
                BankContent::validate($row);
                $rows[] = $row;
            }
            BankImportLedger::unique($rows);
            $dry = (bool) $this->option('dry-run');
            $created = BankImportLedger::transaction(function () use ($items, $rows, $status, $dry, $manifest, $approval): int {
                BankImportLedger::lock();
                $evidence = [];
                if ($status === 'active') {
                    $evidence = $approval->verify($manifest, 'import-batch-active', $this->option('approval'), $this->option('review-report'));
                }
                $plan = [];
                foreach ($items as $index => $item) {
                    // Preserve all content and grouping metadata; review labels may change after approval.
                    $existing = BankImportLedger::existing($item, 'import-batch', $status, $status === 'active');
                    if ($existing !== null && $existing->status->value === $status) {
                        continue;
                    }
                    if ($existing === null && BankImportLedger::collision($item['stem'])) {
                        throw new RuntimeException('Stem collision; existing rows cannot be adopted or overwritten.');
                    }
                    $plan[] = [$item, $rows[$index], $existing];
                }
                if (! $dry) {
                    foreach ($plan as [$item, $row, $existing]) {
                        $question = $existing ?? $this->insert($item, $row, $status);
                        if ($existing !== null) {
                            $question->update(['status' => $status]);
                        }
                        BankImportLedger::record($item, 'import-batch', $status, $manifest, $question, $evidence);
                    }
                    if ($plan !== []) {
                        BankImportLedger::invalidate();
                    }
                }

                return count($plan);
            });
            $this->info(($dry ? 'Validated' : 'Imported').' '.count($items)." item(s): {$created} inserted or promoted, ".(count($items) - $created).' unchanged.');

            return self::SUCCESS;
        } catch (JsonException|RuntimeException $exception) {
            $this->error($exception->getMessage());

            return self::FAILURE;
        }
    }

    public static function problem(array $item): ?string
    {
        foreach (['id', 'domain', 'competency', 'stem', 'answer_option_id'] as $field) {
            if (! BankContent::text($item[$field] ?? null)) {
                return "Invalid {$field}.";
            }
        }
        if (! isset(self::CATEGORIES[$item['domain']]) || ! in_array($item['language'] ?? 'en', ['en', 'fil'], true)) {
            return 'Unknown domain or language.';
        }
        if (! is_array($item['options'] ?? null) || ! array_is_list($item['options']) || count($item['options']) !== 4) {
            return 'Exactly four option objects are required.';
        }
        if (trim((string) preg_replace('/\\s*\\(.*\\)\\s*$/', '', $item['competency'])) === '') {
            return 'Competency must contain a name.';
        }
        $ids = [];
        foreach ($item['options'] as $option) {
            if (! is_array($option) || ! BankContent::text($option['option_id'] ?? null) || ! BankContent::text($option['text'] ?? null)) {
                return 'Invalid option object.';
            }
            $ids[] = $option['option_id'];
        }
        if (count(array_unique($ids)) !== 4 || ! in_array($item['answer_option_id'], $ids, true)) {
            return 'Option identities must be unique and contain the answer.';
        }
        $reveal = $item['reveal'] ?? null;
        if (! is_array($reveal) || ! BankContent::text($reveal['why_correct'] ?? null) || ! is_array($reveal['why_wrong'] ?? null)) {
            return 'A correct-answer explanation and distractor explanations are required.';
        }
        foreach ($ids as $id) {
            if ($id !== $item['answer_option_id'] && ! BankContent::text($reveal['why_wrong'][$id] ?? null)) {
                return 'Each distractor needs its own explanation.';
            }
        }
        foreach ($reveal['why_wrong'] as $id => $why) {
            if (! in_array($id, $ids, true) || ! BankContent::text($why)) {
                return 'Invalid distractor explanation.';
            }
        }
        foreach (['terms', 'shortcut'] as $field) {
            if (isset($reveal[$field]) && ! is_string($reveal[$field])) {
                return 'Reveal fields must be text.';
            }
        }
        foreach (['shortcut', 'source', 'source_url'] as $field) {
            if (isset($item[$field]) && ! is_string($item[$field])) {
                return 'Source and shortcut fields must be text.';
            }
        }

        return null;
    }

    private function insert(array $item, array $row, string $status): Question
    {
        $category = Category::firstOrCreate(
            ['name' => self::CATEGORIES[$item['domain']]],
            ['slug' => Str::slug(self::CATEGORIES[$item['domain']]), 'is_demographic' => false],
        );
        $subName = trim((string) preg_replace('/\\s*\\(.*\\)\\s*$/', '', $item['competency']));
        $slug = Str::slug($subName);
        $slug = Subcategory::query()->where('slug', $slug)->where('category_id', '!=', $category->id)->exists()
            ? Str::slug($category->name.' '.$subName) : $slug;
        $subcategory = Subcategory::firstOrCreate(
            ['category_id' => $category->id, 'name' => $subName], ['slug' => $slug],
        );

        $texts = array_column($item['options'], 'text', 'option_id');
        $correct = array_search($item['answer_option_id'], array_keys($texts), true);

        $values = [
            'subcategory_id' => $subcategory->id,
            'language' => ($item['language'] ?? 'en') === 'fil' ? 'Filipino' : 'English',
            'options' => array_values($texts),
            'correct_option' => (int) $correct,
            'explanation' => self::explanation($item, $texts),
            'status' => $status,
        ];

        // Spec tags. Saved only when the file carries them, so re-importing an
        // untagged twin never clears a tag another batch set.
        foreach (['fact_id', 'theme'] as $tag) {
            $value = trim((string) ($item[$tag] ?? ''));

            if ($value !== '') {
                $values[$tag] = mb_substr($value, 0, 100);
            }
        }

        return Question::updateOrCreate(
            ['source_group' => QuestionSourceGroup::Civio->value, 'stem' => $item['stem']],
            $values,
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

        // Optional item-level shortcut (spec 0.1.7): one short, honest technique. When present it leads,
        // and the Reveal's worked method follows under its own label, so the Reveal UI needs no change.
        if (! empty($item['shortcut'])) {
            $lines[] = 'Shortcut: '.$item['shortcut'];

            if (! empty($r['shortcut'])) {
                $lines[] = 'Method: '.$r['shortcut'];
            }
        } elseif (! empty($r['shortcut'])) {
            $lines[] = 'Shortcut: '.$r['shortcut'];
        }
        $lines[] = 'Why it is right: '.$r['why_correct'];
        $lines[] = 'Why the others are wrong:';

        foreach ((array) $r['why_wrong'] as $optionId => $why) {
            $lines[] = '- '.($texts[$optionId] ?? $optionId).': '.$why;
        }

        $lines[] = 'Source: '.($item['source'] ?? 'Original, Civio').(! empty($item['source_url']) ? ' ('.$item['source_url'].')' : '');

        return implode("\n", $lines);
    }
}
