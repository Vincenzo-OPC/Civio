<?php

namespace App\Observers;

use App\Models\Category;
use App\Services\Bank\BankImportLedger;
use Illuminate\Support\Facades\Cache;

class CategoryObserver
{
    /**
     * Handle the Category "created" event.
     */
    public function created(Category $category): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Category "updated" event.
     */
    public function updated(Category $category): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Category "deleted" event.
     */
    public function deleted(Category $category): void
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
