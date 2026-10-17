<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Enums\QuestionLanguage;
use App\Models\Question;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Question
 */
class DrillQuestionResource extends JsonResource
{
    /**
     * The "data" wrapper that should be applied.
     *
     * @var string|null
     */
    public static $wrap = null;

    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        $rawLang = $this->language instanceof QuestionLanguage
            ? $this->language->value
            : (string) ($this->language ?? '');

        $language = QuestionLanguage::fromRaw($rawLang)->value;

        $data = [
            'id' => $this->id,
            'stem' => $this->stem,
            'options' => $this->options ?? [],
            'category' => $this->subcategory?->category?->name ?? 'General Information',
            'subcategory' => $this->subcategory?->name ?? '',
            'language' => $language,
            'isDemographic' => (bool) ($this->subcategory?->category?->is_demographic ?? false),
        ];

        // Bank keys stay on the server: the drills hub, saved sets and the
        // weakness drill only need stems, choices and IDs. Drills run on
        // /exams with shuffled choices, keyless items and server grading, and
        // a key here would also expose Strict Mock items. A learner still
        // sees the key of a question they wrote themselves.
        $ownerId = $request->user()?->id;

        if ($this->created_by !== null) {
            $data['isCustom'] = true;

            if ($ownerId !== null && (int) $this->created_by === (int) $ownerId) {
                $data['correct_option'] = (int) $this->correct_option;
                $data['explanation'] = $this->explanation ?? '';
            }
        }

        return $data;
    }
}
