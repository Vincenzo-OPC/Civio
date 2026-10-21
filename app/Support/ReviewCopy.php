<?php

declare(strict_types=1);

namespace App\Support;

/** Learner-facing review words. Keep in step with resources/js/lib/review-mistakes.ts. */
final class ReviewCopy
{
    public const TITLE = 'Review Mistakes';

    public const NOTE = 'Civio reminds you to practice a question again before you forget it. A correct answer without an explanation clears the mistake. One clear does not finish the question.';

    public const EMPTY = 'No mistakes to review yet.';

    public const COMPLETE = 'Review Complete';

    public const DUE = 'Due Today';

    public const UPCOMING = 'Upcoming Reviews';

    public const NEEDS = 'Needs Review';
}
