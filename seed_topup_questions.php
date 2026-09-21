<?php
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Str;

require __DIR__ . '/vendor/autoload.php';
$app = require __DIR__ . '/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$user = User::first();
$targets = [
    'Analytical Ability' => 20,
    'Numerical Ability' => 20,
    'Verbal Ability' => 8,
    'Clerical Ability' => 10,
    'General Information' => 5,
];
$n = 0;
foreach ($targets as $catName => $extraPerSub) {
    $cat = Category::where('name', $catName)->first();
    if (!$cat) continue;
    foreach ($cat->subcategory as $sub) {
        for ($i = 1; $i <= $extraPerSub; $i++) {
            $lang = ($catName === 'Verbal Ability' && $i % 2 === 0) ? 'Filipino' : 'English';
            Question::create([
                'subcategory_id' => $sub->id,
                'language' => $lang,
                'stem' => '[' . $sub->name . '] Extra Q' . $i . ' (' . $lang . '): Which option is correct?',
                'options' => ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct_option' => 0,
                'explanation' => 'Local sample for Docker mock exam.',
                'created_by' => $user->id,
                'status' => 'active',
            ]);
            $n++;
        }
    }
}
Cache::forget('questions.active');
Cache::forget('categories.tree');
Cache::forget('active_announcements');
echo "ADDED=$n TOTAL_ACTIVE=" . Question::where('status','active')->count() . PHP_EOL;
