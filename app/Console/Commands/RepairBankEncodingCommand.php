<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Models\Question;
use App\Support\Bank\EncodingArtifacts;
use App\Support\Bank\ReferenceTextIndex;
use Illuminate\Console\Command;

/**
 * Idempotent repair for "??" artifacts (lost × ÷ − √ ² ≤ ≥ ₱, curly quotes…)
 * in question stems, options and explanations. See EncodingArtifacts for the
 * root cause. Only exact matches against the original UTF-8 seed text, or
 * arithmetic with a single possible operator, are written. Everything else is
 * listed by ID for a human to fix.
 */
class RepairBankEncodingCommand extends Command
{
    protected $signature = 'civio:repair-bank-encoding
        {--dry-run : Report what would change without saving}
        {--reference=* : Extra UTF-8 reference files (.sql, .php or .json)}
        {--no-default-references : Skip the seed files under scripts/}';

    protected $description = 'Repair "??" encoding artifacts in question-bank text from the original UTF-8 seeds';

    public function handle(): int
    {
        $index = new ReferenceTextIndex;

        foreach ($this->referenceFiles() as $file) {
            $index->addFile($file);
        }

        $dryRun = (bool) $this->option('dry-run');
        $scanned = 0;
        $repairedIds = [];
        $unrepairedIds = [];

        Question::query()->orderBy('id')->chunkById(200, function ($questions) use ($index, $dryRun, &$scanned, &$repairedIds, &$unrepairedIds) {
            foreach ($questions as $question) {
                $scanned++;
                $changes = [];
                $stillBroken = false;

                foreach (['stem', 'explanation'] as $field) {
                    $value = $question->{$field};

                    if (! is_string($value) || $value === '') {
                        continue;
                    }

                    $fixed = $this->repairText($value, $index);

                    if ($fixed !== null && $fixed !== $value) {
                        $changes[$field] = $fixed;
                    }

                    if (EncodingArtifacts::hasArtifact($fixed ?? $value)) {
                        $stillBroken = true;
                    }
                }

                $options = $question->options;

                if (is_array($options)) {
                    $newOptions = $options;

                    foreach ($options as $i => $option) {
                        if (! is_string($option)) {
                            continue;
                        }

                        $fixed = $this->repairText($option, $index);

                        if ($fixed !== null) {
                            $newOptions[$i] = $fixed;
                        }
                    }

                    $optionsBroken = array_filter(
                        $newOptions,
                        fn ($o) => is_string($o) && EncodingArtifacts::hasArtifact($o),
                    ) !== [];

                    if ($optionsBroken) {
                        // Symbol-only options ("???") are ambiguous one by one;
                        // match the whole option list via the row's stem.
                        $stem = $changes['stem'] ?? (string) $question->stem;
                        $wholeRow = $index->lookupOptions($stem, $options);

                        if ($wholeRow !== null) {
                            $newOptions = $wholeRow;
                            $optionsBroken = false;
                        }
                    }

                    if ($optionsBroken) {
                        $stillBroken = true;
                    }

                    if ($newOptions !== $options) {
                        $changes['options'] = $newOptions;
                    }
                }

                if ($changes !== []) {
                    $repairedIds[] = $question->id;

                    if (! $dryRun) {
                        $question->forceFill($changes)->saveQuietly();
                    }
                }

                if ($stillBroken) {
                    $unrepairedIds[] = $question->id;
                }
            }
        });

        $this->info(sprintf(
            '%s %d question(s); scanned %d; reference strings %d.',
            $dryRun ? 'Would repair' : 'Repaired',
            count($repairedIds),
            $scanned,
            $index->sourceCount(),
        ));

        if ($repairedIds !== []) {
            $this->line('Repaired IDs: '.implode(', ', $repairedIds));
        }

        if ($unrepairedIds !== []) {
            $this->warn(sprintf(
                '%d question(s) still contain "??" and need a manual fix: %s',
                count($unrepairedIds),
                implode(', ', $unrepairedIds),
            ));
        } else {
            $this->info('No remaining "??" artifacts.');
        }

        return self::SUCCESS;
    }

    /**
     * Returns the repaired text, or null when no safe repair exists.
     * Partial repairs are not written: a field changes only when it ends up
     * free of artifacts (or exactly matches its original seed text).
     */
    private function repairText(string $value, ReferenceTextIndex $index): ?string
    {
        $original = $index->lookup($value);

        if ($original !== null) {
            return $original;
        }

        if (! EncodingArtifacts::hasArtifact($value)) {
            return null;
        }

        $inferred = EncodingArtifacts::inferArithmetic($value);

        return $inferred !== null && ! EncodingArtifacts::hasArtifact($inferred)
            ? $inferred
            : null;
    }

    /** @return list<string> */
    private function referenceFiles(): array
    {
        $files = [];

        if (! $this->option('no-default-references')) {
            foreach (['scripts/*.sql', 'scripts/seeds/*.sql', 'scripts/seeds/*.php'] as $glob) {
                $files = [...$files, ...(glob(base_path($glob)) ?: [])];
            }
        }

        foreach ((array) $this->option('reference') as $path) {
            if (is_string($path) && is_file($path)) {
                $files[] = $path;
            } else {
                $this->warn("Reference file not found: {$path}");
            }
        }

        return array_values(array_unique($files));
    }
}
