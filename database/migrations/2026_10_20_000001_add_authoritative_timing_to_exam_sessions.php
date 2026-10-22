<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('exam_sessions', function (Blueprint $table) {
            $table->string('owner_session_hash', 64)->nullable()->index();
            $table->timestamp('started_at')->nullable();
            $table->timestamp('deadline_at')->nullable();
            $table->json('saved_answers')->nullable();
            $table->unsignedInteger('save_version')->default(0);
        });
    }

    public function down(): void
    {
        Schema::table('exam_sessions', fn (Blueprint $table) => $table->dropColumn([
            'owner_session_hash', 'started_at', 'deadline_at', 'saved_answers', 'save_version',
        ]));
    }
};
