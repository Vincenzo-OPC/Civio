<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * ADR-0002: record which selection policy (and version) built a mock. Null on rows created
 * before this change (unknown, not guessed).
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('exam_sessions', function (Blueprint $table) {
            $table->string('selection_policy', 20)->nullable()->after('mode');
            $table->string('selection_policy_version', 40)->nullable()->after('selection_policy');
        });
        Schema::table('exam_attempts', function (Blueprint $table) {
            $table->string('selection_policy', 20)->nullable()->after('mode');
            $table->string('selection_policy_version', 40)->nullable()->after('selection_policy');
        });
    }

    public function down(): void
    {
        Schema::table('exam_sessions', fn (Blueprint $table) => $table->dropColumn(['selection_policy', 'selection_policy_version']));
        Schema::table('exam_attempts', fn (Blueprint $table) => $table->dropColumn(['selection_policy', 'selection_policy_version']));
    }
};
