<?php

declare(strict_types=1);

namespace App\Enums;

enum ExamTrack: string
{
    case Professional = 'Professional';
    case Subprofessional = 'Subprofessional';
    case Drill = 'Drill';
}
