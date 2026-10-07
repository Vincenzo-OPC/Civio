<?php

declare(strict_types=1);

namespace App\Support\Bank;

/**
 * Index of original UTF-8 bank text (from the seed SQL / PHP files kept in
 * scripts/) keyed by every corrupted form that text could have taken.
 * A lookup only succeeds when exactly one original matches.
 */
final class ReferenceTextIndex
{
    /** @var array<string, array<string, true>> corrupted form => originals */
    private array $byCorrupted = [];

    /** @var array<string, list<list<string>>> original stem => option lists */
    private array $optionsByStem = [];

    private int $sources = 0;

    public function add(string $text): void
    {
        foreach (EncodingArtifacts::corruptedForms($text) as $form) {
            if (! isset($this->byCorrupted[$form][$text])) {
                $this->byCorrupted[$form][$text] = true;
            }
        }

        $this->sources++;
    }

    public function addFile(string $path): void
    {
        $raw = (string) file_get_contents($path);
        $raw = (string) preg_replace('/^\xEF\xBB\xBF/', '', $raw);

        match (strtolower(pathinfo($path, PATHINFO_EXTENSION))) {
            'sql' => $this->addSqlLiterals($raw),
            'php' => $this->addPhpStrings($raw),
            'json' => $this->addJsonStrings(json_decode($raw, true)),
            default => null,
        };
    }

    /** The original text for a corrupted value, or null if unknown/ambiguous. */
    public function lookup(string $value): ?string
    {
        $originals = $this->byCorrupted[$value] ?? [];

        return count($originals) === 1 ? (string) array_key_first($originals) : null;
    }

    public function sourceCount(): int
    {
        return $this->sources;
    }

    private function addSqlLiterals(string $sql): void
    {
        preg_match_all("/'((?:[^']|'')*)'/s", $sql, $matches);
        $previous = null;

        foreach ($matches[1] as $literal) {
            $text = str_replace("''", "'", $literal);
            $this->addMaybeJson($text);

            // Seed rows are (…, stem, options JSON, …): remember which option
            // list belongs to which stem so symbol-only options can be matched
            // as a whole row.
            $decoded = str_starts_with(ltrim($text), '[') ? json_decode($text, true) : null;

            if (is_array($decoded) && $previous !== null && array_is_list($decoded)
                && array_filter($decoded, 'is_string') === $decoded) {
                $this->optionsByStem[$previous][] = $decoded;
            }

            $previous = $text;
        }
    }

    /**
     * The original option list for a (repaired) stem whose options still match
     * element by element, or null when unknown / ambiguous.
     *
     * @param  array<int, mixed>  $current
     * @return list<string>|null
     */
    public function lookupOptions(string $stem, array $current): ?array
    {
        $found = [];

        foreach ($this->optionsByStem[$stem] ?? [] as $candidate) {
            if (count($candidate) !== count($current)) {
                continue;
            }

            foreach (array_values($current) as $i => $value) {
                $original = $candidate[$i];

                if (! is_string($value)
                    || ($value !== $original && ! in_array($value, EncodingArtifacts::corruptedForms($original), true))) {
                    continue 2;
                }
            }

            $found[json_encode($candidate)] = $candidate;
        }

        return count($found) === 1 ? array_values($found)[0] : null;
    }

    private function addPhpStrings(string $php): void
    {
        foreach (token_get_all($php) as $token) {
            if (! is_array($token) || $token[0] !== T_CONSTANT_ENCAPSED_STRING) {
                continue;
            }

            $quoted = $token[1];
            $inner = substr($quoted, 1, -1);
            $text = $quoted[0] === "'"
                ? strtr($inner, ["\\'" => "'", '\\\\' => '\\'])
                : stripcslashes($inner);

            $this->addMaybeJson($text);
        }
    }

    private function addJsonStrings(mixed $value): void
    {
        if (is_string($value)) {
            $this->addMaybeJson($value);
        } elseif (is_array($value)) {
            foreach ($value as $item) {
                $this->addJsonStrings($item);
            }
        }
    }

    /** Option lists are stored as JSON arrays; index each option too. */
    private function addMaybeJson(string $text): void
    {
        if (str_starts_with(ltrim($text), '[')) {
            $decoded = json_decode($text, true);

            if (is_array($decoded)) {
                foreach ($decoded as $item) {
                    if (is_string($item) && EncodingArtifacts::hasNonAscii($item)) {
                        $this->add($item);
                    }
                }
            }
        }

        if (EncodingArtifacts::hasNonAscii($text)) {
            $this->add($text);
        }
    }
}
