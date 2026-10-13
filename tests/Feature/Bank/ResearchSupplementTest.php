<?php

use App\Console\Commands\ImportBatchCommand;

test('new Subprofessional supplements are unique, import-shaped, and not accidentally approved', function () {
    $files = [
        'docs/research/filipino-supplement-001.json' => ['expected' => 80, 'domain' => 'verbal_fil'],
        'docs/research/subprofessional-general-info-supplement-001.json' => ['expected' => 30, 'domain' => 'general_information'],
        'docs/research/subprofessional-clerical-supplement-001.json' => ['expected' => 40, 'domain' => 'clerical'],
    ];

    $allIds = [];
    $allStems = [];
    $total = 0;

    foreach ($files as $path => $config) {
        $payload = json_decode((string) file_get_contents(base_path($path)), true, 512, JSON_THROW_ON_ERROR);
        $items = $payload['items'];

        expect($items)->toHaveCount($config['expected']);

        foreach ($items as $item) {
            expect(ImportBatchCommand::problem($item))->toBeNull()
                ->and($item['domain'])->toBe($config['domain'])
                ->and($item['status'])->toBe('draft')
                ->and($item['review_status'])->toBe('unreviewed')
                ->and($item['source_group'])->toBe('civio');

            $ids = array_column($item['options'], 'option_id');
            $texts = array_map(fn (array $option): string => mb_strtolower(trim($option['text'])), $item['options']);

            expect(count(array_unique($ids)))->toBe(4)
                ->and(count(array_unique($texts)))->toBe(4)
                ->and(count(array_filter($ids, fn (string $id): bool => $id === $item['answer_option_id'])))->toBe(1)
                ->and(count($item['reveal']['why_wrong']))->toBe(3);

            if ($item['domain'] === 'verbal_fil') {
                expect($item['language'])->toBe('fil');
            }

            if ($item['domain'] === 'general_information') {
                expect($item['source_url'])->toStartWith('https://lawphil.net/');
            }

            if ($item['domain'] === 'clerical') {
                expect($item['track'])->toBe('subprofessional');
            }

            $allIds[] = $item['id'];
            $allStems[] = mb_strtolower(trim($item['stem']));
            $total++;
        }
    }

    expect($total)->toBe(150)
        ->and(count(array_unique($allIds)))->toBe($total)
        ->and(count(array_unique($allStems)))->toBe($total);
});
