<?php

declare(strict_types=1);

namespace App\Data\Offline;

use Carbon\CarbonImmutable;

/** One queued offline answer as sent by the client (Lite L2). */
final readonly class OfflineAnswer
{
    public function __construct(
        public string $clientId,
        public int $questionId,
        public int $selectedOption,
        public int $claimedCorrectOption,
        public ?string $packVersion,
        public ?CarbonImmutable $answeredAt,
    ) {}

    /** @param array<string, mixed> $input validated item */
    public static function fromArray(array $input): self
    {
        $answeredAt = isset($input['answered_at']) ? CarbonImmutable::parse((string) $input['answered_at']) : null;

        return new self(
            clientId: (string) $input['client_id'],
            questionId: (int) $input['question_id'],
            selectedOption: (int) $input['selected_option'],
            claimedCorrectOption: (int) $input['claimed_correct_option'],
            packVersion: isset($input['pack_version']) ? (string) $input['pack_version'] : null,
            answeredAt: $answeredAt !== null && $answeredAt->isFuture() ? CarbonImmutable::now() : $answeredAt,
        );
    }
}
