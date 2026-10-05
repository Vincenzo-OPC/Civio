<?php
require __DIR__ . "/vendor/autoload.php";
$app = require __DIR__ . "/bootstrap/app.php";
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
echo "active=" . DB::table("questions")->count() . PHP_EOL;
foreach (DB::table("questions")->orderByDesc("id")->limit(4)->get() as $r) {
  $opts = is_string($r->options) ? json_decode($r->options, true) : $r->options;
  echo "ID {$r->id}" . PHP_EOL . $r->stem . PHP_EOL;
  if (is_array($opts)) { foreach ($opts as $i => $o) echo "  [$i] $o" . PHP_EOL; }
  echo "correct={$r->correct_option}" . PHP_EOL . $r->explanation . PHP_EOL . "---" . PHP_EOL;
}