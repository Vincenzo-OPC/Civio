<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/*
 * Deterministic Dexter metadata (no AI). Both columns are nullable and are
 * filled only by the reviewed bank importer, never by learners or agents.
 * - archetype: the spec archetype code, e.g. NUM-WP-PCT-CHANGE (spec section 3).
 * - distractor_codes: {stored option index: distractor code} for each wrong choice.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->string('archetype', 64)->nullable();
            $table->json('distractor_codes')->nullable();
        });
    }

    public function down(): void
    {
        Schema::table('questions', function (Blueprint $table) {
            $table->dropColumn(['archetype', 'distractor_codes']);
        });
    }
};
