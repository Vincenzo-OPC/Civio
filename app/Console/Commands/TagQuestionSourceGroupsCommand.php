<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionSourceGroup;
use App\Models\Question;
use Illuminate\Console\Command;

/**
 * Tags questions that have no source_group yet. The app always sets one when it
 * creates a question, so an untagged row was inserted by a raw SQL seed, which
 * means it is baseline content. Idempotent; never changes question text.
 */
class TagQuestionSourceGroupsCommand extends Command
{
    protected $signature = 'civio:tag-source-groups
        {--dry-run : Report what would change without saving}';

    protected $description = 'Tag untagged questions (raw SQL seed rows) with source_group "baseline" and show totals per group';

    public function handle(): int
    {
        $untagged = Question::query()->whereNull('source_group')->count();

        if (! $this->option('dry-run') && $untagged > 0) {
            Question::query()
                ->whereNull('source_group')
                ->update(['source_group' => QuestionSourceGroup::Baseline->value]);
        }

        $verb = $this->option('dry-run') ? 'Would tag' : 'Tagged';
        $this->info("{$verb} {$untagged} untagged question(s) as \"baseline\".");

        $this->table(['source_group', 'questions'], Question::query()
            ->selectRaw('coalesce(source_group, ?) as grp, count(*) as total', ['(none)'])
            ->groupBy('grp')
            ->orderBy('grp')
            ->get()
            ->map(fn ($row): array => [(string) $row->grp, (int) $row->total])
            ->all());

        return self::SUCCESS;
    }
}
