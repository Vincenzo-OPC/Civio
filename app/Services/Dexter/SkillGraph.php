<?php

declare(strict_types=1);

namespace App\Services\Dexter;

use App\Models\Question;

/**
 * Versioned prerequisite graph over spec archetypes (config/dexter_skill_graph.php).
 */
final class SkillGraph
{
    /** @var array<string, array{label: string, domain: string, prerequisites: list<string>}> */
    private array $skills;

    /** @param  array<string, array<string, mixed>>|null  $skills */
    public function __construct(?array $skills = null)
    {
        /** @var array<string, array{label: string, domain: string, prerequisites: list<string>}> $resolved */
        $resolved = $skills ?? (array) config('dexter_skill_graph.skills', []);
        $this->skills = $resolved;
    }

    public function version(): string
    {
        return (string) config('dexter_skill_graph.version');
    }

    public function has(string $skill): bool
    {
        return isset($this->skills[$skill]);
    }

    public function label(string $skill): string
    {
        return $this->skills[$skill]['label'] ?? $skill;
    }

    public function skillFor(Question $question): ?string
    {
        $archetype = (string) ($question->archetype ?? '');

        return $this->has($archetype) ? $archetype : null;
    }

    /** @return list<string> */
    public function prerequisitesOf(string $skill): array
    {
        return array_values($this->skills[$skill]['prerequisites'] ?? []);
    }

    /**
     * Every prerequisite (transitively), foundations first.
     *
     * @return list<string>
     */
    public function foundationsOf(string $skill): array
    {
        $order = [];
        $seen = [];
        $visit = function (string $s) use (&$visit, &$order, &$seen): void {
            foreach ($this->prerequisitesOf($s) as $p) {
                if (! isset($seen[$p])) {
                    $seen[$p] = true;
                    $visit($p);
                    $order[] = $p;
                }
            }
        };
        $visit($skill);

        return $order;
    }

    /**
     * Structural problems: dangling prerequisites, self-loops and cycles.
     *
     * @return list<string>
     */
    public function problems(): array
    {
        $problems = [];
        foreach ($this->skills as $id => $node) {
            foreach ($node['prerequisites'] ?? [] as $p) {
                if ($p === $id) {
                    $problems[] = "{$id} lists itself";
                } elseif (! isset($this->skills[$p])) {
                    $problems[] = "{$id} needs unknown skill {$p}";
                }
            }
        }

        $state = [];
        $dfs = function (string $id, array $path) use (&$dfs, &$state, &$problems): void {
            $state[$id] = 1;
            foreach ($this->prerequisitesOf($id) as $p) {
                if (! isset($this->skills[$p]) || $p === $id) {
                    continue;
                }
                if (($state[$p] ?? 0) === 1) {
                    $problems[] = 'cycle: '.implode(' -> ', [...$path, $id, $p]);
                } elseif (($state[$p] ?? 0) === 0) {
                    $dfs($p, [...$path, $id]);
                }
            }
            $state[$id] = 2;
        };
        foreach (array_keys($this->skills) as $id) {
            if (($state[$id] ?? 0) === 0) {
                $dfs($id, []);
            }
        }

        return $problems;
    }
}
