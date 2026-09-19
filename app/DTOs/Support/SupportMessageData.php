<?php

declare(strict_types=1);

namespace App\DTOs\Support;

use App\Http\Requests\Public\SupportRequest;

readonly class SupportMessageData
{
    public function __construct(
        public string $name,
        public string $email,
        public string $message,
    ) {}

    public static function fromRequest(SupportRequest $request): self
    {
        $v = $request->validated();

        return new self(
            name: trim((string) $v['name']),
            email: trim((string) $v['email']),
            message: trim((string) $v['message']),
        );
    }

    /**
     * @return array{name: string, email: string, message: string}
     */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'email' => $this->email,
            'message' => $this->message,
        ];
    }
}
