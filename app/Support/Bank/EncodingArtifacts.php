<?php

declare(strict_types=1);

namespace App\Support\Bank;

/**
 * Detects and safely repairs "??" artifacts in question-bank text.
 *
 * Root cause (MSI desktop bank): UTF-8 seed SQL was piped into Postgres with
 * Windows PowerShell 5.1 (`Get-Content file.sql | docker exec -i ... psql`).
 * Without a BOM, Get-Content decodes the UTF-8 file as Windows-1252, so every
 * byte of a multi-byte character becomes its own character; piping to a native
 * program then re-encodes with $OutputEncoding = US-ASCII, which turns every
 * non-ASCII character into "?". The result: one "?" per UTF-8 byte, e.g.
 * × (C3 97) becomes "??", − (E2 88 92) and curly quotes become "???".
 * Files with a BOM lose one "?" per character instead.
 *
 * Repairs here never guess: text is restored only from an exact match against
 * the original UTF-8 seed source, or from arithmetic that has exactly one
 * possible operator. Anything else is reported, not rewritten.
 */
final class EncodingArtifacts
{
    /** Two or more question marks in a row, or a Unicode replacement char. */
    public static function hasArtifact(string $text): bool
    {
        return preg_match('/\?{2,}|\x{FFFD}/u', $text) === 1;
    }

    public static function hasNonAscii(string $text): bool
    {
        return preg_match('/[^\x00-\x7F]/', $text) === 1;
    }

    /**
     * Every way the given UTF-8 source text could have been mangled on its way
     * into the desktop database. Returns an empty list for pure-ASCII text.
     *
     * @return list<string>
     */
    public static function corruptedForms(string $source): array
    {
        if (! self::hasNonAscii($source) || ! mb_check_encoding($source, 'UTF-8')) {
            return [];
        }

        $forms = [];

        foreach ([$source, self::straightenQuotes($source)] as $variant) {
            // No BOM: read as Windows-1252, then ASCII-encoded => one "?" per byte.
            $perByte = self::replaceNonAscii($variant, perByte: true);
            // BOM / UTF-8 read, then ASCII-encoded => one "?" per character.
            $perChar = self::replaceNonAscii($variant, perByte: false);

            $forms[] = $perByte;
            $forms[] = $perChar;
            // The 2026-10-03 desktop SQL repair then rewrote "???s" to "'s"
            // and every remaining "???" to a straight double quote.
            $forms[] = str_replace('???', '"', str_replace('???s', "'s", $perByte));
        }

        // A form that only differs by straight vs curly quotes is not damage.
        $cosmetic = self::straightenQuotes($source);

        return array_values(array_unique(array_filter(
            $forms,
            fn (string $form) => $form !== $source && $form !== $cosmetic,
        )));
    }

    /**
     * Restore operators in "a ?? b = c" when exactly one operator makes the
     * arithmetic true. Two "?" can only be a 2-byte symbol (× or ÷); three can
     * only be a 3-byte one (−). Returns null when nothing changed.
     */
    public static function inferArithmetic(string $text): ?string
    {
        $number = '(\d+(?:,\d{3})*(?:\.\d+)?)';
        $pattern = '/'.$number.'(\s*)(\?{2,3})(\s*)'.$number.'(\s*=\s*)'.$number.'/u';
        $changed = false;

        $result = preg_replace_callback($pattern, function (array $m) use (&$changed): string {
            [$whole, $a, $ws1, $marks, $ws2, $b, $eq, $c] = $m;
            $x = (float) str_replace(',', '', $a);
            $y = (float) str_replace(',', '', $b);
            $z = (float) str_replace(',', '', $c);

            $candidates = strlen($marks) === 2
                ? ['×' => $x * $y, '÷' => $y != 0.0 ? $x / $y : null]
                : ['−' => $x - $y];

            $fits = array_keys(array_filter(
                $candidates,
                fn (?float $value) => $value !== null && abs($value - $z) < 1e-9,
            ));

            if (count($fits) !== 1) {
                return $whole;
            }

            $changed = true;

            return $a.$ws1.$fits[0].$ws2.$b.$eq.$c;
        }, $text);

        return $changed && is_string($result) ? $result : null;
    }

    private static function straightenQuotes(string $text): string
    {
        return strtr($text, [
            "\u{2018}" => "'",
            "\u{2019}" => "'",
            "\u{201C}" => '"',
            "\u{201D}" => '"',
        ]);
    }

    private static function replaceNonAscii(string $text, bool $perByte): string
    {
        return (string) preg_replace_callback(
            '/[^\x00-\x7F]/u',
            fn (array $m) => str_repeat('?', $perByte ? strlen($m[0]) : 1),
            $text,
        );
    }
}
