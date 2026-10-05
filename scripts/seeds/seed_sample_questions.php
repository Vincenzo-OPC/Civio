<?php
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\Cache;

require __DIR__ . '/vendor/autoload.php';
$app = require __DIR__ . '/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$subs = Subcategory::all();
echo "SUBS=" . $subs->count() . PHP_EOL;
$user = User::first();
if (!$user) {
    $user = User::create([
        'name' => 'Local Admin',
        'email' => 'admin@hiraya.local',
        'password' => bcrypt('password'),
    ]);
    echo "USER_CREATED\n";
}
$n = 0;
foreach ($subs as $sub) {
    for ($i = 1; $i <= 12; $i++) {
        Question::create([
            'subcategory_id' => $sub->id,
            'language' => 'English',
            'stem' => '[' . $sub->name . '] Sample Q' . $i . ': Which option is correct?',
            'options' => ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct_option' => 0,
            'explanation' => 'Local Docker sample question. Replace later via Gemini admin generator.',
            'created_by' => $user->id,
            'status' => 'active',
        ]);
        $n++;
    }
}
Cache::forget('questions.active');
Cache::forget('categories.tree');
echo "CREATED={$n} TOTAL=" . Question::where('status','active')->count() . PHP_EOL;
