<?php

declare(strict_types=1);

namespace App\DTOs\Announcement;

use App\Http\Requests\Admin\Announcement\StoreAnnouncementRequest;

readonly class UpsertAnnouncementData
{
    public function __construct(
        public string $title,
        public string $message,
        public string $type,
        public bool $isActive = true,
        public ?string $expiresAt = null,
    ) {}

    public static function fromRequest(StoreAnnouncementRequest $request): self
    {
        $v = $request->validated();

        return new self(
            title: trim((string) $v['title']),
            message: trim((string) $v['message']),
            type: (string) $v['type'],
            isActive: (bool) ($v['is_active'] ?? true),
            expiresAt: ! empty($v['expires_at']) ? (string) $v['expires_at'] : null,
        );
    }

    /**
     * @return array<string, mixed>
     */
    public function toAttributes(): array
    {
        return [
            'title' => $this->title,
            'message' => $this->message,
            'type' => $this->type,
            'is_active' => $this->isActive,
            'expires_at' => $this->expiresAt,
        ];
    }
}
