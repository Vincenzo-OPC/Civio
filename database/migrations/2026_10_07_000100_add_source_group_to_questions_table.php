<?php

use App\Enums\QuestionSourceGroup;
use Carbon\CarbonImmutable;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Adds questions.source_group and tags existing rows:
     * - draft rows created after the baseline cutoff are Civio-era custom or AI
     *   drafts -> "civio";
     * - everything else already in the bank came with the baseline -> "baseline".
     */
    public function up(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->string('source_group', 16)->nullable()->after('status')->index();
        });

        $cutoff = CarbonImmutable::parse(QuestionSourceGroup::BASELINE_CUTOFF, 'Asia/Manila')
            ->setTimezone(config('app.timezone'))
            ->toDateTimeString();

        DB::table('questions')
            ->whereNull('source_group')
            ->where('status', 'draft')
            ->where('created_at', '>=', $cutoff)
            ->update(['source_group' => QuestionSourceGroup::Civio->value]);

        DB::table('questions')
            ->whereNull('source_group')
            ->update(['source_group' => QuestionSourceGroup::Baseline->value]);
    }

    public function down(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->dropIndex(['source_group']);
            $table->dropColumn('source_group');
        });
    }
};
