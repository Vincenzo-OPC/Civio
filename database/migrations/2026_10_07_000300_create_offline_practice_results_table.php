<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Lite L2: answers given offline, synced later and re-graded on the server.
     * One row per (owner, client_id), so re-sending a queue is idempotent.
     */
    public function up(): void
    {
        Schema::create('offline_practice_results', function (Blueprint $table) {
            $table->id();
            $table->string('owner_key', 80);
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->string('client_id', 64);
            $table->foreignId('question_id')->nullable()->constrained()->nullOnDelete();
            $table->unsignedTinyInteger('selected_option');
            $table->unsignedTinyInteger('claimed_correct_option')->nullable();
            $table->boolean('is_correct')->default(false);
            $table->string('status', 16);
            $table->string('reason', 32)->nullable();
            $table->string('source', 32)->default('offline_practice');
            $table->string('pack_version', 40)->nullable();
            $table->timestamp('answered_at')->nullable();
            $table->timestamps();

            $table->unique(['owner_key', 'client_id']);
            $table->index(['user_id', 'status']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('offline_practice_results');
    }
};
