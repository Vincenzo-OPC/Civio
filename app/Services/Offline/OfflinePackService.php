<?php

declare(strict_types=1);

namespace App\Services\Offline;

use App\Enums\QuestionStatus;
use App\Models\Question;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;

/**
 * Builds offline drill packs (Lite L2) from offline-eligible items only.
 *
 * A pack is one category; the manifest also lists subcategory slices. Packs
 * include `correct_option` and the explanation, because offline items never
 * appear in strict mocks (see MockPoolSelector::uniqueSource).
 *
 * The version is a short hash of every item's id and updated_at in the scope,
 * so any edit, retirement or new eligible item changes it.
 */
final class OfflinePackService
{
    public const PER_PAGE = 40;

    /** @return Builder<Question> */
    public function eligibleQuery(?int $categoryId = null, ?int $subcategoryId = null): Builder
    {
        return Question::query()
            ->where('status', QuestionStatus::Active->value)
            ->where('offline_eligible', true)
            ->whereHas('subcategory.category', function (Builder $query) use ($categoryId): void {
                $query->where('is_demographic', false);

                if ($categoryId !== null) {
                    $query->whereKey($categoryId);
                }
            })
            ->when($subcategoryId !== null, fn (Builder $query) => $query->where('subcategory_id', $subcategoryId))
            ->orderBy('id');
    }

    /**
     * @return array{packs: array<int, array<string, mixed>>, per_page: int, version: string}
     */
    public function manifest(): array
    {
        $questions = $this->eligibleQuery()->with('subcategory.category')->get();
        $packs = [];

        foreach ($questions->groupBy(fn (Question $q): int => (int) $q->subcategory?->category_id) as $categoryQuestions) {
            /** @var Collection<int, Question> $categoryQuestions */
            $category = $categoryQuestions->first()?->subcategory?->category;

            if ($category === null) {
                continue;
            }

            $subcategories = [];

            foreach ($categoryQuestions->groupBy('subcategory_id') as $subQuestions) {
                /** @var Collection<int, Question> $subQuestions */
                $sub = $subQuestions->first()?->subcategory;
                $subcategories[] = [
                    'id' => (int) $sub?->id,
                    'name' => (string) $sub?->name,
                    'items' => $subQuestions->count(),
                    'pages' => (int) ceil($subQuestions->count() / self::PER_PAGE),
                    'version' => self::versionFor($subQuestions),
                    'bytes' => self::approxBytes($subQuestions),
                ];
            }

            usort($subcategories, fn (array $a, array $b): int => strcmp($a['name'], $b['name']));

            $packs[] = [
                'category_id' => (int) $category->id,
                'category' => (string) $category->name,
                'sort_order' => (int) $category->sort_order,
                'items' => $categoryQuestions->count(),
                'pages' => (int) ceil($categoryQuestions->count() / self::PER_PAGE),
                'version' => self::versionFor($categoryQuestions),
                'bytes' => self::approxBytes($categoryQuestions),
                'subcategories' => $subcategories,
            ];
        }

        usort($packs, fn (array $a, array $b): int => [$a['sort_order'], $a['category']] <=> [$b['sort_order'], $b['category']]);

        return [
            'packs' => $packs,
            'per_page' => self::PER_PAGE,
            'version' => self::versionFor($questions),
        ];
    }

    /** Version of one scope without loading full rows. */
    public function scopeVersion(int $categoryId, ?int $subcategoryId): ?string
    {
        $rows = $this->eligibleQuery($categoryId, $subcategoryId)->get(['id', 'updated_at']);

        return $rows->isEmpty() ? null : self::versionFor($rows);
    }

    /**
     * @return array{category_id: int, subcategory_id: int|null, page: int, pages: int, per_page: int, total: int, version: string, items: array<int, array<string, mixed>>}|null
     */
    public function page(int $categoryId, ?int $subcategoryId, int $page): ?array
    {
        $all = $this->eligibleQuery($categoryId, $subcategoryId)->with('subcategory.category')->get();

        if ($all->isEmpty()) {
            return null;
        }

        $pages = (int) ceil($all->count() / self::PER_PAGE);

        if ($page < 1 || $page > $pages) {
            return null;
        }

        return [
            'category_id' => $categoryId,
            'subcategory_id' => $subcategoryId,
            'page' => $page,
            'pages' => $pages,
            'per_page' => self::PER_PAGE,
            'total' => $all->count(),
            'version' => self::versionFor($all),
            'items' => $all->forPage($page, self::PER_PAGE)
                ->map(fn (Question $q): array => self::itemPayload($q))
                ->values()
                ->all(),
        ];
    }

    /** @return array<string, mixed> */
    public static function itemPayload(Question $question): array
    {
        return [
            'id' => (int) $question->id,
            'stem' => (string) $question->stem,
            'options' => array_values(array_map('strval', (array) $question->options)),
            'correct_option' => (int) $question->correct_option,
            'explanation' => (string) ($question->explanation ?? ''),
            'category' => (string) ($question->subcategory?->category?->name ?? ''),
            'subcategory' => (string) ($question->subcategory?->name ?? ''),
            'language' => (string) ($question->language ?? ''),
        ];
    }

    /** @param iterable<int, Question> $questions */
    public static function versionFor(iterable $questions): string
    {
        $parts = [];

        foreach ($questions as $question) {
            $parts[] = $question->id.':'.($question->updated_at?->getTimestamp() ?? 0);
        }

        sort($parts);

        return substr(sha1(implode('|', $parts)), 0, 12);
    }

    /** @param Collection<int, Question> $questions */
    private static function approxBytes(Collection $questions): int
    {
        return strlen((string) json_encode($questions->map(fn (Question $q): array => self::itemPayload($q))->values()->all()));
    }
}
