<?php

use App\Services\Ai\OwnerAiSpendLock;
use Illuminate\Support\Env;

return [
    /*
    | Dexter Rescue (ADR-0003). Deterministic, no AI. Off unless the raw value
    | of DEXTER_RESCUE_ENABLED is exactly "true".
    */
    'enabled' => OwnerAiSpendLock::parseFlag(Env::getRepository()->get('DEXTER_RESCUE_ENABLED')),

    // Pilot scope: Study Mode only, these graph skills only.
    'skills' => ['NUM-WP-PCT-CHANGE', 'NUM-WP-RATIO', 'CLR-SPELL-WRONG'],

    /*
    | Question ids whose distractor codes passed the editorial pilot
    | (docs/research/dexter2/pilot). Filled by a human after adjudication,
    | never by an agent. Empty: no item gets a diagnosis, only the checked
    | explanation fallback.
    */
    'validated_question_ids' => [],
];
