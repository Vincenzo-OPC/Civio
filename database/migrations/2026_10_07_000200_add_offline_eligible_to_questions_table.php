<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Lite L2: items that may be downloaded in offline drill packs. They are
     * excluded from strict mock pools, so a downloaded key never helps on a mock.
     * Marked by `php artisan civio:mark-offline-eligible`.
     */
    public function up(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->boolean('offline_eligible')->default(false)->after('source_group')->index();
        });
    }

    public function down(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->dropIndex(['offline_eligible']);
            $table->dropColumn('offline_eligible');
        });
    }
};
