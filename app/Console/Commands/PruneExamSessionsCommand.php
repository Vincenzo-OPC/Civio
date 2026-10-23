<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Models\ExamSession;
use Illuminate\Console\Command;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\DB;

/**
 * Deletes abandoned, never-submitted guest exam sessions whose last activity
 * is older than the retention window (Issue #26).
 *
 * Kept, always:
 * - any session linked to a submitted attempt (exam_attempt_id set);
 * - any session owned by a signed-in learner: ExposureHistory reads them so
 *   Strict selection keeps avoiding items the learner was already shown;
 * - any session touched (created, saved, started) inside the window;
 * - any Strict session whose deadline is not also older than the window.
 * Attempts, results and bank rows are never queried for deletion. Sessions
 * have no child rows; the attempt foreign key points from session to attempt.
 */
class PruneExamSessionsCommand extends Command
{
    protected $signature = 'civio:prune-exam-sessions
        {--days= : Retention in days (clamped to the configured safe bounds)}
        {--dry-run : Count what would be deleted without deleting}';

    protected $description = 'Delete abandoned, unsubmitted guest exam sessions older than the retention window';

    public function handle(): int
    {
        $config = (array) config('civio.prune_exam_sessions', []);
        $min = max(31, (int) ($config['min_days'] ?? 31));
        $max = max($min, (int) ($config['max_days'] ?? 365));
        $batch = max(1, min(5000, (int) ($config['batch_size'] ?? 500)));

        $raw = $this->option('days');
        if ($raw !== null && (! is_numeric($raw) || (int) $raw != $raw)) {
            $this->error('--days must be a whole number.');

            return self::INVALID;
        }

        $requested = $raw !== null ? (int) $raw : (int) ($config['retention_days'] ?? 45);
        $days = max($min, min($max, $requested));

        if ($days !== $requested) {
            $this->warn("Retention {$requested} days is outside {$min}..{$max}; using {$days}.");
        }

        $cutoff = now()->subDays($days);
        $dryRun = (bool) $this->option('dry-run');
        $eligible = fn (): Builder => self::eligible($cutoff);

        if ($dryRun) {
            $count = $eligible()->count();
            $this->info("Dry run: {$count} abandoned exam session(s) older than {$days} days would be deleted.");

            return self::SUCCESS;
        }

        $deleted = 0;
        do {
            $ids = $eligible()->orderBy('id')->limit($batch)->pluck('id')->all();
            if ($ids === []) {
                break;
            }

            // Re-check the conditions inside the delete so a row resumed or
            // submitted between select and delete is left alone.
            $deleted += DB::transaction(fn (): int => self::eligible($cutoff)->whereIn('id', $ids)->delete());
        } while (count($ids) === $batch);

        $this->info("Deleted {$deleted} abandoned exam session(s) older than {$days} days.");

        return self::SUCCESS;
    }

    private static function eligible(\DateTimeInterface $cutoff): Builder
    {
        return ExamSession::query()
            ->whereNull('exam_attempt_id')
            ->whereNull('user_id')
            ->where('created_at', '<', $cutoff)
            ->where(fn (Builder $q) => $q->whereNull('updated_at')->orWhere('updated_at', '<', $cutoff))
            ->where(fn (Builder $q) => $q->whereNull('started_at')->orWhere('started_at', '<', $cutoff))
            ->where(fn (Builder $q) => $q->whereNull('deadline_at')->orWhere('deadline_at', '<', $cutoff));
    }
}
