<?php

declare(strict_types=1);

namespace App\DTOs\User;

use App\Http\Requests\Admin\User\AdminUserUpdateRequest;

readonly class UpdateUserData
{
    public function __construct(
        public ?string $role = null,
        public ?bool $isActive = null,
        public ?bool $canDownloadPdf = null,
        public bool $hasRole = false,
        public bool $hasIsActive = false,
        public bool $hasCanDownloadPdf = false,
    ) {}

    public static function fromRequest(AdminUserUpdateRequest $request): self
    {
        return new self(
            role: $request->has('role') ? (string) $request->input('role') : null,
            isActive: $request->has('is_active') ? $request->boolean('is_active') : null,
            canDownloadPdf: $request->has('can_download_pdf') ? $request->boolean('can_download_pdf') : null,
            hasRole: $request->has('role'),
            hasIsActive: $request->has('is_active'),
            hasCanDownloadPdf: $request->has('can_download_pdf'),
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toAttributes(): array
    {
        $attributes = [];

        if ($this->hasRole && $this->role !== null) {
            $attributes['role'] = $this->role;
        }

        if ($this->hasIsActive && $this->isActive !== null) {
            $attributes['is_active'] = $this->isActive;
        }

        if ($this->hasCanDownloadPdf && $this->canDownloadPdf !== null) {
            $attributes['can_download_pdf'] = $this->canDownloadPdf;
        }

        return $attributes;
    }
}
