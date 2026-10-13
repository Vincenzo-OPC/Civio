<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionSourceGroup;
use App\Enums\QuestionStatus;
use App\Models\Question;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use JsonException;

/**
 * Insert re-parameterized copies of baseline items and draft the originals.
 *
 * Matches on the exact prior stem, so it can run on a database whose ids
 * differ from the snapshot used to build the file. Idempotent.
 */
class ReparameterizeBaselineCommand extends Command
{
    protected $signature = 'civio:reparameterize-baseline
        {--dry-run : Report what would change without saving}
        {--path= : JSON file of replacement items}';

    protected $description = 'Replace baseline practice items with re-parameterized Civio items and draft the originals';

    public function handle(): int
    {
        $path = $this->option('path') ?: base_path('scripts/seeds/baseline_reparameterized.json');

        if (! is_string($path) || ! is_file($path)) {
            $this->error('Replacement file not found.');

            return self::FAILURE;
        }

        try {
            $rows = json_decode((string) file_get_contents($path), true, 512, JSON_THROW_ON_ERROR);
        } catch (JsonException $exception) {
            $this->error('Replacement file is not valid JSON: '.$exception->getMessage());

            return self::FAILURE;
        }

        if (! is_array($rows)) {
            $this->error('Replacement file must be a list of items.');

            return self::FAILURE;
        }

        $dryRun = (bool) $this->option('dry-run');
        $inserted = 0;
        $updated = 0;
        $drafted = 0;
        $skipped = 0;

        $apply = function () use ($rows, $dryRun, &$inserted, &$updated, &$drafted, &$skipped): void {
            foreach ($rows as $row) {
                if (! is_array($row) || ! isset($row['prior_stem'], $row['stem'], $row['options'], $row['correct_option'], $row['explanation'])) {
                    $skipped++;

                    continue;
                }

                $old = Question::query()->where('stem', $row['prior_stem'])->first();

                if ($old === null) {
                    $skipped++;

                    continue;
                }

                $existing = Question::query()->where('stem', $row['stem'])->first();

                if ($existing !== null) {
                    $isOwnReplacement = (int) $existing->replaces_question_id === (int) $old->id;

                    if ($isOwnReplacement) {
                        $changed = $existing->explanation !== $row['explanation']
                            || $existing->options !== $row['options']
                            || (int) $existing->correct_option !== (int) $row['correct_option'];

                        if ($changed && ! $dryRun) {
                            $existing->options = $row['options'];
                            $existing->correct_option = (int) $row['correct_option'];
                            $existing->explanation = $row['explanation'];
                            $existing->save();
                        }

                        if ($changed) {
                            $updated++;
                        } else {
                            $skipped++;
                        }

                        if ($old->status === QuestionStatus::Active) {
                            if (! $dryRun) {
                                $old->status = QuestionStatus::Draft;
                                $old->save();
                            }
                            $drafted++;
                        }
                    } else {
                        $skipped++;
                    }

                    continue;
                }

                if (! $dryRun) {
                    Question::query()->create([
                        'subcategory_id' => $old->subcategory_id,
                        'language' => is_string($row['language'] ?? null) ? $row['language'] : $old->language,
                        'stem' => $row['stem'],
                        'options' => $row['options'],
                        'correct_option' => (int) $row['correct_option'],
                        'explanation' => $row['explanation'],
                        'status' => QuestionStatus::Active,
                        'created_by' => $old->created_by,
                        'source_group' => QuestionSourceGroup::Civio,
                        'replaces_question_id' => $old->id,
                        'offline_eligible' => false,
                    ]);

                    $old->status = QuestionStatus::Draft;
                    $old->save();
                }

                $inserted++;
                $drafted++;
            }
        };

        if ($dryRun) {
            $apply();
        } else {
            DB::transaction($apply);
            Cache::forget('questions.all');
            Cache::forget('questions.active');
            Cache::forget('categories.tree');
        }

        $this->info("Inserted: {$inserted}, updated: {$updated}, drafted: {$drafted}, skipped: {$skipped}.");

        return self::SUCCESS;
    }
}
