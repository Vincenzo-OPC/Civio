<?php

namespace App\Observers;

use App\Models\Question;
use App\Services\Bank\BankImportLedger;
use Illuminate\Support\Facades\Cache;

class QuestionObserver
{
    /**
     * Handle the Question "created" event.
     */
    public function created(Question $question): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Question "updated" event.
     */
    public function updated(Question $question): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Question "deleted" event.
     */
    public function deleted(Question $question): void
    {
        $this->clearCache();
    }

    /**
     * Clear the cache.
     */
    private function clearCache(): void
    {
        if (BankImportLedger::importing()) {
            BankImportLedger::invalidate();

            return;
        }

        Cache::forget('questions.all');
        Cache::forget('questions.active');
        Cache::forget('categories.tree');
    }
}
