<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Artisan;

class SystemController extends Controller
{
    public function index()
    {
        return $this->render('admin/system/index', [
            'isMaintenanceMode' => App::isDownForMaintenance(),
            'environment' => App::environment(),
            'laravelVersion' => app()->version(),
            'phpVersion' => PHP_VERSION,
            'browserMigrationsEnabled' => $this->browserMigrationsEnabled(),
        ]);
    }

    public function clearCache()
    {
        Artisan::call('optimize:clear');

        return $this->backWithSuccess('System cache cleared successfully.');
    }

    public function optimize()
    {
        Artisan::call('optimize');

        return $this->backWithSuccess('System optimized successfully.');
    }

    public function runMigrations()
    {
        if (! $this->browserMigrationsEnabled()) {
            return $this->backWithError('Browser migrations are disabled. Use CLI: php artisan migrate');
        }

        try {
            Artisan::call('migrate', ['--force' => true]);
            $output = Artisan::output();

            return $this->backWithSuccess('Migrations ran successfully: '.$output);
        } catch (\Exception $e) {
            return $this->backWithError('Migration failed: '.$e->getMessage());
        }
    }

    public function rollbackMigrations()
    {
        if (! $this->browserMigrationsEnabled()) {
            return $this->backWithError('Browser rollbacks are disabled. Use CLI: php artisan migrate:rollback');
        }

        try {
            Artisan::call('migrate:rollback', ['--force' => true]);
            $output = Artisan::output();

            return $this->backWithSuccess('Database rolled back successfully: '.$output);
        } catch (\Exception $e) {
            return $this->backWithError('Rollback failed: '.$e->getMessage());
        }
    }

    public function toggleMaintenance(Request $request)
    {
        if (App::isDownForMaintenance()) {
            Artisan::call('up');

            return $this->backWithSuccess('Application is now LIVE.');
        } else {
            Artisan::call('down');

            return $this->backWithSuccess('Application is now in Maintenance Mode. You have automatic Admin bypass privileges.');
        }
    }

    /**
     * Browser migrate/rollback only when explicitly enabled AND not production.
     */
    protected function browserMigrationsEnabled(): bool
    {
        if (App::environment('production')) {
            return false;
        }

        return (bool) config('civio.allow_browser_migrations', false);
    }
}
