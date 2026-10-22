<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('bank_import_locks', function (Blueprint $table) {
            $table->unsignedInteger('id')->primary();
        });
        DB::table('bank_import_locks')->insert(['id' => 1]);
        Schema::create('bank_import_entries', function (Blueprint $table) {
            $table->string('id', 191)->primary();
            $table->string('operation');
            $table->char('digest', 64);
            $table->foreignId('question_id')->unique()->constrained()->restrictOnDelete();
            $table->char('question_fingerprint', 64);
            $table->char('manifest_sha256', 64);
            $table->string('status');
            foreach (['approval_sha256', 'review_report_sha256', 'signature_sha256', 'signer_key_sha256'] as $field) {
                $table->char($field, 64)->nullable();
            }
            $table->timestamp('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('bank_import_entries');
        Schema::dropIfExists('bank_import_locks');
    }
};
