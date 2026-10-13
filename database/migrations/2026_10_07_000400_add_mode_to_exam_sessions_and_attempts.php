<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Exam Simulation modes: `study` (Reveal allowed, timer optional) or `strict`
 * (timed rehearsal, keys locked on the server until submit). Every existing
 * mock was taken with Reveal available, so existing rows become `study`.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('exam_sessions', function (Blueprint $table) {
            $table->string('mode', 10)->default('study')->after('track');
            $table->index(['mode', 'exam_attempt_id', 'created_at']);
        });

        Schema::table('exam_attempts', function (Blueprint $table) {
            $table->string('mode', 10)->default('study')->after('category_id');
        });
    }

    public function down(): void
    {
        Schema::table('exam_sessions', function (Blueprint $table) {
            $table->dropIndex(['mode', 'exam_attempt_id', 'created_at']);
            $table->dropColumn('mode');
        });

        Schema::table('exam_attempts', function (Blueprint $table) {
            $table->dropColumn('mode');
        });
    }
};
