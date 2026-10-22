<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Enums\QuestionSourceGroup;
use App\Enums\QuestionStatus;
use App\Models\Question;
use App\Services\Bank\BankApproval;
use App\Services\Bank\BankContent;
use App\Services\Bank\BankImportLedger;
use Illuminate\Console\Command;
use JsonException;
use RuntimeException;

class ReparameterizeBaselineCommand extends Command
{
    protected $signature = 'civio:reparameterize-baseline
        {--dry-run : Validate the complete approved plan without writing}
        {--path= : JSON replacement manifest}
        {--approval= : GT-signed approval JSON; detached signature at PATH.sig}
        {--review-report= : Independent review report bound by the approval}';

    protected $description = 'Apply independently reviewed baseline replacements atomically';

    public function handle(BankApproval $approval): int
    {
        try {
            $manifest = BankApproval::read($this->option('path') ?: base_path('scripts/seeds/baseline_reparameterized.json'));
            $rows = json_decode($manifest, true, 512, JSON_THROW_ON_ERROR);
            if (! is_array($rows) || ! array_is_list($rows) || $rows === []) {
                throw new RuntimeException('Replacement file must be a nonempty list.');
            }
            foreach ($rows as $row) {
                if (! is_array($row)) {
                    throw new RuntimeException('Every replacement must be an object.');
                }
                BankContent::validate($row);
                if (! BankContent::text($row['prior_stem'] ?? null) || ! is_string($row['original_sha256'] ?? null)
                    || ! preg_match('/\A[a-f0-9]{64}\z/D', $row['original_sha256']) || $row['prior_stem'] === $row['stem']) {
                    throw new RuntimeException('Each replacement requires a distinct prior stem and reviewed original_sha256.');
                }
            }
            BankImportLedger::unique($rows);
            if (count(array_unique(array_column($rows, 'prior_stem'))) !== count($rows)) {
                throw new RuntimeException('Repeated baseline source in manifest.');
            }
            $dry = (bool) $this->option('dry-run');
            $inserted = BankImportLedger::transaction(function () use ($rows, $manifest, $dry, $approval): int {
                BankImportLedger::lock();
                $evidence = $approval->verify($manifest, 'replace-baseline', $this->option('approval'), $this->option('review-report'));
                $plan = [];
                foreach ($rows as $row) {
                    $matches = Question::query()->where('source_group', QuestionSourceGroup::Baseline)
                        ->where('stem', $row['prior_stem'])->lockForUpdate()->get();
                    if ($matches->count() !== 1 || BankContent::fingerprint($matches->first()) !== $row['original_sha256']) {
                        throw new RuntimeException('Missing, ambiguous or stale baseline source.');
                    }
                    $old = $matches->first();
                    $existing = BankImportLedger::existing($row, 'replace-baseline', 'active');
                    if ($existing !== null) {
                        if ($existing->replaces_question_id !== $old->id || $old->status !== QuestionStatus::Draft) {
                            throw new RuntimeException('Replacement provenance or original status has drifted.');
                        }

                        continue;
                    }
                    if ($old->status !== QuestionStatus::Active || BankImportLedger::collision($row['stem'])
                        || Question::query()->where('replaces_question_id', $old->id)->exists()) {
                        throw new RuntimeException('Replacement collision or baseline already replaced.');
                    }
                    $plan[] = [$row, $old];
                }
                if (! $dry) {
                    foreach ($plan as [$row, $old]) {
                        $question = Question::query()->create([
                            'subcategory_id' => $old->subcategory_id, 'language' => $row['language'],
                            'stem' => $row['stem'], 'options' => $row['options'], 'correct_option' => $row['correct_option'],
                            'explanation' => $row['explanation'], 'status' => QuestionStatus::Active,
                            'created_by' => $old->created_by, 'source_group' => QuestionSourceGroup::Civio,
                            'replaces_question_id' => $old->id, 'offline_eligible' => false,
                        ]);
                        $old->update(['status' => QuestionStatus::Draft]);
                        BankImportLedger::record($row, 'replace-baseline', 'active', $manifest, $question, $evidence);
                    }
                    if ($plan !== []) {
                        BankImportLedger::invalidate();
                    }
                }

                return count($plan);
            });
            $this->info(($dry ? 'Validated' : 'Inserted').": {$inserted}; unchanged: ".(count($rows) - $inserted).'.');

            return self::SUCCESS;
        } catch (JsonException|RuntimeException $exception) {
            $this->error($exception->getMessage());

            return self::FAILURE;
        }
    }
}
