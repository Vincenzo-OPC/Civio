<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('review_items', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('question_id')->constrained()->cascadeOnDelete();
            $table->foreignId('source_attempt_id')->constrained('exam_attempts')->cascadeOnDelete();
            $table->timestamp('first_wrong_at');
            $table->timestamp('last_result_at');
            $table->unsignedInteger('wrong_count')->default(1);
            $table->string('status', 16)->default('pending');
            $table->timestamp('resolved_at')->nullable();
            $table->foreignId('resolved_by_attempt_id')->nullable()->constrained('exam_attempts')->nullOnDelete();
            $table->foreignId('last_attempt_id')->constrained('exam_attempts')->cascadeOnDelete();
            $table->timestamps();

            $table->unique(['user_id', 'question_id']);
        });

        Schema::create('review_helps', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('question_id')->constrained()->cascadeOnDelete();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['user_id', 'question_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('review_helps');
        Schema::dropIfExists('review_items');
    }
};
