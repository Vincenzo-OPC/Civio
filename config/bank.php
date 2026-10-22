<?php

declare(strict_types=1);

return [
    // Trust is provisioned by the operator, never supplied by an import file.
    'approval_public_key' => env('CIVIO_BANK_APPROVAL_PUBLIC_KEY'),
];
