<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Services\Exam\Reveal\RevealTutor;
use Illuminate\Console\Command;

class AuditExplanationsCommand extends Command
{
    protected $signature = 'civio:audit-explanations';

    protected $description = 'Count empty, thin, and key-contradicting explanations. Does not rewrite any item.';

    public function handle(RevealTutor $tutor): int
    {
        $audit = $tutor->audit();
        $this->line('Checked against the key: '.$audit['checked']);
        $this->line('Stored explanation only: '.$audit['stored']);
        $this->line('Empty explanation: '.$audit['empty']);
        $this->line('Thin explanation: '.$audit['thin']);
        $this->line('Pattern disagrees with the key: '.$audit['conflicts']);

        return self::SUCCESS;
    }
}
