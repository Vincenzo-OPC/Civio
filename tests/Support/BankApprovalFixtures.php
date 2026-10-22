<?php

use App\Services\Bank\BankApproval;

function bankArtifact(string $content): string
{
    $path = tempnam(sys_get_temp_dir(), 'civio-bank-test-');
    file_put_contents($path, $content);
    register_shutdown_function(static fn () => is_file($path) ? unlink($path) : null);

    return $path;
}

function bankJson(array $value): string
{
    return bankArtifact(json_encode($value, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE));
}

function bankSign(string $path, string $operation = 'replace-baseline', array $override = []): array
{
    $pair = sodium_crypto_sign_keypair();
    $public = sodium_crypto_sign_publickey($pair);
    $encode = fn (string $s): string => pack('N', strlen($s)).$s;
    $key = $encode('ssh-ed25519').$encode($public);
    config(['bank.approval_public_key' => 'ssh-ed25519 '.base64_encode($key)]);
    $report = bankArtifact('Synthetic independent-review fixture; no editorial approval.');
    $record = bankJson(array_replace([
        'schema' => 1, 'operation' => $operation, 'approver' => 'GT',
        'author' => 'test-author', 'reviewer' => 'test-independent-reviewer',
        'manifest_sha256' => hash_file('sha256', $path),
        'review_report_sha256' => hash_file('sha256', $report),
        'expires_at' => now()->addDay()->format('Y-m-d\TH:i:s\Z'),
    ], $override));
    $namespace = BankApproval::NAMESPACE;
    $message = 'SSHSIG'.$encode($namespace).$encode('').$encode('sha512').$encode(hash('sha512', file_get_contents($record), true));
    $signature = sodium_crypto_sign_detached($message, sodium_crypto_sign_secretkey($pair));
    // SSHSIG has a six-byte magic followed by a four-byte version.
    $blob = 'SSHSIG'.pack('N', 1).$encode($key).$encode($namespace).$encode('').$encode('sha512')
        .$encode($encode('ssh-ed25519').$encode($signature));
    file_put_contents($record.'.sig', "-----BEGIN SSH SIGNATURE-----\n".chunk_split(base64_encode($blob), 70, "\n")."-----END SSH SIGNATURE-----\n");
    register_shutdown_function(static fn () => is_file($record.'.sig') ? unlink($record.'.sig') : null);

    return ['--approval' => $record, '--review-report' => $report];
}
