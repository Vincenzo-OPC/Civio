<?php

use Illuminate\Support\Facades\Http;

test('dexter explains a miss offline when no provider key is set', function () {
    config([
        'civio.explain_provider' => 'stub',
        'civio.explain_api_key' => null,
        'civio.tutor_name' => 'Dexter',
    ]);

    $response = $this->postJson(route('exams.explain'), [
        'stem' => 'R.A. 6713 is also known as the:',
        'options' => [
            'Code of Conduct and Ethical Standards for Public Officials and Employees',
            'Anti-Graft and Corrupt Practices Act',
            'Civil Service Law',
            'Government Procurement Act',
        ],
        'chosen_index' => 1,
        'correct_index' => 0,
        'explanation' => 'R.A. 6713 is the Code of Conduct.',
        'subcategory' => 'Code of Conduct and Ethical Standards (R.A. 6713)',
    ]);

    $response->assertOk();
    $response->assertJsonPath('tutor', 'Dexter');
    $response->assertJsonPath('explain.provider', 'stub');
    expect($response->json('explain.eli5'))->toContain('Code of Conduct');
    expect($response->json('explain.why_wrong'))->toContain('Anti-Graft');
    expect($response->json('explain.citation'))->toContain('6713');
});

test('dexter uses a configured chat provider', function () {
    config([
        'civio.explain_provider' => 'groq',
        'civio.explain_api_key' => 'test-key',
        'civio.explain_model' => 'llama-test',
    ]);

    Http::fake([
        'https://api.groq.com/openai/v1/chat/completions' => Http::response([
            'choices' => [[
                'message' => [
                    'content' => json_encode([
                        'eli5' => 'The law is the code of conduct.',
                        'why_right' => 'That title is the statute name.',
                        'why_wrong' => 'Anti-graft is a different law.',
                        'tip' => 'Match the number to the title.',
                        'citation' => 'R.A. 6713',
                    ]),
                ],
            ]],
        ]),
    ]);

    $this->postJson(route('exams.explain'), [
        'stem' => 'R.A. 6713 is also known as the:',
        'options' => ['Code of Conduct', 'Anti-Graft'],
        'chosen_index' => 1,
        'correct_index' => 0,
    ])->assertOk()
        ->assertJsonPath('explain.provider', 'groq')
        ->assertJsonPath('explain.eli5', 'The law is the code of conduct.');
});
