<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Atomic accounting for the custom-drill new-question budget.
 *
 * custom_drill_grants: one row per (principal, question) the first time a
 * never-encountered ID is served through custom_question_ids. The unique key
 * makes repeat requests for the same ID free and concurrent duplicates no-ops.
 * custom_drill_budgets: per-principal per-day counter row, locked FOR UPDATE
 * while a launch spends budget so parallel requests cannot overspend.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('custom_drill_grants', function (Blueprint $table) {
            $table->id();
            $table->string('principal', 80);
            $table->unsignedBigInteger('question_id');
            $table->date('granted_on');
            $table->timestamps();
            $table->unique(['principal', 'question_id']);
            $table->index(['principal', 'granted_on']);
        });

        Schema::create('custom_drill_budgets', function (Blueprint $table) {
            $table->id();
            $table->string('principal', 80);
            $table->date('day');
            $table->unsignedInteger('used')->default(0);
            $table->timestamps();
            $table->unique(['principal', 'day']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('custom_drill_budgets');
        Schema::dropIfExists('custom_drill_grants');
    }
};
