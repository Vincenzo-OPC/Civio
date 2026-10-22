<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('review_helps', function (Blueprint $table) {
            $table->char('session_hash', 64)->nullable()->after('question_id');
            $table->index(['user_id', 'question_id', 'session_hash']);
        });
    }

    public function down(): void
    {
        Schema::table('review_helps', function (Blueprint $table) {
            $table->dropIndex(['user_id', 'question_id', 'session_hash']);
            $table->dropColumn('session_hash');
        });
    }
};
