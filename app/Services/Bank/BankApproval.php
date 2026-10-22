<?php

declare(strict_types=1);

namespace App\Services\Bank;

use DateTimeImmutable;
use DateTimeZone;
use RuntimeException;

/** Ed25519 SSHSIG verification per OpenSSH PROTOCOL.sshsig, namespace civio-bank-approval. */
final class BankApproval
{
    public const NAMESPACE = 'civio-bank-approval';

    public function verify(string $manifest, string $operation, ?string $recordPath, ?string $reportPath): array
    {
        $record = self::read($recordPath);
        $approval = json_decode($record, true, 512, JSON_THROW_ON_ERROR);
        $report = self::read($reportPath);
        if (! is_array($approval) || ($approval['schema'] ?? null) !== 1
            || ($approval['operation'] ?? null) !== $operation
            || ($approval['approver'] ?? null) !== 'GT'
            || ($approval['manifest_sha256'] ?? null) !== hash('sha256', $manifest)
            || ($approval['review_report_sha256'] ?? null) !== hash('sha256', $report)
            || ! BankContent::text($approval['author'] ?? null)
            || ! BankContent::text($approval['reviewer'] ?? null)
            || mb_strtolower(trim($approval['author'])) === mb_strtolower(trim($approval['reviewer']))
            || ! is_string($approval['expires_at'] ?? null)
            || ! preg_match('/\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\z/D', $approval['expires_at'])
        ) {
            throw new RuntimeException('Missing, stale or mismatched independent approval record.');
        }
        $expires = DateTimeImmutable::createFromFormat('!Y-m-d\\TH:i:s\\Z', $approval['expires_at'], new DateTimeZone('UTC'));
        $errors = DateTimeImmutable::getLastErrors();
        if ($expires === false || ($errors !== false && ($errors['warning_count'] || $errors['error_count'])) || $expires <= now()->toDateTimeImmutable()) {
            throw new RuntimeException('Invalid or expired approval date.');
        }
        $signature = self::read($recordPath.'.sig');
        $trustedKey = (string) config('bank.approval_public_key');
        $this->verifySignature($record, $signature, $trustedKey);

        return [
            'approval_sha256' => hash('sha256', $record),
            'review_report_sha256' => hash('sha256', $report),
            'signature_sha256' => hash('sha256', $signature),
            'signer_key_sha256' => hash('sha256', trim($trustedKey)),
        ];
    }

    public static function read(?string $path): string
    {
        if ($path === null || ! is_file($path) || ! is_readable($path)) {
            throw new RuntimeException('Required manifest, approval, signature or review report is missing.');
        }
        $data = file_get_contents($path);
        if ($data === false || strlen($data) > 20_000_000) {
            throw new RuntimeException('Import artifact is unreadable or too large.');
        }

        return $data;
    }

    private function verifySignature(string $message, string $armor, string $trustedKey): void
    {
        if (! function_exists('sodium_crypto_sign_verify_detached')
            || ! preg_match('/\Assh-ed25519 ([A-Za-z0-9+\/=]+)(?:\s.*)?\z/sD', trim($trustedKey), $key)
            || ! preg_match('/\A-----BEGIN SSH SIGNATURE-----\r?\n([A-Za-z0-9+\/=\r\n]+)\r?\n-----END SSH SIGNATURE-----\s*\z/D', $armor, $match)) {
            throw new RuntimeException('Trusted Ed25519 key and valid SSH signature are required.');
        }
        $blob = base64_decode(preg_replace('/\s/', '', $match[1]), true);
        $trusted = base64_decode($key[1], true);
        if ($blob === false || $trusted === false || substr($blob, 0, 10) !== "SSHSIG\x00\x00\x00\x01") {
            throw new RuntimeException('Unsupported SSH signature format.');
        }
        $blob = substr($blob, 10);
        $public = $this->field($blob);
        $namespace = $this->field($blob);
        $reserved = $this->field($blob);
        $algorithm = $this->field($blob);
        $signature = $this->field($blob);
        if ($blob !== '' || ! hash_equals($trusted, $public) || $namespace !== self::NAMESPACE
            || ! in_array($algorithm, ['sha256', 'sha512'], true)) {
            throw new RuntimeException('Untrusted key, namespace or signature digest.');
        }
        if ($this->field($public) !== 'ssh-ed25519' || $this->field($signature) !== 'ssh-ed25519') {
            throw new RuntimeException('Only Ed25519 approval signatures are supported.');
        }
        $rawKey = $this->field($public);
        $rawSignature = $this->field($signature);
        $encode = fn (string $value): string => pack('N', strlen($value)).$value;
        $signed = 'SSHSIG'.$encode($namespace).$encode($reserved).$encode($algorithm).$encode(hash($algorithm, $message, true));
        if ($public !== '' || $signature !== '' || strlen($rawKey) !== 32 || strlen($rawSignature) !== 64
            || ! sodium_crypto_sign_verify_detached($rawSignature, $signed, $rawKey)) {
            throw new RuntimeException('Approval signature verification failed.');
        }
    }

    private function field(string &$blob): string
    {
        if (strlen($blob) < 4) {
            throw new RuntimeException('Truncated SSH signature.');
        }
        $length = unpack('N', substr($blob, 0, 4))[1];
        if ($length > strlen($blob) - 4) {
            throw new RuntimeException('Truncated SSH signature field.');
        }
        $value = substr($blob, 4, $length);
        $blob = substr($blob, 4 + $length);

        return $value;
    }
}
