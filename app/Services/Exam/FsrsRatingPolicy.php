<?php

declare(strict_types=1);

namespace App\Services\Exam;

/**
 * civio-fsrs-policy-1
 *
 * A wrong answer is Again. An independent correct answer is Good.
 * An assisted correct answer is not a review. Speed never picks Hard or Easy.
 * One success is not mastery.
 */
final class FsrsRatingPolicy
{
    public const VERSION = 'civio-fsrs-policy-1';

    public function rating(bool $correct, bool $assisted): ?string
    {
        if (! $correct) {
            return 'again';
        }

        if ($assisted) {
            return null;
        }

        return 'good';
    }
}
