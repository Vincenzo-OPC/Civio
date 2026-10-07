<?php

declare(strict_types=1);

namespace App\Enums;

/**
 * Where a bank item came from. Used to group items for later work (for example
 * re-parameterizing baseline items); it never changes grading or visibility.
 *
 * - Baseline: shipped with the baseline seeds (d3f0368) or inserted by raw SQL seeds.
 * - Civio: written in Civio (admin editor, AI generation, user custom drills).
 */
enum QuestionSourceGroup: string
{
    case Baseline = 'baseline';
    case Civio = 'civio';

    /** Items created before this moment (Asia/Manila) belong to the baseline era. */
    public const BASELINE_CUTOFF = '2026-10-06 00:00:00';
}
