<?php

use App\Support\Bank\EncodingArtifacts;
use App\Support\Bank\ReferenceTextIndex;

/** What Windows PowerShell 5.1 did to a BOM-less UTF-8 seed: one "?" per byte. */
function powershellMangle(string $text): string
{
    return (string) preg_replace_callback('/[^\x00-\x7F]/u', fn ($m) => str_repeat('?', strlen($m[0])), $text);
}

test('detects ?? artifacts but not a normal question mark', function () {
    expect(EncodingArtifacts::hasArtifact('What is 12 ?? 3?'))->toBeTrue()
        ->and(EncodingArtifacts::hasArtifact("Bad \u{FFFD} byte"))->toBeTrue()
        ->and(EncodingArtifacts::hasArtifact('What is 12 × 3?'))->toBeFalse();
});

test('corrupted forms mirror the byte-length signature of each symbol', function () {
    $forms = EncodingArtifacts::corruptedForms('5 × 3 − 2');

    expect($forms)->toContain('5 ?? 3 ??? 2')   // per byte (no BOM)
        ->and($forms)->toContain('5 ? 3 ? 2')   // per character (BOM)
        ->and(EncodingArtifacts::corruptedForms('plain ascii'))->toBe([]);
});

test('restores the exact original text from the UTF-8 seed reference', function () {
    $index = new ReferenceTextIndex;
    $original = 'A shirt costs ₱450 after a 10% discount. What was the price × 2?';
    $index->add($original);

    expect($index->lookup(powershellMangle($original)))->toBe($original);
});

test('refuses to guess when two originals share the same corrupted form', function () {
    $index = new ReferenceTextIndex;
    $index->add('Compute 8 × 2.');
    $index->add('Compute 8 ÷ 2.');

    expect($index->lookup('Compute 8 ?? 2.'))->toBeNull();
});

test('infers an operator only when the arithmetic allows exactly one', function () {
    expect(EncodingArtifacts::inferArithmetic('So 12 ?? 3 = 36.'))->toBe('So 12 × 3 = 36.')
        ->and(EncodingArtifacts::inferArithmetic('So 12 ?? 3 = 4.'))->toBe('So 12 ÷ 3 = 4.')
        ->and(EncodingArtifacts::inferArithmetic('Then 1,200 ??? 200 = 1,000.'))->toBe('Then 1,200 − 200 = 1,000.')
        // 2 × 1 = 2 and 2 ÷ 1 = 2: ambiguous, leave alone.
        ->and(EncodingArtifacts::inferArithmetic('2 ?? 1 = 2'))->toBeNull()
        // No operator fits: leave alone.
        ->and(EncodingArtifacts::inferArithmetic('7 ?? 3 = 5'))->toBeNull();
});
