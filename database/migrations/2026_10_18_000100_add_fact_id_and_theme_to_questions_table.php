<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Content tags from the question design spec (v0.1.9):
     * - fact_id: items testing one fact in different formats share it; a mock
     *   should serve one per fact (rule in MockPoolSelector is still to do).
     * - theme: content-theme tag; a mock should serve at most 2 per theme.
     * Both are nullable: null means no constraint.
     */
    public function up(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->string('fact_id', 100)->nullable()->after('replaces_question_id')->index();
            $table->string('theme', 100)->nullable()->after('fact_id')->index();
        });
    }

    public function down(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->dropIndex(['fact_id']);
            $table->dropIndex(['theme']);
            $table->dropColumn(['fact_id', 'theme']);
        });
    }
};
