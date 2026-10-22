<?php

declare(strict_types=1);

namespace App\Services\Ai;

/**
 * Fail-closed lock for every owner-funded external AI request (Issue #18).
 *
 * Owner keys being present never enables a request. The lock opens only when
 * CIVIO_OWNER_FUNDED_AI is exactly the string "true" (see config/ai.php) AND
 * the app is not running in production. Production stays locked until a later,
 * explicitly approved code change removes that condition.
 */
final class OwnerAiSpendLock
{
    public const DISABLED_MESSAGE = 'Owner-funded AI is disabled. No external AI request was made.';

    public static function enabled(): bool
    {
        if (config('ai.owner_funded_inference_enabled') !== true) {
            return false;
        }

        return ! app()->environment('production');
    }

    public static function disabled(): bool
    {
        return ! self::enabled();
    }

    /**
     * Strict parser: only the exact raw string "true" opens the lock.
     */
    public static function parseFlag(mixed $raw): bool
    {
        return $raw === 'true' || $raw === true;
    }

    /**
     * @return array{success: false, disabled: true, error: string}
     */
    public static function disabledResult(): array
    {
        return ['success' => false, 'disabled' => true, 'error' => self::DISABLED_MESSAGE];
    }
}
