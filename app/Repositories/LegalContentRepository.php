<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Enums\LegalContentType;
use App\Models\LegalContent;

class LegalContentRepository extends BaseRepository implements LegalContentRepositoryInterface
{
    public function __construct(LegalContent $model)
    {
        parent::__construct($model);
    }

    public function findByType(LegalContentType|string $type): ?LegalContent
    {
        $val = $type instanceof LegalContentType ? $type->value : $type;

        /** @var LegalContent|null */
        return $this->model->newQuery()->where('type', $val)->first();
    }

    public function upsertContent(LegalContentType|string $type, string $content): LegalContent
    {
        $val = $type instanceof LegalContentType ? $type->value : $type;

        /** @var LegalContent */
        return $this->model->newQuery()->updateOrCreate(
            ['type' => $val],
            ['content' => $content]
        );
    }

    /**
     * @param  array<string, string>  $contents
     */
    public function updateAllContents(array $contents): void
    {
        foreach ($contents as $type => $content) {
            $this->upsertContent($type, $content);
        }
    }
}
