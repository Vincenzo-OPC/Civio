<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Models\Question;
use App\Services\Exam\MockSessionService;
use App\Services\Offline\OfflineEligibilityPlanner;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;

/**
 * Marks items for offline drill packs (Lite L2), per category up to
 * max(0, unique items - ceil(1.5 x max mock quota)). Deterministic and
 * monotonic: never unmarks, never picks demographics, clones, or items with
 * an exact copy. Marked items leave strict mock pools.
 */
class MarkOfflineEligibleCommand extends Command
{
    protected $signature = 'civio:mark-offline-eligible
        {--dry-run : Show the plan without saving}';

    protected $description = 'Mark offline-eligible questions for offline drill packs (excluded from strict mocks)';

    public function handle(OfflineEligibilityPlanner $planner): int
    {
        $rows = Question::query()
            ->where('status', 'active')
            ->with('subcategory.category')
            ->get()
            ->map(fn (Question $q): array => MockSessionService::selectorRow($q))
            ->all();

        $plans = $planner->plan($rows);
        $toMark = [];

        foreach ($plans as $plan) {
            array_push($toMark, ...$plan['added']);

            if ($plan['overCap']) {
                $this->warn("{$plan['category']}: {$plan['existing']} already marked, over the cap of {$plan['cap']}. Nothing is unmarked; review by hand.");
            }
        }

        if (! $this->option('dry-run') && $toMark !== []) {
            foreach (array_chunk($toMark, 500) as $chunk) {
                Question::query()->whereIn('id', $chunk)->update(['offline_eligible' => true, 'updated_at' => now()]);
            }

            Cache::forget('questions.active');
        }

        $verb = $this->option('dry-run') ? 'Would mark' : 'Marked';
        $this->info("{$verb} ".count($toMark).' question(s) offline-eligible.');

        $this->table(
            ['Category', 'Unique', 'Max mock quota', 'Reserve (1.5x)', 'Cap', 'Already', 'New', 'Offline pack', 'Left for mocks'],
            array_map(fn (array $p): array => [
                $p['category'], $p['unique'], $p['maxQuota'], $p['reserve'], $p['cap'],
                $p['existing'], count($p['added']), count($p['eligible']), $p['leftForMocks'],
            ], array_values($plans)),
        );

        return self::SUCCESS;
    }
}
