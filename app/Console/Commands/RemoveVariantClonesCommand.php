<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionStatus;
use App\Models\ExamAttempt;
use App\Models\Question;
use App\Support\Bank\VariantClones;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

/**
 * Idempotent cleanup of "(variant N)" clone questions.
 *
 * - Not referenced anywhere: hard delete.
 * - Referenced by an attempt (question_ids or answers key), a saved drill set
 *   or a feedback report: archived by setting status to "draft". Draft items
 *   are excluded from the active pool, so they never enter a mock or drill,
 *   while old attempts, saved drills and reports keep a valid row to point at.
 * - Already-draft referenced clones: skipped (nothing to do).
 */
class RemoveVariantClonesCommand extends Command
{
    protected $signature = 'civio:remove-variant-clones
        {--dry-run : Report what would change without saving}';

    protected $description = 'Delete unreferenced "(variant N)" clone questions and archive (draft) referenced ones';

    public function handle(): int
    {
        $dryRun = (bool) $this->option('dry-run');

        $clones = Question::query()
            ->whereRaw('lower(stem) like ?', ['%(variant%'])
            ->orderBy('id')
            ->get(['id', 'stem', 'status'])
            ->filter(fn (Question $q) => VariantClones::isClone($q->stem));

        if ($clones->isEmpty()) {
            $this->info('No "(variant N)" clones found. Deleted: 0, archived: 0, skipped: 0.');

            return self::SUCCESS;
        }

        $referenced = $this->referencedQuestionIds();

        $toDelete = [];
        $toArchive = [];
        $skipped = [];

        foreach ($clones as $question) {
            $id = (int) $question->id;

            if (! isset($referenced[$id])) {
                $toDelete[] = $id;
            } elseif ($question->status === QuestionStatus::Active) {
                $toArchive[] = $id;
            } else {
                $skipped[] = $id;
            }
        }

        if (! $dryRun && ($toDelete !== [] || $toArchive !== [])) {
            DB::transaction(function () use ($toDelete, $toArchive) {
                foreach (array_chunk($toArchive, 500) as $chunk) {
                    Question::query()->whereIn('id', $chunk)->update([
                        'status' => QuestionStatus::Draft->value,
                        'updated_at' => now(),
                    ]);
                }

                foreach (array_chunk($toDelete, 500) as $chunk) {
                    Question::query()->whereIn('id', $chunk)->delete();
                }
            });

            Cache::forget('questions.active');
            Cache::forget('categories.tree');
        }

        $verb = $dryRun ? 'Would delete' : 'Deleted';
        $this->info(sprintf(
            '%s%s: %d, %s: %d, skipped (already archived): %d. Clones found: %d.',
            $dryRun ? '[dry run] ' : '',
            $verb,
            count($toDelete),
            $dryRun ? 'would archive' : 'archived',
            count($toArchive),
            count($skipped),
            $clones->count(),
        ));

        if ($toArchive !== []) {
            $this->line(($dryRun ? 'Would archive' : 'Archived').' IDs (status=draft): '.implode(', ', $toArchive));
        }

        return self::SUCCESS;
    }

    /**
     * Every question ID referenced by attempts, saved drills or feedback.
     *
     * @return array<int, true>
     */
    private function referencedQuestionIds(): array
    {
        $ids = [];

        ExamAttempt::query()->select(['id', 'question_ids', 'answers'])->chunkById(500, function ($attempts) use (&$ids) {
            foreach ($attempts as $attempt) {
                foreach ((array) ($attempt->question_ids ?? []) as $qid) {
                    if (is_numeric($qid)) {
                        $ids[(int) $qid] = true;
                    }
                }

                // Answers are keyed by question ID. Legacy rows used a plain
                // list keyed by position; those IDs are already in question_ids.
                $answers = (array) ($attempt->answers ?? []);

                if (array_is_list($answers)) {
                    continue;
                }

                foreach (array_keys($answers) as $key) {
                    if (is_numeric($key)) {
                        $ids[(int) $key] = true;
                    }
                }
            }
        });

        DB::table('saved_drill_items')->distinct()->pluck('question_id')
            ->each(function ($qid) use (&$ids) {
                $ids[(int) $qid] = true;
            });

        DB::table('feedbacks')->where('flaggable_type', Question::class)->distinct()->pluck('flaggable_id')
            ->each(function ($qid) use (&$ids) {
                $ids[(int) $qid] = true;
            });

        return $ids;
    }
}
