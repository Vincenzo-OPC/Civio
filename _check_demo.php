<?php
require __DIR__ . "/vendor/autoload.php";
$app = require __DIR__ . "/bootstrap/app.php";
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
$demoCats = App\Models\Category::where("is_demographic", true)->get(["id","name"]);
echo "demo_cats=" . json_encode($demoCats) . PHP_EOL;
$count = App\Models\Question::query()->where("is_active", true)->whereHas("subcategory.category", function ($q) { $q->where("is_demographic", true); })->count();
echo "active_demo_questions=$count" . PHP_EOL;
$samples = App\Models\Question::query()->where("is_active", true)->whereHas("subcategory.category", function ($q) { $q->where("is_demographic", true); })->with("subcategory.category")->limit(8)->get()->map(function ($q) { return ["id"=>$q->id,"stem"=>mb_substr($q->stem,0,90),"cat"=>optional(optional($q->subcategory)->category)->name]; });
echo "samples=" . json_encode($samples, JSON_UNESCAPED_UNICODE) . PHP_EOL;
$cols = Schema::getColumnListing("exam_attempts");
echo "attempt_cols=" . implode(",", $cols) . PHP_EOL;
foreach (DB::table("exam_attempts")->orderByDesc("id")->limit(8)->get() as $a) {
  $arr = (array)$a;
  $qids = $arr["question_ids"] ?? null;
  $decoded = is_string($qids) ? json_decode($qids, true) : $qids;
  $first = is_array($decoded) ? array_slice($decoded, 0, 8) : [];
  echo "id=" . $arr["id"] . " keys=" . json_encode(array_keys($arr)) . " first=" . json_encode($first) . PHP_EOL;
}