<?php

declare(strict_types=1);

namespace App\Enums;

/**
 * How a full mock picks its items. Derived on the server from the mode, never
 * from the client (ADR-0002).
 *
 * - Adaptive (Study): favours previously wrong items, weak subcategories and
 *   harder-looking items inside the Civio blueprint.
 * - Representative (Strict): uniform random within the Civio blueprint
 *   quotas. Ignores history, weak lists and the difficulty heuristic. It does
 *   not claim equal difficulty between two Strict mocks.
 */
enum SelectionPolicy: string
{
    case Adaptive = 'adaptive';
    case Representative = 'representative';

    public static function forMode(ExamMode $mode): self
    {
        return $mode === ExamMode::Strict ? self::Representative : self::Adaptive;
    }
}
