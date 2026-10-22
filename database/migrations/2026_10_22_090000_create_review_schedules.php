<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('review_cards', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('question_id')->constrained()->cascadeOnDelete();
            $table->string('scheduler_version', 32);
            $table->string('policy_version', 32);
            $table->json('card_state');
            $table->timestamp('due_at')->index();
            $table->string('state', 16);
            $table->string('last_rating', 8)->nullable();
            $table->timestamp('last_reviewed_at')->nullable();
            $table->unsignedInteger('reps')->default(0);
            $table->unsignedInteger('lapses')->default(0);
            $table->char('question_fingerprint', 64)->nullable();
            $table->timestamps();

            $table->unique(['user_id', 'question_id']);
            $table->index(['user_id', 'due_at']);
        });

        Schema::create('review_events', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('question_id')->constrained()->cascadeOnDelete();
            $table->foreignId('source_attempt_id')->nullable()->constrained('exam_attempts')->nullOnDelete();
            $table->string('outcome', 32);
            $table->string('rating', 8)->nullable();
            $table->boolean('assisted')->default(false);
            $table->boolean('scheduled')->default(false);
            $table->timestamp('due_at')->nullable();
            $table->timestamp('reviewed_at');
            $table->string('scheduler_version', 32);
            $table->string('policy_version', 32);
            $table->json('card_before')->nullable();
            $table->json('card_after')->nullable();
            $table->char('question_fingerprint', 64)->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->unique(['user_id', 'source_attempt_id', 'question_id']);
            $table->index(['user_id', 'reviewed_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('review_events');
        Schema::dropIfExists('review_cards');
    }
};
