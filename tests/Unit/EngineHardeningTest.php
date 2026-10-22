<?php

use App\Services\Exam\MockPoolSelector;

function engClerical(int $id): array
{
    return ['id' => $id, 'stem' => "Clerical item number {$id} unique stem text", 'options' => ["a{$id}", "b{$id}", "c{$id}", "d{$id}"], 'correct' => 0, 'category' => 'Clerical Ability', 'subcategory' => 'Spelling', 'language' => 'English', 'isDemographic' => false];
}

function engFil(int $id, array $options, int $correct, string $stem): array
{
    return ['id' => $id, 'stem' => $stem, 'options' => $options, 'correct' => $correct, 'category' => 'Verbal Ability', 'subcategory' => 'Filipino', 'language' => 'Filipino', 'isDemographic' => false];
}

test('weak-category top-up never adds a key-trap pair the blueprint picks would refuse', function () {
    $bank = array_map('engClerical', range(100, 160));
    $bank[] = engFil(1, ['tuyo', 'napakalaki', 'malago', 'mabango'], 2, 'Kahulugan ng MAYABONG?');
    $bank[] = engFil(2, ['kalbo', 'mabango', 'malago', 'lubos na patay'], 0, 'Kasalungat ng MALABAY?');

    for ($run = 0; $run < 20; $run++) {
        $ids = array_column((new MockPoolSelector)->select($bank, MockPoolSelector::SUBPROFESSIONAL, ['weakCategories' => ['Verbal Ability']])['items'], 'id');
        expect(in_array(1, $ids, true) && in_array(2, $ids, true))->toBeFalse()
            ->and(count($ids))->toBe(count(array_unique($ids)));
    }
});
