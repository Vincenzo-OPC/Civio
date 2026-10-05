<?php
require __DIR__.'/vendor/autoload.php';
$app = require __DIR__.'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$demoCats = App\Models\Category::where('is_demographic', true)->get(['id','name']);
echo "demo_cats=".json_encode($demoCats)."\n";

$count = App\Models\Question::query()
  ->where('is_active', true)
  ->whereHas('subcategory.category', fn($q) => $q->where('is_demographic', true))
  ->count();
echo "active_demo_questions=$count\n";

$samples = App\Models\Question::query()
  ->where('is_active', true)
  ->whereHas('subcategory.category', fn($q) => $q->where('is_demographic', true))
  ->with('subcategory.category')
  ->limit(5)
  ->get()
  ->map(fn($q) => ['id'=>$q->id,'stem'=>mb_substr($q->stem,0,80),'cat'=>$q->subcategory?->category?->name]);
echo "samples=".json_encode($samples, JSON_UNESCAPED_UNICODE)."\n";

$cols = Schema::getColumnListing('exam_attempts');
echo "attempt_cols=".implode(',', $cols)."\n";
$attempts = DB::table('exam_attempts')->orderByDesc('id')->limit(8)->get();
foreach ($attempts as $a) {
  $arr = (array)$a;
  $qids = $arr['question_ids'] ?? null;
  $decoded = is_string($qids) ? json_decode($qids, true) : $qids;
  $first = is_array($decoded) ? array_slice($decoded, 0, 5) : [];
  echo "attempt id={$arr['id']} status=".($arr['status']??'?')." total=".($arr['total_questions']??$arr['items_count']??'?')." first_qids=".json_encode($first)."\n";
}
