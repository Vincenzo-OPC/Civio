<?php

// Fails (exit 1) when the running PHP is affected by CVE-2026-109618 /
// CVE-2026-109619 (GHSA-w8hw-w9fx-j79w, GHSA-6wmf-4rv5-p3rp).
// First fixed releases per php.net ChangeLog, 21-22 Oct 2026.
// Used by the Dockerfile build, CI and tests/Unit/Security/PatchedPhpRuntimeTest.php.

$minimums = require __DIR__.'/patched-php-minimums.php';

$version = $argv[1] ?? PHP_VERSION;
if (! preg_match('/^(\d+)\.(\d+)\.(\d+)/', $version, $m)) {
    fwrite(STDERR, "Cannot parse PHP version '{$version}'.\n");
    exit(1);
}
$branch = $m[1].'.'.$m[2];
$plain = $m[1].'.'.$m[2].'.'.$m[3];

if (! isset($minimums[$branch])) {
    fwrite(STDERR, "PHP {$plain}: branch {$branch} has no fix for CVE-2026-109618/109619. Use 8.2.35+, 8.3.36+, 8.4.27+ or 8.5.12+.\n");
    exit(1);
}
if (version_compare($plain, $minimums[$branch], '<')) {
    fwrite(STDERR, "PHP {$plain} is vulnerable to CVE-2026-109618/109619. Minimum for {$branch} is {$minimums[$branch]}.\n");
    exit(1);
}
echo "PHP {$plain} is patched for CVE-2026-109618/109619 (minimum {$minimums[$branch]}).\n";
