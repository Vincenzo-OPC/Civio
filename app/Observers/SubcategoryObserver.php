<?php

namespace App\Observers;

use App\Models\Subcategory;
use App\Services\Bank\BankImportLedger;
use Illuminate\Support\Facades\Cache;

class SubcategoryObserver
{
    /**
     * Handle the Subcategory "created" event.
     */
    public function created(Subcategory $subcategory): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Subcategory "updated" event.
     */
    public function updated(Subcategory $subcategory): void
    {
        $this->clearCache();
    }

    /**
     * Handle the Subcategory "deleted" event.
     */
    public function deleted(Subcategory $subcategory): void
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
