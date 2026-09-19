<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Enums\LegalContentType;
use App\Models\LegalContent;

interface LegalContentRepositoryInterface extends BaseRepositoryInterface
{
    public function findByType(LegalContentType|string $type): ?LegalContent;

    public function upsertContent(LegalContentType|string $type, string $content): LegalContent;

    /**
     * @param  array<string, string>  $contents
     */
    public function updateAllContents(array $contents): void;
}
